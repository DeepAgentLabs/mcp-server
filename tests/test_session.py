from deep_agentic_core_mcp.services import session


def setup_function() -> None:
    # Each test gets a clean slate for the sessions it touches.
    session.reset_session("default")
    session.reset_session("custom")


def test_get_session_creates_and_reuses_default() -> None:
    first = session.get_session()
    first.workflow = {"name": "example"}
    assert session.get_session() is first
    assert session.get_session("default") is first


def test_get_session_is_isolated_per_id() -> None:
    default_state = session.get_session("default")
    custom_state = session.get_session("custom")
    assert default_state is not custom_state


def test_record_call_appends_history_entry() -> None:
    session.record_call("default", "core.health", ok=True)
    history = session.get_session("default").history
    assert len(history) == 1
    assert history[0]["tool"] == "core.health"
    assert history[0]["ok"] is True
    assert "at" in history[0]


def test_record_call_with_note_on_failure() -> None:
    session.record_call("default", "lens.analyze_workflow", ok=False, note="boom")
    entry = session.get_session("default").history[-1]
    assert entry["ok"] is False
    assert entry["note"] == "boom"


def test_history_is_capped() -> None:
    limit = session._HISTORY_LIMIT
    for i in range(limit + 10):
        session.record_call("default", f"tool.{i}", ok=True)
    history = session.get_session("default").history
    assert len(history) == limit
    assert history[-1]["tool"] == f"tool.{limit + 9}"


def test_last_successful_calls_ignores_failures() -> None:
    session.record_call("default", "chaos.run_experiment", ok=False, note="timed out")
    session.record_call("default", "chaos.run_experiment", ok=True)
    latest = session.last_successful_calls("default")
    assert "chaos.run_experiment" in latest


def test_reset_session_drops_state() -> None:
    session.get_session("default").workflow = {"name": "example"}
    session.reset_session("default")
    assert session.get_session("default").workflow is None


def test_summary_reports_stored_artifacts() -> None:
    state = session.get_session("default")
    state.workflow = {"name": "example"}
    state.baseline_runs = [{}]
    state.candidate_runs = [{}, {}]
    summary = state.summary()
    assert summary["has_workflow"] is True
    assert summary["baseline_run_count"] == 1
    assert summary["candidate_run_count"] == 2
