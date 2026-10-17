"""`lens.suite_from_traces` and `lens.suite_check` (agenticlens >= 0.8.0)."""

import json
from pathlib import Path

import pytest

from deep_agentic_core_mcp.tools.registry import list_tools

ROOT = Path(__file__).resolve().parents[2]
SUITES = ROOT / "agenticlens" / "examples" / "suites"
TRACES = SUITES / "inputs" / "traces"
APPROVED = SUITES / "store" / "support-regression" / "1.0.0.json"

pytestmark = pytest.mark.skipif(
    not APPROVED.exists(), reason="agenticlens>=0.8.0 sibling checkout unavailable"
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


async def _call(name: str, arguments: dict) -> dict:
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool(name, arguments)
    return json.loads(result[0].text)


def test_suite_tools_are_registered_read_only() -> None:
    tools = {tool["name"]: tool for tool in list_tools()}
    for name in ("lens.suite_from_traces", "lens.suite_check"):
        assert tools[name]["category"] == "lens"
        assert tools[name]["mutates_session"] is False
        assert "agenticlens>=0.8.0" in tools[name]["description"]


@pytest.mark.asyncio
async def test_suite_from_traces_converts_masks_and_skips() -> None:
    runs = [_load(path) for path in sorted(TRACES.glob("*.json"))]
    payload = await _call(
        "lens.suite_from_traces", {"runs": runs, "name": "prod", "version": "1.0.0"}
    )
    assert payload["ok"] is True
    cases = payload["suite"]["cases"]
    assert [case["id"] for case in cases] == ["trace-prod-0001", "trace-prod-0002"]
    assert cases[1]["required_tool_order"] == ["lookup_account", "cancel_subscription"]
    assert all(case["metadata"]["review_status"] == "needs_review" for case in cases)
    assert "ana@example.org" not in json.dumps(payload)
    assert payload["masking"]["total"] >= 1
    assert [item["source_id"] for item in payload["skipped"]] == ["prod-0003"]


@pytest.mark.asyncio
async def test_suite_from_traces_without_masking_or_convertible_runs() -> None:
    failed = _load(TRACES / "prod-0003.json")
    payload = await _call(
        "lens.suite_from_traces", {"runs": [failed], "name": "p", "version": "1", "mask": False}
    )
    assert payload["ok"] is True and payload["suite"] is None and payload["masking"] is None
    assert "did not succeed" in payload["skipped"][0]["reason"]
    missing = await _call("lens.suite_from_traces", {"runs": [failed]})
    assert missing["ok"] is False and "name, version" in missing["error"]
    invalid = await _call(
        "lens.suite_from_traces", {"runs": [{"spans": "x"}], "name": "p", "version": "1"}
    )
    assert invalid["ok"] is False and invalid["error"].startswith("Invalid suite input")


@pytest.mark.asyncio
async def test_suite_check_reports_approval_readiness() -> None:
    approved = _load(APPROVED)["suite"]
    payload = await _call("lens.suite_check", {"suite": approved})
    assert payload["ok"] is True and payload["approvable"] is True
    assert payload["summary"]["total_cases"] == 15
    assert [check["name"] for check in payload["approval_checks"]] == [
        "review",
        "pii",
        "conflicting_duplicates",
    ]

    leaky = {
        "name": "s",
        "version": "1",
        "cases": [
            {"id": "a", "name": "a", "input": "mail a@b.io", "expected_output": "x"},
            {"id": "b", "name": "b", "input": "mail a@b.io", "expected_output": "y"},
        ],
    }
    payload = await _call("lens.suite_check", {"suite": leaky})
    assert payload["ok"] is True and payload["approvable"] is False
    failed = {check["name"] for check in payload["approval_checks"] if not check["passed"]}
    assert failed == {"pii", "conflicting_duplicates"}
    assert payload["duplicates"]["conflicting_groups"] == 1
    assert "a@b.io" not in json.dumps(payload["approval_checks"])


@pytest.mark.asyncio
async def test_suite_check_rejects_missing_or_invalid_suite() -> None:
    assert (await _call("lens.suite_check", {}))["ok"] is False
    invalid = await _call("lens.suite_check", {"suite": {"name": "s", "version": "1", "cases": []}})
    assert invalid["ok"] is False and invalid["error"].startswith("Invalid suite")
