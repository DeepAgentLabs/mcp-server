"""Adapter boundary for agentic-sidecar integration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from deep_agentic_core_mcp.adapters import AdapterUnavailableError, ensure_repo_on_path

_IMPORT_ERROR: Exception | None = None
_version: str | None = None
_repo_root: Path | None = None

_CURRENT_STATUS = {
    "package_status": "scaffold",
    "release_stage": "pre-alpha",
    "runtime_ready": False,
    "summary": (
        "agentic-sidecar is importable, but its decision runtime is still planned rather "
        "than implemented."
    ),
    "first_runtime_milestone": "v0.1 — Sidecar Runtime, Policy Advisor & Rule-Based Decision Gate",
    "current_focus": "LangGraph adapter first, deterministic policy/risk Decision Gate.",
}

_PLANNED_MODULES = [
    "core",
    "gate",
    "intent",
    "evaluators",
    "status",
    "adapters",
    "integrations",
    "cli",
]

try:
    _repo_root = ensure_repo_on_path("agentic-sidecar")

    import agentic_sidecar as _agentic_sidecar_pkg

    _version = _agentic_sidecar_pkg.__version__
except Exception as exc:  # noqa: BLE001 - captured for core.verify/core.health reporting
    _IMPORT_ERROR = exc


def _require_available() -> None:
    if _IMPORT_ERROR is not None:
        raise AdapterUnavailableError("agentic_sidecar", _IMPORT_ERROR)


def probe() -> dict[str, Any]:
    """Report whether the agentic-sidecar integration is reachable."""
    if _IMPORT_ERROR is not None:
        return {
            "available": False,
            "version": None,
            "error": str(_IMPORT_ERROR),
            "package_status": "unavailable",
            "release_stage": None,
            "runtime_ready": False,
            "summary": "agentic-sidecar could not be imported in this environment.",
            "first_runtime_milestone": _CURRENT_STATUS["first_runtime_milestone"],
            "current_focus": None,
        }
    return {"available": True, "version": _version, "error": None, **_CURRENT_STATUS}


def describe_capabilities() -> list[str]:
    """Return the currently supported MCP-facing sidecar capabilities."""
    return ["status", "module_inventory"]


def status_summary() -> dict[str, Any]:
    """Return importability plus honest readiness information for sidecar."""
    _require_available()
    return {
        "package": "agentic-sidecar",
        "version": _version,
        **_CURRENT_STATUS,
    }


def _list_package_modules(package_root: Path) -> list[str]:
    return sorted(
        child.name
        for child in package_root.iterdir()
        if child.is_dir() and child.name != "__pycache__"
    )


def _list_python_stems(package_root: Path, subdir: str) -> list[str]:
    return sorted(
        path.stem for path in (package_root / subdir).glob("*.py") if path.stem != "__init__"
    )


def module_inventory() -> dict[str, Any]:
    """Return the current scaffold inventory exposed by the sidecar package."""
    _require_available()
    if _repo_root is None:
        raise AdapterUnavailableError("agentic_sidecar", RuntimeError("repo root unavailable"))

    package_root = _repo_root / "src" / "agentic_sidecar"
    modules = _list_package_modules(package_root)
    return {
        "package": "agentic-sidecar",
        "version": _version,
        "package_status": _CURRENT_STATUS["package_status"],
        "top_level_modules": modules,
        "framework_adapters": _list_python_stems(package_root, "adapters"),
        "integrations": _list_python_stems(package_root, "integrations"),
        "planned_runtime_modules": list(_PLANNED_MODULES),
    }
