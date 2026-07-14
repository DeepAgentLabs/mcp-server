"""Adapter boundary for agenticlens integration."""


def describe_capabilities() -> list[str]:
    """Return the initial capability placeholders for lens integration."""
    return ["analyze_workflow", "profile_workflow"]
