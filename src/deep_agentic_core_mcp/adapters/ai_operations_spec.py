"""Adapter helpers for the sibling AI Operations specification repo.

Everything normative comes from `ai-operations-spec`: the schema sets published
behind each `spec_version` marker and the version grammar
(`specification/v0.5/compatibility.json`), and the rule identifiers a
conformance report cites (`specification/v0.4/conformance-rules.json`). This
module only routes artifacts to the matching schema set, runs the checks, and
labels each issue with the rule it violates.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from deep_agentic_core_mcp.adapters import AdapterUnavailableError, ensure_repo_on_path

# Date this server's checks were last compared against the specification; cited
# in draft-alignment claims as the v0.4 conformance document requires (K01).
OBSERVED_ON = "2026-10-13"

# The v0.5 grammar, used only when the sibling checkout predates compatibility.json.
_FALLBACK_VERSION_PATTERN = r"^(0\.[1-9][0-9]*|[1-9][0-9]*\.(0|[1-9][0-9]*))(-draft)?$"
_FALLBACK_SCHEMA_SETS = {
    "0.4-draft": {
        "schema_directory": "specification/v0.4/schemas",
        "conformance_rules": "specification/v0.4/conformance-rules.json",
        "frozen": False,
    }
}

PRESENTATION_NOTE = (
    "Only the `conformance` section reports AI Operations Specification rules. "
    "`ok`, `claim`, `schema_errors`, `semantic_errors` and `server` are "
    "deep-agentic-core-mcp presentation and are not defined by the specification."
)


@dataclass
class SchemaSet:
    """The schema documents and rule catalog published behind one `spec_version`."""

    marker: str
    frozen: bool
    documents: dict[str, dict[str, Any]]
    registry: Registry
    rules: list[dict[str, Any]] = field(default_factory=list)
    rules_source: str | None = None
    claim_template: str | None = None

    @property
    def path_label(self) -> str:
        """Short label used in resource URIs, e.g. `v0.4` for `0.4-draft`."""
        return "v" + self.marker.removesuffix("-draft")


# Markers whose conformance rules this module implements (`_schema_issues` and
# `semantic_issues_for` emit AIOS-0.4-* rules for the v0.4 artifact shape). A
# schema set the specification publishes for any other marker is not loaded:
# accepting it would mislabel issues or report its rules as passing unchecked.
CHECKED_MARKERS = frozenset({"0.4-draft"})

_IMPORT_ERROR: Exception | None = None
SCHEMA_SETS: dict[str, SchemaSet] = {}
# Markers the specification publishes that this server cannot yet check.
UNCHECKED_MARKERS: list[str] = []
VERSION_PATTERN = re.compile(_FALLBACK_VERSION_PATTERN)
COMPATIBILITY: dict[str, Any] = {}
CATALOG_DOCUMENTS: dict[str, dict[str, Any]] = {}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def _load_schema_set(repo: Path, marker: str, entry: dict[str, Any]) -> SchemaSet | None:
    schema_dir = repo / entry["schema_directory"]
    documents = {path.name: _load_json(path) for path in schema_dir.glob("*.schema.json")}
    if not documents:
        return None
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in documents.values()
    )
    schema_set = SchemaSet(
        marker=marker, frozen=bool(entry.get("frozen")), documents=documents, registry=registry
    )
    rules_path = repo / entry.get("conformance_rules", "")
    if entry.get("conformance_rules") and rules_path.is_file():
        catalog = _load_json(rules_path)
        schema_set.rules = list(catalog.get("rules", []))
        schema_set.rules_source = entry["conformance_rules"]
        schema_set.claim_template = catalog.get("claim_template")
        CATALOG_DOCUMENTS[entry["conformance_rules"]] = catalog
    return schema_set


try:
    SPEC_REPO = ensure_repo_on_path("ai-operations-spec", src=False)
    compatibility_path = SPEC_REPO / "specification" / "v0.5" / "compatibility.json"
    if compatibility_path.is_file():
        COMPATIBILITY = _load_json(compatibility_path)
        CATALOG_DOCUMENTS["specification/v0.5/compatibility.json"] = COMPATIBILITY
        VERSION_PATTERN = re.compile(COMPATIBILITY["spec_version_pattern"])
    published = COMPATIBILITY.get("published_schema_sets", _FALLBACK_SCHEMA_SETS)
    for _marker, _entry in published.items():
        if _marker not in CHECKED_MARKERS:
            UNCHECKED_MARKERS.append(_marker)
            continue
        _schema_set = _load_schema_set(SPEC_REPO, _marker, _entry)
        if _schema_set is not None:
            SCHEMA_SETS[_marker] = _schema_set
    if not SCHEMA_SETS:
        raise FileNotFoundError(f"no published schema documents found under {SPEC_REPO}")
except Exception as exc:  # noqa: BLE001 - captured for core.verify/core.health reporting
    _IMPORT_ERROR = exc

# Back-compat aliases for the v0.4 set, which existing callers and tests import.
SCHEMA_DOCUMENTS: dict[str, dict[str, Any]] = (
    SCHEMA_SETS["0.4-draft"].documents if "0.4-draft" in SCHEMA_SETS else {}
)
REGISTRY: Registry = SCHEMA_SETS["0.4-draft"].registry if "0.4-draft" in SCHEMA_SETS else Registry()


def _require_available() -> None:
    if _IMPORT_ERROR is not None:
        raise AdapterUnavailableError("ai_operations_spec", _IMPORT_ERROR)


def supported_versions() -> list[str]:
    """`spec_version` markers this server holds a published schema set for."""
    return sorted(SCHEMA_SETS)


def probe() -> dict[str, Any]:
    """Report whether the ai-operations-spec schemas are reachable."""
    available = _IMPORT_ERROR is None
    return {
        "available": available,
        "version": ", ".join(supported_versions()) if available else None,
        "supported_versions": supported_versions() if available else [],
        "published_unchecked_versions": sorted(UNCHECKED_MARKERS) if available else [],
        "conformance_catalog": any(s.rules for s in SCHEMA_SETS.values()),
        "compatibility_catalog": bool(COMPATIBILITY),
        "error": None if available else str(_IMPORT_ERROR),
    }


def describe_capabilities() -> list[str]:
    """Return the MCP-visible specification capabilities."""
    return ["validate_artifact", "semantic_validate_run", "conformance_report", "version_routing"]


def claim_for(marker: str) -> str:
    """The draft-alignment claim for a marker, in the specification's claim format."""
    schema_set = SCHEMA_SETS.get(marker)
    if schema_set is not None and schema_set.claim_template:
        return schema_set.claim_template.replace("{date}", OBSERVED_ON)
    return f"Aligned with AI Operations Specification v{marker} as observed on {OBSERVED_ON}."


