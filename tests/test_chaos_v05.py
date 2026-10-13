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


async def test_aios_export_matches_the_installed_chaos_version():
    """Chaos 0.5.0 (the advertised minimum) runs experiments but has no AIOS exporter."""
    from deep_agentic_core_mcp.adapters.agentic_chaos import aios_export_available, probe

    result = await handle_call_tool(
        "chaos.run_experiment",
        {
            "script": "mcp-server/examples/chaos_stream_target.py",
            "faults": ["stream_cut"],
            "session_id": "chaos-v05-export",
        },
    )
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    if probe()["version"] == "0.5.0":
        assert aios_export_available() is False
        assert payload["aios_run"] is None
        assert payload["aios_export"]["available"] is False
    else:
        assert payload["aios_export"]["aligned"] is True
