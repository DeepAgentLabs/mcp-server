"""Protocol-level tests for authenticated multi-user HTTP access."""

import json

import httpx
import pytest

from deep_agentic_core_mcp import config
from deep_agentic_core_mcp.services.remote_sessions import MemorySessionStore
from deep_agentic_core_mcp.transport_http import create_app

KEYS = {"alice": "a" * 40, "bob": "b" * 40}


@pytest.fixture(autouse=True)
def remote_environment(monkeypatch):
    monkeypatch.delenv(config.REMOTE_TRANSPORT_ENV, raising=False)
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_API_KEYS", raising=False)
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_REDIS_URL", raising=False)
    yield
    monkeypatch.delenv(config.REMOTE_TRANSPORT_ENV, raising=False)


def app_for_test(**kwargs):
    return create_app(
        api_keys=KEYS, store=MemorySessionStore(), allowed_hosts=["testserver"], **kwargs
    )


async def rpc(client, method, params=None, user="alice", **kwargs):
    headers = {
        "Authorization": f"Bearer {KEYS[user]}",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": "2025-11-25",
    }
    headers.update(kwargs.pop("headers", {}))
    return await client.post(
        "/mcp",
        headers=headers,
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}},
        **kwargs,
    )


def tool_payload(response):
    assert response.status_code == 200, response.text
    return json.loads(response.json()["result"]["content"][0]["text"])


def test_service_requires_credentials_and_storage():
    with pytest.raises(ValueError, match="API_KEYS"):
        create_app()
    with pytest.raises(ValueError, match="REDIS_URL"):
        create_app(api_keys=KEYS)
    with pytest.raises(ValueError, match="unique"):
        create_app(api_keys={"alice": "x" * 40, "bob": "x" * 40})


@pytest.mark.asyncio
async def test_mixed_case_configured_hostname_accepts_lowercase_proxy_host():
    app = create_app(
        api_keys=KEYS, store=MemorySessionStore(), allowed_hosts=["Internal-ALB.example.com"]
    )
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://internal-alb.example.com"
        ) as client,
    ):
        assert (await rpc(client, "tools/list")).status_code == 200
        assert (
            await rpc(client, "tools/list", headers={"Host": "untrusted.example.com"})
        ).status_code == 421


@pytest.mark.asyncio
async def test_health_auth_and_protocol():
    app = app_for_test()
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        ) as client,
    ):
        assert (await client.get("/healthz")).status_code == 200
        for headers in [{}, {"Authorization": "Bearer invalid"}]:
            denied = await client.post("/mcp", headers=headers, json={})
            assert denied.status_code == 401
            assert "WWW-Authenticate" in denied.headers
        initialized = await rpc(
            client,
            "initialize",
            {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "review", "version": "1"},
            },
        )
        assert initialized.status_code == 200
        assert "location" not in initialized.headers
        assert "mcp-session-id" not in initialized.headers
        listed = await rpc(client, "tools/list")
        assert listed.status_code == 200
        names = {tool["name"] for tool in listed.json()["result"]["tools"]}
        assert "core.session_state" in names
        assert "chaos.run_experiment" not in names
        chaos = await rpc(
            client,
            "tools/call",
            {"name": "chaos.run_experiment", "arguments": {"script": "any", "faults": []}},
        )
        assert chaos.json()["result"]["isError"] is True


