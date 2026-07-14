"""Chaos tool placeholders."""

from deep_agentic_core_mcp.adapters.agentic_chaos import describe_capabilities


def capabilities() -> dict[str, list[str]]:
    """Return placeholder chaos capabilities."""
    return {"chaos": describe_capabilities()}
