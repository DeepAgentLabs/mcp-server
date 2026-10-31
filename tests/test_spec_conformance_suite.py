"""Run the AIOS v0.6.1 portable conformance suite against spec.validate_artifact.

The suite lives in the sibling ai-operations-spec checkout. Cases whose marker
this server checks must match the expected outcome and rule citations; every
other case must be rejected under AIOS-0.5-V03 rather than validated.
"""

import json
from pathlib import Path

import pytest

from deep_agentic_core_mcp.adapters import ai_operations_spec as spec_adapter

SUITE_DIR = (
    Path(__file__).resolve().parents[2]
    / "ai-operations-spec"
    / "specification"
    / "v0.6"
    / "conformance-suite"
)
SUITE = (
    json.loads((SUITE_DIR / "suite.json").read_text(encoding="utf-8"))
    if (SUITE_DIR / "suite.json").is_file()
    else {"cases": []}
)
pytestmark = pytest.mark.skipif(not SUITE["cases"], reason="AIOS conformance suite not checked out")


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
    if (
        document.get("spec_version") not in spec_adapter.SCHEMA_SETS
        and case["expected"] != "unsupported"
    ):
        assert (outcome, rules) == ("unsupported", ["AIOS-0.5-V03"])
        return
    assert outcome == case["expected"]
    if outcome != "schema-invalid":
        assert rules == case["rules"]
