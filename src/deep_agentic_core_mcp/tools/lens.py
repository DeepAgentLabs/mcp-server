"""AgenticLens-backed MCP tools."""

from typing import Any

from deep_agentic_core_mcp.adapters import AdapterUnavailableError
from deep_agentic_core_mcp.adapters.agenticlens import analyze_workflow as adapter_analyze_workflow
from deep_agentic_core_mcp.adapters.agenticlens import audit_report as adapter_audit_report
from deep_agentic_core_mcp.adapters.agenticlens import compare_runs as adapter_compare_runs
from deep_agentic_core_mcp.adapters.agenticlens import describe_capabilities
from deep_agentic_core_mcp.adapters.agenticlens import report_summary as adapter_report_summary
from deep_agentic_core_mcp.adapters.agenticlens import slo_summary as adapter_slo_summary
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
    except AdapterUnavailableError as exc:
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
    except AdapterUnavailableError as exc:
        session.record_call(session_id, "lens.audit_report", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    session.record_call(session_id, "lens.audit_report", ok=True)
    return result
