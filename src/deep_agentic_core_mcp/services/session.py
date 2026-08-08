"""Lightweight in-memory session state shared across sequential tool calls.

The MCP server runs as a single stdio process per client, so a simple
module-level store keyed by an optional `session_id` (defaulting to
`"default"`) is enough to let tools such as `lens.analyze_workflow` ->
`lens.compare_runs` -> `chaos.run_experiment` share artifacts without the
client resending them on every call. This intentionally does not persist
across process restarts.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

DEFAULT_SESSION_ID = "default"
_HISTORY_LIMIT = 50


@dataclass
class SessionState:
    """Artifacts and recent activity for one session."""

    workflow: dict[str, Any] | None = None
    last_analysis: dict[str, Any] | None = None
    baseline_runs: list[dict[str, Any]] | None = None
    candidate_runs: list[dict[str, Any]] | None = None
    last_comparison: dict[str, Any] | None = None
    last_chaos_report: dict[str, Any] | None = None
    history: deque[dict[str, Any]] = field(default_factory=lambda: deque(maxlen=_HISTORY_LIMIT))

    def summary(self) -> dict[str, Any]:
        """A compact, JSON-friendly view of what this session currently holds."""
        return {
            "has_workflow": self.workflow is not None,
            "has_analysis": self.last_analysis is not None,
            "baseline_run_count": len(self.baseline_runs) if self.baseline_runs else 0,
            "candidate_run_count": len(self.candidate_runs) if self.candidate_runs else 0,
            "has_comparison": self.last_comparison is not None,
            "has_chaos_report": self.last_chaos_report is not None,
            "history": list(self.history),
        }


_SESSIONS: dict[str, SessionState] = {}


def get_session(session_id: str = DEFAULT_SESSION_ID) -> SessionState:
    """Return the session state for `session_id`, creating it if needed."""
    return _SESSIONS.setdefault(session_id, SessionState())


def record_call(session_id: str, tool: str, ok: bool, note: str = "") -> None:
    """Append a call outcome to the session's history."""
    session = get_session(session_id)
    entry: dict[str, Any] = {
        "tool": tool,
        "ok": ok,
        "at": datetime.now(timezone.utc).isoformat(),
    }
    if note:
        entry["note"] = note
    session.history.append(entry)


def last_successful_calls(session_id: str = DEFAULT_SESSION_ID) -> dict[str, str]:
    """Return the most recent successful-call timestamp per tool name."""
    session = get_session(session_id)
    latest: dict[str, str] = {}
    for entry in session.history:
        if entry["ok"]:
            latest[entry["tool"]] = entry["at"]
    return latest


def reset_session(session_id: str = DEFAULT_SESSION_ID) -> None:
    """Discard a session's stored state."""
    _SESSIONS.pop(session_id, None)


def all_sessions() -> dict[str, SessionState]:
    """Return every tracked session, for diagnostics."""
    return dict(_SESSIONS)
