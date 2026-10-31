"""Phase 3b: chaos results are convertible to, and validated as, AIOS run artifacts."""

import json

import pytest

from deep_agentic_core_mcp.adapters import agentic_chaos as chaos_adapter
from deep_agentic_core_mcp.server import handle_call_tool
from deep_agentic_core_mcp.services import session as session_service

requires_export = pytest.mark.skipif(
    not chaos_adapter.aios_export_available(),
    reason="installed agentic-chaos predates AIOS run export (needs >=0.5.1)",
)

CHAOS_TARGET = "mcp-server/examples/chaos_target.py"
CHAOS_FAILING = "mcp-server/examples/chaos_exit_nonzero.py"


async def _call(name: str, arguments: dict) -> dict:
    return json.loads((await handle_call_tool(name, arguments))[0].text)


@pytest.fixture(autouse=True)
def _fresh_session():
    session_service.reset_session("aios")
    yield
    session_service.reset_session("aios")


@requires_export
async def test_run_experiment_attaches_an_aligned_aios_run() -> None:
    payload = await _call(
        "chaos.run_experiment",
        {
            "script": CHAOS_TARGET,
            "faults": ["silent_degradation"],
            "workflow_id": "support-workflow",
            "session_id": "aios",
        },
    )

    assert payload["ok"] is True
    run = payload["aios_run"]
    assert run["spec_version"] == "0.4-draft"
    assert run["id"] == payload["id"]
    assert run["status"] == "completed"
    assert run["workflow_id"] == "support-workflow"
    assert [evidence["type"] for evidence in run["evidence"]] == ["reliability_event"]
    assert payload["aios_export"]["aligned"] is True
    assert payload["aios_export"]["issues"] == []
    assert "0.4-draft" in payload["aios_export"]["claim"]


@requires_export
async def test_crashed_experiment_exports_a_failed_run() -> None:
    payload = await _call(
        "chaos.run_experiment",
        {"script": CHAOS_FAILING, "faults": ["token_timeout"], "session_id": "aios"},
    )

    assert payload["ok"] is False
    assert payload["aios_run"]["status"] == "failed"
    assert payload["aios_export"]["aligned"] is True


async def test_export_can_be_disabled() -> None:
    payload = await _call(
        "chaos.run_experiment",
        {
            "script": CHAOS_TARGET,
            "faults": ["silent_degradation"],
            "export_aios": False,
            "session_id": "aios",
        },
    )

    assert payload["ok"] is True
    assert "aios_run" not in payload


@requires_export
async def test_export_tool_reuses_the_session_report() -> None:
    await _call(
        "chaos.run_experiment",
        {
            "script": CHAOS_TARGET,
            "faults": ["silent_degradation"],
            "export_aios": False,
            "session_id": "aios",
        },
    )

    payload = await _call("chaos.export_aios_run", {"session_id": "aios", "workflow_id": "wf-1"})

    assert payload["ok"] is True
    assert payload["aios_run"]["workflow_id"] == "wf-1"
    assert payload["aios_export"]["aligned"] is True


@requires_export
async def test_export_tool_accepts_an_explicit_report_and_status() -> None:
    report = {
        "id": "report-7",
        "name": "saved",
        "start_time": "2026-10-13T12:00:00Z",
        "end_time": "2026-10-13T12:00:01Z",
        "chaos_events": [
            {
                "id": "e1",
                "fault_type": "tool_failure",
                "step_name": "Search",
                "outcome": "errored",
                "message": "boom",
                "timestamp": "2026-10-13T12:00:00.5Z",
            }
        ],
    }

    payload = await _call(
        "chaos.export_aios_run", {"report": report, "status": "cancelled", "session_id": "aios"}
    )

    assert payload["ok"] is True
    run = payload["aios_run"]
    assert run["status"] == "cancelled"
    assert run["occurrences"][0]["type"] == "tool_invocation"
    assert run["events"][-1]["event_name"] == "aiops.run.cancelled"


async def test_export_tool_requires_a_report() -> None:
    payload = await _call("chaos.export_aios_run", {"session_id": "aios"})

    assert payload["ok"] is False
    assert "no chaos report stored" in payload["error"]


async def test_export_degrades_without_the_chaos_exporter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(chaos_adapter, "_AIOS_EXPORT_ERROR", ImportError("old chaos"))
    from deep_agentic_core_mcp.tools import chaos as chaos_tools

    monkeypatch.setattr(chaos_tools, "aios_export_available", chaos_adapter.aios_export_available)

    payload = await _call(
        "chaos.run_experiment",
        {"script": CHAOS_TARGET, "faults": ["silent_degradation"], "session_id": "aios"},
    )
    exported = await _call("chaos.export_aios_run", {"session_id": "aios"})

    assert payload["ok"] is True
    assert payload["aios_run"] is None
    assert payload["aios_export"] == {
        "available": False,
        "reason": f"requires agentic-chaos>={chaos_adapter.AIOS_EXPORT_MIN_VERSION}",
    }
    assert exported["ok"] is False
    assert "agentic-chaos>=" in exported["error"]


async def test_probe_reports_export_capability() -> None:
    health = await _call("core.health", {})

    assert health["adapters"]["agentic_chaos"]["aios_export"] is (
        chaos_adapter.aios_export_available()
    )


async def test_export_tool_is_offered_over_remote_transport(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from deep_agentic_core_mcp.server import handle_list_tools

    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_REMOTE", "1")
    names = {tool.name for tool in await handle_list_tools()}

    assert "chaos.export_aios_run" in names
    assert "chaos.run_experiment" not in names


def _chaos_version() -> tuple[int, ...]:
    from importlib.metadata import PackageNotFoundError, version

    try:
        return tuple(int(part) for part in version("agentic-chaos").split(".")[:2])
    except (PackageNotFoundError, ValueError):
        return (0, 0)


@pytest.mark.skipif(_chaos_version() < (0, 9), reason="resilience scores need agentic-chaos>=0.9")
async def test_export_tool_passes_the_chaos_resilience_score_through() -> None:
    report = {
        "id": "report-9",
        "name": "scored",
        "start_time": "2026-10-31T12:00:00Z",
        "end_time": "2026-10-31T12:00:01Z",
        "chaos_events": [
            {
                "id": "e1",
                "fault_type": "rate_limit_storm",
                "step_name": "llm",
                "outcome": "errored",
                "message": "429",
                "timestamp": "2026-10-31T12:00:00.5Z",
            }
        ],
        "probes": [{"probe": "ping", "phase": "post", "status": "passed"}],
        "resilience": {"version": "1.0", "score": 88, "status": "scored", "grade": "B"},
    }

    payload = await _call("chaos.export_aios_run", {"report": report, "session_id": "aios"})

    assert payload["ok"] is True
    run = payload["aios_run"]
    measurements = {m["name"]: m for m in run["measurements"]}
    assert measurements["resilience_score"] == {
        "name": "resilience_score",
        "value": 88,
        "unit": "score",
        "kind": "derived",
    }
    extension = run["extensions"]["io.deepagentlabs.agentic-chaos"]
    assert extension["resilience"]["grade"] == "B"
    assert extension["probes"][0]["probe"] == "ping"
