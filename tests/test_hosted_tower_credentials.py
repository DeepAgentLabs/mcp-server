"""Hosted Tower credentials are selected only by authenticated user, at dispatch."""

import json
from unittest.mock import MagicMock, patch

import pytest

from deep_agentic_core_mcp import config
from deep_agentic_core_mcp.server import handle_call_tool, handle_list_tools
from deep_agentic_core_mcp.services.access_policy import AccessPolicy, Principal
from deep_agentic_core_mcp.services.remote_sessions import MemorySessionStore
from deep_agentic_core_mcp.services.tower_credentials import for_user


@pytest.fixture
def bindings(monkeypatch):
    monkeypatch.setenv(config.REMOTE_TRANSPORT_ENV, "1")
    monkeypatch.setenv("AGENTICOPS_TOWER_WRITE_TOKEN", "NEVER-USE-GLOBAL")
    value = {
        "alice": {
            "origin": "https://alice.example",
            "read_token": "alice-read",
            "write_token": "alice-write",
        },
        "bob": {"origin": "https://bob.example", "read_token": "bob-read"},
    }
    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_TOWER_BINDINGS", json.dumps(value))
    return value


async def test_user_binding_and_policy_are_both_required(bindings):
    store = MemorySessionStore()
    completed = MagicMock(returncode=0, stdout=b'{"ok":true}')
    with patch(
        "deep_agentic_core_mcp.tools.tower.subprocess.run", return_value=completed
    ) as worker:
        for user in ("alice", "bob"):
            principal = Principal(user)
            result = await handle_call_tool(
                "tower.agents",
                {},
                owner=user,
                store=store,
                authorizer=lambda principal=principal: principal,
            )
            assert json.loads(result[0].text)["ok"]
            sent = json.loads(worker.call_args.kwargs["input"])
            assert sent["url"] == f"https://{user}.example/agents"
            assert sent["token"] == user + "-read"
            assert "tower.agents" in {t.name for t in await handle_list_tools(principal)}
        denied = Principal("alice", AccessPolicy(allow=("core.*",)))
        before = worker.call_count
        result = await handle_call_tool(
            "tower.agents", {}, owner="alice", store=store, authorizer=lambda: denied
        )
        assert json.loads(result[0].text)["access_denied"]
        assert worker.call_count == before
        for user in ("bob", "unbound"):
            principal = Principal(user)
            result = await handle_call_tool(
                "tower.detect",
                {"agent_id": "x", "evidence_id": "e"},
                owner=user,
                store=store,
                authorizer=lambda principal=principal: principal,
            )
            assert json.loads(result[0].text).get("error")
        assert worker.call_count == before


@pytest.mark.parametrize(
    "entry",
    [
        None,
        [],
        {"origin": "http://bad", "read_token": "r"},
        {"origin": "https://bad/path", "read_token": "r"},
        {"origin": "https://bad", "read_token": "r", "extra": True},
    ],
)
def test_malformed_bindings_fail_closed(monkeypatch, entry):
    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_TOWER_BINDINGS", json.dumps({"alice": entry}))
    assert for_user("alice") is None


async def test_incomplete_hosted_context_never_uses_global_credentials(bindings):
    with patch("deep_agentic_core_mcp.tools.tower.subprocess.run") as worker:
        for context in [
            {},
            {"store": MemorySessionStore()},
            {"authorizer": lambda: Principal("alice")},
        ]:
            result = await handle_call_tool("tower.agents", {}, owner="alice", **context)
            assert json.loads(result[0].text)["access_denied"]
        worker.assert_not_called()
