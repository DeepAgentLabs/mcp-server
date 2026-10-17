"""AgenticLens-backed MCP tools."""

from typing import Any

from deep_agentic_core_mcp.adapters import AdapterUnavailableError
from deep_agentic_core_mcp.adapters.agenticlens import analyze_workflow as adapter_analyze_workflow
from deep_agentic_core_mcp.adapters.agenticlens import audit_report as adapter_audit_report
from deep_agentic_core_mcp.adapters.agenticlens import compare_runs as adapter_compare_runs
from deep_agentic_core_mcp.adapters.agenticlens import describe_capabilities
from deep_agentic_core_mcp.adapters.agenticlens import diagnose_run as adapter_diagnose_run
from deep_agentic_core_mcp.adapters.agenticlens import report_summary as adapter_report_summary
from deep_agentic_core_mcp.adapters.agenticlens import score_analysis as adapter_score_analysis
from deep_agentic_core_mcp.adapters.agenticlens import slo_summary as adapter_slo_summary
from deep_agentic_core_mcp.adapters.agenticlens import suite_check as adapter_suite_check
from deep_agentic_core_mcp.adapters.agenticlens import (
    suite_from_traces as adapter_suite_from_traces,
)
from deep_agentic_core_mcp.services import session


def capabilities() -> dict[str, list[str]]:
    """Return lens capabilities."""
    return {"lens": describe_capabilities()}


