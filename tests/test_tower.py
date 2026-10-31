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
    assert len(tool_definitions()) == 20
    names = {tool.name: tool for tool in TOOLS}
    assert names["tower.agents"].annotations.read_only_hint
    assert not names["tower.execute"].annotations.read_only_hint
    assert names["tower.execute"].annotations.open_world_hint
    assert "tower.approval" not in names
    assert not any("approv" in name or "revoke" in name for name in names if "tower." in name)
    assert names["tower.runbook_recommendations"].annotations.read_only_hint
    assert not names["tower.runbook_execute"].annotations.read_only_hint
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


def test_runbook_tools_use_role_credentials_and_exact_routes():
    completed = MagicMock(returncode=0, stdout=b'{"ok": true, "data": []}')
    with patch("deep_agentic_core_mcp.tools.tower.subprocess.run", return_value=completed) as run:
        assert query({"operation": "runbook_recommendations", "incident_id": "i/1"})["ok"]
        request = json.loads(run.call_args.kwargs["input"])
        assert request["token"] == "reader-secret"
        assert request["url"] == "http://127.0.0.1:8000/incidents/i%2F1/runbooks"
        assert query({"operation": "runbook_execution", "execution_id": "e1"})["ok"]
        assert json.loads(run.call_args.kwargs["input"])["url"].endswith("/runbook-executions/e1")
        preview = {
            "operation": "runbook_preview",
            "incident_id": "i1",
            "runbook_id": "staging.dependency_recovery",
            "version": "1.0.0",
            "parameters": {"dependency": "search"},
        }
        assert query(preview)["ok"]
        request = json.loads(run.call_args.kwargs["input"])
        assert request["token"] == "writer-secret"
        assert request["url"].endswith("/incidents/i1/runbooks/preview")
        assert request["arguments"]["parameters"] == {"dependency": "search"}
        for operation, extra in (
            ("runbook_execute", {"preview_digest": "d"}),
            ("runbook_cancel", {}),
            ("runbook_verify", {"lens_evidence_id": "l", "evals_evidence_id": "e"}),
        ):
            assert query({"operation": operation, "execution_id": "e1", **extra})["ok"]
            request = json.loads(run.call_args.kwargs["input"])
            assert request["write"] and request["token"] == "writer-secret"
            assert request["url"].endswith("/runbook-executions/e1/" + operation[8:])


@pytest.mark.parametrize(
    "args",
    [
        {"operation": "runbook_approval", "execution_id": "e"},
        {"operation": "runbook_execution", "execution_id": ".."},
        {"operation": "runbook_execute", "preview_digest": "d"},
        {"operation": "runbook_preview", "incident_id": "i", "parameters": {"a": 1}},
        {"operation": "runbook_preview", "incident_id": "i", "parameters": "dependency=x"},
        {
            "operation": "runbook_preview",
            "incident_id": "i",
            "parameters": {str(n): "x" for n in range(21)},
        },
        {"operation": "runbook_execute", "execution_id": "e", "parameters": {"a": "b"}},
        {"operation": "runbook_execution", "execution_id": "e", "steps": "rm -rf /"},
    ],
)
def test_runbook_tools_reject_unsupported_input(args):
    with patch("deep_agentic_core_mcp.tools.tower.subprocess.run") as run:
        assert not query(args)["ok"]
    run.assert_not_called()


def test_runbook_tool_schemas():
    tools = {tool["name"]: tool for tool in tool_definitions()}
    preview = tools["tower.runbook_preview"]["input_schema"]
    assert preview["required"] == ["incident_id", "runbook_id", "version", "parameters"]
    assert preview["properties"]["parameters"]["additionalProperties"] == {"type": "string"}
    assert tools["tower.runbook_execute"]["input_schema"]["required"] == [
        "execution_id",
        "preview_digest",
    ]
    assert tools["tower.runbooks"]["prerequisites"] == ["configured Tower 0.9 API"]
    assert tools["tower.detect"]["prerequisites"] == ["configured Tower 0.6 API"]


def test_runbook_execute_waits_for_the_runbook_budget_and_requires_arguments():
    completed = MagicMock(returncode=0, stdout=b'{"ok": true, "data": {}}')
    with patch("deep_agentic_core_mcp.tools.tower.subprocess.run", return_value=completed) as run:
        assert query({"operation": "runbook_execute", "execution_id": "e", "preview_digest": "d"})[
            "ok"
        ]
        assert run.call_args.kwargs["timeout"] == 150
        assert json.loads(run.call_args.kwargs["input"])["timeout"] == 149
        assert query({"operation": "runbook_cancel", "execution_id": "e"})["ok"]
        assert run.call_args.kwargs["timeout"] == 10
        run.reset_mock()
        for args in (
            {"operation": "runbook_preview", "incident_id": "i"},
            {
                "operation": "runbook_preview",
                "incident_id": "i",
                "runbook_id": "r",
                "version": "1.0.0",
                "parameters": None,
            },
            {"operation": "runbook_execute", "execution_id": "e"},
            {"operation": "runbook_verify", "execution_id": "e", "lens_evidence_id": "l"},
        ):
            assert query(args) == {"ok": False, "error": "Required Tower arguments are missing"}
        run.assert_not_called()
    tools = {tool["name"]: tool for tool in tool_definitions()}
    assert tools["tower.runbook_execute"]["expected_duration"] == "slow"
    assert tools["tower.runbook_cancel"]["expected_duration"] == "fast"
