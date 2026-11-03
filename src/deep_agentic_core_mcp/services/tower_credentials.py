"""Host-owned per-user Tower bindings. Tool arguments cannot select credentials."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from urllib.parse import urlsplit


@dataclass(frozen=True)
class TowerCredentials:
    origin: str
    read_token: str = field(repr=False)
    write_token: str = field(default="", repr=False)


def for_user(user: str) -> TowerCredentials | None:
    """Reload trusted host configuration per dispatch; never fall back to local tokens."""
    try:
        bindings = json.loads(os.environ.get("DEEP_AGENTIC_CORE_MCP_TOWER_BINDINGS", "{}"))
        entry = bindings.get(user)
        if not isinstance(entry, dict) or set(entry) - {"origin", "read_token", "write_token"}:
            return None
        origin = entry["origin"]
        read = entry["read_token"]
        write = entry.get("write_token", "")
        if not all(isinstance(v, str) for v in (origin, read, write)) or not read:
            return None
        parsed = urlsplit(origin)
        if (
            parsed.scheme != "https"
            or not parsed.netloc
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or parsed.path not in ("", "/")
            or any(c.isspace() for c in origin + read + write)
        ):
            return None
        return TowerCredentials(origin.rstrip("/"), read, write)
    except (ValueError, TypeError, KeyError, AttributeError):
        return None
