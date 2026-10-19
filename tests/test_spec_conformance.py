"""Phase 3c: spec_version-routed validation and rule-cited conformance reports."""

import json
from pathlib import Path

import pytest

from deep_agentic_core_mcp.adapters import ai_operations_spec as spec_adapter
from deep_agentic_core_mcp.server import (
    handle_call_tool,
    handle_list_resources,
    handle_read_resource,
)

SPEC_ROOT = Path(__file__).resolve().parents[2] / "ai-operations-spec"
EXAMPLES = SPEC_ROOT / "specification" / "v0.4" / "examples"
REVIEW_ARTIFACTS = SPEC_ROOT / "reviews" / "artifacts"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


async def _validate(artifact: dict) -> dict:
    result = await handle_call_tool("spec.validate_artifact", {"artifact": artifact})
    return json.loads(result[0].text)


def _rule_ids(payload: dict) -> set[str]:
    return {issue["rule_id"] for issue in payload["conformance"]["issues"]}


@pytest.mark.parametrize(
    "path",
    sorted((EXAMPLES / "valid").glob("*.json")) + sorted(REVIEW_ARTIFACTS.glob("*.aios.json")),
    ids=lambda path: path.name,
)
async def test_valid_and_review_artifacts_are_aligned(path: Path) -> None:
    payload = await _validate(_load(path))

    assert payload["ok"] is True
    conformance = payload["conformance"]
    assert conformance["aligned"] is True
    assert conformance["catalog_available"] is True
    assert conformance["rules_source"] == "specification/v0.4/conformance-rules.json"
    assert conformance["summary"]["fail"] == 0
    assert payload["compatibility"]["rule_id"] == "AIOS-0.5-V02"
    assert payload["compatibility"]["decision"] == "accept_informal"


@pytest.mark.parametrize(
    ("relative", "expected"),
    [
        ("invalid/run-unknown-object-type.json", {"AIOS-0.4-P01", "AIOS-0.4-U02"}),
        ("invalid/run-unknown-relationship-type.json", {"AIOS-0.4-P01", "AIOS-0.4-U02"}),
        ("invalid/run-namespace-collision.json", {"AIOS-0.4-P01", "AIOS-0.4-U02", "AIOS-0.4-E01"}),
        ("invalid/workflow-missing-name.json", {"AIOS-0.4-P01"}),
        ("semantic-invalid/dangling-reference.json", {"AIOS-0.4-P05", "AIOS-0.4-X01"}),
        ("semantic-invalid/run-retry-merged-attempts.json", {"AIOS-0.4-P12"}),
    ],
)
async def test_invalid_examples_cite_the_violated_rules(relative: str, expected: set[str]) -> None:
    payload = await _validate(_load(EXAMPLES / relative))

    assert payload["ok"] is False
    assert payload["conformance"]["aligned"] is False
    assert _rule_ids(payload) == expected
    statuses = {rule["id"]: rule["status"] for rule in payload["conformance"]["rules"]}
    for rule_id in expected:
        assert statuses[rule_id] == "fail"


async def test_schema_invalid_runs_skip_semantic_rules() -> None:
    payload = await _validate(_load(EXAMPLES / "invalid" / "run-unknown-object-type.json"))

    assert payload["semantic_checked"] is False
    statuses = {rule["id"]: rule["status"] for rule in payload["conformance"]["rules"]}
    assert statuses["AIOS-0.4-P06"] == "not_evaluated"


async def test_process_rules_are_never_reported_as_passing() -> None:
    payload = await _validate(_load(EXAMPLES / "valid" / "run.json"))

    for rule in payload["conformance"]["rules"]:
        if rule["check"] == "process":
            assert rule["status"] == "not_evaluated", rule["id"]


async def test_report_separates_spec_rules_from_server_presentation() -> None:
    payload = await _validate(_load(EXAMPLES / "valid" / "workflow.json"))

    assert "not defined by the specification" in payload["server"]["note"]
    assert payload["claim"] == (
        "Aligned with AI Operations Specification v0.4-draft as observed on "
        f"{spec_adapter.OBSERVED_ON}."
    )
    run_only = {
        rule["id"] for rule in payload["conformance"]["rules"] if rule["status"] == "not_applicable"
    }
    assert "AIOS-0.4-P06" in run_only


async def test_workflow_references_must_be_marked_external() -> None:
    artifact = _load(EXAMPLES / "valid" / "workflow.json")
    artifact["references"] = [{"id": "run-001", "type": "run"}]

    payload = await _validate(artifact)

    assert payload["ok"] is False
    assert _rule_ids(payload) == {"AIOS-0.4-X01"}


