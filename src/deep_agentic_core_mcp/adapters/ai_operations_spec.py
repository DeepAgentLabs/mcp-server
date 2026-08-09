"""Adapter helpers for the sibling AI Operations specification repo."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from deep_agentic_core_mcp.adapters import AdapterUnavailableError, ensure_repo_on_path

CLAIM = "Aligned with AI Operations Specification v0.4-draft as observed on 2026-08-07."

_IMPORT_ERROR: Exception | None = None
SCHEMA_DOCUMENTS: dict[str, dict[str, Any]] = {}
REGISTRY: Registry = Registry()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


try:
    SPEC_REPO = ensure_repo_on_path("ai-operations-spec", src=False)
    SPEC_V04_DIR = SPEC_REPO / "specification" / "v0.4"
    SCHEMA_DIR = SPEC_V04_DIR / "schemas"
    SCHEMA_DOCUMENTS = {path.name: _load_json(path) for path in SCHEMA_DIR.glob("*.schema.json")}
    if not SCHEMA_DOCUMENTS:
        raise FileNotFoundError(f"no v0.4 schema documents found under {SCHEMA_DIR}")
    REGISTRY = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in SCHEMA_DOCUMENTS.values()
    )
except Exception as exc:  # noqa: BLE001 - captured for core.verify/core.health reporting
    _IMPORT_ERROR = exc


def _require_available() -> None:
    if _IMPORT_ERROR is not None:
        raise AdapterUnavailableError("ai_operations_spec", _IMPORT_ERROR)


def probe() -> dict[str, Any]:
    """Report whether the ai-operations-spec schemas are reachable."""
    return {
        "available": _IMPORT_ERROR is None,
        "version": "v0.4" if _IMPORT_ERROR is None else None,
        "error": None if _IMPORT_ERROR is None else str(_IMPORT_ERROR),
    }


def describe_capabilities() -> list[str]:
    """Return the MCP-visible specification capabilities."""
    return ["validate_artifact", "semantic_validate_run"]


# Single source of truth for schema-file -> MCP resource mapping, so the
# advertised resource list (`list_schema_resources`) and its actual content
# (`schema_resource_content`) can never drift out of sync with each other or
# with what's really in `SCHEMA_DOCUMENTS`. Both derive from this and skip
# any file that isn't loaded (e.g. because the sibling repo is unavailable),
# rather than assuming all three are always present.
_SCHEMA_RESOURCES: dict[str, tuple[str, str]] = {
    "workflow.schema.json": (
        "resource://schemas/aiops/v0.4/workflow",
        "AI Operations v0.4 workflow schema",
    ),
    "run.schema.json": (
        "resource://schemas/aiops/v0.4/run",
        "AI Operations v0.4 run schema",
    ),
    "common.schema.json": (
        "resource://schemas/aiops/v0.4/common",
        "AI Operations v0.4 common schema",
    ),
}


def list_schema_resources() -> list[dict[str, str]]:
    """Expose the draft schema assets as MCP resources - only those actually loaded."""
    return [
        {"uri": uri, "name": name, "kind": "json-schema"}
        for filename, (uri, name) in _SCHEMA_RESOURCES.items()
        if filename in SCHEMA_DOCUMENTS
    ]


def schema_resource_content() -> dict[str, dict[str, Any]]:
    """Map each available schema resource's URI to its document, for resources/read."""
    return {
        uri: SCHEMA_DOCUMENTS[filename]
        for filename, (uri, _name) in _SCHEMA_RESOURCES.items()
        if filename in SCHEMA_DOCUMENTS
    }


