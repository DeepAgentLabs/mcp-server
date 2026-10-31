"""Read-only optimization MCP boundary and graceful older-Lens behavior."""

import json
from pathlib import Path

import pytest

from deep_agentic_core_mcp.adapters import agenticlens as adapter
from deep_agentic_core_mcp.server import handle_call_tool
from deep_agentic_core_mcp.tools.registry import list_tools

TRACES = Path(__file__).resolve().parents[2] / "agenticlens/examples/optimization/traces/before"
CONFIG = {"tradeoff_max_success_rate_drop": 0.25, "monthly_runs": 30000}


def _traces() -> list[dict]:
    return [json.loads(path.read_text()) for path in sorted(TRACES.glob("*.json"))]


def test_registered_read_only():
    tool = next(t for t in list_tools() if t["name"] == "lens.optimization_analyze")
    assert tool["mutates_session"] is False
    assert tool["input_schema"]["required"] == ["traces"]


@pytest.mark.asyncio
@pytest.mark.skipif(not TRACES.exists(), reason="sibling example unavailable")
async def test_ranks_opportunities_with_separate_benefit_and_risk():
    args = {"traces": _traces(), "config": CONFIG, "baseline_variant_id": "large"}
    payload = json.loads((await handle_call_tool("lens.optimization_analyze", args))[0].text)
    assert payload["ok"] and payload["advisory"] is True, payload
    kinds = {item["kind"] for item in payload["opportunities"]}
    assert {"tool_result_caching", "retry_policy", "quality_cost_tradeoff"} <= kinds
    first = payload["opportunities"][0]
    assert first["cost_usd_per_run"] is not None and first["risks"]
    assert payload["baseline_variant_id"] == "large"
    assert payload["optimization"]["schema_version"] == "1.0"


@pytest.mark.asyncio
@pytest.mark.skipif(not TRACES.exists(), reason="sibling example unavailable")
async def test_invalid_config_and_duplicate_runs_are_reported():
    traces = _traces()
    bad = {"traces": traces, "config": {"memory_max_shar": 0.3}}
    payload = json.loads((await handle_call_tool("lens.optimization_analyze", bad))[0].text)
    assert not payload["ok"] and "Invalid optimization input" in payload["error"]
    dup = {"traces": [traces[0], traces[0]]}
    payload = json.loads((await handle_call_tool("lens.optimization_analyze", dup))[0].text)
    assert not payload["ok"] and "unique" in payload["error"]


@pytest.mark.asyncio
async def test_missing_and_unavailable_inputs(monkeypatch):
    result = await handle_call_tool("lens.optimization_analyze", {})
    assert not json.loads(result[0].text)["ok"]
    monkeypatch.setattr(adapter, "_OPTIMIZATION_ERROR", ImportError("older lens"))
    result = await handle_call_tool("lens.optimization_analyze", {"traces": [{}]})
    payload = json.loads(result[0].text)
    assert not payload["ok"] and "agenticlens>=0.11.0" in payload["error"]
    assert adapter.probe()["available"]
