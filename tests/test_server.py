"""Smoke tests for MCP server boot and tool discovery."""

import json
import time
from pathlib import Path

import pytest

from deep_agentic_core_mcp.server import _TOOL_DISPATCH, TOOLS, server
from deep_agentic_core_mcp.services import session as session_service

ROOT = Path(__file__).resolve().parents[2]
SPEC_V04 = ROOT / "ai-operations-spec" / "specification" / "v0.4" / "examples"
AGENTICLENS_ARTIFACTS = ROOT / "agenticlens" / "examples" / "pitch_demo" / "artifacts"
CHAOS_TARGET_SCRIPT = "mcp-server/examples/chaos_target.py"

WORKFLOW_ARTIFACT = {
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


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def _isolated_default_session():
    """Keep the shared in-memory session from leaking state between tests."""
    session_service.reset_session("default")
    yield
    session_service.reset_session("default")


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

    result = await handle_list_tools()
    names = {t.name for t in result}
    assert "core.health" in names
    assert "core.version" in names


@pytest.mark.asyncio
async def test_handle_call_tool_health() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool("core.health", None)
    payload = json.loads(result[0].text)
    assert payload["status"] == "ok"


@pytest.mark.asyncio
async def test_handle_call_tool_version() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool("core.version", None)
    payload = json.loads(result[0].text)
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

    result = await handle_call_tool("lens.analyze_workflow", {"artifact": WORKFLOW_ARTIFACT})
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert payload["workflow"]["name"] == "Support workflow"
    assert "recommendations" in payload


@pytest.mark.asyncio
async def test_handle_call_tool_analyze_workflow_malformed_artifact() -> None:
    """A validation failure deep in an adapter must not raise past handle_call_tool."""
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool("lens.analyze_workflow", {"artifact": {"not": "a workflow"}})
    payload = json.loads(result[0].text)
    assert payload["ok"] is False
    assert "error" in payload


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

    result = await handle_call_tool("nonexistent.tool", None)
    payload = json.loads(result[0].text)
    assert "error" in payload


# ---------------------------------------------------------------------------
# Phase 2: session state, verify
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_handle_call_tool_verify() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool("core.verify", {})
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert set(payload["adapters"]) == {"agenticlens", "agentic_chaos", "ai_operations_spec"}


@pytest.mark.asyncio
async def test_handle_call_tool_session_state_tracks_calls() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    empty = json.loads((await handle_call_tool("core.session_state", {}))[0].text)
    assert empty["has_workflow"] is False
    assert empty["history"] == []

    await handle_call_tool("lens.analyze_workflow", {"artifact": WORKFLOW_ARTIFACT})
    after = json.loads((await handle_call_tool("core.session_state", {}))[0].text)
    assert after["has_workflow"] is True
    assert after["has_analysis"] is True
    assert after["history"][-1]["tool"] == "lens.analyze_workflow"


# ---------------------------------------------------------------------------
# Phase 3a: AgenticLens additions
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_handle_call_tool_report_summary_reuses_session_workflow() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    await handle_call_tool("lens.analyze_workflow", {"artifact": WORKFLOW_ARTIFACT})
    result = await handle_call_tool("lens.report_summary", {})
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert "Support workflow" in payload["markdown_report"]


@pytest.mark.asyncio
async def test_handle_call_tool_report_summary_without_artifact_or_session_fails() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool("lens.report_summary", {})
    payload = json.loads(result[0].text)
    assert payload["ok"] is False
    assert "error" in payload


@pytest.mark.asyncio
async def test_handle_call_tool_compare_runs() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    trace = _load_json(AGENTICLENS_ARTIFACTS / "trace.json")
    result = await handle_call_tool(
        "lens.compare_runs", {"baseline": [trace], "candidate": [trace]}
    )
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert payload["regressions"] == []


@pytest.mark.asyncio
async def test_handle_call_tool_slo_summary() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    report = _load_json(AGENTICLENS_ARTIFACTS / "evaluation.json")
    result = await handle_call_tool(
        "lens.slo_summary", {"report": report, "thresholds": {"min_pass_rate": 0.0}}
    )
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert payload["decision"]["passed"] is True


@pytest.mark.asyncio
async def test_handle_call_tool_audit_report() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    report = _load_json(AGENTICLENS_ARTIFACTS / "evaluation.json")
    result = await handle_call_tool("lens.audit_report", {"report": report, "include_html": True})
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert payload["cases"]
    assert "<html" in payload["html_report"]


# ---------------------------------------------------------------------------
# Phase 3b: Agentic Chaos additions
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_handle_call_tool_run_experiment_success() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool(
        "chaos.run_experiment",
        {"script": CHAOS_TARGET_SCRIPT, "faults": ["silent_degradation"]},
    )
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert payload["timed_out"] is False
    fault_types = {event["fault_type"] for event in payload["chaos_events"]}
    assert fault_types == {"silent_degradation"}


@pytest.mark.asyncio
async def test_handle_call_tool_run_experiment_honors_timeout() -> None:
    """timeout_seconds must bound wall-clock time, not just the reported result.

    `token_timeout`'s default hang is 2s; a 0.3s timeout must make this call
    return promptly rather than block for the full 2s regardless.
    """
    from deep_agentic_core_mcp.server import handle_call_tool

    started = time.monotonic()
    result = await handle_call_tool(
        "chaos.run_experiment",
        {"script": CHAOS_TARGET_SCRIPT, "faults": ["token_timeout"], "timeout_seconds": 0.3},
    )
    elapsed = time.monotonic() - started
    payload = json.loads(result[0].text)
    assert elapsed < 1.5, f"call blocked for {elapsed:.2f}s despite a 0.3s timeout"
    assert payload["ok"] is False
    assert payload["timed_out"] is True


@pytest.mark.asyncio
async def test_handle_call_tool_run_experiment_rejects_path_outside_workspace() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool(
        "chaos.run_experiment",
        {"script": "/etc/passwd", "faults": ["silent_degradation"]},
    )
    payload = json.loads(result[0].text)
    assert payload["ok"] is False
    assert "workspace" in payload["error"]


@pytest.mark.asyncio
async def test_handle_call_tool_run_experiment_rejects_unknown_fault() -> None:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool(
        "chaos.run_experiment",
        {"script": CHAOS_TARGET_SCRIPT, "faults": ["not_a_real_fault"]},
    )
    payload = json.loads(result[0].text)
    assert payload["ok"] is False
    assert "error" in payload


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_handle_list_prompts() -> None:
    from deep_agentic_core_mcp.server import handle_list_prompts

    prompts = await handle_list_prompts()
    names = {p.name for p in prompts}
    assert "chaos.experiment_brief" in names
    assert "lens.workflow_summary" in names


@pytest.mark.asyncio
async def test_handle_get_prompt_renders_arguments() -> None:
    from deep_agentic_core_mcp.server import handle_get_prompt

    result = await handle_get_prompt(
        "chaos.experiment_brief", {"faults": "silent_degradation", "script": "chaos_target.py"}
    )
    assert len(result.messages) == 1
    text = result.messages[0].content.text
    assert "silent_degradation" in text
    assert "chaos_target.py" in text


@pytest.mark.asyncio
async def test_handle_get_prompt_unknown_name() -> None:
    from deep_agentic_core_mcp.server import handle_get_prompt

    result = await handle_get_prompt("nonexistent.prompt", None)
    assert result.messages == []
    assert result.description is not None and "Unknown" in result.description
