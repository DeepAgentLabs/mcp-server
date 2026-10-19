"""Upstream schema parity and native-artifact validation regressions."""

import json
import subprocess
import sys
from copy import deepcopy
from importlib.resources import files

import pytest
from agentic_evals import (
    EvalTrace,
    EvaluationSample,
    GateConfig,
    evaluate_gate,
    evaluate_suite,
)
from agentic_evals import (
    TestCase as Case,
)
from agentic_evals import (
    TestSuite as Suite,
)

from deep_agentic_core_mcp.services.evals_contract import validate_evals_artifact


@pytest.fixture
def report():
    suite = Suite(
        name="contract", version="1", cases=[Case(id="a", name="a", expected_output="ok")]
    )
    return evaluate_suite(
        suite, [EvaluationSample(case_id="a", output="wrong", trace=EvalTrace())]
    ).model_dump(mode="json")


@pytest.mark.parametrize("name", ["evaluation-report", "gate-decision"])
def test_packaged_schemas_are_exact_upstream_contracts(name):
    # An isolated interpreter avoids MCP's legacy sibling-venv import bootstrap.
    output = subprocess.check_output(
        [
            sys.executable,
            "-I",
            "-c",
            "import json; from agentic_evals import report_schema, gate_decision_schema; "
            "print(json.dumps({'evaluation-report': report_schema(), "
            "'gate-decision': gate_decision_schema()}))",
        ],
        text=True,
    )
    resource = files("deep_agentic_core_mcp").joinpath("schemas").joinpath("evals")
    schema = json.loads(resource.joinpath(f"{name}-1.0.schema.json").read_text())
    assert schema == json.loads(output)[name]


@pytest.mark.parametrize("field", ["cases", "summary"])
def test_partial_reports_are_rejected(report, field):
    del report[field]
    with pytest.raises(ValueError, match="required"):
        validate_evals_artifact(report, "evaluation_report")


def test_nested_invalid_score_is_rejected_without_echoing_input(report):
    report["cases"][0]["scores"][0]["value"] = "SECRET_INVALID_VALUE"
    with pytest.raises(ValueError) as error:
        validate_evals_artifact(report, "evaluation_report")
    assert "/cases/0/scores/0/value" in str(error.value)
    assert "SECRET" not in str(error.value)


def test_unknown_fields_are_tolerated_without_mutation(report):
    report["future_field"] = {"$ref": "https://example.invalid/do-not-fetch"}
    report["summary"]["future_field"] = True
    report["cases"][0]["scores"][0]["future_field"] = True
    before = deepcopy(report)
    validate_evals_artifact(report, "evaluation_report")
    assert report == before


def test_unsupported_contract_and_artifact_types_are_rejected(report):
    report["schema_version"] = "2.0"
    with pytest.raises(ValueError, match="unsupported schema_version"):
        validate_evals_artifact(report, "evaluation_report")
    with pytest.raises(ValueError, match="Unsupported"):
        validate_evals_artifact({}, "unknown")


@pytest.mark.parametrize("gate", [{}, {"passed": "false", "reasons": [], "observed": {}}])
def test_invalid_gates_are_rejected(gate):
    with pytest.raises(ValueError, match="gate_decision"):
        validate_evals_artifact(gate, "gate_decision")


def test_a_structurally_valid_failed_gate_is_not_recomputed(report):
    from agentic_evals import EvaluationReport

    decision = evaluate_gate(EvaluationReport.model_validate(report), GateConfig())
    gate = decision.model_dump(mode="json")
    assert not gate["passed"]
    validate_evals_artifact(gate, "gate_decision")
    assert gate == decision.model_dump(mode="json")


@pytest.mark.asyncio
async def test_registered_mcp_validation_tool_accepts_failed_gate():
    from deep_agentic_core_mcp.server import handle_call_tool

    result = await handle_call_tool(
        "evals.validate_artifact",
        {
            "artifact_type": "gate_decision",
            "artifact": {"passed": False, "reasons": ["blocked"], "observed": {}},
        },
    )
    payload = json.loads(result[0].text)
    assert payload["ok"] is True
    assert payload["valid"] is True


@pytest.mark.parametrize("operation", ["slo_summary", "audit_report", "score_analysis"])
def test_lens_report_consumers_reject_invalid_nested_score(report, operation):
    from deep_agentic_core_mcp.adapters import agenticlens
    from deep_agentic_core_mcp.tools import lens

    if agenticlens._IMPORT_ERROR is not None:
        pytest.skip("Lens unavailable")
    report["cases"][0]["scores"][0]["value"] = 99
    result = getattr(lens, operation)({"report": report})
    assert result["ok"] is False
    assert "native Evals" in result["error"]
