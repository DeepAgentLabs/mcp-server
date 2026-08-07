"""AI Operations specification MCP tools."""

from __future__ import annotations

from typing import Any

from deep_agentic_core_mcp.adapters.ai_operations_spec import (
    describe_capabilities,
    validate_artifact as adapter_validate_artifact,
)


def capabilities() -> dict[str, list[str]]:
    """Return specification capabilities."""
    return {"spec": describe_capabilities()}


def validate_artifact(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Validate a workflow or run artifact against the v0.4 draft."""
    if not arguments or "artifact" not in arguments:
        return {"ok": False, "error": "Missing required 'artifact' argument"}
    return adapter_validate_artifact(arguments["artifact"])
