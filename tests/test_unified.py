"""Unified workflow tools: fail-closed release checks, incidents and report export."""

import json
from pathlib import Path
from typing import Any

import pytest

from deep_agentic_core_mcp.server import handle_call_tool
from deep_agentic_core_mcp.services import session as session_service
from deep_agentic_core_mcp.services.remote_sessions import MemorySessionStore

ROOT = Path(__file__).resolve().parents[2]
AGENTICLENS_ARTIFACTS = ROOT / "agenticlens" / "examples" / "pitch_demo" / "artifacts"

CLEAN_CHAOS = {"ok": True, "crashed": None, "timed_out": False, "chaos_events": [{"f": 1}]}
CRASHED_CHAOS = {"ok": False, "crashed": "RuntimeError('boom')", "timed_out": False,
                 "chaos_events": []}  # fmt: skip


def _load(name: str) -> dict[str, Any]:
    return json.loads((AGENTICLENS_ARTIFACTS / name).read_text(encoding="utf-8"))


async def _call(name: str, arguments: dict[str, Any] | None = None, **kwargs: Any) -> Any:
    return json.loads((await handle_call_tool(name, arguments, **kwargs))[0].text)


def _failing_report() -> dict[str, Any]:
    report = _load("evaluation.json")
    report["summary"].update(passed_cases=0, failed_cases=1, pass_rate=0.0)
    report["cases"][0]["passed"] = False
    return report


async def _comparison() -> dict[str, Any]:
    trace = _load("trace.json")
    return await _call("core.compare_runs", {"baseline": [trace], "candidate": [trace]})


@pytest.fixture(autouse=True)
def _isolated_default_session():
    session_service.reset_session("default")
    yield
    session_service.reset_session("default")


@pytest.mark.asyncio
async def test_release_check_ready_with_all_valid_evidence() -> None:
    comparison = await _comparison()
    assert comparison["ok"] is True
    assert session_service.get_session().history[-1]["tool"] == "core.compare_runs"

    payload = await _call(
        "core.release_check",
        {"evaluation_report": _load("evaluation.json"), "chaos_report": CLEAN_CHAOS},
    )
    assert payload["ok"] is True
    assert payload["ready"] is True
    assert payload["missing_evidence"] == []
    assert [gate["name"] for gate in payload["gates"]] == ["comparison", "evaluation", "chaos"]
    assert all(gate["status"] == "passed" for gate in payload["gates"])
    evaluation = payload["gates"][1]
    assert evaluation["thresholds"]["min_pass_rate"] == 1.0
    assert evaluation["observed"]["pass_rate"] == 1.0


@pytest.mark.asyncio
async def test_release_check_requires_all_evidence_by_default() -> None:
    payload = await _call("core.release_check", {"chaos_report": CLEAN_CHAOS})
    assert payload["ok"] is True
    assert payload["ready"] is False
    assert payload["missing_evidence"] == ["comparison", "evaluation"]


@pytest.mark.asyncio
async def test_release_check_with_nothing_is_not_ready() -> None:
    payload = await _call("core.release_check", {})
    assert payload["ready"] is False
    assert payload["missing_evidence"] == ["comparison", "evaluation", "chaos"]


@pytest.mark.asyncio
async def test_required_evidence_narrows_the_check() -> None:
    payload = await _call(
        "core.release_check", {"chaos_report": CLEAN_CHAOS, "required_evidence": ["chaos"]}
    )
    assert payload["ready"] is True
    assert payload["required_evidence"] == ["chaos"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("arguments", "status"),
    [
        ({"chaos_report": {}}, "invalid"),
        ({"chaos_report": {"ok": False, "error": "boom"}}, "invalid"),
        ({"chaos_report": CRASHED_CHAOS}, "failed"),
        ({"chaos_report": {**CLEAN_CHAOS, "timed_out": True}}, "failed"),
        ({"comparison": {}}, "invalid"),
        ({"comparison": {"regressions": []}}, "invalid"),
        ({"comparison": {"ok": False, "error": "x"}}, "invalid"),
        ({"evaluation_report": {"summary": {"pass_rate": 1.0}}}, "invalid"),
        ({"evaluation_report": {"summary": []}}, "invalid"),
    ],
)
async def test_bad_or_failing_evidence_blocks_release(
    arguments: dict[str, Any], status: str
) -> None:
    kind = next(iter(arguments)).removesuffix("_report")
    payload = await _call("core.release_check", {**arguments, "required_evidence": [kind]})
    assert payload["ok"] is True
    assert payload["ready"] is False
    assert payload["gates"][0]["status"] == status
    assert payload["gates"][0]["reasons"]


