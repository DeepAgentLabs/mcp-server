"""Evals 0.10 AIOS evaluation evidence validates with spec.validate_artifact."""

import json
from pathlib import Path

import pytest

from deep_agentic_core_mcp.server import handle_call_tool

evals = pytest.importorskip("agentic_evals")
pytestmark = pytest.mark.skipif(
    not hasattr(evals, "to_aios_evidence"),
    reason="installed agentic-evals predates AIOS evidence export (needs >=0.10.0)",
)

RUN = (
    Path(__file__).resolve().parents[2]
    / "ai-operations-spec/specification/v0.4/examples/valid/run.json"
)


def _report() -> "evals.EvaluationReport":
    suite = evals.TestSuite(
        name="support",
        version="1",
        cases=[
            evals.TestCase(id="answer", name="Grounded answer", expected_output="Paris"),
            evals.TestCase(id="wrong", name="Wrong answer", expected_output="42"),
        ],
    )
    samples = [
        evals.EvaluationSample(case_id=case_id, output=output, trace=evals.EvalTrace())
        for case_id, output in (("answer", "Paris"), ("wrong", "41"))
    ]
    return evals.evaluate_suite(suite, samples)


def _merged() -> dict:
    report = _report()
    export = evals.to_aios_evidence(
        report,
        run_id="run-001",
        targets={"answer": "step-answer", "wrong": "step-answer"},
        gate=evals.evaluate_gate(report, evals.GateConfig()),
    )
    return evals.attach_aios_evidence(json.loads(RUN.read_text(encoding="utf-8")), export)


async def _validate(artifact: dict) -> dict:
    result = await handle_call_tool("spec.validate_artifact", {"artifact": artifact})
    return json.loads(result[0].text)


async def test_merged_evals_evidence_is_aligned() -> None:
    payload = await _validate(_merged())

    assert payload["ok"], payload
    assert payload["conformance"]["aligned"] is True
    p08 = next(rule for rule in payload["conformance"]["rules"] if rule["id"] == "AIOS-0.4-P08")
    assert p08["status"] == "pass"


async def test_alignment_does_not_hide_failed_evaluations() -> None:
    merged = _merged()
    statuses = {item["id"]: item["status"] for item in merged["evidence"]}

    assert (await _validate(merged))["conformance"]["aligned"] is True
    assert statuses["run-001:evals:support:wrong:case"] == "failed"
    assert statuses["run-001:evals:support:gate"] == "failed"


async def test_orphaned_evaluation_is_cited_as_p08() -> None:
    merged = _merged()
    orphan = merged["evidence"][-1]["id"]
    merged["relationships"] = [
        rel for rel in merged["relationships"] if rel["source"]["id"] != orphan
    ]
    payload = await _validate(merged)

    assert payload["conformance"]["aligned"] is False
    assert "AIOS-0.4-P08" in {issue["rule_id"] for issue in payload["conformance"]["issues"]}
