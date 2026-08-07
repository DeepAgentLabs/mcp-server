"""Chaos MCP tools."""

from typing import Any

from deep_agentic_core_mcp.adapters.agentic_chaos import (
    describe_capabilities,
    list_faults as adapter_list_faults,
)

def capabilities() -> dict[str, list[str]]:
    """Return chaos capabilities."""
    return {"chaos": describe_capabilities()}


def list_faults(_: dict[str, Any] | None = None) -> dict[str, list[dict[str, Any]]]:
    """Return the supported chaos faults."""
    return adapter_list_faults()
