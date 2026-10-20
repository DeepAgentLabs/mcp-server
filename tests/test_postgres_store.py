"""PostgreSQL/Supabase keys, sessions, and signup limits against a real database.

Set DEEP_AGENTIC_CORE_MCP_TEST_DATABASE_URL to a disposable superuser database, e.g.
docker run --rm -e POSTGRES_PASSWORD=pw -p 55432:5432 postgres:16-alpine
"""

import json
import os
import threading
import time
from pathlib import Path

import httpx
import pytest

from deep_agentic_core_mcp.services import session
from deep_agentic_core_mcp.services.api_keys import KeyConflictError

ADMIN_URL = os.environ.get("DEEP_AGENTIC_CORE_MCP_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not ADMIN_URL, reason="no test PostgreSQL configured")
SCHEMA = Path(__file__).parents[1] / "deploy" / "supabase" / "schema.sql"


@pytest.fixture
def service_url():
    import psycopg

    with psycopg.connect(ADMIN_URL, autocommit=True) as conn:
        conn.execute("DROP SCHEMA IF EXISTS mcp CASCADE")
        conn.execute(SCHEMA.read_text())
        conn.execute("ALTER ROLE mcp_service WITH PASSWORD 'service-test-password'")
    # Connect as the least-privilege role so grants and RLS policies are exercised.
    url = psycopg.conninfo.make_conninfo(
        ADMIN_URL, user="mcp_service", password="service-test-password"
    )
    return url


@pytest.fixture
def pool(service_url):
    from deep_agentic_core_mcp.services.postgres_store import connect

    pool = connect(service_url)
    yield pool
    pool.close()


def test_keys_rotate_revoke_and_hash_only_storage(pool):
    from deep_agentic_core_mcp.services.postgres_store import PostgresKeyStore

    keys = PostgresKeyStore(pool)
    assert keys.ping()
    issued = keys.issue("Ada")
    user, token = issued["user_id"], issued["api_key"]
    assert keys.authenticate(token) == user
    assert keys.profile(user) == {"user_id": user, "display_name": "Ada", "status": "active"}
    with pool.connection() as conn:
        stored = conn.execute("SELECT key_hash FROM mcp.users").fetchone()[0]
    assert token not in stored

    rotated = keys.rotate(user, token)["api_key"]
    assert keys.authenticate(token) is None
    assert keys.authenticate(rotated) == user
    with pytest.raises(KeyConflictError):
        keys.rotate(user, token)
    keys.revoke(user, rotated)
    assert keys.authenticate(rotated) is None
    with pytest.raises(KeyConflictError):
        keys.revoke(user, rotated)
    assert keys.authenticate("short") is None


def test_import_never_overwrites_existing_user(pool):
    import psycopg

    from deep_agentic_core_mcp.services.postgres_store import PostgresKeyStore

    keys = PostgresKeyStore(pool)
    keys.import_key("alice", "a" * 40, "Alice")
    with pytest.raises(psycopg.errors.UniqueViolation):
        keys.import_key("alice", "b" * 40, "Mallory")
    assert keys.authenticate("a" * 40) == "alice"
    assert keys.authenticate("b" * 40) is None


def test_sessions_isolation_rollback_limits_and_expiry(pool):
    from deep_agentic_core_mcp.services.postgres_store import PostgresSessionStore

    first, second = PostgresSessionStore(pool), PostgresSessionStore(pool)
    assert first.ping()
    with first.transaction("alice"):
        session.get_session().workflow = {"name": "private"}
    with second.transaction("bob"):
        assert session.get_session().workflow is None
    with second.transaction("alice"):
        assert session.get_session().workflow == {"name": "private"}

    with pytest.raises(RuntimeError, match="failed"), first.transaction("alice"):
        session.get_session().workflow = {"name": "discard"}
        raise RuntimeError("failed")
    with pytest.raises(ValueError, match="limit"), first.transaction("alice"):
        for i in range(101):
            session.get_session(str(i))
    with first.transaction("alice"):
        assert session.get_session().workflow == {"name": "private"}

    with pool.connection() as conn:
        conn.execute("UPDATE mcp.sessions SET expires_at = now() - interval '1 second'")
    with first.transaction("alice"):
        assert session.get_session().workflow is None


def test_concurrent_calls_for_one_user_are_serialized(pool):
    from deep_agentic_core_mcp.services.postgres_store import PostgresSessionStore

    store = PostgresSessionStore(pool)

    def increment():
        with store.transaction("alice"):
            state = session.get_session()
            count = (state.workflow or {}).get("count", 0)
            time.sleep(0.05)
            state.workflow = {"count": count + 1}

    threads = [threading.Thread(target=increment) for _ in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    with store.transaction("alice"):
        assert session.get_session().workflow == {"count": 5}


def test_signup_limits_are_shared_and_do_not_store_client_ips(pool):
    from deep_agentic_core_mcp.services.postgres_store import PostgresSignupLimiter

    first, second = PostgresSignupLimiter(pool), PostgresSignupLimiter(pool)
    assert all(first.allow("203.0.113.9") for _ in range(5))
    assert all(second.allow("203.0.113.9") for _ in range(5))
    assert not first.allow("203.0.113.9")
    assert second.allow("198.51.100.4")
    with pool.connection() as conn:
        buckets = [row[0] for row in conn.execute("SELECT bucket FROM mcp.signup_counters")]
        assert not any("203.0.113.9" in bucket for bucket in buckets)
        conn.execute("UPDATE mcp.signup_counters SET expires_at = now()")
    assert first.allow("203.0.113.9")


async def test_app_uses_database_for_signup_auth_and_sessions(service_url, monkeypatch):
    from deep_agentic_core_mcp import config
    from deep_agentic_core_mcp.transport_http import create_app

    monkeypatch.setenv(config.REMOTE_TRANSPORT_ENV, "0")
    for name in ("REDIS_URL", "USERS_TABLE", "API_KEYS"):
        monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_" + name, raising=False)
    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_DATABASE_URL", service_url)
    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_PUBLIC_URL", "https://mcp.example")
    app = create_app(allowed_hosts=["mcp.example"])
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="https://mcp.example") as client:
            assert (await client.get("/healthz")).text == "ok"
            assert (await client.post("/mcp", json={})).status_code == 401
            created = await client.post(
                "/api/signup",
                json={"display_name": "Grace"},
                headers={"origin": "https://mcp.example"},
            )
            assert created.status_code == 201
            token = created.json()["api_key"]
            headers = {
                "authorization": "Bearer " + token,
                "accept": "application/json, text/event-stream",
            }

            async def call(name, arguments):
                reply = await client.post(
                    "/mcp",
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {"name": name, "arguments": arguments},
                    },
                    headers=headers,
                )
                assert reply.status_code == 200
                return json.loads(reply.json()["result"]["content"][0]["text"])

            stored = await call(
                "lens.analyze_workflow",
                {"artifact": {"name": "grace-run", "start_time": "2026-01-01T00:00:00Z"}},
            )
            assert stored["ok"] is True, stored
            # A separate request reads the state back from PostgreSQL.
            summary = await call("lens.report_summary", {})
            assert summary["workflow"]["name"] == "grace-run"
            account = await client.get(
                "/api/account", headers={**headers, "origin": "https://mcp.example"}
            )
            assert account.json()["display_name"] == "Grace"
