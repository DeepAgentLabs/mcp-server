"""MCP server entrypoint using the official MCP Python SDK (stdio transport)."""

import asyncio
import json
from collections.abc import Callable
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool
from pydantic import AnyUrl

from deep_agentic_core_mcp.config import SERVER_NAME
from deep_agentic_core_mcp.resources.catalog import list_resources as _catalog_resources
from deep_agentic_core_mcp.tools.core import health, version
from deep_agentic_core_mcp.tools.registry import list_tools as _registry_tools

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------

server = Server(SERVER_NAME)

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
    """Build Tool objects from the central tool registry.

    Only tools with a registered handler are advertised.
    """
    return [
        Tool(
            name=entry["name"],
            description=entry["description"],
            inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
        )
        for entry in _registry_tools()
        if entry["name"] in _TOOL_DISPATCH
    ]


def _build_resources() -> list[Resource]:
    """Build Resource objects from the central resource catalog."""
    return [
        Resource(
            uri=AnyUrl(entry["uri"]),
            name=entry["name"],
            mimeType="application/json",
        )
        for entry in _catalog_resources()
    ]


TOOLS: list[Tool] = _build_tools()
RESOURCES: list[Resource] = _build_resources()

# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


@server.list_tools()  # type: ignore[no-untyped-call, untyped-decorator]
async def handle_list_tools() -> list[Tool]:
    """Advertise available tools."""
    return TOOLS


@server.call_tool()  # type: ignore[untyped-decorator]
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    """Dispatch tool calls and return JSON results."""
    handler = _TOOL_DISPATCH.get(name)
    if handler is None:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]
    result = handler()
    return [TextContent(type="text", text=json.dumps(result))]


@server.list_resources()  # type: ignore[no-untyped-call, untyped-decorator]
async def handle_list_resources() -> list[Resource]:
    """Advertise available resources."""
    return RESOURCES


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
