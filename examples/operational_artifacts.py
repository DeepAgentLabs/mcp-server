"""Offline native-to-AIOS projection; grants no authority or stable conformance."""

import json
from datetime import datetime, timezone

from deep_agentic_core_mcp.services.access_evidence import export_audit_event, record

native = record("denial", correlation_id="call-1", user="public-service", tool="lookup")
target = {"id": "target", "producer": "example", "artifact_id": "lookup", "format": "mcp.tool"}
print(
    json.dumps(
        export_audit_event(native, target=target, created_at=datetime.now(timezone.utc)), indent=2
    )
)
