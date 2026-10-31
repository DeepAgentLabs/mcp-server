"""Hosted tool permissions and revocation enforced at dispatch, with correlated evidence."""

import asyncio
import json
import logging
import threading

import httpx
import pytest

from deep_agentic_core_mcp import config
from deep_agentic_core_mcp.server import _TOOL_DISPATCH, handle_call_tool, handle_list_tools
from deep_agentic_core_mcp.services.access_policy import AccessPolicy, Principal
from deep_agentic_core_mcp.services.api_keys import StaticKeyStore
from deep_agentic_core_mcp.services.remote_sessions import MemorySessionStore
from deep_agentic_core_mcp.transport_http import create_app

ALICE, BOB, CAROL = "a" * 40, "b" * 40, "c" * 40


@pytest.fixture(autouse=True)
def remote_environment(monkeypatch):
    monkeypatch.setenv(config.REMOTE_TRANSPORT_ENV, "0")
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_REDIS_URL", raising=False)
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_DATABASE_URL", raising=False)


class MutableKeyStore(StaticKeyStore):
    """A static store an operator can change mid-test, like the hosted stores."""

    def revoke_user(self, user):
        self.credentials = {k: v for k, v in self.credentials.items() if v != user}

    def set_access_policy(self, user, policy):
        self.policies[user] = policy or AccessPolicy()


def keys():
    return MutableKeyStore(
        {
            "alice": ALICE,
            "bob": {
                "key": BOB,
                "permissions": {
                    "allow": ["core.*", "spec.*"],
                    "deny": ["core.session_state"],
                    "task_id": "task-42",
                },
            },
            "carol": {"key": CAROL, "permissions": {"expires_at": "2000-01-01T00:00:00Z"}},
        }
    )


async def rpc(client, method, params=None, token=ALICE):
    return await client.post(
        "/mcp",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2025-11-25",
        },
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}},
    )


async def call(client, name, token, arguments=None):
    response = await rpc(client, "tools/call", {"name": name, "arguments": arguments or {}}, token)
    assert response.status_code == 200, response.text
    result = response.json()["result"]
    return result["isError"], json.loads(result["content"][0]["text"])


def client_for(app):
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testserver")


def evidence(caplog):
    return [
        json.loads(r.getMessage())
        for r in caplog.records
        if r.name == "deep_agentic_core_mcp.access"
    ]


@pytest.mark.asyncio
async def test_policy_filters_tools_list_and_denies_direct_calls(caplog):
    caplog.set_level(logging.INFO, logger="deep_agentic_core_mcp.access")
    app = create_app(key_store=keys(), store=MemorySessionStore(), allowed_hosts=["testserver"])
    async with app.router.lifespan_context(app), client_for(app) as client:
        listed = await rpc(client, "tools/list", token=BOB)
        names = {tool["name"] for tool in listed.json()["result"]["tools"]}
        assert "core.version" in names and "spec.validate_artifact" in names
        assert "core.access_status" in names
        assert "core.session_state" not in names and "lens.analyze_workflow" not in names

        # A client that skips tools/list and calls a hidden tool is still refused.
        is_error, denied = await call(client, "lens.analyze_workflow", BOB, {"artifact": {}})
        assert is_error and denied["access_denied"] and not denied["revoked"]
        assert denied["error"] == "Access denied: tool not in policy allow list"
        decision = denied["access_decision"]
        assert decision["schema"] == "mcp.access-decision.v1"
        assert decision["event"] == "denial" and decision["decision"] == "deny"
        assert decision["subject"] == "bob" and decision["task_id"] == "task-42"
        is_error, denied = await call(client, "core.session_state", BOB)
        assert denied["error"] == "Access denied: tool denied by policy"

        is_error, allowed = await call(client, "core.version", BOB)
        assert not is_error and "version" in allowed
        # Alice has no policy: the default hosted surface.
        is_error, allowed = await call(client, "lens.report_summary", ALICE)
        assert "access_denied" not in allowed

    records = evidence(caplog)
    assert BOB not in caplog.text and "artifact" not in json.dumps(records)
    version = [r for r in records if r["tool"] == "core.version"]
    assert [r["event"] for r in version] == ["dispatch", "completion"]
    assert version[0]["correlation_id"] == version[1]["correlation_id"]
    assert version[1]["outcome"] == "ok" and version[0]["task_id"] == "task-42"
    failed = [r for r in records if r["tool"] == "lens.report_summary"]
    assert failed[-1]["outcome"] == "error"


