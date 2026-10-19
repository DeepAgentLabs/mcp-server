"""Adapter boundary for agentic-chaos integration."""

from __future__ import annotations

import fnmatch
import runpy
import uuid
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from deep_agentic_core_mcp import config
from deep_agentic_core_mcp.adapters import (
    AdapterUnavailableError,
    ensure_repo_on_path,
    workspace_root,
)

_IMPORT_ERROR: Exception | None = None
_version: str | None = None

try:
    ensure_repo_on_path("agentic-chaos")

    import agentic_chaos as _agentic_chaos_pkg
    from agentic_chaos.chaos.faults import FAULT_REGISTRY, resolve_faults
    from agentic_chaos.chaos.session import chaos_session

    _version = _agentic_chaos_pkg.__version__
except Exception as exc:  # noqa: BLE001 - captured for core.verify/core.health reporting
    _IMPORT_ERROR = exc

# AIOS run export ships in agentic-chaos 0.5.1; older installs still run experiments.
_AIOS_EXPORT_ERROR: Exception | None = None
try:
    from agentic_chaos.export.aios import to_aios_run as _to_aios_run
except Exception as exc:  # noqa: BLE001 - reported per call and by probe()
    _AIOS_EXPORT_ERROR = exc

AIOS_EXPORT_MIN_VERSION = "0.5.1"


def _require_available() -> None:
    if _IMPORT_ERROR is not None:
        raise AdapterUnavailableError("agentic_chaos", _IMPORT_ERROR)


def probe() -> dict[str, Any]:
    """Report whether the agentic-chaos integration is reachable."""
    return {
        "available": _IMPORT_ERROR is None,
        "version": _version,
        "aios_export": _IMPORT_ERROR is None and _AIOS_EXPORT_ERROR is None,
        "error": None if _IMPORT_ERROR is None else str(_IMPORT_ERROR),
    }


def describe_capabilities() -> list[str]:
    """Return the supported chaos integration capabilities."""
    return ["list_faults", "run_experiment", "export_aios_run"]


def aios_export_available() -> bool:
    """Whether the installed agentic-chaos can export AIOS run artifacts."""
    return _IMPORT_ERROR is None and _AIOS_EXPORT_ERROR is None


def export_aios_run(
    report: dict[str, Any],
    *,
    status: str = "completed",
    workflow_id: str | None = None,
) -> dict[str, Any]:
    """Convert a ChaosReport-shaped dict into an AIOS v0.4-draft run via agentic-chaos."""
    _require_available()
    if _AIOS_EXPORT_ERROR is not None:
        raise AdapterUnavailableError(
            "agentic_chaos",
            RuntimeError(
                f"AIOS run export requires agentic-chaos>={AIOS_EXPORT_MIN_VERSION} "
                f"(installed: {_version}): {_AIOS_EXPORT_ERROR}"
            ),
        )
    return _to_aios_run(report, status=status, workflow_id=workflow_id)  # type: ignore[no-any-return]


def list_faults() -> dict[str, list[dict[str, Any]]]:
    """Return the registered chaos fault inventory."""
    _require_available()
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


def _resolve_sandboxed_script(script: str) -> Path:
    """Resolve `script` and reject anything outside the workspace.

    Mirrors the confinement `chaos.run_experiment` promises MCP clients: the
    tool can execute code, but only code already living somewhere in this
    workspace (mcp-server, its sibling repos, or the caller's own checkout
    alongside them) - not an arbitrary path on the host machine.
    """
    root = workspace_root().resolve()
    raw_path = Path(script)
    candidate = raw_path.resolve() if raw_path.is_absolute() else (root / raw_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"script must resolve inside the workspace ({root}): {script}") from exc
    if not candidate.is_file():
        raise ValueError(f"script not found: {candidate}")
    _enforce_script_policy(candidate.relative_to(root).as_posix())
    return candidate


def _enforce_script_policy(relative_path: str) -> None:
    """Apply the configured allow/deny globs on top of workspace confinement.

    Deny always wins; when an allowlist is configured, the script must match it.
    """
    policy = config.script_policy()
    denied = next(
        (glob for glob in policy["denied"] if fnmatch.fnmatchcase(relative_path, glob)), None
    )
    if denied is not None:
        raise ValueError(f"script {relative_path} is denied by script policy glob {denied!r}")
    if policy["allowed"] and not any(
        fnmatch.fnmatchcase(relative_path, glob) for glob in policy["allowed"]
    ):
        raise ValueError(
            f"script {relative_path} is not in the configured allowlist "
            f"({config.ALLOWED_SCRIPT_GLOBS_ENV})"
        )


def run_experiment(
    script: str,
    faults: list[str],
    *,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    """Run a sandboxed target script inside a chaos_session and report what happened.

    Mirrors what the agentic-chaos CLI's `chaos run` command does internally
    (runpy.run_path inside chaos_session) against the library's public API -
    that command's own helper is private, so it isn't imported directly.

    Runs on a worker thread so `timeout_seconds` can be enforced even when a
    fault (e.g. TokenTimeoutFault) sleeps past it. Python cannot forcibly
    kill a thread, so on timeout the script's thread may keep running in the
    background after this function returns a "timed_out" result - this is a
    real limitation of in-process sandboxing, not a hard kill.
    """
    _require_available()
    script_path = _resolve_sandboxed_script(script)
    resolved_faults = resolve_faults(faults)  # raises ValueError on unknown fault names

    def _run() -> tuple[Any, BaseException | None]:
        with chaos_session(resolved_faults) as session:
            crashed: BaseException | None = None
            try:
                runpy.run_path(str(script_path), run_name="__main__")
            except SystemExit as exc:
                if exc.code not in (None, 0):
                    crashed = exc
            except Exception as exc:  # noqa: BLE001 - reported back, not swallowed silently
                crashed = exc
        return session, crashed

    started_at = datetime.now(timezone.utc)
    timed_out = False
    session = None
    crashed: BaseException | None = None
    # Deliberately not a `with` block: ThreadPoolExecutor.__exit__ calls
    # shutdown(wait=True), which would block for the worker thread to finish
    # regardless of the timeout below - defeating the whole point of it.
    # shutdown(wait=False) lets this function return promptly on timeout; the
    # thread is intentionally left to finish (or not) in the background, per
    # this function's documented can't-force-kill-a-thread limitation.
    executor = ThreadPoolExecutor(max_workers=1)
    try:
        future = executor.submit(_run)
        try:
            session, crashed = future.result(timeout=timeout_seconds)
        except FutureTimeoutError:
            timed_out = True
    finally:
        executor.shutdown(wait=False)
    ended_at = datetime.now(timezone.utc)

    events = session.events_as_json() if session is not None else []
    return {
        "ok": not timed_out and crashed is None,
        "id": str(uuid.uuid4()),
        "name": script_path.stem,
        "start_time": started_at.isoformat(),
        "end_time": ended_at.isoformat(),
        "chaos_events": events,
        "crashed": repr(crashed) if crashed is not None else None,
        "timed_out": timed_out,
    }
