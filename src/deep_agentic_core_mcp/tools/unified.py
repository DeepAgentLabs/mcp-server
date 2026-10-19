"""Unified workflow tools that compose existing Lens, Evals and Chaos evidence.

These tools judge nothing themselves. Comparisons are validated with the Lens
comparison model, evaluation reports go through the Evals release gate (via
the same adapter as `lens.slo_summary`), and chaos reports must be
`chaos.run_experiment` results. The release check fails closed: required
evidence that is missing, malformed or from a failed call blocks readiness.
"""

from typing import Any

from deep_agentic_core_mcp.adapters import AdapterUnavailableError
from deep_agentic_core_mcp.adapters.agenticlens import gate_threshold_names
from deep_agentic_core_mcp.adapters.agenticlens import slo_summary as adapter_slo_summary
from deep_agentic_core_mcp.adapters.agenticlens import (
    validate_comparison as adapter_validate_comparison,
)
from deep_agentic_core_mcp.config import SERVER_NAME, VERSION
from deep_agentic_core_mcp.services import session
from deep_agentic_core_mcp.tools.lens import run_comparison

EVIDENCE_KINDS = ("comparison", "evaluation", "chaos")
REPORT_SCHEMA_VERSION = "mcp.unified-report.v1"
_CHAOS_REPORT_KEYS = ("crashed", "timed_out", "chaos_events")


