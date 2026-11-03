"""Read-only guided setup, session recall and authenticated resource isolation."""

import json

import httpx

from deep_agentic_core_mcp import config
from deep_agentic_core_mcp.server import (
    handle_call_tool,
    handle_list_resources,
    handle_read_resource,
)
from deep_agentic_core_mcp.services import session
from deep_agentic_core_mcp.services.remote_sessions import MemorySessionStore
from deep_agentic_core_mcp.tools.intelligence import onboard, report_recall
from deep_agentic_core_mcp.transport_http import create_app


def test_setup_reports_steps_and_unknowns():
    result = onboard()
    assert result["steps"][0]["tool"] == "core.verify"
    assert not report_recall({"session_id": "missing-601"})["ok"]


async def test_saved_resources_and_cited_recall():
    with session.session_scope({}):
        state = session.get_session("report-601")
        state.last_release_check = {
            "ready": False,
            "gates": [{"name": "chaos", "status": "missing"}],
        }
        result = report_recall({"session_id": "report-601"})
        assert result["narrative"]["observations"][0]["source"] == "release_check.gates[0]"
        assert "analysis" in result["narrative"]["unknowns"]
        resources = await handle_list_resources()
        assert any(str(r.uri) == "resource://sessions/report-601" for r in resources)
        recalled = await handle_read_resource("resource://sessions/report-601")
        assert json.loads(recalled[0].text)["report"]["release_check"]["ready"] is False
        result["report"]["release_check"]["ready"] = True
        assert state.last_release_check["ready"] is False
        assert json.loads((await handle_call_tool("core.report_recall", {}))[0].text)["ok"]


async def test_hosted_saved_resources_are_tenant_scoped(monkeypatch):
    monkeypatch.setenv(config.REMOTE_TRANSPORT_ENV, "0")
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_DATABASE_URL", raising=False)
    store = MemorySessionStore()
    with store.transaction("alice"):
        session.get_session("private").last_analysis = {"private": "alice-report"}
    app = create_app(
        api_keys={"alice": "a" * 40, "bob": "b" * 40}, store=store, allowed_hosts=["testserver"]
    )
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        ) as client,
    ):

        async def rpc(method, params, key):
            response = await client.post(
                "/mcp",
                headers={
                    "Authorization": "Bearer " + key,
                    "Accept": "application/json, text/event-stream",
                    "MCP-Protocol-Version": "2025-11-25",
                },
                json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
            )
            return response.json()["result"]

        listed = await rpc("resources/list", {}, "b" * 40)
        assert "private" not in json.dumps(listed)
        read = await rpc("resources/read", {"uri": "resource://sessions/private"}, "b" * 40)
        assert "alice-report" not in json.dumps(read)
        read = await rpc("resources/read", {"uri": "resource://sessions/private"}, "a" * 40)
        assert "alice-report" in json.dumps(read)