# Back-compat: the v0.4 claim string earlier releases exposed as a constant.
CLAIM = claim_for("0.4-draft")


# ---------------------------------------------------------------------------
# MCP resources
# ---------------------------------------------------------------------------

_SCHEMA_NAMES = {
    "workflow.schema.json": "workflow",
    "run.schema.json": "run",
    "common.schema.json": "common",
}


def _schema_resources() -> list[tuple[str, str, dict[str, Any]]]:
    resources = []
    for schema_set in SCHEMA_SETS.values():
        for filename, document in sorted(schema_set.documents.items()):
            short = _SCHEMA_NAMES.get(filename, filename.removesuffix(".schema.json"))
            uri = f"resource://schemas/aiops/{schema_set.path_label}/{short}"
            name = f"AI Operations {schema_set.path_label} {short} schema"
            resources.append((uri, name, document))
    return resources


def _catalog_resources() -> list[tuple[str, str, dict[str, Any]]]:
    resources = []
    for schema_set in SCHEMA_SETS.values():
        if schema_set.rules_source:
            resources.append(
                (
                    f"resource://specs/aiops/{schema_set.path_label}/conformance-rules",
                    f"AI Operations {schema_set.path_label} conformance rule catalog",
                    CATALOG_DOCUMENTS[schema_set.rules_source],
                )
            )
    if COMPATIBILITY:
        resources.append(
            (
                "resource://specs/aiops/v0.5/compatibility",
                "AI Operations v0.5 version compatibility catalog",
                COMPATIBILITY,
            )
        )
    return resources


