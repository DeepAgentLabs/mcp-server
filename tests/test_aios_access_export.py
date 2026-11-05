from datetime import datetime, timedelta, timezone

import pytest

from aios08_helpers import assert_schema
from deep_agentic_core_mcp.services.access_evidence import export_audit_event, record

TARGET = {"id": "target", "producer": "host", "artifact_id": "tool", "format": "mcp.tool"}


@pytest.mark.parametrize(
    "event,outcome,expected",
    [
        ("dispatch", None, "started"),
        ("denial", None, "denied"),
        ("revocation_acknowledged", None, "denied"),
        ("completion", "ok", "succeeded"),
        ("completion", "error", "failed"),
        ("completion", None, "unknown"),
    ],
)
def test_access_projection_preserves_native_evidence(event, outcome, expected):
    native = record(
        event,
        correlation_id="call-1",
        user="private-user",
        tool="private-tool",
        reason="secret",
        outcome=outcome,
    )
    doc = export_audit_event(native, target=TARGET, created_at=datetime.now(timezone.utc))
    assert_schema(doc)
    assert doc["outcome"] == expected and doc["correlation_id"] == "call-1"
    assert (
        doc["source"]["artifact_id"] == native["extensions"]["io.deepagentlabs.access"]["event_id"]
    )
    assert "secret" not in str(doc) and "private" not in str(doc)


def test_source_id_and_observation_time_are_required():
    native = record("dispatch", correlation_id="c", user="u", tool="t")
    with pytest.raises(ValueError, match="precede"):
        export_audit_event(
            native, target=TARGET, created_at=datetime.now(timezone.utc) - timedelta(days=1)
        )
    native.pop("extensions")
    with pytest.raises(ValueError, match="identifier"):
        export_audit_event(native, target=TARGET, created_at=datetime.now(timezone.utc))