def compare_runs(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Compare baseline and candidate runs; the same path as `lens.compare_runs`."""
    return run_comparison(arguments, tool="core.compare_runs")


def _gate(
    name: str,
    status: str,
    reasons: list[str],
    observed: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "name": name,
        "status": status,
        "passed": status == "passed",
        "reasons": reasons,
        "observed": observed or {},
    }


def _failed_call(kind: str, evidence: dict[str, Any]) -> dict[str, Any] | None:
    if evidence.get("ok") is False:
        error = evidence.get("error", "no error recorded")
        return _gate(kind, "invalid", [f"The {kind} evidence is from a failed call: {error}"])
    return None


def _comparison_gate(comparison: dict[str, Any]) -> dict[str, Any]:
    failed = _failed_call("comparison", comparison)
    if failed:
        return failed
    try:
        report = adapter_validate_comparison({k: v for k, v in comparison.items() if k != "ok"})
    except (AdapterUnavailableError, ValueError) as exc:
        return _gate("comparison", "invalid", [f"Not a Lens comparison report: {exc}"])
    regressions = report["regressions"]
    observed = {
        "regression_count": len(regressions),
        "regression_threshold": report["regression_threshold"],
        "sample_size_guidance": report.get("sample_size_guidance"),
    }
    return _gate("comparison", "failed" if regressions else "passed", regressions, observed)


def _evaluation_gate(report: dict[str, Any], thresholds: dict[str, Any]) -> dict[str, Any]:
    failed = _failed_call("evaluation", report)
    if failed:
        return failed
    try:
        result = adapter_slo_summary(report, thresholds)
    except (AdapterUnavailableError, ValueError) as exc:
        return _gate("evaluation", "invalid", [f"Evals gate could not run: {exc}"])
    decision = result["decision"]
    gate = _gate(
        "evaluation",
        "passed" if decision["passed"] else "failed",
        decision["reasons"],
        decision["observed"],
    )
    gate["thresholds"] = result["thresholds"]
    return gate


def _chaos_gate(report: dict[str, Any]) -> dict[str, Any]:
    # A crashed or timed-out run is a real report with ok=false, so check its
    # shape before treating ok=false as a failed call.
    absent = [key for key in _CHAOS_REPORT_KEYS if key not in report]
    if absent:
        failed = _failed_call("chaos", report)
        missing = f"Not a chaos.run_experiment report; missing {', '.join(absent)}"
        return failed or _gate("chaos", "invalid", [missing])
    reasons = []
    if report["crashed"]:
        reasons.append(f"Target crashed under chaos: {report['crashed']}")
    if report["timed_out"]:
        reasons.append("Target timed out under chaos")
    if report.get("ok") is False and not reasons:
        reasons.append("Chaos run reported ok=false")
    observed = {"event_count": len(report["chaos_events"] or [])}
    return _gate("chaos", "failed" if reasons else "passed", reasons, observed)


def _required_evidence(arguments: dict[str, Any]) -> list[str] | str:
    required = arguments.get("required_evidence", list(EVIDENCE_KINDS))
    if (
        not isinstance(required, list)
        or not required
        or any(kind not in EVIDENCE_KINDS for kind in required)
    ):
        return f"required_evidence must be a nonempty list drawn from {list(EVIDENCE_KINDS)}"
    return [kind for kind in EVIDENCE_KINDS if kind in required]


def _thresholds(arguments: dict[str, Any]) -> dict[str, Any] | str:
    thresholds = arguments.get("thresholds") or {}
    if not isinstance(thresholds, dict):
        return "thresholds must be an object of Evals GateConfig fields"
    if thresholds:
        try:
            unknown = sorted(set(thresholds) - gate_threshold_names())
        except AdapterUnavailableError as exc:
            return str(exc)
        if unknown:
            return f"Unknown Evals gate thresholds: {', '.join(unknown)}"
    return thresholds


def _evidence(
    arguments: dict[str, Any], state: session.SessionState
) -> dict[str, dict[str, Any] | None]:
    """Explicit arguments win; comparison and chaos fall back to this session."""
    supplied = {
        "comparison": arguments.get("comparison", state.last_comparison),
        "evaluation": arguments.get("evaluation_report"),
        "chaos": arguments.get("chaos_report", state.last_chaos_report),
    }
    return {kind: value if isinstance(value, dict) else None for kind, value in supplied.items()}


def _reject(session_id: str, error: str) -> dict[str, Any]:
    session.record_call(session_id, "core.release_check", ok=False, note=error)
    return {"ok": False, "error": error}


def release_check(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Decide readiness from comparison, evaluation and chaos evidence, failing closed."""
    arguments = arguments or {}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    state = session.get_session(session_id)
    required = _required_evidence(arguments)
    if isinstance(required, str):
        return _reject(session_id, required)
    thresholds = _thresholds(arguments)
    if isinstance(thresholds, str):
        return _reject(session_id, thresholds)

    evidence = _evidence(arguments, state)
    gates: list[dict[str, Any]] = []
    for kind in EVIDENCE_KINDS:
        item = evidence[kind]
        if item is None:
            if kind in required:
                gates.append(_gate(kind, "missing", [f"No {kind} evidence supplied or stored"]))
            continue
        if kind == "comparison":
            gates.append(_comparison_gate(item))
        elif kind == "evaluation":
            gates.append(_evaluation_gate(item, thresholds))
        else:
            gates.append(_chaos_gate(item))

    result = {
        "ok": True,
        "ready": all(gate["passed"] for gate in gates),
        "required_evidence": required,
        "missing_evidence": [gate["name"] for gate in gates if gate["status"] == "missing"],
        "gates": gates,
    }
    state.last_release_check = result
    session.record_call(session_id, "core.release_check", ok=True)
    return result


def incident_summary(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Collect failure signals from supplied or session evidence for investigation."""
    arguments = arguments or {}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    state = session.get_session(session_id)
    evidence = _evidence(arguments, state)
    if not any(evidence.values()) and state.last_release_check is None:
        return {"ok": False, "error": "No incident evidence supplied or stored in session"}

    findings: list[dict[str, Any]] = []
    comparison = evidence["comparison"]
    if comparison and isinstance(comparison.get("regressions"), list) and comparison["regressions"]:
        findings.append(
            {"source": "comparison", "type": "regression", "items": comparison["regressions"]}
        )
    chaos = evidence["chaos"]
    if chaos and (chaos.get("crashed") or chaos.get("timed_out")):
        findings.append(
            {
                "source": "chaos",
                "type": "resilience_failure",
                "crashed": chaos.get("crashed"),
                "timed_out": bool(chaos.get("timed_out")),
                "events": chaos.get("chaos_events", []),
            }
        )
    evaluation = evidence["evaluation"]
    summary = evaluation.get("summary") if evaluation else None
    if isinstance(summary, dict) and summary.get("failed_cases"):
        findings.append(
            {
                "source": "evaluation",
                "type": "failed_cases",
                "failed_cases": summary["failed_cases"],
                "pass_rate": summary.get("pass_rate"),
            }
        )
    release = state.last_release_check
    if release and not release["ready"]:
        findings.append(
            {
                "source": "release_check",
                "type": "blocked_release",
                "gates": [gate for gate in release["gates"] if not gate["passed"]],
            }
        )

    result = {
        "ok": True,
        "status": "investigate" if findings else "no_signals",
        "workflow": state.workflow,
        "findings": findings,
        "history": list(state.history),
    }
    state.last_incident_summary = result
    session.record_call(session_id, "core.incident_summary", ok=True)
    return result


def export_report(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Export a session's evidence as an MCP-local envelope (not an AIOS artifact)."""
    arguments = arguments or {}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    state = session.get_session(session_id)
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "generator": {"name": SERVER_NAME, "version": VERSION},
        "session_id": session_id,
        "workflow": state.workflow,
        "analysis": state.last_analysis,
        "comparison": state.last_comparison,
        "chaos": state.last_chaos_report,
        "release_check": state.last_release_check,
        "incident_summary": state.last_incident_summary,
        "history": list(state.history),
    }
    session.record_call(session_id, "core.export_report", ok=True)
    return {"ok": True, "report": report}
