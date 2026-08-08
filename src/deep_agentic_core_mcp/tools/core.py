"""Core server tools."""

from typing import Any

from deep_agentic_core_mcp.config import SERVER_NAME, VERSION


def health(_: dict[str, Any] | None = None) -> dict[str, str]:
    """Return a basic health payload."""
    return {"status": "ok", "server": SERVER_NAME}


def version(_: dict[str, Any] | None = None) -> dict[str, str]:
    """Return the current package version."""
    return {"version": VERSION}
