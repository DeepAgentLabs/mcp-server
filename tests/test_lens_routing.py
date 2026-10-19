"""Read-only routing MCP boundary and graceful older-Lens behavior."""

import json
from pathlib import Path

import pytest

from deep_agentic_core_mcp.adapters import agenticlens as adapter
from deep_agentic_core_mcp.server import handle_call_tool
from deep_agentic_core_mcp.tools.registry import list_tools

REPORT = (
    Path(__file__).resolve().parents[2] / "agenticlens/examples/modelfit/artifacts/modelfit.json"
)


def test_registered_read_only():
    tool = next(t for t in list_tools() if t["name"] == "lens.routing_decide")
    assert tool["mutates_session"] is False
    assert tool["input_schema"]["required"] == ["report", "request"]


@pytest.mark.asyncio
@pytest.mark.skipif(not REPORT.exists(), reason="sibling example unavailable")
async def test_decides_without_execution_in_enforcement_mode():
    args = {
        "report": json.loads(REPORT.read_text()),
        "request": {"category_id": "orders", "request_id": "mcp-1"},
        "policy": {"mode": "enforce", "minimum_confidence": "low"},
    }
    result = await handle_call_tool("lens.routing_decide", args)
    payload = json.loads(result[0].text)
    assert payload["ok"] and payload["executed"] is False, payload
    assert payload["decision"]["targets"][0]["variant_id"] == "small-a"
    assert payload["decision"]["report_sha256"]
    args["request"]["category_id"] = "unknown"
    result = await handle_call_tool("lens.routing_decide", args)
    assert json.loads(result[0].text)["decision"]["status"] == "escalated"


@pytest.mark.asyncio
async def test_invalid_and_unavailable_inputs(monkeypatch):
    result = await handle_call_tool("lens.routing_decide", {})
    assert not json.loads(result[0].text)["ok"]
    monkeypatch.setattr(adapter, "_ROUTING_ERROR", ImportError("older lens"))
    result = await handle_call_tool("lens.routing_decide", {"report": {}, "request": {}})
    payload = json.loads(result[0].text)
    assert not payload["ok"] and "agenticlens>=0.10.0" in payload["error"]
    assert adapter.probe()["available"]


def test_workspace_source_precedes_stale_sibling_install(tmp_path, monkeypatch):
    import sys

    from deep_agentic_core_mcp import adapters

    root = tmp_path / "agenticlens"
    (root / "src").mkdir(parents=True)
    site = root / ".venv/lib/python3.12/site-packages"
    site.mkdir(parents=True)
    monkeypatch.setattr(adapters, "workspace_root", lambda: tmp_path)
    monkeypatch.setattr(sys, "path", [str(root / "src"), *sys.path])
    adapters.ensure_repo_on_path("agenticlens")
    assert sys.path.index(str(root / "src")) < sys.path.index(str(site))
