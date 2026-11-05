"""Correlated hosted access evidence: dispatch, completion, denial, revocation.

Records are MCP-local (`mcp.access-decision.v1`), not AIOS artifacts; a shared
authority/evidence format belongs in ai-operations-spec first. Every record of
one tool call shares a `correlation_id` so Tower, or any log consumer, can join
a denial or revocation acknowledgement to the call it stopped. Records go to the
`deep_agentic_core_mcp.access` logger as one JSON object per line and never
include keys, key digests or tool arguments.
"""

from __future__ import annotations

import json
import logging
import sys
import uuid
from datetime import datetime, timezone
from typing import Any

SCHEMA = "mcp.access-decision.v1"
EVENTS = ("dispatch", "completion", "denial", "revocation_acknowledged")

logger = logging.getLogger("deep_agentic_core_mcp.access")


def install_default_handler() -> None:
    """Emit evidence as JSON lines on stdout unless the host configured the logger.

    Called by the hosted entrypoint: without a handler, Python drops INFO records.
    """
    if logger.handlers:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def new_correlation_id() -> str:
    return str(uuid.uuid4())


def record(
    event: str,
    *,
    correlation_id: str,
    user: str,
    tool: str,
    task_id: str | None = None,
    reason: str | None = None,
    outcome: str | None = None,
) -> dict[str, Any]:
    """Build and log one evidence record."""
    if event not in EVENTS:
        raise ValueError(f"Unknown access evidence event: {event}")
    evidence: dict[str, Any] = {
        "schema": SCHEMA,
        "event": event,
        "decision": "deny" if event in ("denial", "revocation_acknowledged") else "allow",
        "correlation_id": correlation_id,
        "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "subject": user,
        "tool": tool,
        "task_id": task_id,
    }
    if reason is not None:
        evidence["reason"] = reason
    if outcome is not None:
        evidence["outcome"] = outcome
    evidence["extensions"] = {
        "io.deepagentlabs.access": {
            "format": "access/1",
            "event_id": new_correlation_id(),
            "producer": "deep-agentic-core-mcp",
            "subject": user,
            "task_id": task_id,
            "correlation_id": correlation_id,
            "occurred_at": evidence["recorded_at"],
            "kind": {"dispatch": "dispatched", "completion": "completed", "denial": "denied"}.get(
                event, event
            ),
            "tool": tool,
            **({"reason": reason} if reason is not None else {}),
            **({"outcome": outcome} if outcome is not None else {}),
        }
    }
    logger.info(json.dumps(evidence, sort_keys=True))
    return evidence


def export_audit_event(
    evidence: dict[str, Any],
    *,
    target: dict[str, Any],
    created_at: datetime,
    public_actor_id: str | None = None,
) -> dict[str, Any]:
    """Project a native access observation without arguments, reasons or credentials.

    Callers provide a public target and may provide a public actor pseudonym.
    The source remains authoritative; this projection never grants tool access.
    """
    from deep_agentic_core_mcp import __version__
    from deep_agentic_core_mcp.services._aios import identifier, reference, timestamp

    if evidence.get("schema") != SCHEMA or evidence.get("event") not in EVENTS:
        raise ValueError("A native MCP access-decision observation is required")
    native_extension = evidence.get("extensions", {}).get("io.deepagentlabs.access", {})
    source_id = identifier(native_extension.get("event_id"))
    observed = datetime.fromisoformat(str(evidence["recorded_at"]).upper().replace("Z", "+00:00"))
    occurred_at = timestamp(observed)
    recorded_at = timestamp(created_at)
    if created_at < observed:
        raise ValueError("Recording time cannot precede occurrence")
    event = evidence["event"]
    native_outcome = evidence.get("outcome")
    if native_outcome is not None and (not isinstance(native_outcome, str) or not native_outcome):
        raise ValueError("A native completion outcome must be a nonempty string")
    outcome = {"dispatch": "started", "denial": "denied", "revocation_acknowledged": "denied"}.get(
        event
    )
    if outcome is None:
        outcome = {"ok": "succeeded", "error": "failed"}.get(native_outcome or "", "unknown")
    return {
        "spec_version": "0.8-draft",
        "artifact_type": "audit_event",
        "id": f"mcp:audit:{source_id}",
        "created_at": recorded_at,
        "producer": {"name": "deep-agentic-core-mcp", "version": __version__},
        "source": {
            "id": "native-access",
            "producer": "deep-agentic-core-mcp",
            "artifact_id": source_id,
            "format": SCHEMA,
        },
        "occurred_at": occurred_at,
        "actor": {"kind": "service", "id": identifier(public_actor_id)}
        if public_actor_id is not None
        else {"kind": "unknown"},
        "action": f"mcp.{event}",
        "target": reference(target),
        "outcome": outcome,
        "native_outcome": {"format": SCHEMA, "value": evidence.get("outcome") or event},
        "correlation_id": identifier(evidence["correlation_id"]),
        "causal_event_ids": [],
    }