@pytest.mark.asyncio
async def test_users_cannot_read_overwrite_or_impersonate_each_other(monkeypatch):
    from deep_agentic_core_mcp.tools import lens

    monkeypatch.setattr(
        lens, "adapter_analyze_workflow", lambda artifact: {"name": artifact["name"]}
    )
    monkeypatch.setattr(lens, "adapter_report_summary", lambda artifact: {"name": artifact["name"]})
    app = app_for_test()
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        ) as client,
    ):
        for session_id in ["default", "alice", "bob", "shared"]:
            for user in KEYS:
                result = tool_payload(
                    await rpc(
                        client,
                        "tools/call",
                        {
                            "name": "lens.analyze_workflow",
                            "arguments": {
                                "artifact": {"name": f"{user}-private"},
                                "session_id": session_id,
                                "user_id": "alice",
                                "owner": "alice",
                            },
                        },
                        user=user,
                        headers={"X-User-ID": "alice"},
                    )
                )
                assert result["ok"] is True
            for user in KEYS:
                summary = tool_payload(
                    await rpc(
                        client,
                        "tools/call",
                        {
                            "name": "lens.report_summary",
                            "arguments": {"session_id": session_id},
                        },
                        user=user,
                    )
                )
                assert summary["name"] == f"{user}-private"
        absent = tool_payload(
            await rpc(
                client,
                "tools/call",
                {
                    "name": "lens.report_summary",
                    "arguments": {"session_id": "not-created"},
                },
                user="bob",
            )
        )
        assert absent["ok"] is False


@pytest.mark.asyncio
async def test_origin_host_and_rate_limits():
    app = app_for_test(requests_per_minute=3)
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        ) as client,
    ):
        assert (
            await rpc(client, "tools/list", headers={"Origin": "https://evil.example"})
        ).status_code == 403
        assert (
            await rpc(client, "tools/list", headers={"Host": "evil.example"})
        ).status_code == 421
        assert (await rpc(client, "tools/list")).status_code == 200
        assert (await rpc(client, "tools/list")).status_code == 429
        assert (await rpc(client, "tools/list", user="bob")).status_code == 200


@pytest.mark.asyncio
async def test_request_size_and_storage_unavailability():
    app = app_for_test()
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        ) as client,
    ):
        oversized = await rpc(
            client,
            "tools/call",
            {
                "name": "core.version",
                "arguments": {"padding": "x" * (1024 * 1024)},
            },
        )
        assert oversized.status_code == 413

    class UnavailableStore(MemorySessionStore):
        def ping(self):
            return False

    app = create_app(api_keys=KEYS, store=UnavailableStore(), allowed_hosts=["testserver"])
    with pytest.raises(RuntimeError, match="unavailable"):
        async with app.router.lifespan_context(app):
            pass
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        assert (await client.get("/healthz")).status_code == 503


@pytest.mark.asyncio
async def test_user_concurrency_limit_recovers(monkeypatch):
    import asyncio
    import threading

    from deep_agentic_core_mcp.server import _TOOL_DISPATCH

    started, release = threading.Event(), threading.Event()

    def slow_handler(arguments):
        if arguments and arguments.get("slow"):
            started.set()
            assert release.wait(timeout=5)
        return {"ok": True}

    monkeypatch.setitem(_TOOL_DISPATCH, "core.version", slow_handler)
    app = app_for_test(max_concurrent_per_user=1)
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        ) as client,
    ):
        pending = asyncio.create_task(
            rpc(
                client,
                "tools/call",
                {
                    "name": "core.version",
                    "arguments": {"slow": True},
                },
            )
        )
        try:
            assert await asyncio.to_thread(started.wait, 5)
            assert (await rpc(client, "tools/list")).status_code == 429
            assert (await rpc(client, "tools/list", user="bob")).status_code == 200
        finally:
            release.set()
            assert (await pending).status_code == 200
        assert (await rpc(client, "tools/list")).status_code == 200


def test_render_hostname_and_port_are_used(monkeypatch):
    import uvicorn

    from deep_agentic_core_mcp import transport_http

    captured = {}

    def fake_create(**kwargs):
        captured.update(kwargs)
        return "app"

    def fake_run(app, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(transport_http, "create_app", fake_create)
    monkeypatch.setattr(uvicorn, "run", fake_run)
    monkeypatch.setenv("RENDER_EXTERNAL_HOSTNAME", "mcp-test.onrender.com")
    monkeypatch.setenv("PORT", "10000")
    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_HTTP_HOST", "0.0.0.0")
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_ALLOWED_HOSTS", raising=False)
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_HTTP_PORT", raising=False)
    transport_http.main()
    assert "mcp-test.onrender.com" in captured["allowed_hosts"]
    assert captured["port"] == 10000
    assert captured["host"] == "0.0.0.0"
