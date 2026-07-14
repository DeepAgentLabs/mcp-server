"""Core server tool stubs."""

from deep_agentic_core_mcp.config import SERVER_NAME, VERSION


def health() -> dict[str, str]:
    """Return a basic health payload."""
    return {"status": "ok", "server": SERVER_NAME}


def version() -> dict[str, str]:
    """Return the current package version."""
    return {"version": VERSION}
