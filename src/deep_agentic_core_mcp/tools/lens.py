"""Lens tool placeholders."""

from deep_agentic_core_mcp.adapters.agenticlens import describe_capabilities


def capabilities() -> dict[str, list[str]]:
    """Return placeholder lens capabilities."""
    return {"lens": describe_capabilities()}
