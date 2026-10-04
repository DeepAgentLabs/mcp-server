"""Shared storage, rollback, expiry, and scoped diagnostics."""

import fakeredis
import pytest

from deep_agentic_core_mcp.services import session
from deep_agentic_core_mcp.services.remote_sessions import (
    MemorySessionStore,
    RedisSessionStore,
)


def redis_store(client):
    store = RedisSessionStore("redis://localhost")
    store.client = client
    return store


def test_shared_redis_across_workers_and_isolation():
    client = fakeredis.FakeRedis(decode_responses=True)
    first = redis_store(client)
    second = redis_store(client)
    with first.transaction("alice"):
        session.get_session().workflow = {"name": "private"}
    with second.transaction("bob"):
        assert session.get_session().workflow is None
        assert set(session.all_sessions()) == {"default"}
    with second.transaction("alice"):
        assert session.get_session().workflow == {"name": "private"}
    assert all(client.ttl(key) > 0 for key in client.keys("*"))


def test_redis_conflicting_update_does_not_overwrite():
    client = fakeredis.FakeRedis(decode_responses=True)
    first, second = redis_store(client), redis_store(client)
    with pytest.raises(RuntimeError, match="Concurrent"), first.transaction("alice"):
        session.get_session().workflow = {"name": "loser"}
        with second.transaction("alice"):
            session.get_session().workflow = {"name": "winner"}
    with first.transaction("alice"):
        assert session.get_session().workflow == {"name": "winner"}


@pytest.mark.parametrize("kind", ["memory", "redis"])
def test_transaction_rollback_and_session_limit(kind):
    store = (
        MemorySessionStore()
        if kind == "memory"
        else redis_store(fakeredis.FakeRedis(decode_responses=True))
    )
    with pytest.raises(ValueError, match="limit"), store.transaction("alice"):
        for i in range(101):
            session.get_session(str(i))
    with store.transaction("alice"):
        assert session.all_sessions() == {}
    with pytest.raises(RuntimeError, match="failed"), store.transaction("alice"):
        session.get_session().workflow = {"name": "discard"}
        raise RuntimeError("failed")
    with store.transaction("alice"):
        assert session.get_session().workflow is None


def test_memory_expiry_and_byte_quota(monkeypatch):
    from deep_agentic_core_mcp.services import remote_sessions

    now = [0.0]
    monkeypatch.setattr(remote_sessions.time, "monotonic", lambda: now[0])
    store = MemorySessionStore(ttl_seconds=10)
    with store.transaction("alice"):
        session.get_session().workflow = {"name": "expires"}
    now[0] = 11
    with store.transaction("alice"):
        assert session.get_session().workflow is None
    with pytest.raises(ValueError, match="storage limit"), store.transaction("alice"):
        session.get_session().workflow = {"payload": "x" * remote_sessions.MAX_STATE_BYTES}
    with store.transaction("alice"):
        assert session.get_session().workflow is None
