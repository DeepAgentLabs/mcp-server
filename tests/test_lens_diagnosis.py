"""`lens.diagnose_run` and `lens.score_analysis` (agenticlens >= 0.7.0)."""

import json
from pathlib import Path

import pytest

from deep_agentic_core_mcp.tools.registry import list_tools

ROOT = Path(__file__).resolve().parents[2]
LENS_EXAMPLES = ROOT / "agenticlens" / "examples"
DIAGNOSIS = LENS_EXAMPLES / "diagnosis" / "artifacts"
EVALUATION = LENS_EXAMPLES / "advanced_evaluation" / "artifacts" / "evaluation.json"

pytestmark = pytest.mark.skipif(
    not DIAGNOSIS.exists(), reason="agenticlens>=0.7.0 sibling checkout unavailable"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


async def _call(name: str, arguments: dict) -> dict:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool(name, arguments)
    return json.loads(result[0].text)


def test_new_lens_tools_are_registered_read_only() -> None:
    tools = {tool["name"]: tool for tool in list_tools()}
    for name in ("lens.diagnose_run", "lens.score_analysis"):
        assert tools[name]["category"] == "lens"
        assert tools[name]["mutates_session"] is False


@pytest.mark.asyncio
async def test_diagnose_run_attributes_the_faulty_step() -> None:
    baseline = [_load(path) for path in sorted((DIAGNOSIS / "baseline").glob("*.json"))]
    payload = await _call(
        "lens.diagnose_run", {"run": _load(DIAGNOSIS / "incident.json"), "baseline": baseline}
    )
    assert payload["ok"] is True
    attribution = payload["report"]["attribution"]
    assert attribution["faulty_step"] == "issue_refund"
    assert attribution["faulty_agent"] == "refunds"
    assert payload["report"]["anomalies"]["anomalies"]
    assert payload["narrative_markdown"].startswith("# Investigation")


@pytest.mark.asyncio
async def test_diagnose_run_budget_and_narrative_toggle() -> None:
    payload = await _call(
        "lens.diagnose_run",
        {
            "run": _load(DIAGNOSIS / "incident.json"),
            "budget": {"max_spans": 2},
            "include_narrative": False,
        },
    )
    assert payload["ok"] is True
    assert payload["report"]["guardrails"]["truncated"] is True
    assert "narrative_markdown" not in payload


@pytest.mark.asyncio
async def test_diagnose_run_rejects_missing_or_invalid_runs() -> None:
    assert (await _call("lens.diagnose_run", {}))["ok"] is False
    invalid = await _call("lens.diagnose_run", {"run": {"spans": "nope"}})
    assert invalid["ok"] is False and "Invalid diagnosis input" in invalid["error"]


@pytest.mark.asyncio
async def test_score_analysis_separates_judge_scores() -> None:
    payload = await _call("lens.score_analysis", {"report": _load(EVALUATION)})
    assert payload["ok"] is True
    assert payload["model_based"]["total"] == 3
    assert payload["judge_cost"]["total_cost_usd"] > 0
    assert payload["disagreement_cases"] == 2
    assert (await _call("lens.score_analysis", {}))["ok"] is False


@pytest.mark.asyncio
async def test_older_agenticlens_degrades_only_the_new_tools(monkeypatch) -> None:
    from deep_agentic_core_mcp.adapters import agenticlens as adapter

    monkeypatch.setattr(adapter, "_DIAGNOSIS_ERROR", ImportError("no agenticlens.diagnosis"))
    for name, arguments in (
        ("lens.diagnose_run", {"run": _load(DIAGNOSIS / "incident.json")}),
        ("lens.score_analysis", {"report": _load(EVALUATION)}),
    ):
        payload = await _call(name, arguments)
        assert payload["ok"] is False
        assert "agenticlens>=0.7.0" in payload["error"]
    audit = await _call("lens.audit_report", {"report": _load(EVALUATION)})
    assert audit["ok"] is True