@pytest.mark.parametrize(
    ("marker", "rule_id"),
    [("0.5-draft", "AIOS-0.5-V03"), ("1.0", "AIOS-0.5-V05"), ("0.4", "AIOS-0.5-V05")],
)
async def test_unsupported_markers_are_rejected_not_revalidated(marker: str, rule_id: str) -> None:
    artifact = {**_load(EXAMPLES / "valid" / "run.json"), "spec_version": marker}

    payload = await _validate(artifact)

    assert payload["ok"] is False
    assert payload["compatibility"]["decision"] == "reject"
    assert payload["compatibility"]["rule_id"] == rule_id
    assert payload["compatibility"]["supported_versions"] == ["0.4-draft"]
    assert "conformance" not in payload


@pytest.mark.parametrize("marker", [None, "v0.4", "1.00", 4])
async def test_missing_or_malformed_markers_are_rejected(marker: object) -> None:
    artifact = _load(EXAMPLES / "valid" / "run.json")
    if marker is None:
        artifact.pop("spec_version")
    else:
        artifact["spec_version"] = marker

    payload = await _validate(artifact)

    assert payload["ok"] is False
    assert payload["compatibility"]["decision"] == "reject"
    assert payload["compatibility"]["rule_id"] is None


def test_newer_frozen_minor_and_older_minor_cite_their_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    frozen = spec_adapter.SchemaSet(
        marker="1.1", frozen=True, documents={}, registry=spec_adapter.Registry()
    )
    monkeypatch.setitem(spec_adapter.SCHEMA_SETS, "1.1", frozen)

    assert spec_adapter.compatibility_decision("1.1")["rule_id"] == "AIOS-0.5-V01"
    assert spec_adapter.compatibility_decision("1.2")["rule_id"] == "AIOS-0.5-V04"
    assert spec_adapter.compatibility_decision("1.0")["rule_id"] == "AIOS-0.5-V06"


async def test_issues_keep_rule_ids_without_a_catalog(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(spec_adapter.SCHEMA_SETS["0.4-draft"], "rules", [])

    payload = await _validate(_load(EXAMPLES / "semantic-invalid" / "dangling-reference.json"))

    assert payload["conformance"]["catalog_available"] is False
    assert payload["conformance"]["rules"] == []
    assert _rule_ids(payload) == {"AIOS-0.4-P05", "AIOS-0.4-X01"}


async def test_catalogs_are_exposed_as_resources() -> None:
    uris = {str(resource.uri) for resource in await handle_list_resources()}
    assert {
        "resource://schemas/aiops/v0.4/workflow",
        "resource://schemas/aiops/v0.4/run",
        "resource://schemas/aiops/v0.4/common",
        "resource://specs/aiops/v0.4/conformance-rules",
        "resource://specs/aiops/v0.5/compatibility",
    } <= uris

    rules = json.loads(
        (await handle_read_resource("resource://specs/aiops/v0.4/conformance-rules"))[0].text
    )
    compatibility = json.loads(
        (await handle_read_resource("resource://specs/aiops/v0.5/compatibility"))[0].text
    )
    assert rules["spec_version"] == "0.4-draft"
    assert "0.4-draft" in compatibility["published_schema_sets"]


async def test_verify_reports_supported_versions_and_catalogs() -> None:
    verify = json.loads((await handle_call_tool("core.verify", {}))[0].text)

    spec = verify["adapters"]["ai_operations_spec"]
    assert spec["supported_versions"] == ["0.4-draft"]
    assert spec["conformance_catalog"] is True
    assert spec["compatibility_catalog"] is True


async def test_published_markers_without_a_checker_are_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(spec_adapter, "UNCHECKED_MARKERS", ["0.6-draft"])
    artifact = {**_load(EXAMPLES / "valid" / "run.json"), "spec_version": "0.6-draft"}

    payload = await _validate(artifact)

    assert payload["compatibility"]["decision"] == "reject"
    assert "no conformance checker" in payload["compatibility"]["reason"]
    assert "conformance" not in payload


def test_only_checked_markers_are_loaded() -> None:
    assert set(spec_adapter.SCHEMA_SETS) <= spec_adapter.CHECKED_MARKERS
    assert spec_adapter.probe()["published_unchecked_versions"] == sorted(
        spec_adapter.UNCHECKED_MARKERS
    )