def list_schema_resources() -> list[dict[str, str]]:
    """Expose loaded schemas and specification catalogs as MCP resources."""
    return [
        {"uri": uri, "name": name, "kind": "json-schema"} for uri, name, _ in _schema_resources()
    ] + [
        {"uri": uri, "name": name, "kind": "spec-catalog"} for uri, name, _ in _catalog_resources()
    ]


def schema_resource_content() -> dict[str, dict[str, Any]]:
    """Map each available schema/catalog resource's URI to its document, for resources/read."""
    return {uri: doc for uri, _name, doc in _schema_resources() + _catalog_resources()}


# ---------------------------------------------------------------------------
# Version routing (v0.5 consumer compatibility rules)
# ---------------------------------------------------------------------------


def _parse_marker(marker: str) -> tuple[int, int, bool]:
    draft = marker.endswith("-draft")
    major, minor = marker.removesuffix("-draft").split(".")
    return int(major), int(minor), draft


def compatibility_decision(marker: Any) -> dict[str, Any]:
    """Decide how to consume an artifact declaring `marker`, per the v0.5 table.

    A supported marker validates against its own schema set (V01/V02). Every
    unsupported marker is rejected: each remaining row requires validating
    against the schema the artifact itself names, and this server holds none
    for it. The cited rule identifies which row applies.
    """
    supported = supported_versions()
    base: dict[str, Any] = {"spec_version": marker, "supported_versions": supported}
    if not isinstance(marker, str):
        return {
            **base,
            "decision": "reject",
            "rule_id": None,
            "reason": "artifact does not declare a spec_version string",
        }
    if not VERSION_PATTERN.match(marker):
        return {
            **base,
            "decision": "reject",
            "rule_id": None,
            "reason": "spec_version does not match the v0.5 version-marker grammar",
        }
    if marker in SCHEMA_SETS:
        frozen = SCHEMA_SETS[marker].frozen
        return {
            **base,
            "decision": "accept" if frozen else "accept_informal",
            "rule_id": "AIOS-0.5-V01" if frozen else "AIOS-0.5-V02",
            "reason": (
                "validated against the schema set published for this exact marker"
                + ("" if frozen else "; draft alignment only, not stable conformance")
            ),
        }

    major, minor, draft = _parse_marker(marker)
    rule_id = "AIOS-0.5-V03"
    if not draft:
        frozen_supported = [_parse_marker(m) for m in supported if not m.endswith("-draft")]
        same_major = [m for m in frozen_supported if m[0] == major]
        if not same_major:
            rule_id = "AIOS-0.5-V05"
        elif minor > max(m[1] for m in same_major):
            rule_id = "AIOS-0.5-V04"
        else:
            rule_id = "AIOS-0.5-V06"
    reason = (
        "the specification publishes a schema set for this spec_version, but this server "
        "version has no conformance checker for it yet; upgrade deep-agentic-core-mcp"
        if marker in UNCHECKED_MARKERS
        else "no schema set is published for this spec_version"
    )
    return {
        **base,
        "decision": "reject",
        "rule_id": rule_id,
        "reason": reason + "; the artifact must be validated against the schema its own "
        "marker names, never a different version's",
    }


# ---------------------------------------------------------------------------
# Validation and conformance reporting
# ---------------------------------------------------------------------------

Issue = tuple[str, str]  # (rule_id, message)


