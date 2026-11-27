"""Expiring OAuth records, isolated from workflow state; secrets are indexed by hash."""

from __future__ import annotations

import json
import threading
import time
from typing import Any, Protocol

from deep_agentic_core_mcp.services.api_keys import key_digest


class OAuthStore(Protocol):
    def put(self, kind: str, secret: str, value: dict[str, Any], ttl: int) -> None: ...

    def get(self, kind: str, secret: str) -> dict[str, Any] | None: ...

    def take(self, kind: str, secret: str) -> dict[str, Any] | None: ...

    def compare_swap(
        self, kind: str, secret: str, expected: dict[str, Any], value: dict[str, Any], ttl: int
    ) -> bool: ...

    def ping(self) -> bool: ...

    def allow(self, peer: str) -> bool: ...


class MemoryOAuthStore:
    """Explicit test/development backend; never selected by hosted startup."""

    def __init__(self) -> None:
        self.records: dict[tuple[str, str], tuple[float, dict[str, Any]]] = {}
        self.lock = threading.Lock()
        self.counts: dict[str, tuple[float, int]] = {}

    def put(self, kind: str, secret: str, value: dict[str, Any], ttl: int) -> None:
        with self.lock:
            now = time.time()
            self.records = {k: v for k, v in self.records.items() if v[0] > now}
            self.records[kind, key_digest(secret)] = (now + ttl, dict(value))

    def get(self, kind: str, secret: str) -> dict[str, Any] | None:
        with self.lock:
            entry = self.records.get((kind, key_digest(secret)))
            return dict(entry[1]) if entry and entry[0] > time.time() else None

    def take(self, kind: str, secret: str) -> dict[str, Any] | None:
        with self.lock:
            entry = self.records.pop((kind, key_digest(secret)), None)
            return dict(entry[1]) if entry and entry[0] > time.time() else None

    def compare_swap(
        self, kind: str, secret: str, expected: dict[str, Any], value: dict[str, Any], ttl: int
    ) -> bool:
        with self.lock:
            entry = self.records.get((kind, key_digest(secret)))
            if not entry or entry[0] <= time.time() or entry[1] != expected:
                return False
            self.records[kind, key_digest(secret)] = (time.time() + ttl, dict(value))
            return True

    def ping(self) -> bool:
        return True

    def allow(self, peer: str) -> bool:
        with self.lock:
            now = time.time()
            self.counts = {k: v for k, v in self.counts.items() if v[0] > now}
            expiry, count = self.counts.get(peer, (now + 60, 0))
            self.counts[peer] = (expiry, count + 1)
            return count < 60


class RedisOAuthStore:
    def __init__(self, client: Any) -> None:
        self.client = client

    @staticmethod
    def _key(kind: str, secret: str) -> str:
        return "mcp:oauth:" + kind + ":" + key_digest(secret)

    def put(self, kind: str, secret: str, value: dict[str, Any], ttl: int) -> None:
        self.client.set(self._key(kind, secret), json.dumps(value, sort_keys=True), ex=ttl)

    def get(self, kind: str, secret: str) -> dict[str, Any] | None:
        value = self.client.get(self._key(kind, secret))
        return dict(json.loads(value)) if value else None

    def take(self, kind: str, secret: str) -> dict[str, Any] | None:
        # Atomic across workers: exactly one exchange can consume a code.
        value = self.client.eval(
            "local v = redis.call('GET', KEYS[1]); redis.call('DEL', KEYS[1]); return v",
            1,
            self._key(kind, secret),
        )
        return dict(json.loads(value)) if value else None

    def compare_swap(
        self, kind: str, secret: str, expected: dict[str, Any], value: dict[str, Any], ttl: int
    ) -> bool:
        return bool(
            self.client.eval(
                "if redis.call('GET', KEYS[1]) ~= ARGV[1] then return 0 end; "
                "redis.call('SET', KEYS[1], ARGV[2], 'EX', ARGV[3]); return 1",
                1,
                self._key(kind, secret),
                json.dumps(expected, sort_keys=True),
                json.dumps(value, sort_keys=True),
                ttl,
            )
        )

    def ping(self) -> bool:
        return bool(self.client.ping())

    def allow(self, peer: str) -> bool:
        return bool(
            self.client.eval(
                "local n = redis.call('INCR', KEYS[1]); "
                "if n == 1 then redis.call('EXPIRE', KEYS[1], 60) end; "
                "return n <= 60 and 1 or 0",
                1,
                "mcp:oauth:rate:" + key_digest(peer),
            )
        )


class PostgresOAuthStore:
    def __init__(self, pool: Any) -> None:
        self.pool = pool

    def put(self, kind: str, secret: str, value: dict[str, Any], ttl: int) -> None:
        with self.pool.connection() as conn:
            conn.execute("DELETE FROM mcp.oauth_records WHERE expires_at <= now()")
            conn.execute(
                "INSERT INTO mcp.oauth_records (kind, secret_hash, payload, expires_at)"
                " VALUES (%s, %s, %s, now() + make_interval(secs => %s))",
                (kind, key_digest(secret), json.dumps(value, sort_keys=True), ttl),
            )

    def get(self, kind: str, secret: str) -> dict[str, Any] | None:
        with self.pool.connection() as conn:
            row = conn.execute(
                "SELECT payload FROM mcp.oauth_records"
                " WHERE kind = %s AND secret_hash = %s AND expires_at > now()",
                (kind, key_digest(secret)),
            ).fetchone()
        return dict(json.loads(row[0])) if row else None

    def take(self, kind: str, secret: str) -> dict[str, Any] | None:
        with self.pool.connection() as conn:
            row = conn.execute(
                "DELETE FROM mcp.oauth_records WHERE kind = %s AND secret_hash = %s"
                " AND expires_at > now() RETURNING payload",
                (kind, key_digest(secret)),
            ).fetchone()
        return dict(json.loads(row[0])) if row else None

    def compare_swap(
        self, kind: str, secret: str, expected: dict[str, Any], value: dict[str, Any], ttl: int
    ) -> bool:
        with self.pool.connection() as conn:
            updated = conn.execute(
                "UPDATE mcp.oauth_records SET payload = %s,"
                " expires_at = now() + make_interval(secs => %s)"
                " WHERE kind = %s AND secret_hash = %s AND expires_at > now()"
                " AND payload::jsonb = %s::jsonb",
                (
                    json.dumps(value, sort_keys=True),
                    ttl,
                    kind,
                    key_digest(secret),
                    json.dumps(expected, sort_keys=True),
                ),
            ).rowcount
        return bool(updated == 1)

    def ping(self) -> bool:
        with self.pool.connection() as conn:
            conn.execute("SELECT 1 FROM mcp.oauth_records LIMIT 1")
        return True

    def allow(self, peer: str) -> bool:
        with self.pool.connection() as conn:
            conn.execute("DELETE FROM mcp.signup_counters WHERE expires_at <= now()")
            row = conn.execute(
                "INSERT INTO mcp.signup_counters AS c (bucket, count, expires_at)"
                " VALUES (%s, 1, now() + interval '60 seconds')"
                " ON CONFLICT (bucket) DO UPDATE SET"
                " count = CASE WHEN c.expires_at <= now() THEN 1 ELSE c.count + 1 END,"
                " expires_at = CASE WHEN c.expires_at <= now() THEN excluded.expires_at"
                " ELSE c.expires_at END RETURNING count",
                ("oauth:" + key_digest(peer),),
            ).fetchone()
        return bool(row and row[0] <= 60)
