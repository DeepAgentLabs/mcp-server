"""Core server tools."""

from typing import Any

from deep_agentic_core_mcp.adapters import agentic_chaos as agentic_chaos_adapter
from deep_agentic_core_mcp.adapters import agentic_sidecar as agentic_sidecar_adapter
from deep_agentic_core_mcp.adapters import agenticlens as agenticlens_adapter
from deep_agentic_core_mcp.adapters import ai_operations_spec as ai_operations_spec_adapter
from deep_agentic_core_mcp.adapters import workspace_root
from deep_agentic_core_mcp.config import SERVER_NAME, VERSION
from deep_agentic_core_mcp.prompts.registry import list_prompts
from deep_agentic_core_mcp.resources.catalog import list_resources
from deep_agentic_core_mcp.services import session
from deep_agentic_core_mcp.tools.registry import list_tools

_ADAPTER_PROBES = {
    "agenticlens": agenticlens_adapter.probe,
    "agentic_chaos": agentic_chaos_adapter.probe,
    "agentic_sidecar": agentic_sidecar_adapter.probe,
    "ai_operations_spec": ai_operations_spec_adapter.probe,
}


def _probe_adapters() -> dict[str, dict[str, Any]]:
    return {name: probe() for name, probe in _ADAPTER_PROBES.items()}


def health(_: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return rich diagnostics: adapter availability, loaded surface, recent activity."""
    adapters = _probe_adapters()
    status = "ok" if all(info["available"] for info in adapters.values()) else "degraded"
    return {
        "status": status,
        "server": SERVER_NAME,
        "version": VERSION,
        "adapters": adapters,
        "tools_loaded": len(list_tools()),
        "resources_loaded": len(list_resources()),
        "prompts_loaded": len(list_prompts()),
        "workspace_root": str(workspace_root()),
        "last_successful_calls": session.last_successful_calls(),
    }


def version(_: dict[str, Any] | None = None) -> dict[str, str]:
    """Return the current package version."""
    return {"version": VERSION}


def verify(_: dict[str, Any] | None = None) -> dict[str, Any]:
    """Check connectivity to each integrated sibling project and report readiness."""
    adapters = _probe_adapters()
    return {
        "ok": all(info["available"] for info in adapters.values()),
        "adapters": adapters,
    }


def session_state(arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return what the active session currently holds, so shared context is inspectable."""
    session_id = (arguments or {}).get("session_id", session.DEFAULT_SESSION_ID)
    return {"session_id": session_id, **session.get_session(session_id).summary()}
