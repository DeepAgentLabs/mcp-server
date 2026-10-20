"""Adapter boundary for agentic-sidecar integration."""

from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Any

from deep_agentic_core_mcp.adapters import AdapterUnavailableError, ensure_repo_on_path

_IMPORT_ERROR: Exception | None = None
_package_root: Path | None = None
_version: str | None = None
_repo_root: Path | None = None

_package: ModuleType | None = None


def _runtime_status(package: Any) -> dict[str, Any]:
    """Inspect public APIs without starting a task, provider or operator server."""
    sidecar = getattr(package, "Sidecar", None)
    ready = callable(getattr(sidecar, "evaluate", None))
    features = []
    for owner, method, capability in (
        (sidecar, "evaluate", "decision_evaluation"),
        (sidecar, "enforce", "governance_enforcement"),
        (sidecar, "evaluate_plan", "plan_evaluation"),
        (getattr(package, "TaskRuntime", None), "snapshot", "runtime_events"),
        (getattr(package, "TaskRuntime", None), "control", "task_controls"),
        (getattr(package, "EventJournal", None), "export", "durable_audit"),
        (getattr(package, "AuthorityRegistry", None), "grant", "task_authority"),
        (getattr(package, "AuthorityRegistry", None), "revoke", "authority_revocation"),
        (getattr(package, "BoundAgent", None), "evidence", "redacted_evidence"),
    ):
        if callable(getattr(owner, method, None)):
            features.append(capability)
    if callable(getattr(package, "OperatorServer", None)):
        features.append("local_operator_http")
    return {
        "package_status": "implemented" if ready else "scaffold",
        "release_stage": "pre-alpha",
        "runtime_ready": ready,
        "runtime_connected": False,
        "mcp_runtime_controls": False,
        "installed_runtime_capabilities": features,
        "summary": (
            "Sidecar decision runtime is installed; MCP exposes package discovery only. "
            "No live task is connected through these tools."
            if ready
            else "Package is importable but no decision evaluation API was found."
        ),
        "first_runtime_milestone": (
            "v0.1 — Sidecar Runtime, Policy Advisor & Rule-Based Decision Gate"
        ),
        "current_focus": (
            "Installed local status/audit/operator APIs; MCP runtime bridging remains planned."
            if "local_operator_http" in features
            else "Installed deterministic decision supervision."
            if ready
            else "No implemented runtime detected."
        ),
    }


_PLANNED_MODULES = [
    "core",
    "gate",
    "intent",
    "evaluators",
    "status",
    "operations",
    "adapters",
    "integrations",
    "cli",
]

try:
    _repo_root = ensure_repo_on_path("agentic-sidecar")

    import agentic_sidecar as _agentic_sidecar_pkg

    _package = _agentic_sidecar_pkg
    _package_root = Path(_agentic_sidecar_pkg.__file__).resolve().parent
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
            "first_runtime_milestone": _runtime_status(None)["first_runtime_milestone"],
            "current_focus": None,
            "runtime_connected": False,
            "mcp_runtime_controls": False,
            "installed_runtime_capabilities": [],
        }
    return {"available": True, "version": _version, "error": None, **_runtime_status(_package)}


def describe_capabilities() -> list[str]:
    """Return the currently supported MCP-facing sidecar capabilities."""
    return ["status", "module_inventory"]


def status_summary() -> dict[str, Any]:
    """Return importability plus honest readiness information for sidecar."""
    _require_available()
    return {
        "package": "agentic-sidecar",
        "version": _version,
        **_runtime_status(_package),
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
    """Return the installed module inventory exposed by the sidecar package."""
    _require_available()
    if _package_root is None:
        raise AdapterUnavailableError("agentic_sidecar", RuntimeError("package root unavailable"))

    modules = _list_package_modules(_package_root)
    return {
        "package": "agentic-sidecar",
        "version": _version,
        "package_status": _runtime_status(_package)["package_status"],
        "top_level_modules": modules,
        "framework_adapters": _list_python_stems(_package_root, "adapters"),
        "integrations": _list_python_stems(_package_root, "integrations"),
        "planned_runtime_modules": [name for name in _PLANNED_MODULES if name not in modules],
        "installed_runtime_capabilities": _runtime_status(_package)[
            "installed_runtime_capabilities"
        ],
        "runtime_connected": False,
        "mcp_runtime_controls": False,
    }
