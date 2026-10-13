"""Chaos MCP tools."""

from typing import Any

from deep_agentic_core_mcp import config
from deep_agentic_core_mcp.adapters import AdapterUnavailableError
from deep_agentic_core_mcp.adapters.agentic_chaos import (
    AIOS_EXPORT_MIN_VERSION,
    aios_export_available,
    describe_capabilities,
)
from deep_agentic_core_mcp.adapters.agentic_chaos import export_aios_run as adapter_export_aios_run
from deep_agentic_core_mcp.adapters.agentic_chaos import list_faults as adapter_list_faults
from deep_agentic_core_mcp.adapters.agentic_chaos import run_experiment as adapter_run_experiment
from deep_agentic_core_mcp.adapters.ai_operations_spec import (
    validate_artifact as adapter_validate_artifact,
)
from deep_agentic_core_mcp.services import session


def capabilities() -> dict[str, list[str]]:
    """Return chaos capabilities."""
    return {"chaos": describe_capabilities()}


def list_faults(_: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return the supported chaos faults."""
    try:
        return adapter_list_faults()
    except AdapterUnavailableError as exc:
        return {"ok": False, "error": str(exc)}


def run_experiment(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Run a sandboxed target script under selected chaos faults."""
    if config.is_remote_transport() and not config.remote_chaos_allowed():
        return {
            "ok": False,
            "error": (
                "chaos.run_experiment is disabled over remote transport: it executes "
                "arbitrary code and workspace-path confinement alone is not a sandbox. "
                "See SECURITY.md. Set DEEP_AGENTIC_CORE_MCP_ALLOW_REMOTE_CHAOS=1 only "
                "after adding a real sandbox (container, restricted user, hard limits)."
            ),
        }
    if not arguments or "script" not in arguments or "faults" not in arguments:
        return {"ok": False, "error": "Missing required 'script' and/or 'faults' argument"}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    timeout_seconds = arguments.get("timeout_seconds", 30.0)
    try:
        result = adapter_run_experiment(
            arguments["script"],
            arguments["faults"],
            timeout_seconds=timeout_seconds,
        )
    except (AdapterUnavailableError, ValueError) as exc:
        session.record_call(session_id, "chaos.run_experiment", ok=False, note=str(exc))
        return {"ok": False, "error": str(exc)}
    if arguments.get("export_aios", True):
        result.update(_aios_export(result, arguments.get("workflow_id")))
    state = session.get_session(session_id)
    state.last_chaos_report = result
    session.record_call(session_id, "chaos.run_experiment", ok=result["ok"])
    return result


def _run_status(report: dict[str, Any]) -> str:
    """The AIOS Run status this server observed for a chaos report it produced."""
    return "failed" if report.get("crashed") or report.get("timed_out") else "completed"


def _aios_export(
    report: dict[str, Any], workflow_id: str | None, *, status: str | None = None
) -> dict[str, Any]:
    """Export via agentic-chaos, then validate the result with the specification adapter."""
    if not aios_export_available():
        return {
            "aios_run": None,
            "aios_export": {
                "available": False,
                "reason": f"requires agentic-chaos>={AIOS_EXPORT_MIN_VERSION}",
            },
        }
    try:
        artifact = adapter_export_aios_run(
            report, status=status or _run_status(report), workflow_id=workflow_id
        )
    except (AdapterUnavailableError, ValueError) as exc:
        return {"aios_run": None, "aios_export": {"available": False, "reason": str(exc)}}
    try:
        validation = adapter_validate_artifact(artifact)
    except AdapterUnavailableError as exc:
        return {
            "aios_run": artifact,
            "aios_export": {"available": True, "validated": False, "reason": str(exc)},
        }
    conformance = validation.get("conformance", {})
    return {
        "aios_run": artifact,
        "aios_export": {
            "available": True,
            "validated": True,
            "aligned": bool(conformance.get("aligned")),
            "claim": validation.get("claim"),
            "issues": conformance.get("issues", validation.get("errors", [])),
        },
    }


def export_aios_run(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Convert a chaos report to an AIOS v0.4-draft run artifact and validate it.

    `report` may be omitted to reuse the session's last `chaos.run_experiment`
    result. No code runs, so this tool is also available over remote transport.
    """
    arguments = arguments or {}
    session_id = arguments.get("session_id", session.DEFAULT_SESSION_ID)
    state = session.get_session(session_id)
    report = arguments.get("report", state.last_chaos_report)
    if not report:
        return {"ok": False, "error": "Missing 'report' and no chaos report stored in session"}
    status = arguments.get("status")
    exported = _aios_export(report, arguments.get("workflow_id"), status=status)
    if exported["aios_run"] is None:
        reason = exported["aios_export"]["reason"]
        session.record_call(session_id, "chaos.export_aios_run", ok=False, note=reason)
        return {"ok": False, "error": reason, **exported}
    aligned = bool(exported["aios_export"].get("aligned"))
    session.record_call(session_id, "chaos.export_aios_run", ok=aligned)
    return {"ok": aligned, **exported}
