"""Phase 3a: every lens.analyze_workflow finding carries source provenance."""

import json
from pathlib import Path

from deep_agentic_core_mcp.adapters.agenticlens import artifact_digest
from deep_agentic_core_mcp.server import handle_call_tool

# The example artifact used by examples/phase3_walkthrough.py, so the walkthrough
# can never drift from what these tests prove.
PROVENANCE_WORKFLOW = json.loads(
    (Path(__file__).resolve().parents[1] / "examples" / "provenance_workflow.json").read_text(
        encoding="utf-8"
    )
)


async def _analyze(artifact: dict) -> dict:
    result = await handle_call_tool(
        "lens.analyze_workflow", {"artifact": artifact, "session_id": "provenance"}
    )
    return json.loads(result[0].text)


async def test_every_finding_resolves_to_artifact_step_and_spans() -> None:
    payload = await _analyze(PROVENANCE_WORKFLOW)

    assert payload["ok"] is True
    assert payload["recommendation_count"] >= 3
    step_ids = {step["id"] for step in PROVENANCE_WORKFLOW["steps"]}
    for recommendation in payload["recommendations"]:
        provenance = recommendation["provenance"]
        assert provenance["resolved"] is True, recommendation["title"]
        assert provenance["artifact"] == {
            "workflow_id": "wf-provenance",
            "workflow_name": "Provenance workflow",
            "digest": artifact_digest(PROVENANCE_WORKFLOW),
        }
        assert provenance["step"]["id"] in step_ids
        assert provenance["step"]["id_in_artifact"] is True
        assert provenance["span_ids"] == [provenance["step"]["id"]]
        assert provenance["producer"]["name"] == "agenticlens"
    summary = payload["provenance_summary"]
    assert summary["findings"] == summary["resolved"] == payload["recommendation_count"]
    assert summary["unresolved_titles"] == []


async def test_chaos_finding_cites_its_source_event() -> None:
    payload = await _analyze(PROVENANCE_WORKFLOW)

    chaos = next(r for r in payload["recommendations"] if r["optimization_type"] == "resilience")
    assert chaos["provenance"]["step"]["name"] == "Answer"
    assert chaos["provenance"]["evidence_sources"] == ["workflow.chaos_event"]
    assert chaos["evidence"][0]["details"]["chaos_event_id"] == "chaos-1"


async def test_digest_is_stable_and_input_sensitive() -> None:
    first = await _analyze(PROVENANCE_WORKFLOW)
    second = await _analyze(dict(reversed(list(PROVENANCE_WORKFLOW.items()))))
    changed = await _analyze({**PROVENANCE_WORKFLOW, "name": "Renamed"})

    digest = first["provenance_summary"]["artifact"]["digest"]
    assert digest.startswith("sha256:")
    assert second["provenance_summary"]["artifact"]["digest"] == digest
    assert changed["provenance_summary"]["artifact"]["digest"] != digest


async def test_generated_ids_are_not_presented_as_artifact_ids() -> None:
    artifact = {
        "name": "No ids",
        "start_time": "2026-10-13T12:00:00Z",
        "steps": [
            {
                "name": "Retriever",
                "type": "retriever",
                "metrics": {"total_tokens": 120},
                "metadata": {"chunk_count": 12, "avg_tokens_per_chunk": 50},
            }
        ],
    }
    payload = await _analyze(artifact)

    provenance = payload["recommendations"][0]["provenance"]
    assert provenance["artifact"]["workflow_id"] is None
    assert provenance["step"]["index"] == 0
    assert provenance["step"]["id_in_artifact"] is False
    # A generated ID cannot be traced back to the input, so the finding is unresolved.
    assert provenance["resolved"] is False
    assert payload["provenance_summary"]["resolved"] == 0
