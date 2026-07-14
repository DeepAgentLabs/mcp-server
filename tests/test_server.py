"""Smoke tests for MCP server boot and tool discovery."""

import json

import pytest

from deep_agentic_core_mcp.server import _TOOL_DISPATCH, TOOLS, server


def test_server_has_name() -> None:
    assert server.name == "io.github.deepagentlabs/deep-agentic-core-mcp"


def test_tools_registered() -> None:
    tool_names = {t.name for t in TOOLS}
    assert "core.health" in tool_names
    assert "core.version" in tool_names


def test_tool_dispatch_covers_all_tools() -> None:
    for tool in TOOLS:
        assert tool.name in _TOOL_DISPATCH, f"No handler for {tool.name}"


@pytest.mark.asyncio
async def test_handle_list_tools() -> None:
    from deep_agentic_core_mcp.server import handle_list_tools

    tools = await handle_list_tools()
    names = {t.name for t in tools}
    assert "core.health" in names
    assert "core.version" in names


@pytest.mark.asyncio
async def test_handle_call_tool_health() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool("core.health", {})
    payload = json.loads(result[0].text)
    assert payload["status"] == "ok"


@pytest.mark.asyncio
async def test_handle_call_tool_version() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool("core.version", {})
    payload = json.loads(result[0].text)
    assert "version" in payload


@pytest.mark.asyncio
async def test_handle_call_tool_unknown() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool("nonexistent.tool", {})
    payload = json.loads(result[0].text)
    assert "error" in payload
