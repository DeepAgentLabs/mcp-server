"""Adapter boundary for agentic-chaos integration."""

from __future__ import annotations

from typing import Any

from deep_agentic_core_mcp.adapters import ensure_repo_on_path

ensure_repo_on_path("agentic-chaos")

from agentic_chaos.chaos.faults import FAULT_REGISTRY  # noqa: E402


def describe_capabilities() -> list[str]:
    """Return the supported chaos integration capabilities."""
    return ["list_faults", "run_experiment"]


def list_faults() -> dict[str, list[dict[str, Any]]]:
    """Return the registered chaos fault inventory."""
    return {
        "faults": [
            {
                "name": name,
                "class_name": fault_cls.__name__,
                "module": fault_cls.__module__,
            }
            for name, fault_cls in sorted(FAULT_REGISTRY.items())
        ]
    }