@pytest.mark.asyncio
async def test_evaluation_uses_the_strict_evals_gate() -> None:
    arguments = {"evaluation_report": _failing_report(), "required_evidence": ["evaluation"]}
    strict = await _call("core.release_check", arguments)
    assert strict["ready"] is False
    assert "Pass rate" in strict["gates"][0]["reasons"][0]

    relaxed = await _call("core.release_check", {**arguments, "thresholds": {"min_pass_rate": 0}})
    assert relaxed["ready"] is True


@pytest.mark.asyncio
async def test_evaluation_honours_every_evals_threshold() -> None:
    payload = await _call(
        "core.release_check",
        {
            "evaluation_report": _load("evaluation.json"),
            "thresholds": {"max_average_latency_ms": 1},
            "required_evidence": ["evaluation"],
        },
    )
    assert payload["ready"] is False
    assert "latency" in payload["gates"][0]["reasons"][0]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arguments",
    [
        {"thresholds": {"min_pass_rat": 0.9}},
        {"thresholds": [0.9]},
        {"required_evidence": []},
        {"required_evidence": ["traces"]},
        {"required_evidence": "chaos"},
    ],
)
async def test_invalid_options_are_rejected(arguments: dict[str, Any]) -> None:
    payload = await _call("core.release_check", arguments)
    assert payload["ok"] is False
    assert session_service.get_session().history[-1]["ok"] is False


@pytest.mark.asyncio
async def test_regressions_fail_the_comparison_gate() -> None:
    comparison = await _comparison()
    comparison["regressions"] = ["success_rate dropped 50.0%"]
    payload = await _call(
        "core.release_check", {"comparison": comparison, "required_evidence": ["comparison"]}
    )
    assert payload["ready"] is False
    assert payload["gates"][0]["reasons"] == ["success_rate dropped 50.0%"]


@pytest.mark.asyncio
async def test_incident_summary_requires_evidence() -> None:
    payload = await _call("core.incident_summary", {})
    assert payload["ok"] is False


@pytest.mark.asyncio
async def test_incident_summary_ignores_passing_evidence() -> None:
    payload = await _call(
        "core.incident_summary",
        {"evaluation_report": _load("evaluation.json"), "chaos_report": CLEAN_CHAOS},
    )
    assert payload["ok"] is True
    assert payload["status"] == "no_signals"
    assert payload["findings"] == []


@pytest.mark.asyncio
async def test_incident_summary_collects_failures_and_blocked_release() -> None:
    await _call("core.release_check", {"chaos_report": CRASHED_CHAOS})
    payload = await _call(
        "core.incident_summary",
        {"chaos_report": CRASHED_CHAOS, "evaluation_report": _failing_report()},
    )
    assert payload["status"] == "investigate"
    assert [finding["type"] for finding in payload["findings"]] == [
        "resilience_failure",
        "failed_cases",
        "blocked_release",
    ]


@pytest.mark.asyncio
async def test_export_report_collects_session_evidence() -> None:
    await _comparison()
    await _call("core.release_check", {"chaos_report": CLEAN_CHAOS})
    payload = await _call("core.export_report", {})
    report = payload["report"]
    assert report["schema_version"] == "mcp.unified-report.v1"
    assert report["generator"]["name"] == "io.github.DeepAgentLabs/deep-agentic-core-mcp"
    assert report["comparison"]["ok"] is True
    assert report["release_check"]["missing_evidence"] == ["evaluation"]
    assert [entry["tool"] for entry in report["history"]] == [
        "core.compare_runs",
        "core.release_check",
    ]
    assert session_service.get_session().history[-1]["tool"] == "core.export_report"


@pytest.mark.asyncio
async def test_hosted_calls_keep_evidence_per_user() -> None:
    store = MemorySessionStore()
    trace = _load("trace.json")
    runs = {"baseline": [trace], "candidate": [trace]}
    await _call("core.compare_runs", runs, owner="alice", store=store)
    alice = await _call(
        "core.release_check",
        {"required_evidence": ["comparison"]},
        owner="alice",
        store=store,
    )
    bob = await _call(
        "core.release_check",
        {"required_evidence": ["comparison"]},
        owner="bob",
        store=store,
    )
    assert alice["ready"] is True
    assert bob["ready"] is False
    exported = await _call("core.export_report", {}, owner="alice", store=store)
    assert exported["report"]["release_check"]["ready"] is True
