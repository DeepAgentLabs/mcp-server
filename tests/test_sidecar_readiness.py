"""Package APIs are discovery evidence, not a live task/operator connection."""

from types import SimpleNamespace

import pytest

from deep_agentic_core_mcp.adapters import AdapterUnavailableError
from deep_agentic_core_mcp.adapters import agentic_sidecar as adapter


def test_scaffold_does_not_claim_runtime():
    status = adapter._runtime_status(SimpleNamespace(Sidecar=type("Empty", (), {})))
    assert status["package_status"] == "scaffold"
    assert not status["runtime_ready"]
    assert status["installed_runtime_capabilities"] == []


def test_older_runtime_does_not_claim_new_operator_features():
    class Runtime:
        def evaluate(self):
            raise AssertionError("Discovery must not evaluate")

    status = adapter._runtime_status(SimpleNamespace(Sidecar=Runtime))
    assert status["runtime_ready"]
    assert status["installed_runtime_capabilities"] == ["decision_evaluation"]
    assert status["runtime_connected"] is False
    assert status["mcp_runtime_controls"] is False


def test_real_v07_package_reports_capabilities_without_connecting_task(monkeypatch):
    package = pytest.importorskip("agentic_sidecar")
    if not hasattr(package, "TaskRuntime"):
        pytest.skip("Sidecar v0.7 runtime is not installed")
    monkeypatch.setattr(adapter, "_IMPORT_ERROR", None)
    monkeypatch.setattr(adapter, "_package", package)
    probe = adapter.probe()
    status = adapter.status_summary()
    assert probe["runtime_ready"] is True
    assert status["package_status"] == "implemented"
    expected = {
        "decision_evaluation",
        "governance_enforcement",
        "plan_evaluation",
        "runtime_events",
        "task_controls",
        "durable_audit",
        "local_operator_http",
    }
    if hasattr(package, "AuthorityRegistry"):
        expected |= {"task_authority", "authority_revocation", "redacted_evidence"}
    assert set(status["installed_runtime_capabilities"]) == expected
    assert not status["runtime_connected"]
    assert not status["mcp_runtime_controls"]
    inventory = adapter.module_inventory()
    assert "operations" in inventory["top_level_modules"]
    assert "operations" not in inventory["planned_runtime_modules"]


def test_missing_package_remains_unavailable(monkeypatch):
    monkeypatch.setattr(adapter, "_IMPORT_ERROR", ImportError("not installed"))
    assert adapter.probe()["available"] is False
    assert adapter.probe()["runtime_ready"] is False
    assert adapter.probe()["installed_runtime_capabilities"] == []
    with pytest.raises(AdapterUnavailableError):
        adapter.status_summary()


def test_v07_discovery_and_inventory_without_an_installed_sibling(monkeypatch, tmp_path):
    def must_not_run(*args, **kwargs):
        raise AssertionError("Discovery must not start/evaluate/control a task")

    package = SimpleNamespace(
        Sidecar=SimpleNamespace(
            evaluate=must_not_run, enforce=must_not_run, evaluate_plan=must_not_run
        ),
        TaskRuntime=SimpleNamespace(snapshot=must_not_run, control=must_not_run),
        EventJournal=SimpleNamespace(export=must_not_run),
        OperatorServer=must_not_run,
    )
    for name in (
        "core",
        "gate",
        "intent",
        "evaluators",
        "status",
        "operations",
        "adapters",
        "integrations",
        "cli",
        "__pycache__",
    ):
        (tmp_path / name).mkdir()
    for directory, names in (
        ("adapters", ["langgraph", "crewai"]),
        ("integrations", ["agenticlens", "agentic_chaos"]),
    ):
        for name in ["__init__", *names]:
            (tmp_path / directory / (name + ".py")).write_text('"""Discovery fixture."""\n')
    monkeypatch.setattr(adapter, "_IMPORT_ERROR", None)
    monkeypatch.setattr(adapter, "_package", package)
    monkeypatch.setattr(adapter, "_package_root", tmp_path)
    monkeypatch.setattr(adapter, "_version", "0.7.0")
    expected = {
        "decision_evaluation",
        "governance_enforcement",
        "plan_evaluation",
        "runtime_events",
        "task_controls",
        "durable_audit",
        "local_operator_http",
    }
    status = adapter.status_summary()
    assert status["version"] == "0.7.0"
    assert status["runtime_ready"]
    assert status["package_status"] == "implemented"
    assert set(status["installed_runtime_capabilities"]) == expected
    assert set(adapter.probe()["installed_runtime_capabilities"]) == expected
    inventory = adapter.module_inventory()
    assert "operations" in inventory["top_level_modules"]
    assert "__pycache__" not in inventory["top_level_modules"]
    assert inventory["planned_runtime_modules"] == []
    assert inventory["framework_adapters"] == ["crewai", "langgraph"]
    assert inventory["integrations"] == ["agentic_chaos", "agenticlens"]
    assert set(inventory["installed_runtime_capabilities"]) == expected
    for result in (status, adapter.probe(), inventory):
        assert not result["runtime_connected"]
        assert not result["mcp_runtime_controls"]
    (tmp_path / "operations").rmdir()
    assert adapter.module_inventory()["planned_runtime_modules"] == ["operations"]


def test_v09_discovery_is_read_only():
    def must_not_run(*args, **kwargs):
        raise AssertionError("Discovery must not issue grants, revoke or read evidence")

    package = SimpleNamespace(
        Sidecar=SimpleNamespace(evaluate=must_not_run),
        AuthorityRegistry=SimpleNamespace(grant=must_not_run, revoke=must_not_run),
        BoundAgent=SimpleNamespace(evidence=must_not_run),
    )
    status = adapter._runtime_status(package)
    assert set(status["installed_runtime_capabilities"]) == {
        "decision_evaluation",
        "task_authority",
        "authority_revocation",
        "redacted_evidence",
    }
    assert status["runtime_connected"] is False
    assert status["mcp_runtime_controls"] is False
