"""Exercise the actual optional Chaos v0.5 package through the MCP boundary."""

import json

from deep_agentic_core_mcp.server import handle_call_tool


async def test_catalog_includes_chaos_v05_faults():
    result = await handle_call_tool("chaos.list_faults", {})
    payload = json.loads(result[0].text)
    names = {fault["name"] for fault in payload["faults"]}
    assert {
        "stream_cut",
        "stream_hang",
        "slow_ttft",
        "slow_chunks",
        "auth_error",
        "context_length",
    } <= names


async def test_stream_fault_experiment_returns_native_event():
    result = await handle_call_tool(
        "chaos.run_experiment",
        {
            "script": "mcp-server/examples/chaos_stream_target.py",
            "faults": ["stream_cut"],
            "session_id": "chaos-v05",
        },
    )
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert payload["timed_out"] is False
    assert len(payload["chaos_events"]) == 1
    event = payload["chaos_events"][0]
    assert event["fault_type"] == "stream_cut"
    assert event["outcome"] == "degraded"
    assert event["detail"]["chunks_delivered"] == 1
