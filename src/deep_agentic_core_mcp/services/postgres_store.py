"""PostgreSQL (e.g. Supabase) backends for keys, sessions, and signup limits.

Apply deploy/supabase/schema.sql first. One connection pool is shared by all
three stores. Prepared statements are disabled so Supabase's transaction-mode
pooler (port 6543) works; the session pooler and direct connections work too.
"""

from __future__ import annotations

import hashlib
import random
import secrets
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from deep_agentic_core_mcp.services import session
from deep_agentic_core_mcp.services.access_policy import AccessPolicy, Principal
from deep_agentic_core_mcp.services.api_keys import KeyConflictError, key_digest
from deep_agentic_core_mcp.services.remote_sessions import decode, encode


def connect(url: str, *, max_size: int = 10) -> Any:
    """Open a pool; connections commit on success and roll back on error."""
    from psycopg_pool import ConnectionPool

    return ConnectionPool(
        url,
        min_size=1,
        max_size=max_size,
        timeout=10,
        kwargs={"prepare_threshold": None, "connect_timeout": 5},
        open=True,
    )


class PostgresKeyStore:
    """One active key per user in mcp.users; reads are immediately consistent."""

    def __init__(self, pool: Any) -> None:
        self.pool = pool

    def ping(self) -> bool:
        with self.pool.connection() as conn:
            conn.execute("SELECT 1 FROM mcp.users LIMIT 1")
        return True

    def authenticate(self, token: str) -> str | None:
        if len(token) < 32 or len(token) > 256 or any(c.isspace() for c in token):
            return None
        with self.pool.connection() as conn:
            row = conn.execute(
                "SELECT user_id FROM mcp.users WHERE key_hash = %s AND status = 'active'",
                (key_digest(token),),
            ).fetchone()
        return str(row[0]) if row else None

    def authorize(self, token: str) -> Principal | None:
        """Key, status and policy in one read, so a dispatch sees one consistent row."""
        if len(token) < 32 or len(token) > 256 or any(c.isspace() for c in token):
            return None
        with self.pool.connection() as conn:
            row = conn.execute(
                "SELECT user_id, permissions FROM mcp.users"
                " WHERE key_hash = %s AND status = 'active'",
                (key_digest(token),),
            ).fetchone()
        return Principal(str(row[0]), AccessPolicy.load(row[1])) if row else None

    def stored_access_policy(self, user: str) -> Any:
        with self.pool.connection() as conn:
            row = conn.execute(
                "SELECT permissions FROM mcp.users WHERE user_id = %s", (user,)
            ).fetchone()
        if row is None:
            raise KeyError(user)
        return row[0]

    def set_access_policy(self, user: str, policy: AccessPolicy | None) -> None:
        from psycopg.types.json import Jsonb

        value = None if policy is None else Jsonb(policy.to_config())
        with self.pool.connection() as conn:
            updated = conn.execute(
                "UPDATE mcp.users SET permissions = %s WHERE user_id = %s", (value, user)
            ).rowcount
        if updated != 1:
            raise KeyError(user)

    def revoke_user(self, user: str) -> None:
        with self.pool.connection() as conn:
            updated = conn.execute(
                "UPDATE mcp.users SET status = 'revoked' WHERE user_id = %s", (user,)
            ).rowcount
        if updated != 1:
            raise KeyError(user)

    def issue(self, display_name: str) -> dict[str, str]:
        user = str(uuid.uuid4())
        token = "dal_" + secrets.token_urlsafe(36)
        self.import_key(user, token, display_name)
        return {"user_id": user, "display_name": display_name, "api_key": token}

    def import_key(self, user: str, token: str, display_name: str) -> None:
        # Unique constraints reject an existing user ID or key; nothing is overwritten.
        with self.pool.connection() as conn:
            conn.execute(
                "INSERT INTO mcp.users (user_id, display_name, status, key_hash)"
                " VALUES (%s, %s, 'active', %s)",
                (user, display_name, key_digest(token)),
            )

    def profile(self, user: str) -> dict[str, str]:
        with self.pool.connection() as conn:
            row = conn.execute(
                "SELECT display_name, status FROM mcp.users WHERE user_id = %s", (user,)
            ).fetchone()
        return {
            "user_id": user,
            "display_name": str(row[0]) if row else "",
            "status": str(row[1]) if row else "unknown",
        }

    def rotate(self, user: str, old_token: str) -> dict[str, str]:
        token = "dal_" + secrets.token_urlsafe(36)
        with self.pool.connection() as conn:
            updated = conn.execute(
                "UPDATE mcp.users SET key_hash = %s"
                " WHERE user_id = %s AND key_hash = %s AND status = 'active'",
                (key_digest(token), user, key_digest(old_token)),
            ).rowcount
        if updated != 1:
            raise KeyConflictError("Account changed")
        return {"user_id": user, "api_key": token}

    def revoke(self, user: str, token: str) -> None:
        with self.pool.connection() as conn:
            updated = conn.execute(
                "UPDATE mcp.users SET status = 'revoked'"
                " WHERE user_id = %s AND key_hash = %s AND status = 'active'",
                (user, key_digest(token)),
            ).rowcount
        if updated != 1:
            raise KeyConflictError("Account changed")


