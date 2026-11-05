"""Run the pinned full AIOS v0.8.0 suite against the runtime implementation.

Fixtures are vendored; no sibling checkout, network or spec test code is needed.
"""

import json
from pathlib import Path

import pytest

from deep_agentic_core_mcp.adapters import ai_operations_spec as spec_adapter

SUITE_DIR = Path(__file__).parent / "fixtures/aios-v0.8/specification/v0.6/conformance-suite"
SUITE = json.loads((SUITE_DIR / "suite.json").read_text(encoding="utf-8"))


def _outcome(payload: dict) -> tuple[str, list[str]]:
    if payload["compatibility"]["decision"] == "reject":
        return "unsupported", [payload["compatibility"]["rule_id"]]
    if payload["schema_errors"]:
        return "schema-invalid", []
    issues = payload["conformance"]["issues"]
    if issues:
        return "semantic-invalid", sorted({issue["rule_id"] for issue in issues})
    return "valid", []


@pytest.mark.parametrize("case", SUITE["cases"], ids=lambda case: case["id"])
def test_suite_case(case: dict) -> None:
    document = json.loads((SUITE_DIR / case["path"]).read_text(encoding="utf-8"))
    outcome, rules = _outcome(spec_adapter.validate_artifact(document))
    assert outcome == case["expected"]
    if outcome != "schema-invalid":
        assert rules == case["rules"]


@pytest.mark.parametrize("case", SUITE["resolution_cases"], ids=lambda c: c["id"])
def test_provenance_resolution(case: dict) -> None:
    record = json.loads((SUITE_DIR / case["record"]).read_text())
    held = {key: (SUITE_DIR / path).read_bytes() for key, path in case["subjects"].items()}
    assert spec_adapter.resolve_provenance(record, held) == case["expected"]


def test_nonfinite_json_is_not_schema_valid():
    document = json.loads((SUITE_DIR / "cases/operational-valid-signal.json").read_text())
    document["confidence"] = float("nan")
    report = spec_adapter.validate_artifact(document)
    assert not report["ok"] and report["schema_errors"]
    assert not report["semantic_checked"]


def test_process_and_resolution_rules_are_not_claimed_from_a_record_alone():
    document = json.loads((SUITE_DIR / "cases/provenance-valid-support-finding.json").read_text())
    report = spec_adapter.validate_artifact(document)
    assert report["ok"]
    assert all(
        rule["status"] == "not_evaluated"
        for rule in report["conformance"]["rules"]
        if rule["check"] in {"process", "cross_artifact"}
    )
