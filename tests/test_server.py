"""Smoke tests for MCP server boot and tool discovery."""

import json
from pathlib import Path

import pytest
from mcp.types import CallToolRequestParams

from deep_agentic_core_mcp.server import _TOOL_DISPATCH, TOOLS, server

ROOT = Path(__file__).resolve().parents[2]
SPEC_V04 = ROOT / "ai-operations-spec" / "specification" / "v0.4" / "examples"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_server_has_name() -> None:
    assert server.name == "io.github.DeepAgentLabs/deep-agentic-core-mcp"


def test_tools_registered() -> None:
    tool_names = {t.name for t in TOOLS}
    assert "core.health" in tool_names
    assert "core.version" in tool_names
    assert "lens.analyze_workflow" in tool_names
    assert "chaos.list_faults" in tool_names
    assert "spec.validate_artifact" in tool_names


def test_tool_dispatch_covers_all_tools() -> None:
    for tool in TOOLS:
        assert tool.name in _TOOL_DISPATCH, f"No handler for {tool.name}"


@pytest.mark.asyncio
async def test_handle_list_tools() -> None:
    from deep_agentic_core_mcp.server import handle_list_tools

    result = await handle_list_tools(None, None)  # type: ignore[arg-type]
    names = {t.name for t in result.tools}
    assert "core.health" in names
    assert "core.version" in names


@pytest.mark.asyncio
async def test_handle_call_tool_health() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    params = CallToolRequestParams(name="core.health")
    result = await handle_call_tool(None, params)  # type: ignore[arg-type]
    payload = json.loads(result.content[0].text)
    assert payload["status"] == "ok"


@pytest.mark.asyncio
async def test_handle_call_tool_version() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    params = CallToolRequestParams(name="core.version")
    result = await handle_call_tool(None, params)  # type: ignore[arg-type]
    payload = json.loads(result.content[0].text)
    assert "version" in payload


@pytest.mark.asyncio
async def test_handle_call_tool_list_faults() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool("chaos.list_faults", {})
    payload = json.loads(result[0].text)
    fault_names = {fault["name"] for fault in payload["faults"]}
    assert "token_timeout" in fault_names
    assert "tool_failure" in fault_names


@pytest.mark.asyncio
async def test_handle_call_tool_analyze_workflow() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    artifact = {
        "name": "Support workflow",
        "start_time": "2026-08-07T12:00:00Z",
        "end_time": "2026-08-07T12:00:03Z",
        "steps": [
            {
                "name": "Retriever",
                "type": "retriever",
                "metrics": {
                    "prompt_tokens": 100,
                    "completion_tokens": 20,
                    "total_tokens": 120,
                    "latency": 1.0,
                    "cost": 0.01,
                },
                "metadata": {
                    "chunk_count": 6,
                    "retrieved_chunks": ["a", "b", "c", "d", "e", "f"],
                },
            }
        ],
    }
    result = await handle_call_tool("lens.analyze_workflow", {"artifact": artifact})
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert payload["workflow"]["name"] == "Support workflow"
    assert "recommendations" in payload


@pytest.mark.asyncio
async def test_handle_call_tool_validate_valid_run() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    artifact = _load_json(SPEC_V04 / "valid" / "run.json")
    result = await handle_call_tool("spec.validate_artifact", {"artifact": artifact})
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert payload["semantic_errors"] == []


@pytest.mark.asyncio
async def test_handle_call_tool_validate_semantic_invalid_run() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    artifact = _load_json(SPEC_V04 / "semantic-invalid" / "dangling-reference.json")
    result = await handle_call_tool("spec.validate_artifact", {"artifact": artifact})
    payload = json.loads(result[0].text)
    assert payload["ok"] is False
    assert payload["semantic_errors"]


@pytest.mark.asyncio
async def test_handle_call_tool_unknown() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    params = CallToolRequestParams(name="nonexistent.tool")
    result = await handle_call_tool(None, params)  # type: ignore[arg-type]
    payload = json.loads(result.content[0].text)
    assert "error" in payload
