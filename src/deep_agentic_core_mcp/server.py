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
    GetPromptRequestParams,
    GetPromptResult,
    ListPromptsResult,
    ListResourcesResult,
    ListToolsResult,
    PaginatedRequestParams,
    Prompt,
    PromptArgument,
    PromptMessage,
    ReadResourceRequestParams,
    ReadResourceResult,
    Resource,
    TextContent,
    TextResourceContents,
    Tool,
    ToolAnnotations,
)

from deep_agentic_core_mcp.adapters.ai_operations_spec import schema_resource_content
from deep_agentic_core_mcp.config import SERVER_NAME
from deep_agentic_core_mcp.prompts.registry import list_prompts as _registry_prompts
from deep_agentic_core_mcp.prompts.registry import render_prompt
from deep_agentic_core_mcp.resources.catalog import list_resources as _catalog_resources
from deep_agentic_core_mcp.tools.chaos import list_faults, run_experiment
from deep_agentic_core_mcp.tools.core import health, session_state, verify, version
from deep_agentic_core_mcp.tools.lens import (
    analyze_workflow,
    audit_report,
    compare_runs,
    report_summary,
    slo_summary,
)
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
    "core.verify": verify,
    "core.session_state": session_state,
    "lens.analyze_workflow": analyze_workflow,
    "lens.report_summary": report_summary,
    "lens.compare_runs": compare_runs,
    "lens.slo_summary": slo_summary,
    "lens.audit_report": audit_report,
    "chaos.list_faults": list_faults,
    "chaos.run_experiment": run_experiment,
    "spec.validate_artifact": validate_artifact,
}

# Tools whose execution has real-world side effects (they run external code),
# rather than just reading/deriving from arguments already in hand.
_OPEN_WORLD_TOOLS = {"chaos.run_experiment"}

# ---------------------------------------------------------------------------
# Tool and prompt definitions (derived from the canonical registries)
# ---------------------------------------------------------------------------


def _build_tools() -> list[Tool]:
    """Build Tool objects from the central tool registry.

    Only tools with a registered handler are advertised. Registry metadata
    beyond the MCP-standard fields (category, prerequisites, expected
    duration) rides in `_meta`; `mutates_session`/side effects map onto the
    standard MCP tool annotations so hosts get them without custom parsing.
    """
    tools = []
    for entry in _registry_tools():
        if entry["name"] not in _TOOL_DISPATCH:
            continue
        open_world = entry["name"] in _OPEN_WORLD_TOOLS
        tools.append(
            Tool(
                name=entry["name"],
                title=str(entry["title"]),
                description=str(entry["description"]),
                input_schema=entry["input_schema"],
                annotations=ToolAnnotations(
                    read_only_hint=not entry.get("mutates_session", False),
                    destructive_hint=open_world or None,
                    open_world_hint=open_world or None,
                ),
                _meta={
                    "category": entry.get("category"),
                    "prerequisites": entry.get("prerequisites", []),
                    "expected_duration": entry.get("expected_duration"),
                },
            )
        )
    return tools


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


def _build_prompts() -> list[Prompt]:
    """Build Prompt objects from the central prompt registry."""
    return [
        Prompt(
            name=entry["name"],
            description=entry["description"],
            arguments=[PromptArgument(**argument) for argument in entry.get("arguments", [])],
        )
        for entry in _registry_prompts()
    ]


TOOLS: list[Tool] = _build_tools()
RESOURCES: list[Resource] = _build_resources()
PROMPTS: list[Prompt] = _build_prompts()
RESOURCE_CONTENT: dict[str, dict[str, Any]] = {
    "resource://examples/sample_workflow": {
        "name": "Customer support answer",
        "start_time": "2026-08-07T12:00:00Z",
        "end_time": "2026-08-07T12:00:03Z",
        "steps": [],
        "chaos_events": [],
    },
    "resource://catalogs/chaos_faults": list_faults(),
    **schema_resource_content(),
}

# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_list_tools() -> list[Tool]:
    """Advertise available tools."""
    return TOOLS


async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    """Dispatch tool calls and return JSON results.

    Tool handlers are expected to catch their own known failure modes (e.g.
    `AdapterUnavailableError`) and return a structured `{"ok": False, ...}`
    payload. This is the safety net for whatever they don't: malformed
    client input can still surface as a raw exception from deep inside a
    handler (a pydantic `ValidationError` from `Workflow.model_validate`, a
    `KeyError` from an artifact missing an expected field, ...), and that
    must become a structured MCP tool error here rather than propagate.
    """
    handler = _TOOL_DISPATCH.get(name)
    if handler is None:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]
    try:
        result = handler(arguments)
    except Exception as exc:  # noqa: BLE001 - last-resort boundary, see docstring
        error = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        return [TextContent(type="text", text=json.dumps(error))]
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


async def handle_list_prompts() -> list[Prompt]:
    """Advertise available prompts."""
    return PROMPTS


async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
    """Render a prompt template into a ready-to-send message."""
    try:
        text = render_prompt(name, arguments)
    except KeyError:
        return GetPromptResult(description=f"Unknown prompt: {name}", messages=[])
    description = next((p.description for p in PROMPTS if p.name == name), None)
    return GetPromptResult(
        description=description,
        messages=[PromptMessage(role="user", content=TextContent(type="text", text=text))],
    )


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


async def _on_list_prompts(_: Any, params: PaginatedRequestParams) -> ListPromptsResult:
    del params
    return ListPromptsResult(prompts=await handle_list_prompts())


async def _on_get_prompt(_: Any, params: GetPromptRequestParams) -> GetPromptResult:
    return await handle_get_prompt(params.name, params.arguments)


server.add_request_handler("tools/list", PaginatedRequestParams, _on_list_tools)
server.add_request_handler("tools/call", CallToolRequestParams, _on_call_tool)
server.add_request_handler("resources/list", PaginatedRequestParams, _on_list_resources)
server.add_request_handler("resources/read", ReadResourceRequestParams, _on_read_resource)
server.add_request_handler("prompts/list", PaginatedRequestParams, _on_list_prompts)
server.add_request_handler("prompts/get", GetPromptRequestParams, _on_get_prompt)


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
