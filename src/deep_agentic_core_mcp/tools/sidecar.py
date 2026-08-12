"""Agentic Sidecar-backed MCP tools."""

from __future__ import annotations

from typing import Any

from deep_agentic_core_mcp.adapters import AdapterUnavailableError
from deep_agentic_core_mcp.adapters.agentic_sidecar import describe_capabilities
from deep_agentic_core_mcp.adapters.agentic_sidecar import (
    module_inventory as adapter_module_inventory,
)
from deep_agentic_core_mcp.adapters.agentic_sidecar import status_summary as adapter_status_summary


def capabilities() -> dict[str, list[str]]:
    """Return sidecar capabilities."""
    return {"sidecar": describe_capabilities()}


def status(_: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return sidecar package availability and runtime readiness."""
    try:
        return {"ok": True, **adapter_status_summary()}
    except AdapterUnavailableError as exc:
        return {"ok": False, "error": str(exc)}


def module_inventory(_: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return the scaffolded module, adapter, and integration inventory."""
    try:
        return {"ok": True, **adapter_module_inventory()}
    except AdapterUnavailableError as exc:
        return {"ok": False, "error": str(exc)}
