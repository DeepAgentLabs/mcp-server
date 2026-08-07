"""AgenticLens-backed MCP tools."""

from typing import Any

from deep_agentic_core_mcp.adapters.agenticlens import (
    analyze_workflow as adapter_analyze_workflow,
    describe_capabilities,
)

def capabilities() -> dict[str, list[str]]:
    """Return lens capabilities."""
    return {"lens": describe_capabilities()}


def analyze_workflow(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Analyze an AgenticLens-compatible workflow artifact."""
    if not arguments or "artifact" not in arguments:
        return {"ok": False, "error": "Missing required 'artifact' argument"}
    return {"ok": True, **adapter_analyze_workflow(arguments["artifact"])}
