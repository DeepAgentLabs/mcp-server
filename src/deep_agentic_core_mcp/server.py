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

from deep_agentic_core_mcp import config
from deep_agentic_core_mcp.adapters.ai_operations_spec import schema_resource_content
from deep_agentic_core_mcp.config import SERVER_NAME
from deep_agentic_core_mcp.prompts.registry import list_prompts as _registry_prompts
from deep_agentic_core_mcp.prompts.registry import render_prompt
from deep_agentic_core_mcp.resources.catalog import list_resources as _catalog_resources
from deep_agentic_core_mcp.services import access_evidence
from deep_agentic_core_mcp.services.access_policy import Principal
from deep_agentic_core_mcp.services.remote_sessions import SessionStore
from deep_agentic_core_mcp.tools import access
from deep_agentic_core_mcp.tools.chaos import export_aios_run, list_faults, run_experiment
from deep_agentic_core_mcp.tools.core import health, session_state, verify, version
from deep_agentic_core_mcp.tools.evals import validate_artifact as validate_evals_artifact
from deep_agentic_core_mcp.tools.lens import (
    analyze_workflow,
    audit_report,
    compare_runs,
    diagnose_run,
    modelfit_recommend,
    optimization_analyze,
    report_summary,
    routing_decide,
    score_analysis,
    slo_summary,
    suite_check,
    suite_from_traces,
)
from deep_agentic_core_mcp.tools.registry import list_tools as _registry_tools
from deep_agentic_core_mcp.tools.sidecar import module_inventory, status
from deep_agentic_core_mcp.tools.spec import validate_artifact
from deep_agentic_core_mcp.tools.tower import READ_OPERATIONS, WRITE_OPERATIONS
from deep_agentic_core_mcp.tools.tower import query as tower_query
from deep_agentic_core_mcp.tools.unified import (
    compare_runs as unified_compare_runs,
)
from deep_agentic_core_mcp.tools.unified import (
    export_report,
    incident_summary,
    release_check,
)

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------

server = Server(SERVER_NAME, version=config.VERSION)

# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------

_TOOL_DISPATCH: dict[str, Callable[[dict[str, Any] | None], dict[str, Any]]] = {
    "evals.validate_artifact": validate_evals_artifact,
    "core.health": health,
    "core.version": version,
    "core.verify": verify,
    "core.session_state": session_state,
    "core.access_status": access.access_status,
    "lens.analyze_workflow": analyze_workflow,
    "lens.report_summary": report_summary,
    "lens.compare_runs": compare_runs,
    "lens.slo_summary": slo_summary,
    "lens.audit_report": audit_report,
    "lens.diagnose_run": diagnose_run,
    "lens.score_analysis": score_analysis,
    "lens.suite_from_traces": suite_from_traces,
    "lens.suite_check": suite_check,
    "lens.modelfit_recommend": modelfit_recommend,
    "lens.routing_decide": routing_decide,
    "lens.optimization_analyze": optimization_analyze,
    "chaos.list_faults": list_faults,
    "chaos.run_experiment": run_experiment,
    "chaos.export_aios_run": export_aios_run,
    "sidecar.status": status,
    "sidecar.module_inventory": module_inventory,
    "spec.validate_artifact": validate_artifact,
    "core.compare_runs": unified_compare_runs,
    "core.release_check": release_check,
    "core.incident_summary": incident_summary,
    "core.export_report": export_report,
}

for _operation in (*READ_OPERATIONS, *WRITE_OPERATIONS):

    def _tower_handler(
        arguments: dict[str, Any] | None, *, operation: str = _operation
    ) -> dict[str, Any]:
        return tower_query({**(arguments or {}), "operation": operation})

    _TOOL_DISPATCH["tower." + _operation] = _tower_handler

# Tools whose execution has real-world side effects (they run external code),
# rather than just reading/deriving from arguments already in hand.
_OPEN_WORLD_TOOLS = {"chaos.run_experiment"} | {"tower." + op for op in WRITE_OPERATIONS}

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
                    read_only_hint=not (entry.get("mutates_session", False) or open_world),
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
    "resource://workflows/release-check": {
        "steps": [
            {
                "tool": "core.compare_runs",
                "produces": "comparison",
                "note": "Baseline and candidate Lens trace runs; stored in the session.",
            },
            {
                "tool": "chaos.run_experiment",
                "produces": "chaos",
                "note": "Local stdio only. Hosted callers pass chaos_report instead.",
            },
            {
                "tool": "core.release_check",
                "produces": "release_check",
                "note": "Pass evaluation_report (native Evals) and optional Evals "
                "GateConfig thresholds; comparison and chaos default to the session.",
            },
            {"tool": "core.incident_summary", "produces": "incident_summary"},
            {"tool": "core.export_report", "produces": "mcp.unified-report.v1"},
        ],
        "rules": [
            "Missing, malformed or failed-call evidence blocks readiness.",
            "Use required_evidence to narrow which kinds a release needs.",
            "The exported report is MCP-local, not an AIOS artifact.",
        ],
    },
    **schema_resource_content(),
}

# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


def _remote_tool_names() -> list[str]:
    return [
        tool.name
        for tool in TOOLS
        if tool.name not in _OPEN_WORLD_TOOLS and not tool.name.startswith("tower.")
    ]


async def handle_list_tools(principal: Principal | None = None) -> list[Tool]:
    """Advertise available tools; a hosted caller sees only what its policy permits."""
    if config.is_remote_transport() or principal is not None:
        names = set(_remote_tool_names())
        return [
            tool
            for tool in TOOLS
            if tool.name in names and (principal is None or principal.policy.permits(tool.name))
        ]
    return TOOLS


