"""Thin connector transport, credential isolation and tool metadata."""

import json
from unittest.mock import MagicMock, patch

import pytest

from deep_agentic_core_mcp.server import TOOLS, handle_call_tool
from deep_agentic_core_mcp.tools.tower import query, tool_definitions


@pytest.fixture(autouse=True)
def tower_environment(monkeypatch):
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_REMOTE", raising=False)
    monkeypatch.setenv("AGENTICOPS_TOWER_URL", "http://127.0.0.1:8000")
    monkeypatch.setenv("AGENTICOPS_TOWER_READ_TOKEN", "reader-secret")
    monkeypatch.setenv("AGENTICOPS_TOWER_WRITE_TOKEN", "writer-secret")


def test_read_and_write_use_distinct_credentials():
    completed = MagicMock(returncode=0, stdout=b'{"ok": true, "data": {"agents": []}}')
    with patch("deep_agentic_core_mcp.tools.tower.subprocess.run", return_value=completed) as run:
        assert query({"operation": "agents", "status": "unhealthy"})["ok"]
        request = json.loads(run.call_args.kwargs["input"])
        assert request["token"] == "reader-secret"
        assert request["url"].endswith("/agents?status=unhealthy")
        assert run.call_args.kwargs["timeout"] == 10
        assert query({"operation": "execute", "incident_id": "safe", "preview_digest": "hash"})[
            "ok"
        ]
        request = json.loads(run.call_args.kwargs["input"])
        assert request["token"] == "writer-secret"
        assert request["arguments"] == {"preview_digest": "hash"}
        assert "writer-secret" not in str(run.call_args.args)


def test_no_configuration_is_honest_unavailable(monkeypatch):
    monkeypatch.delenv("AGENTICOPS_TOWER_URL")
    assert not query({"operation": "status"})["ok"]
    monkeypatch.setenv("AGENTICOPS_TOWER_URL", "https://tower.example")
    monkeypatch.delenv("AGENTICOPS_TOWER_WRITE_TOKEN")
    assert not query({"operation": "detect"})["ok"]


@pytest.mark.parametrize(
    "args",
    [
        {"operation": "approval"},
        {"operation": "agents", "url": "https://attacker.example"},
        {"operation": "incident", "incident_id": ".."},
        {"operation": "incident", "incident_id": []},
        {"operation": "agents", "status": {"nested": "input"}},
    ],
)
def test_rejects_unsupported_input(args):
    assert not query(args)["ok"]


async def test_hosted_dispatch_never_uses_process_credentials(monkeypatch):
    result = await handle_call_tool("tower.status", {}, owner="tenant")
    assert json.loads(result[0].text)["ok"] is False
    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_REMOTE", "1")
    assert not query({"operation": "status"})["ok"]


async def test_dispatch_and_annotations():
    assert len(tool_definitions()) == 12
    names = {tool.name: tool for tool in TOOLS}
    assert names["tower.agents"].annotations.read_only_hint
    assert not names["tower.execute"].annotations.read_only_hint
    assert names["tower.execute"].annotations.open_world_hint
    assert "tower.approval" not in names
    result = await handle_call_tool("tower.agents", {"url": "forbidden"})
    assert not json.loads(result[0].text)["ok"]


def test_response_limit_and_secret_safe_errors():
    from deep_agentic_core_mcp.tools.tower_http import request

    payload = {
        "url": "http://localhost/status",
        "arguments": {},
        "write": False,
        "token": "reader-secret",
    }
    opener = MagicMock()
    opener.open.return_value.__enter__.return_value.read.return_value = b"x" * (1024 * 1024 + 1)
    with patch("deep_agentic_core_mcp.tools.tower_http.build_opener", return_value=opener):
        assert not request(payload)["ok"]
    opener.open.side_effect = OSError("reader-secret")
    with patch("deep_agentic_core_mcp.tools.tower_http.build_opener", return_value=opener):
        assert "reader-secret" not in str(request(payload))


def test_investigation_prompt_preserves_evidence_and_human_authority():
    from deep_agentic_core_mcp.prompts.registry import render_prompt

    prompt = render_prompt("tower.investigation", {"incident_id": "incident-1"})
    assert "incident-1" in prompt
    assert "untrusted data" in prompt
    assert "human approves" in prompt
    assert "fresh Lens, Evals and a probe" in prompt


async def test_hosted_listing_hides_all_tower_tools(monkeypatch):
    from deep_agentic_core_mcp.server import handle_list_tools

    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_REMOTE", "1")
    assert not any(tool.name.startswith("tower.") for tool in await handle_list_tools())


def test_deadline_kills_worker_and_reports_unknown_result():
    import subprocess

    with patch(
        "deep_agentic_core_mcp.tools.tower.subprocess.run",
        side_effect=subprocess.TimeoutExpired("worker", 10),
    ):
        result = query({"operation": "execute", "incident_id": "i", "preview_digest": "d"})
    assert not result["ok"]
    assert "inspect incident" in result["error"]
    assert all(not tool["mutates_session"] for tool in tool_definitions())