def validate_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    """Validate an artifact against the schema set its `spec_version` names.

    Returns a rule-cited `conformance` report alongside the server's existing
    presentation fields (`ok`, `schema_errors`, `semantic_errors`, ...).
    """
    _require_available()
    if not isinstance(artifact, dict):
        return {"ok": False, "errors": ["artifact must be a JSON object"]}
    artifact_type = artifact.get("artifact_type")
    compatibility = compatibility_decision(artifact.get("spec_version"))
    schema_set = SCHEMA_SETS.get(str(artifact.get("spec_version")))
    claim = claim_for(schema_set.marker if schema_set else "0.4-draft")

    if artifact_type not in {"workflow", "run"}:
        if compatibility["decision"] != "reject":
            # The marker is supported, but its schema set publishes no schema for
            # this artifact type; never fall back to another marker's (AIOS-0.5-V03).
            compatibility = {
                **compatibility,
                "decision": "reject",
                "rule_id": "AIOS-0.5-V03",
                "reason": f"no schema for artifact_type {artifact_type!r} is published "
                "behind this spec_version; the artifact must be validated against the "
                "schema its own marker names, never a different version's",
            }
        return {
            "ok": False,
            "claim": claim,
            "compatibility": compatibility,
            "errors": ["artifact_type must be either 'workflow' or 'run'"],
        }
    if compatibility["decision"] == "reject" or schema_set is None:
        return {
            "ok": False,
            "claim": claim,
            "artifact_type": artifact_type,
            "spec_version": artifact.get("spec_version"),
            "compatibility": compatibility,
            "errors": [compatibility["reason"]],
        }

    schema = schema_set.documents[f"{artifact_type}.schema.json"]
    validator = Draft202012Validator(
        schema, registry=schema_set.registry, format_checker=FormatChecker()
    )
    schema_errors = sorted(validator.iter_errors(artifact), key=lambda err: list(err.path))
    schema_issues = [issue for error in schema_errors for issue in _schema_issues(error)]
    # Semantic checks assume a structurally valid artifact; skip them otherwise
    # rather than crash on a missing field the schema already reported.
    semantic_issues: list[Issue] = [] if schema_errors else semantic_issues_for(artifact)

    return {
        "ok": not schema_errors and not semantic_issues,
        "claim": claim,
        "artifact_type": artifact_type,
        "spec_version": schema_set.marker,
        "compatibility": compatibility,
        "schema_errors": [_format_schema_error(error) for error in schema_errors],
        "semantic_errors": [message for _rule, message in semantic_issues],
        "semantic_checked": not schema_errors,
        "conformance": _conformance_report(
            schema_set, artifact_type, schema_issues, semantic_issues, not schema_errors
        ),
        "server": {"note": PRESENTATION_NOTE},
    }


def _schema_issues(error: Any) -> list[Issue]:
    """Map one schema error to the rules it violates (always P01, plus any narrower rule)."""
    message = _format_schema_error(error)
    text = f"{message['path']}: {message['message']}"
    issues: list[Issue] = [("AIOS-0.4-P01", text)]
    path = [str(part) for part in error.absolute_path]
    # `anyOf` covers "canonical value or namespaced extension name" (e.g. event_name),
    # so look at which alternatives failed as well as the error itself.
    validators = {error.validator} | {ctx.validator for ctx in error.context or []}
    if "enum" in validators:
        issues.append(("AIOS-0.4-U02", text))
    if ("extensions" in path and error.validator in {"propertyNames", "pattern"}) or (
        error.validator == "anyOf" and "pattern" in validators
    ):
        issues.append(("AIOS-0.4-E01", text))
    return issues


def _conformance_report(
    schema_set: SchemaSet,
    artifact_type: str,
    schema_issues: list[Issue],
    semantic_issues: list[Issue],
    semantic_checked: bool,
) -> dict[str, Any]:
    issues = [{"rule_id": rule, "message": message} for rule, message in schema_issues]
    issues += [{"rule_id": rule, "message": message} for rule, message in semantic_issues]
    failing = {issue["rule_id"] for issue in issues}
    rules = []
    for rule in schema_set.rules:
        if artifact_type not in rule.get("applies_to", []):
            status = "not_applicable"
        elif rule["check"] == "process" or (rule["check"] == "semantic" and not semantic_checked):
            status = "not_evaluated"
        else:
            status = "fail" if rule["id"] in failing else "pass"
        rules.append(
            {
                "id": rule["id"],
                "role": rule["role"],
                "level": rule["level"],
                "check": rule["check"],
                "status": status,
                "requirement": rule["requirement"],
            }
        )
    evaluated = [rule for rule in rules if rule["status"] in {"pass", "fail"}]
    return {
        "spec_version": schema_set.marker,
        "rules_source": schema_set.rules_source,
        "catalog_available": bool(schema_set.rules),
        # Alignment needs both schema and semantic validation (AIOS-0.4-C01).
        "aligned": not issues and semantic_checked,
        "summary": {
            "pass": sum(rule["status"] == "pass" for rule in rules),
            "fail": sum(rule["status"] == "fail" for rule in rules),
            "not_evaluated": sum(rule["status"] == "not_evaluated" for rule in rules),
            "not_applicable": sum(rule["status"] == "not_applicable" for rule in rules),
            "evaluated": len(evaluated),
        },
        "rules": rules,
        "issues": issues,
    }


