"""Per-key tool permissions for hosted HTTP, enforced at dispatch outside the model.

A policy is operator configuration attached to one hosted key: allow and deny
tool-name globs, an optional expiry and an optional task scope. Deny always wins,
an expired policy denies every tool, and a stored policy that fails validation
denies every tool rather than falling back to the default surface. Local stdio
is trusted and never consults a policy.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from fnmatch import fnmatchcase
from typing import Any

# Answers "what may this key do?" about the caller itself, so a policy that
# omits it still lets a client discover why its other calls are denied.
ALWAYS_PERMITTED = frozenset({"core.access_status"})

_MAX_PATTERNS = 64
_MAX_TEXT = 128
_FIELDS = {"allow", "deny", "expires_at", "task_id"}


def _patterns(value: Any, name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) > _MAX_PATTERNS:
        raise ValueError(f"{name} must be a list of at most {_MAX_PATTERNS} tool-name globs")
    for pattern in value:
        if not isinstance(pattern, str) or not pattern or len(pattern) > _MAX_TEXT:
            raise ValueError(f"{name} entries must be nonempty strings of at most {_MAX_TEXT}")
    return tuple(value)


def _expiry(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("expires_at must be epoch seconds or an ISO 8601 timestamp")
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("expires_at must be an ISO 8601 timestamp") from exc
        if parsed.tzinfo is None:
            raise ValueError("expires_at must include a timezone")
        return parsed.timestamp()
    raise ValueError("expires_at must be epoch seconds or an ISO 8601 timestamp")


@dataclass(frozen=True)
class AccessPolicy:
    allow: tuple[str, ...] = ("*",)
    deny: tuple[str, ...] = ()
    expires_at: float | None = None
    task_id: str | None = None
    configured: bool = False
    error: str | None = field(default=None, compare=False)

    @classmethod
    def from_config(cls, value: Mapping[str, Any] | None) -> AccessPolicy:
        """Validate operator configuration; raises ValueError on any malformed field."""
        if value is None:
            return cls()
        if not isinstance(value, Mapping):
            raise ValueError("An access policy must be an object")
        unknown = set(value) - _FIELDS
        if unknown:
            raise ValueError(f"Unknown access policy fields: {sorted(unknown)}")
        task_id = value.get("task_id")
        if task_id is not None and (
            not isinstance(task_id, str) or not task_id or len(task_id) > _MAX_TEXT
        ):
            raise ValueError(f"task_id must be a nonempty string of at most {_MAX_TEXT}")
        return cls(
            allow=_patterns(value.get("allow", ["*"]), "allow"),
            deny=_patterns(value.get("deny", []), "deny"),
            expires_at=_expiry(value.get("expires_at")),
            task_id=task_id,
            configured=True,
        )

    @classmethod
    def load(cls, value: Any) -> AccessPolicy:
        """Load stored configuration, failing closed: invalid policies deny every tool."""
        try:
            return cls.from_config(value)
        except ValueError as exc:
            return cls(allow=(), configured=True, error=str(exc))

    def to_config(self) -> dict[str, Any]:
        config: dict[str, Any] = {"allow": list(self.allow), "deny": list(self.deny)}
        if self.expires_at is not None:
            config["expires_at"] = self.expires_at
        if self.task_id is not None:
            config["task_id"] = self.task_id
        return config

    def expired(self, now: float | None = None) -> bool:
        return self.expires_at is not None and (time.time() if now is None else now) >= self.expires_at

    def denial_reason(self, tool: str, now: float | None = None) -> str | None:
        """Return why `tool` is denied, or None when the call may dispatch."""
        if self.error is not None:
            return "invalid access policy"
        if any(fnmatchcase(tool, pattern) for pattern in self.deny):
            return "tool denied by policy"
        if tool in ALWAYS_PERMITTED:
            return None
        if self.expired(now):
            return "access policy expired"
        if not any(fnmatchcase(tool, pattern) for pattern in self.allow):
            return "tool not in policy allow list"
        return None

    def permits(self, tool: str, now: float | None = None) -> bool:
        return self.denial_reason(tool, now) is None


@dataclass(frozen=True)
class Principal:
    """An authenticated hosted caller and the policy attached to its key."""

    user: str
    policy: AccessPolicy = AccessPolicy()


def authorize(store: Any, token: str) -> Principal | None:
    """Authenticate a key and load its policy.

    Stores that predate permissions (or third-party KeyStore implementations)
    expose only `authenticate`; their keys keep the default hosted surface.
    """
    native: Callable[[str], Principal | None] | None = getattr(store, "authorize", None)
    if native is not None:
        return native(token)
    user = store.authenticate(token)
    return None if user is None else Principal(user)