class PostgresSessionStore:
    """Per-user state in one row, locked for the duration of each tool call.

    Row locks serialize a user's calls across processes; other users never wait.
    """

    def __init__(self, pool: Any, ttl_seconds: int = 3600) -> None:
        if ttl_seconds < 1:
            raise ValueError("Session TTL must be positive")
        self.pool = pool
        self.ttl_seconds = ttl_seconds

    def ping(self) -> bool:
        with self.pool.connection() as conn:
            conn.execute("SELECT 1 FROM mcp.sessions LIMIT 1")
        return True

    @contextmanager
    def transaction(self, owner: str) -> Iterator[None]:
        key = hashlib.sha256(owner.encode()).hexdigest()
        with self.pool.connection() as conn:
            conn.execute("SET LOCAL lock_timeout = '10s'")
            if random.random() < 0.01:
                conn.execute("DELETE FROM mcp.sessions WHERE expires_at < now()")
            conn.execute(
                "INSERT INTO mcp.sessions (owner_hash, payload, expires_at)"
                " VALUES (%s, '{}', now()) ON CONFLICT (owner_hash) DO NOTHING",
                (key,),
            )
            row = conn.execute(
                "SELECT payload, expires_at > now() FROM mcp.sessions"
                " WHERE owner_hash = %s FOR UPDATE",
                (key,),
            ).fetchone()
            states = decode(row[0] if row and row[1] else None)
            with session.session_scope(states):
                yield
                payload = encode(states)
            conn.execute(
                "UPDATE mcp.sessions SET payload = %s,"
                " expires_at = now() + make_interval(secs => %s) WHERE owner_hash = %s",
                (payload, self.ttl_seconds, key),
            )


class PostgresSignupLimiter:
    """Shared limits: 10 signups/hour/client and 100/day across the service."""

    def __init__(self, pool: Any) -> None:
        self.pool = pool

    def allow(self, peer: str) -> bool:
        # Fixed lock order (client bucket, then global) avoids deadlocks.
        buckets = [
            ("ip:" + hashlib.sha256(peer.encode()).hexdigest(), 10, 3600),
            ("global", 100, 86400),
        ]
        with self.pool.connection() as conn:
            counts = []
            for bucket, _, window in buckets:
                row = conn.execute(
                    "INSERT INTO mcp.signup_counters AS c (bucket, count, expires_at)"
                    " VALUES (%s, 0, now() + make_interval(secs => %s))"
                    " ON CONFLICT (bucket) DO UPDATE SET"
                    " count = CASE WHEN c.expires_at <= now() THEN 0 ELSE c.count END,"
                    " expires_at = CASE WHEN c.expires_at <= now()"
                    " THEN excluded.expires_at ELSE c.expires_at END"
                    " RETURNING count",
                    (bucket, window),
                ).fetchone()
                counts.append(row[0] if row else 0)
            if any(count >= limit for count, (_, limit, _) in zip(counts, buckets, strict=True)):
                return False
            conn.execute(
                "UPDATE mcp.signup_counters SET count = count + 1 WHERE bucket = ANY(%s)",
                ([bucket for bucket, _, _ in buckets],),
            )
        return True
