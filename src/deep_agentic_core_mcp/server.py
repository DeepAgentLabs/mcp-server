"""MCP server entrypoint using the official MCP Python SDK (stdio transport)."""

import asyncio
import json
from collections.abc import Callable
from typing import Any

from mcp.server import Server, ServerRequestContext
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequestParams,
    CallToolResult,
    ListResourcesResult,
    ListToolsResult,
    PaginatedRequestParams,
    Resource,
    TextContent,
    Tool,
)

from deep_agentic_core_mcp.config import SERVER_NAME
from deep_agentic_core_mcp.resources.catalog import list_resources as _catalog_resources
from deep_agentic_core_mcp.tools.core import health, version
from deep_agentic_core_mcp.tools.registry import list_tools as _registry_tools

# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------

_TOOL_DISPATCH: dict[str, Callable[[], dict[str, str]]] = {
    "core.health": health,
    "core.version": version,
}

# ---------------------------------------------------------------------------
# Tool definitions (derived from the canonical registry)
# ---------------------------------------------------------------------------


def _build_tools() -> list[Tool]:
    """Build Tool objects from the central tool registry."""
    return [
        Tool(
            name=entry["name"],
            description=entry["description"],
            input_schema={"type": "object", "properties": {}, "additionalProperties": False},
        )
        for entry in _registry_tools()
        if entry["name"] in _TOOL_DISPATCH
    ]


def _build_resources() -> list[Resource]:
    """Build Resource objects from the central resource catalog."""
    return [
        Resource(
            uri=entry["uri"],
            name=entry["name"],
            mime_type="application/json",
        )
        for entry in _catalog_resources()
    ]


TOOLS: list[Tool] = _build_tools()
RESOURCES: list[Resource] = _build_resources()

# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_list_tools(
    ctx: ServerRequestContext[Any], params: PaginatedRequestParams | None
) -> ListToolsResult:
    """Advertise available tools."""
    return ListToolsResult(tools=TOOLS)


async def handle_call_tool(
    ctx: ServerRequestContext[Any], params: CallToolRequestParams
) -> CallToolResult:
    """Dispatch tool calls and return JSON results."""
    handler = _TOOL_DISPATCH.get(params.name)
    if handler is None:
        error_msg = json.dumps({"error": f"Unknown tool: {params.name}"})
        return CallToolResult(
            content=[TextContent(type="text", text=error_msg)],
            is_error=True,
        )
    result = handler()
    return CallToolResult(content=[TextContent(type="text", text=json.dumps(result))])


async def handle_list_resources(
    ctx: ServerRequestContext[Any], params: PaginatedRequestParams | None
) -> ListResourcesResult:
    """Advertise available resources."""
    return ListResourcesResult(resources=RESOURCES)


# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------

server = Server(
    SERVER_NAME,
    on_list_tools=handle_list_tools,
    on_call_tool=handle_call_tool,
    on_list_resources=handle_list_resources,
)

# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


async def run_server() -> None:
    """Start the MCP server over stdio."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    """Synchronous entrypoint for console_scripts."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
