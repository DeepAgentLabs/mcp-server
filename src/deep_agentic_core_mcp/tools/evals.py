"""Native Evals schema validation, independent of Lens and AIOS."""

from typing import Any

from deep_agentic_core_mcp.services.evals_contract import validate_evals_artifact


def validate_artifact(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Validate a report or gate without scoring, fetching, or modifying it."""
    arguments = arguments or {}
    kind = arguments.get("artifact_type")
    if kind not in ("evaluation_report", "gate_decision") or "artifact" not in arguments:
        return {"ok": False, "error": "Provide artifact and a supported artifact_type"}
    try:
        validate_evals_artifact(arguments["artifact"], kind)
    except ValueError as exc:
        return {"ok": False, "valid": False, "error": str(exc)}
    return {"ok": True, "valid": True, "artifact_type": kind, "contract_version": "1.0"}