def semantic_validate_run(artifact: dict[str, Any]) -> list[str]:
    """Run the v0.4 draft semantic checks for run artifacts (messages only)."""
    if artifact.get("artifact_type") != "run":
        return []
    return [message for _rule, message in semantic_issues_for(artifact)]


def semantic_issues_for(artifact: dict[str, Any]) -> list[Issue]:
    """Run the v0.4 semantic checks, labeling each issue with its conformance rule."""
    if artifact.get("artifact_type") == "workflow":
        return _workflow_reference_issues(artifact)
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

    issues: list[Issue] = []
    ids = [object_id for object_id, _ in objects]
    if len(ids) != len(set(ids)):
        issues.append(("AIOS-0.4-P02", "object identities must be unique within a Run artifact"))

    object_types = dict(objects)
    relationships = artifact.get("relationships", [])
    relationship_ids = [item["id"] for item in relationships]
    if len(relationship_ids) != len(set(relationship_ids)):
        issues.append(("AIOS-0.4-P03", "relationship identities must be unique"))

    event_ids = [item["event_id"] for item in artifact.get("events", [])]
    if len(event_ids) != len(set(event_ids)):
        issues.append(("AIOS-0.4-P03", "event identities must be unique"))

    if artifact.get("ended_at"):
        started = datetime.fromisoformat(artifact["started_at"].replace("Z", "+00:00"))
        ended = datetime.fromisoformat(artifact["ended_at"].replace("Z", "+00:00"))
        if ended < started:
            issues.append(("AIOS-0.4-P04", "ended_at must not precede started_at"))
    for step in artifact.get("steps", []):
        if step.get("started_at") and step.get("ended_at"):
            step_started = datetime.fromisoformat(step["started_at"].replace("Z", "+00:00"))
            step_ended = datetime.fromisoformat(step["ended_at"].replace("Z", "+00:00"))
            if step_ended < step_started:
                issues.append(
                    ("AIOS-0.4-P04", f"Step {step['id']} ended_at must not precede started_at")
                )

    for relationship in relationships:
        source = relationship["source"]
        target = relationship["target"]
        if source["id"] == target["id"]:
            issues.append(
                ("AIOS-0.4-P11", f"{relationship['id']} cannot relate an object to itself")
            )
        for endpoint in (source, target):
            if endpoint.get("external"):
                continue
            actual_type = object_types.get(endpoint["id"])
            if actual_type is None:
                message = f"{relationship['id']} references missing object {endpoint['id']}"
                issues.append(("AIOS-0.4-P05", message))
                issues.append(("AIOS-0.4-X01", f"{message} without external: true"))
            elif actual_type != endpoint["type"]:
                issues.append(
                    (
                        "AIOS-0.4-P05",
                        f"{relationship['id']} declares the wrong type for {endpoint['id']}",
                    )
                )

    for step in artifact.get("steps", []):
        contains = _count_edges(
            relationships, "contains", source_id=artifact["id"], target_id=step["id"]
        )
        if contains != 1:
            issues.append(
                ("AIOS-0.4-P06", f"Step {step['id']} must be contained by its Run exactly once")
            )
    for occurrence in artifact.get("occurrences", []):
        if _count_edges(relationships, "observed-in", source_id=occurrence["id"]) != 1:
            issues.append(
                (
                    "AIOS-0.4-P07",
                    f"Occurrence {occurrence['id']} must be observed in exactly one Step",
                )
            )
    for evidence in artifact.get("evidence", []):
        if (
            evidence["type"] == "evaluation"
            and _count_edges(relationships, "evaluates", source_id=evidence["id"]) < 1
        ):
            issues.append(("AIOS-0.4-P08", f"Evaluation {evidence['id']} must identify a target"))

    workflow_id = artifact.get("workflow_id")
    if workflow_id and not any(
        item["type"] == "run-of"
        and item["source"]["id"] == artifact["id"]
        and item["target"]["id"] == workflow_id
        for item in relationships
    ):
        issues.append(
            ("AIOS-0.4-P09", "workflow_id must be supported by a matching run-of relationship")
        )

    for event in artifact.get("events", []):
        if object_types.get(event["object_id"]) != event["object_type"]:
            issues.append(
                (
                    "AIOS-0.4-P10",
                    f"Event {event['event_id']} must target an object of its declared type",
                )
            )

    issues.extend(_retry_issues(artifact, relationships))

    for edge_types in ({"parent-of"}, {"caused", "follows", "depends-on"}):
        graph: dict[str, set[str]] = {}
        for item in relationships:
            if item["type"] in edge_types:
                graph.setdefault(item["source"]["id"], set()).add(item["target"]["id"])
        if _has_cycle(graph):
            issues.append(
                ("AIOS-0.4-P11", f"relationship graph {sorted(edge_types)} must be acyclic")
            )

    return issues


