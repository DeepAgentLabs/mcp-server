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
import uuid
from datetime import datetime, timezone
from typing import Any

SCHEMA = "mcp.access-decision.v1"
EVENTS = ("dispatch", "completion", "denial", "revocation_acknowledged")

logger = logging.getLogger("deep_agentic_core_mcp.access")


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
    logger.info(json.dumps(evidence, sort_keys=True))
    return evidence