@pytest.mark.asyncio
async def test_expired_policy_denies_everything_but_access_status():
    app = create_app(key_store=keys(), store=MemorySessionStore(), allowed_hosts=["testserver"])
    async with app.router.lifespan_context(app), client_for(app) as client:
        listed = await rpc(client, "tools/list", token=CAROL)
        assert [t["name"] for t in listed.json()["result"]["tools"]] == ["core.access_status"]
        _, denied = await call(client, "core.version", CAROL)
        assert denied["error"] == "Access denied: access policy expired"
        is_error, status = await call(client, "core.access_status", CAROL)
        assert not is_error
        assert status["expired"] is True and status["permitted_tools"] == ["core.access_status"]
        assert status["expires_at"] == "2000-01-01T00:00:00Z"
        _, status = await call(client, "core.access_status", BOB)
        assert status["enforced"] and status["policy_configured"]
        assert (
            status["task_id"] == "task-42" and "core.session_state" not in status["permitted_tools"]
        )
        _, status = await call(client, "core.access_status", ALICE)
        assert (
            not status["policy_configured"] and "lens.analyze_workflow" in status["permitted_tools"]
        )
        assert "chaos.run_experiment" not in status["permitted_tools"]


@pytest.mark.asyncio
async def test_revocation_and_policy_changes_apply_to_queued_calls(monkeypatch, caplog):
    """A call waiting on the user's session lock re-checks the key when it dispatches."""
    caplog.set_level(logging.INFO, logger="deep_agentic_core_mcp.access")
    started, release = threading.Event(), threading.Event()

    def slow(arguments):
        if arguments and arguments.get("slow"):
            started.set()
            assert release.wait(timeout=5)
        return {"ok": True}

    monkeypatch.setitem(_TOOL_DISPATCH, "core.version", slow)
    store = keys()
    app = create_app(
        key_store=store,
        store=MemorySessionStore(),
        allowed_hosts=["testserver"],
        max_concurrent_per_user=3,
    )
    async with app.router.lifespan_context(app), client_for(app) as client:
        running = asyncio.create_task(call(client, "core.version", ALICE, {"slow": True}))
        assert await asyncio.to_thread(started.wait, 5)
        queued = asyncio.create_task(call(client, "core.version", ALICE))
        await asyncio.sleep(0.2)  # admitted by the endpoint, now waiting on the lock
        store.revoke_user("alice")
        release.set()
        is_error, first = await running
        assert not is_error and first == {"ok": True}  # in-flight calls are not cancelled
        is_error, second = await queued
        assert is_error and second["revoked"] is True
        assert second["error"] == "Access denied: credential revoked"
        assert second["access_decision"]["event"] == "revocation_acknowledged"
        # New requests with the revoked key fail authentication outright.
        assert (await rpc(client, "tools/list", token=ALICE)).status_code == 401

        # Narrowing a policy applies on the next dispatch, without a new key.
        _, ok = await call(client, "spec.validate_artifact", BOB, {"artifact": {}})
        assert "access_denied" not in ok
        store.set_access_policy("bob", AccessPolicy.from_config({"allow": ["core.version"]}))
        _, denied = await call(client, "spec.validate_artifact", BOB, {"artifact": {}})
        assert denied["access_denied"]

    events = [r["event"] for r in evidence(caplog) if r["subject"] == "alice"]
    assert events.count("revocation_acknowledged") == 1


@pytest.mark.asyncio
async def test_authorizer_failures_and_identity_changes_fail_closed():
    store = MemorySessionStore()

    def unavailable():
        raise ConnectionError("store down")

    payload = json.loads(
        (
            await handle_call_tool(
                "core.version", None, owner="alice", store=store, authorizer=unavailable
            )
        )[0].text
    )
    assert payload["error"] == "Access denied: authorization unavailable"
    payload = json.loads(
        (
            await handle_call_tool(
                "core.version",
                None,
                owner="alice",
                store=store,
                authorizer=lambda: Principal("mallory"),
            )
        )[0].text
    )
    assert payload["revoked"] is True


