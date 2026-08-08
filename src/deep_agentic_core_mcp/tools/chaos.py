"""Chaos MCP tools."""

from typing import Any

from deep_agentic_core_mcp.adapters import AdapterUnavailableError
from deep_agentic_core_mcp.adapters.agentic_chaos import describe_capabilities
from deep_agentic_core_mcp.adapters.agentic_chaos import list_faults as adapter_list_faults
from deep_agentic_core_mcp.adapters.agentic_chaos import run_experiment as adapter_run_experiment
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
    state = session.get_session(session_id)
    state.last_chaos_report = result
    session.record_call(session_id, "chaos.run_experiment", ok=result["ok"])
    return result
