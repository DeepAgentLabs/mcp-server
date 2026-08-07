"""MCP server entrypoint using the official MCP Python SDK (stdio transport)."""

import asyncio
import json
from collections.abc import Callable
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequestParams,
    CallToolResult,
    ListResourcesResult,
    ListToolsResult,
    PaginatedRequestParams,
    ReadResourceRequestParams,
    ReadResourceResult,
    Resource,
    TextContent,
    TextResourceContents,
    Tool,
)

from deep_agentic_core_mcp.adapters.ai_operations_spec import SCHEMA_DOCUMENTS
from deep_agentic_core_mcp.config import SERVER_NAME
from deep_agentic_core_mcp.resources.catalog import list_resources as _catalog_resources
from deep_agentic_core_mcp.tools.chaos import list_faults
from deep_agentic_core_mcp.tools.core import health, version
from deep_agentic_core_mcp.tools.lens import analyze_workflow
from deep_agentic_core_mcp.tools.registry import list_tools as _registry_tools
from deep_agentic_core_mcp.tools.spec import validate_artifact

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------

server = Server(SERVER_NAME)

# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------

_TOOL_DISPATCH: dict[str, Callable[[dict[str, Any] | None], dict[str, Any]]] = {
    "core.health": health,
    "core.version": version,
    "lens.analyze_workflow": analyze_workflow,
    "chaos.list_faults": list_faults,
    "spec.validate_artifact": validate_artifact,
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
            description=str(entry["description"]),
            input_schema=entry["input_schema"],
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
RESOURCE_CONTENT: dict[str, dict[str, Any]] = {
    "resource://examples/sample_workflow": {
        "name": "Customer support answer",
        "start_time": "2026-08-07T12:00:00Z",
        "end_time": "2026-08-07T12:00:03Z",
        "steps": [],
        "chaos_events": [],
    },
    "resource://catalogs/chaos_faults": list_faults(),
    "resource://schemas/aiops/v0.4/workflow": SCHEMA_DOCUMENTS["workflow.schema.json"],
    "resource://schemas/aiops/v0.4/run": SCHEMA_DOCUMENTS["run.schema.json"],
    "resource://schemas/aiops/v0.4/common": SCHEMA_DOCUMENTS["common.schema.json"],
}

# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_list_tools() -> list[Tool]:
    """Advertise available tools."""
    return TOOLS


async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    """Dispatch tool calls and return JSON results."""
    handler = _TOOL_DISPATCH.get(name)
    if handler is None:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]
    result = handler(arguments)
    return [TextContent(type="text", text=json.dumps(result))]


async def handle_list_resources() -> list[Resource]:
    """Advertise available resources."""
    return RESOURCES


async def handle_read_resource(uri: str) -> list[TextResourceContents]:
    """Return resource contents for known MCP resources."""
    payload = RESOURCE_CONTENT.get(uri)
    if payload is None:
        return [
            TextResourceContents(
                uri=uri,
                mime_type="application/json",
                text=json.dumps({"error": f"Unknown resource: {uri}"}),
            )
        ]
    return [
        TextResourceContents(
            uri=uri,
            mime_type="application/json",
            text=json.dumps(payload, indent=2),
        )
    ]


async def _on_list_tools(_: Any, params: PaginatedRequestParams) -> ListToolsResult:
    del params
    return ListToolsResult(tools=await handle_list_tools())


async def _on_call_tool(_: Any, params: CallToolRequestParams) -> CallToolResult:
    content = await handle_call_tool(params.name, params.arguments)
    is_error = False
    if content:
        try:
            payload = json.loads(content[0].text)
        except json.JSONDecodeError:
            payload = {}
        is_error = bool(payload.get("error"))
    return CallToolResult(content=list(content), structured_content=None, is_error=is_error)


async def _on_list_resources(_: Any, params: PaginatedRequestParams) -> ListResourcesResult:
    del params
    return ListResourcesResult(resources=await handle_list_resources())


async def _on_read_resource(_: Any, params: ReadResourceRequestParams) -> ReadResourceResult:
    return ReadResourceResult(contents=list(await handle_read_resource(str(params.uri))))


server.add_request_handler("tools/list", PaginatedRequestParams, _on_list_tools)
server.add_request_handler("tools/call", CallToolRequestParams, _on_call_tool)
server.add_request_handler("resources/list", PaginatedRequestParams, _on_list_resources)
server.add_request_handler("resources/read", ReadResourceRequestParams, _on_read_resource)


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