@pytest.mark.asyncio
async def test_handler_exceptions_still_record_completion(monkeypatch, caplog):
    caplog.set_level(logging.INFO, logger="deep_agentic_core_mcp.access")

    def boom(arguments):
        raise KeyError("missing")

    monkeypatch.setitem(_TOOL_DISPATCH, "core.version", boom)
    content = await handle_call_tool(
        "core.version",
        None,
        owner="alice",
        store=MemorySessionStore(),
        authorizer=lambda: Principal("alice"),
    )
    assert json.loads(content[0].text)["error"].startswith("KeyError")
    assert [r["outcome"] for r in evidence(caplog) if r["event"] == "completion"] == ["error"]


@pytest.mark.asyncio
async def test_local_stdio_is_trusted_and_unchanged():
    payload = json.loads((await handle_call_tool("core.access_status", None))[0].text)
    assert payload == {
        "transport": "stdio",
        "enforced": False,
        "note": "Local stdio is trusted; per-key access policies apply to hosted HTTP.",
    }
    names = {tool.name for tool in await handle_list_tools()}
    assert "chaos.run_experiment" in names


@pytest.mark.asyncio
async def test_hosted_list_without_policy_matches_remote_surface():
    names = {t.name for t in await handle_list_tools(Principal("alice"))}
    assert "chaos.run_experiment" not in names and not any(n.startswith("tower.") for n in names)


def test_hosted_access_status_example_prints_denial_evidence(monkeypatch, capsys):
    import importlib.util
    import io
    from pathlib import Path

    path = Path(__file__).parents[1] / "examples" / "hosted_access_status.py"
    spec = importlib.util.spec_from_file_location("hosted_access_status", path)
    example = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example)
    replies = {
        "core.access_status": {"enforced": True, "permitted_tools": ["core.access_status"]},
        "core.version": {
            "ok": False,
            "access_denied": True,
            "access_decision": {"event": "denial"},
        },
    }

    def fake_urlopen(request, timeout):
        assert request.headers["Authorization"] == "Bearer " + "k" * 40
        name = json.loads(request.data)["params"]["name"]
        body = {"result": {"content": [{"text": json.dumps(replies[name])}]}}
        return io.BytesIO(json.dumps(body).encode())

    monkeypatch.setattr(example.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("MCP_API_KEY", "k" * 40)
    monkeypatch.setattr("sys.argv", ["hosted_access_status.py"])
    example.main()
    out = capsys.readouterr().out
    assert '"denied"' in out and '"event": "denial"' in out


def test_default_evidence_handler_writes_json_lines(monkeypatch, capsys):
    from deep_agentic_core_mcp.services import access_evidence

    logger = access_evidence.logger
    monkeypatch.setattr(logger, "handlers", [])
    monkeypatch.setattr(logger, "propagate", True)
    monkeypatch.setattr(logger, "level", logging.NOTSET)
    access_evidence.install_default_handler()
    access_evidence.install_default_handler()  # idempotent
    assert len(logger.handlers) == 1
    access_evidence.record("denial", correlation_id="c-1", user="alice", tool="core.version")
    line = json.loads(capsys.readouterr().out.strip())
    assert line["event"] == "denial" and line["correlation_id"] == "c-1"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool", "message"),
    [
        ("chaos.run_experiment", "chaos.run_experiment is disabled over remote transport"),
        ("tower.detect", "Tower connector is local-only"),
    ],
)
async def test_hosted_only_denials_are_audited(tool, message, caplog):
    caplog.set_level(logging.INFO, logger="deep_agentic_core_mcp.access")
    payload = json.loads(
        (
            await handle_call_tool(
                tool,
                {},
                owner="alice",
                store=MemorySessionStore(),
                authorizer=lambda: Principal("alice"),
            )
        )[0].text
    )
    assert payload["error"] == message and payload["access_denied"]
    decision = payload["access_decision"]
    assert decision["reason"] == "tool unavailable over hosted transport"
    assert evidence(caplog)[-1]["correlation_id"] == decision["correlation_id"]
