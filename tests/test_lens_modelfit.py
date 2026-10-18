"""`lens.modelfit_recommend` (agenticlens >= 0.9.0)."""

import json
from pathlib import Path

import pytest

from deep_agentic_core_mcp.tools.registry import list_tools

yaml = pytest.importorskip("yaml")

ROOT = Path(__file__).resolve().parents[2]
MODELFIT = ROOT / "agenticlens" / "examples" / "modelfit"
EXPERIMENT = MODELFIT / "artifacts" / "experiment.json"

pytestmark = pytest.mark.skipif(
    not EXPERIMENT.exists(), reason="agenticlens>=0.9.0 sibling checkout unavailable"
)


def _experiment() -> dict:
    return json.loads(EXPERIMENT.read_text(encoding="utf-8"))


def _config() -> dict:
    return yaml.safe_load((MODELFIT / "modelfit.yaml").read_text(encoding="utf-8"))


def _metadata() -> dict:
    manifest = yaml.safe_load((MODELFIT / "support-experiment.yaml").read_text(encoding="utf-8"))
    return {variant["id"]: variant.get("metadata", {}) for variant in manifest["variants"]}


async def _call(arguments: dict) -> dict:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool("lens.modelfit_recommend", arguments)
    return json.loads(result[0].text)


def test_modelfit_tool_is_registered_read_only() -> None:
    tool = {tool["name"]: tool for tool in list_tools()}["lens.modelfit_recommend"]
    assert tool["category"] == "lens"
    assert tool["mutates_session"] is False
    assert "agenticlens>=0.9.0" in tool["description"]
    assert tool["input_schema"]["required"] == ["reports"]


@pytest.mark.asyncio
async def test_recommends_per_category_under_constraints() -> None:
    payload = await _call(
        {"reports": [_experiment()], "config": _config(), "variant_metadata": _metadata()}
    )

    assert payload["ok"] is True
    assert payload["unfit_category_ids"] == []
    by_category = {item["category_id"]: item for item in payload["recommendations"]}
    assert set(by_category) == {"all", "policy", "orders", "account", "safety"}
    assert by_category["account"]["variant_id"] == "oss-local"
    assert by_category["account"]["fallback_variant_id"] is None
    assert by_category["orders"]["variant_id"] == "small-a"
    assert "safety_failures" in by_category["orders"]["high_severity_risks"]
    assert by_category["all"]["cost_per_case_savings_usd"] > 0

    report = payload["modelfit"]
    assert report["reference_variant_id"] == "frontier-a"
    assert len(report["sources"][0]["sha256"]) == 64
    assert len(report["matrix"]) == 5 * 4


@pytest.mark.asyncio
async def test_default_config_derives_categories_from_tags() -> None:
    payload = await _call({"reports": [_experiment()]})
    assert payload["ok"] is True
    assert [item["category_id"] for item in payload["recommendations"]] == [
        "all",
        "account",
        "orders",
        "policy",
        "safety",
    ]


@pytest.mark.asyncio
async def test_unfit_categories_are_reported() -> None:
    config = {"defaults": {"max_cost_per_case_usd": 0.00001}}
    payload = await _call({"reports": [_experiment()], "config": config})
    assert payload["ok"] is True
    assert {item["status"] for item in payload["recommendations"]} == {"no_feasible_model"}
    assert payload["unfit_category_ids"]


@pytest.mark.asyncio
async def test_invalid_input_is_a_clear_error() -> None:
    assert (await _call({}))["ok"] is False

    payload = await _call({"reports": []})
    assert payload["ok"] is False and "at least one experiment report" in payload["error"]

    payload = await _call({"reports": [{"not": "a report"}]})
    assert payload["ok"] is False and payload["error"].startswith("Invalid ModelFit input")

    weights = {"quality": 0, "cost": 0, "latency": 0, "reliability": 0}
    payload = await _call({"reports": [_experiment()], "config": {"weights": weights}})
    assert payload["ok"] is False and "scoring weight" in payload["error"]


@pytest.mark.asyncio
async def test_older_agenticlens_degrades_only_the_modelfit_tool(monkeypatch) -> None:
    from deep_agentic_core_mcp.adapters import agenticlens as adapter
    from deep_agentic_core_mcp.server import handle_call_tool

    monkeypatch.setattr(adapter, "_MODELFIT_ERROR", ImportError("no agenticlens.modelfit"))
    payload = await _call({"reports": [_experiment()]})
    assert payload["ok"] is False
    assert "agenticlens>=0.9.0" in payload["error"]

    suite = {"name": "s", "version": "1", "cases": [{"id": "c", "name": "c", "input": "hi"}]}
    result = await handle_call_tool("lens.suite_check", {"suite": suite})
    assert json.loads(result[0].text)["ok"] is True