def validate_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate a draft workflow or run artifact structurally and semantically."""
    _require_available()
    artifact_type = artifact.get("artifact_type")
    if artifact_type not in {"workflow", "run"}:
        return {
            "ok": False,
            "claim": CLAIM,
            "errors": ["artifact_type must be either 'workflow' or 'run'"],
        }

    schema = SCHEMA_DOCUMENTS[f"{artifact_type}.schema.json"]
    validator = Draft202012Validator(schema, registry=REGISTRY, format_checker=FormatChecker())
    schema_errors = sorted(validator.iter_errors(artifact), key=lambda err: list(err.path))
    semantic_errors = semantic_validate_run(artifact) if artifact_type == "run" else []

    return {
        "ok": not schema_errors and not semantic_errors,
        "claim": CLAIM,
        "artifact_type": artifact_type,
        "schema_errors": [_format_schema_error(error) for error in schema_errors],
        "semantic_errors": semantic_errors,
    }


def semantic_validate_run(artifact: dict[str, Any]) -> list[str]:
    """Run the v0.4 draft semantic checks for run artifacts."""
    if artifact.get("artifact_type") != "run":
        return []

    objects: list[tuple[str, str]] = [(artifact["id"], "run")]
    groups = [
        ("requests", "request"),
        ("steps", "step"),
        ("agents", "agent"),
        ("incidents", "incident"),
    ]
    for key, object_type in groups:
        objects.extend((item["id"], object_type) for item in artifact.get(key, []))
    objects.extend((item["id"], item["type"]) for item in artifact.get("occurrences", []))
    objects.extend((item["id"], item["type"]) for item in artifact.get("evidence", []))

    errors: list[str] = []
    ids = [object_id for object_id, _ in objects]
    if len(ids) != len(set(ids)):
        errors.append("object identities must be unique within a Run artifact")

    object_types = dict(objects)
    relationships = artifact.get("relationships", [])
    relationship_ids = [item["id"] for item in relationships]
    if len(relationship_ids) != len(set(relationship_ids)):
        errors.append("relationship identities must be unique")

    event_ids = [item["event_id"] for item in artifact.get("events", [])]
    if len(event_ids) != len(set(event_ids)):
        errors.append("event identities must be unique")

    if artifact.get("ended_at"):
        started = datetime.fromisoformat(artifact["started_at"].replace("Z", "+00:00"))
        ended = datetime.fromisoformat(artifact["ended_at"].replace("Z", "+00:00"))
        if ended < started:
            errors.append("ended_at must not precede started_at")

    for relationship in relationships:
        source = relationship["source"]
        target = relationship["target"]
        if source["id"] == target["id"]:
            errors.append(f"{relationship['id']} cannot relate an object to itself")
        for endpoint in (source, target):
            if endpoint.get("external"):
                continue
            actual_type = object_types.get(endpoint["id"])
            if actual_type is None:
                errors.append(f"{relationship['id']} references missing object {endpoint['id']}")
            elif actual_type != endpoint["type"]:
                errors.append(f"{relationship['id']} declares the wrong type for {endpoint['id']}")

    for step in artifact.get("steps", []):
        contains = _count_edges(
            relationships, "contains", source_id=artifact["id"], target_id=step["id"]
        )
        if contains != 1:
            errors.append(f"Step {step['id']} must be contained by its Run exactly once")
    for occurrence in artifact.get("occurrences", []):
        if _count_edges(relationships, "observed-in", source_id=occurrence["id"]) != 1:
            errors.append(f"Occurrence {occurrence['id']} must be observed in exactly one Step")
    for evidence in artifact.get("evidence", []):
        if (
            evidence["type"] == "evaluation"
            and _count_edges(relationships, "evaluates", source_id=evidence["id"]) < 1
        ):
            errors.append(f"Evaluation {evidence['id']} must identify a target")

    workflow_id = artifact.get("workflow_id")
    if workflow_id and not any(
        item["type"] == "run-of"
        and item["source"]["id"] == artifact["id"]
        and item["target"]["id"] == workflow_id
        for item in relationships
    ):
        errors.append("workflow_id must be supported by a matching run-of relationship")

    for event in artifact.get("events", []):
        if object_types.get(event["object_id"]) != event["object_type"]:
            errors.append(f"Event {event['event_id']} must target an object of its declared type")

    for edge_types in ({"parent-of"}, {"caused", "follows", "depends-on"}):
        graph: dict[str, set[str]] = {}
        for item in relationships:
            if item["type"] in edge_types:
                graph.setdefault(item["source"]["id"], set()).add(item["target"]["id"])
        if _has_cycle(graph):
            errors.append(f"relationship graph {sorted(edge_types)} must be acyclic")

    return errors


def _count_edges(
    relationships: list[dict[str, Any]],
    edge_type: str,
    *,
    source_id: str | None = None,
    target_id: str | None = None,
) -> int:
    return sum(
        item["type"] == edge_type
        and (source_id is None or item["source"]["id"] == source_id)
        and (target_id is None or item["target"]["id"] == target_id)
        for item in relationships
    )


def _has_cycle(graph: dict[str, set[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        cycle = any(visit(target) for target in graph.get(node, set()))
        visiting.remove(node)
        visited.add(node)
        return cycle

    return any(visit(node) for node in list(graph))


def _format_schema_error(error: Any) -> dict[str, Any]:
    location = "$"
    if error.path:
        suffix = ".".join(str(part) for part in error.path)
        location = f"$.{suffix}"
    return {"path": location, "message": error.message}