def _workflow_reference_issues(artifact: dict[str, Any]) -> list[Issue]:
    """A Workflow definition holds no runtime objects, so every reference is external."""
    return [
        (
            "AIOS-0.4-X01",
            f"reference {reference.get('id')} points outside the Workflow artifact "
            "without external: true",
        )
        for reference in artifact.get("references", [])
        if not reference.get("external")
    ]


def _retry_issues(artifact: dict[str, Any], relationships: list[dict[str, Any]]) -> list[Issue]:
    """Rule P12: distinct identities per retry attempt, each linked to the prior attempt."""
    issues: list[Issue] = []
    occurrence_by_id = {item["id"]: item for item in artifact.get("occurrences", [])}
    evidence_by_id = {item["id"]: item for item in artifact.get("evidence", [])}

    attempt_signal_targets: dict[str, list[int]] = {}
    for relationship in relationships:
        if relationship["type"] != "signals-on":
            continue
        source = evidence_by_id.get(relationship["source"]["id"])
        if not source or source.get("type") != "reliability_event":
            continue
        attempt = source.get("attributes", {}).get("attempt")
        if not isinstance(attempt, int):
            continue
        target_id = relationship["target"]["id"]
        attempt_signal_targets.setdefault(target_id, []).append(attempt)
        occurrence = occurrence_by_id.get(target_id)
        if occurrence:
            occurrence_attempt = occurrence.get("attributes", {}).get("attempt")
            if isinstance(occurrence_attempt, int) and occurrence_attempt != attempt:
                issues.append(
                    (
                        "AIOS-0.4-P12",
                        f"Retry evidence {source['id']} must target attempt {attempt}, "
                        f"not occurrence attempt {occurrence_attempt}",
                    )
                )
    for target_id, attempts in attempt_signal_targets.items():
        if len(attempts) > 1:
            ordered = ", ".join(str(attempt) for attempt in sorted(attempts))
            issues.append(
                (
                    "AIOS-0.4-P12",
                    f"Retry attempts {ordered} must not all signal the same occurrence {target_id}",
                )
            )

    retry_groups: dict[str, dict[int, str]] = {}
    for occurrence in artifact.get("occurrences", []):
        attributes = occurrence.get("attributes", {})
        activity = attributes.get("logical_activity_id")
        attempt = attributes.get("attempt")
        if not isinstance(activity, str) or not isinstance(attempt, int):
            continue
        group = retry_groups.setdefault(activity, {})
        if attempt in group:
            message = f"Retry activity {activity} duplicates attempt {attempt}"
            issues.append(("AIOS-0.4-P12", message))
            continue
        group[attempt] = occurrence["id"]
    for activity, attempt_ids in retry_groups.items():
        ordered_attempts = sorted(attempt_ids.items())
        for (_attempt, source_id), (next_attempt, target_id) in zip(
            ordered_attempts, ordered_attempts[1:], strict=False
        ):
            linked = _count_edges(
                relationships, "follows", source_id=source_id, target_id=target_id
            ) or _count_edges(relationships, "caused", source_id=source_id, target_id=target_id)
            if not linked:
                issues.append(
                    (
                        "AIOS-0.4-P12",
                        f"Retry activity {activity} must link attempt {_attempt} to attempt "
                        f"{next_attempt}",
                    )
                )
    return issues


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
