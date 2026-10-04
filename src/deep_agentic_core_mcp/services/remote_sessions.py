"""Tenant-scoped transactional session storage for remote tool calls."""

from __future__ import annotations

import copy
import hashlib
import json
import threading
import time
from collections.abc import Iterator
from contextlib import AbstractContextManager, contextmanager
from dataclasses import asdict
from typing import Protocol, cast

from deep_agentic_core_mcp.services import session

MAX_SESSIONS = 100
MAX_STATE_BYTES = 4 * 1024 * 1024


class SessionStore(Protocol):
    def transaction(self, owner: str) -> AbstractContextManager[None]: ...

    def ping(self) -> bool: ...


def encode(states: dict[str, session.SessionState]) -> str:
    if len(states) > MAX_SESSIONS:
        raise ValueError("User session limit reached")
    data = {}
    for key, state in states.items():
        item = asdict(state)
        item["history"] = list(state.history)
        data[key] = item
    payload = json.dumps(data)
    if len(payload.encode()) > MAX_STATE_BYTES:
        raise ValueError("User session storage limit reached")
    return payload


def decode(payload: str | None) -> dict[str, session.SessionState]:
    from collections import deque

    states = {}
    for key, item in json.loads(payload or "{}").items():
        item["history"] = deque(item["history"], maxlen=session._HISTORY_LIMIT)
        states[key] = session.SessionState(**item)
    return states


class MemorySessionStore:
    """Explicit development backend; one process, expiring state."""

    def __init__(self, ttl_seconds: int = 3600) -> None:
        if ttl_seconds < 1:
            raise ValueError("Session TTL must be positive")
        self.ttl_seconds = ttl_seconds
        self._states: dict[str, tuple[float, dict[str, session.SessionState]]] = {}
        self._lock = threading.RLock()

    def ping(self) -> bool:
        return True

    @contextmanager
    def transaction(self, owner: str) -> Iterator[None]:
        with self._lock:
            now = time.monotonic()
            self._states = {k: v for k, v in self._states.items() if v[0] > now}
            states = copy.deepcopy(self._states.get(owner, (0, {}))[1])
            with session.session_scope(states):
                yield
                encode(states)
            self._states[owner] = (time.monotonic() + self.ttl_seconds, states)


class RedisSessionStore:
    """Shared state with optimistic commits; conflicting calls must be retried.

    Each user's state is one expiring key. WATCH prevents lost updates across
    processes without expiring distributed locks or executing handlers twice.
    """

    def __init__(self, url: str, ttl_seconds: int = 3600) -> None:
        from redis import Redis

        self.client = Redis.from_url(
            url, decode_responses=True, socket_timeout=5, socket_connect_timeout=5
        )
        if ttl_seconds < 1:
            raise ValueError("Session TTL must be positive")
        self.ttl_seconds = ttl_seconds

    def ping(self) -> bool:
        return bool(self.client.ping())

    @contextmanager
    def transaction(self, owner: str) -> Iterator[None]:
        from redis.exceptions import WatchError

        key = "deep-agentic-core-mcp:user:" + hashlib.sha256(owner.encode()).hexdigest()
        with self.client.pipeline() as pipe:
            pipe.watch(key)  # type: ignore[no-untyped-call]
            states = decode(cast(str | None, pipe.get(key)))
            with session.session_scope(states):
                yield
                payload = encode(states)
            pipe.multi()
            pipe.set(key, payload, ex=self.ttl_seconds)
            try:
                pipe.execute()
            except WatchError as exc:
                raise RuntimeError("Concurrent session update; retry this tool call") from exc