def _deny(evidence: dict[str, Any], message: str, revoked: bool = False) -> dict[str, Any]:
    return {
        "ok": False,
        "error": message,
        "access_denied": True,
        "revoked": revoked,
        "access_decision": evidence,
    }


def _authorize_dispatch(
    name: str,
    owner: str,
    authorizer: Callable[[], Principal | None],
    correlation_id: str,
) -> tuple[Principal | None, dict[str, Any] | None]:
    """Re-check the key and its policy immediately before the handler runs.

    This runs after the caller has waited for its session lock, so a call that
    was queued, retried or sent on an existing connection after revocation, a
    policy change or expiry is rejected. Calls already running are not cancelled.
    """
    try:
        principal = authorizer()
    except Exception:  # noqa: BLE001 - an unreachable key store must fail closed
        evidence = access_evidence.record(
            "denial",
            correlation_id=correlation_id,
            user=owner,
            tool=name,
            reason="authorization unavailable at dispatch",
        )
        return None, _deny(evidence, "Access denied: authorization unavailable")
    if principal is None or principal.user != owner:
        evidence = access_evidence.record(
            "revocation_acknowledged",
            correlation_id=correlation_id,
            user=owner,
            tool=name,
            reason="credential revoked or replaced before dispatch",
        )
        return None, _deny(evidence, "Access denied: credential revoked", revoked=True)
    reason = principal.policy.denial_reason(name)
    if reason is not None:
        evidence = access_evidence.record(
            "denial",
            correlation_id=correlation_id,
            user=owner,
            tool=name,
            task_id=principal.policy.task_id,
            reason=reason,
        )
        return principal, _deny(evidence, f"Access denied: {reason}")
    return principal, None


async def handle_call_tool(
    name: str,
    arguments: dict[str, Any] | None,
    *,
    owner: str | None = None,
    store: SessionStore | None = None,
    authorizer: Callable[[], Principal | None] | None = None,
) -> list[TextContent]:
    """Dispatch tool calls and return JSON results.

    Tool handlers are expected to catch their own known failure modes (e.g.
    `AdapterUnavailableError`) and return a structured `{"ok": False, ...}`
    payload. This is the safety net for whatever they don't: malformed
    client input can still surface as a raw exception from deep inside a
    handler (a pydantic `ValidationError` from `Workflow.model_validate`, a
    `KeyError` from an artifact missing an expected field, ...), and that
    must become a structured MCP tool error here rather than propagate.

    Hosted calls pass `authorizer`, which re-authenticates the caller's key and
    reloads its access policy at dispatch; every hosted call then leaves
    correlated `mcp.access-decision.v1` evidence (see services/access_evidence.py).
    """
    handler = _TOOL_DISPATCH.get(name)
    if handler is None:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

    def transport_denial(message: str) -> dict[str, Any]:
        if owner is None:
            return {"ok": False, "error": message}
        # Hidden from hosted tools/list, but a direct call is still audited.
        evidence = access_evidence.record(
            "denial",
            correlation_id=access_evidence.new_correlation_id(),
            user=owner,
            tool=name,
            reason="tool unavailable over hosted transport",
        )
        return _deny(evidence, message)

    def execute() -> dict[str, Any]:
        if name.startswith("tower.") and (owner is not None or config.is_remote_transport()):
            return transport_denial("Tower connector is local-only")
        if owner is not None and store is not None:
            if name in _OPEN_WORLD_TOOLS:
                return transport_denial("chaos.run_experiment is disabled over remote transport")
            if authorizer is None:
                with store.transaction(owner):
                    return handler(arguments)
            correlation_id = access_evidence.new_correlation_id()
            with store.transaction(owner):
                principal, denied = _authorize_dispatch(name, owner, authorizer, correlation_id)
                if denied is not None or principal is None:
                    return denied or {"ok": False, "error": "Access denied"}
                task_id = principal.policy.task_id
                access_evidence.record(
                    "dispatch",
                    correlation_id=correlation_id,
                    user=owner,
                    tool=name,
                    task_id=task_id,
                )
                with access.principal_scope(principal):
                    try:
                        result = handler(arguments)
                    except Exception:
                        access_evidence.record(
                            "completion",
                            correlation_id=correlation_id,
                            user=owner,
                            tool=name,
                            task_id=task_id,
                            outcome="error",
                        )
                        raise
            access_evidence.record(
                "completion",
                correlation_id=correlation_id,
                user=owner,
                tool=name,
                task_id=task_id,
                outcome="error" if result.get("error") or result.get("ok") is False else "ok",
            )
            return result
        return handler(arguments)

    try:
        # Off the event loop: handlers are synchronous and some (notably
        # chaos.run_experiment) can block for up to tens of seconds, which
        # would otherwise stall every other client under concurrent/remote use.
        result = await asyncio.to_thread(execute)
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


async def _on_list_tools(ctx: Any, params: PaginatedRequestParams) -> ListToolsResult:
    del params
    request = getattr(ctx, "request", None)
    principal = request.scope.get("deep_agentic_principal") if request is not None else None
    return ListToolsResult(tools=await handle_list_tools(principal))


async def _on_call_tool(ctx: Any, params: CallToolRequestParams) -> CallToolResult:
    request = getattr(ctx, "request", None)
    if request is not None:
        # Trusted ASGI scope values, never client arguments or identity headers.
        identity = request.scope.get("deep_agentic_identity")
        store = request.scope.get("deep_agentic_store")
        authorizer = request.scope.get("deep_agentic_authorizer")
        if identity is None or store is None or authorizer is None:
            return CallToolResult(
                content=[TextContent(type="text", text='{"error":"Authentication required"}')],
                is_error=True,
            )
        content = await handle_call_tool(
            params.name, params.arguments, owner=identity, store=store, authorizer=authorizer
        )
    else:
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
