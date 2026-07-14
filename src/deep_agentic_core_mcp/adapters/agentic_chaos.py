"""Adapter boundary for agentic-chaos integration."""


def describe_capabilities() -> list[str]:
    """Return the initial capability placeholders for chaos integration."""
    return ["list_faults", "run_experiment"]
