"""Phase 4 tools that compose existing MCP integrations."""

from typing import Any

from deep_agentic_core_mcp.adapters import AdapterUnavailableError
from deep_agentic_core_mcp.adapters.agenticlens import compare_runs as adapter_compare_runs
from deep_agentic_core_mcp.services import session


def _session_id(arguments: dict[str, Any]) -> str:
    value = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    return value if isinstance(value, str) else session.DEFAULT_SESSION_ID


def compare_runs(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Compare baseline and candidate runs through the existing Lens adapter."""
    arguments = arguments or {}
    session_id = _session_id(arguments)
    state = session.get_session(session_id)
    baseline = arguments.get("baseline", state.baseline_runs)
    candidate = arguments.get("candidate", state.candidate_runs)
    if not baseline or not candidate:
        return {"ok": False, "error": "Provide baseline and candidate runs"}
    try:
        result = adapter_compare_runs(
            baseline,
            candidate,
            regression_threshold=arguments.get("regression_threshold", 0.05),
        )
    except (AdapterUnavailableError, ValueError) as exc:
        session.record_call(session_id, "core.compare_runs", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    state.baseline_runs = baseline
    state.candidate_runs = candidate
    state.last_comparison = {"ok": True, **result}
    session.record_call(session_id, "core.compare_runs", ok=True)
    return state.last_comparison


def _comparison(arguments: dict[str, Any], state: session.SessionState) -> dict[str, Any] | None:
    comparison = arguments.get("comparison", state.last_comparison)
    return comparison if isinstance(comparison, dict) else None


def release_check(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Return a deterministic release decision from supplied evidence."""
    arguments = arguments or {}
    session_id = _session_id(arguments)
    state = session.get_session(session_id)
    gates: list[dict[str, Any]] = []
    comparison = _comparison(arguments, state)
    if comparison is not None:
        regressions = comparison.get("regressions", [])
        gates.append(
            {"name": "regressions", "passed": not bool(regressions), "count": len(regressions)}
        )
    report = arguments.get("evaluation_report")
    if isinstance(report, dict):
        summary = report.get("summary", {})
        pass_rate = summary.get("pass_rate")
        minimum = (arguments.get("thresholds") or {}).get("min_pass_rate")
        passed = isinstance(pass_rate, (int, float)) and (minimum is None or pass_rate >= minimum)
        gates.append({"name": "evaluation", "passed": passed, "pass_rate": pass_rate})
    chaos = arguments.get("chaos_report", state.last_chaos_report)
    if isinstance(chaos, dict):
        events = chaos.get("chaos_events", [])
        gates.append(
            {
                "name": "chaos",
                "passed": not bool(chaos.get("crashed") or chaos.get("timed_out")),
                "event_count": len(events),
            }
        )
    if not gates:
        return {
            "ok": False,
            "error": "Provide comparison, evaluation_report, or chaos_report evidence",
        }
    result = {
        "ok": True,
        "ready": all(gate["passed"] for gate in gates),
        "gates": gates,
        "evidence": {
            "has_comparison": comparison is not None,
            "has_evaluation": isinstance(report, dict),
            "has_chaos": isinstance(chaos, dict),
        },
    }
    state.last_release_check = result
    session.record_call(session_id, "core.release_check", ok=True)
    return result


def incident_summary(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Combine known workflow, comparison, chaos, and evaluation evidence."""
    arguments = arguments or {}
    session_id = _session_id(arguments)
    state = session.get_session(session_id)
    comparison = _comparison(arguments, state)
    chaos = arguments.get("chaos_report", state.last_chaos_report)
    evaluation = arguments.get("evaluation_report")
    findings: list[dict[str, Any]] = []
    if comparison and comparison.get("regressions"):
        findings.append(
            {"source": "comparison", "type": "regression", "items": comparison["regressions"]}
        )
    if isinstance(chaos, dict) and (
        chaos.get("crashed") or chaos.get("timed_out") or chaos.get("chaos_events")
    ):
        findings.append(
            {
                "source": "chaos",
                "type": "resilience_signal",
                "events": chaos.get("chaos_events", []),
                "crashed": bool(chaos.get("crashed")),
                "timed_out": bool(chaos.get("timed_out")),
            }
        )
    if isinstance(evaluation, dict):
        summary = evaluation.get("summary", {})
        if summary.get("pass_rate") is not None:
            findings.append(
                {
                    "source": "evaluation",
                    "type": "evaluation_summary",
                    "pass_rate": summary.get("pass_rate"),
                }
            )
    if not findings:
        return {"ok": False, "error": "No incident evidence supplied or stored in session"}
    result = {
        "ok": True,
        "status": "investigate",
        "workflow": state.workflow,
        "findings": findings,
        "history": list(state.history),
    }
    state.last_incident_summary = result
    session.record_call(session_id, "core.incident_summary", ok=True)
    return result


def export_report(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Export a deterministic, package-neutral unified evidence report."""
    arguments = arguments or {}
    session_id = _session_id(arguments)
    state = session.get_session(session_id)
    report = {
        "schema_version": "mcp.unified-report.v1",
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