def analyze_workflow(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Analyze an AgenticLens-compatible workflow artifact."""
    if not arguments or "artifact" not in arguments:
        return {"ok": False, "error": "Missing required 'artifact' argument"}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    try:
        result = {"ok": True, **adapter_analyze_workflow(arguments["artifact"])}
    except AdapterUnavailableError as exc:
        session.record_call(session_id, "lens.analyze_workflow", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    state = session.get_session(session_id)
    state.workflow = arguments["artifact"]
    state.last_analysis = result
    session.record_call(session_id, "lens.analyze_workflow", ok=True)
    return result


def report_summary(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Render a Markdown workflow report alongside the usual analysis metrics.

    `artifact` may be omitted if a workflow was already analyzed in this
    session (via `lens.analyze_workflow` or a previous `report_summary`
    call) - the stored artifact is reused.
    """
    arguments = arguments or {}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    state = session.get_session(session_id)
    artifact = arguments.get("artifact", state.workflow)
    if artifact is None:
        return {"ok": False, "error": "Missing 'artifact' and no workflow stored in session"}
    try:
        result = {"ok": True, **adapter_report_summary(artifact)}
    except AdapterUnavailableError as exc:
        session.record_call(session_id, "lens.report_summary", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    state.workflow = artifact
    session.record_call(session_id, "lens.report_summary", ok=True)
    return result


def compare_runs(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Compare baseline and candidate trace runs for regressions.

    `baseline`/`candidate` may be omitted if a comparison already stored
    runs in this session under the same slots.
    """
    arguments = arguments or {}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    state = session.get_session(session_id)
    baseline = arguments.get("baseline", state.baseline_runs)
    candidate = arguments.get("candidate", state.candidate_runs)
    if not baseline or not candidate:
        return {
            "ok": False,
            "error": "Missing 'baseline'/'candidate' and none stored in session",
        }
    regression_threshold = arguments.get("regression_threshold", 0.05)
    try:
        result = {
            "ok": True,
            **adapter_compare_runs(baseline, candidate, regression_threshold=regression_threshold),
        }
    except AdapterUnavailableError as exc:
        session.record_call(session_id, "lens.compare_runs", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    state.baseline_runs = baseline
    state.candidate_runs = candidate
    state.last_comparison = result
    session.record_call(session_id, "lens.compare_runs", ok=True)
    return result


def slo_summary(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Apply release-gate style SLO thresholds to an evaluation report."""
    if not arguments or "report" not in arguments:
        return {"ok": False, "error": "Missing required 'report' argument"}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    try:
        result = {
            "ok": True,
            **adapter_slo_summary(arguments["report"], arguments.get("thresholds")),
        }
    except (AdapterUnavailableError, ValueError) as exc:
        session.record_call(session_id, "lens.slo_summary", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    session.record_call(session_id, "lens.slo_summary", ok=True)
    return result


def audit_report(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Return case-by-case evaluation detail for an audit trail."""
    if not arguments or "report" not in arguments:
        return {"ok": False, "error": "Missing required 'report' argument"}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    try:
        result = {
            "ok": True,
            **adapter_audit_report(
                arguments["report"], include_html=bool(arguments.get("include_html", False))
            ),
        }
    except (AdapterUnavailableError, ValueError) as exc:
        session.record_call(session_id, "lens.audit_report", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    session.record_call(session_id, "lens.audit_report", ok=True)
    return result


def diagnose_run(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Diagnose a trace run and attribute its failure to a step and agent."""
    if not arguments or "run" not in arguments:
        return {"ok": False, "error": "Missing required 'run' argument"}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    try:
        result = {
            "ok": True,
            **adapter_diagnose_run(
                arguments["run"],
                baseline=arguments.get("baseline"),
                config=arguments.get("config"),
                budget=arguments.get("budget"),
                include_narrative=bool(arguments.get("include_narrative", True)),
            ),
        }
    except AdapterUnavailableError as exc:
        session.record_call(session_id, "lens.diagnose_run", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    except ValueError as exc:
        session.record_call(session_id, "lens.diagnose_run", ok=False, note=str(exc))
        return {"ok": False, "error": f"Invalid diagnosis input: {exc}"}
    session.record_call(session_id, "lens.diagnose_run", ok=True)
    return result


def score_analysis(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Split an evaluation report into deterministic and model-based results."""
    if not arguments or "report" not in arguments:
        return {"ok": False, "error": "Missing required 'report' argument"}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    try:
        result = {"ok": True, **adapter_score_analysis(arguments["report"])}
    except (AdapterUnavailableError, ValueError) as exc:
        session.record_call(session_id, "lens.score_analysis", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    session.record_call(session_id, "lens.score_analysis", ok=True)
    return result


def suite_from_traces(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Convert trace runs into a draft regression suite (PII masked by default)."""
    arguments = arguments or {}
    missing = [key for key in ("runs", "name", "version") if key not in arguments]
    if missing:
        return {"ok": False, "error": f"Missing required argument(s): {', '.join(missing)}"}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    try:
        result = {
            "ok": True,
            **adapter_suite_from_traces(
                arguments["runs"],
                name=arguments["name"],
                version=arguments["version"],
                latency_margin=arguments.get("latency_margin", 1.5),
                cost_margin=arguments.get("cost_margin", 1.5),
                include_output=bool(arguments.get("include_output", False)),
                mask=bool(arguments.get("mask", True)),
                strategy=arguments.get("strategy", "redact"),
            ),
        }
    except AdapterUnavailableError as exc:
        session.record_call(session_id, "lens.suite_from_traces", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    except ValueError as exc:
        session.record_call(session_id, "lens.suite_from_traces", ok=False, note=str(exc))
        return {"ok": False, "error": f"Invalid suite input: {exc}"}
    session.record_call(session_id, "lens.suite_from_traces", ok=True)
    return result


def suite_check(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Check a suite for duplicates, unmasked PII, and approval readiness."""
    if not arguments or "suite" not in arguments:
        return {"ok": False, "error": "Missing required 'suite' argument"}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    try:
        result = {
            "ok": True,
            **adapter_suite_check(arguments["suite"], threshold=arguments.get("threshold", 0.85)),
        }
    except AdapterUnavailableError as exc:
        session.record_call(session_id, "lens.suite_check", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    except ValueError as exc:
        session.record_call(session_id, "lens.suite_check", ok=False, note=str(exc))
        return {"ok": False, "error": f"Invalid suite: {exc}"}
    session.record_call(session_id, "lens.suite_check", ok=True)
    return result
