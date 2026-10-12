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
    assert set(status["installed_runtime_capabilities"]) == {
        "decision_evaluation",
        "governance_enforcement",
        "plan_evaluation",
        "runtime_events",
        "task_controls",
        "durable_audit",
        "local_operator_http",
    }
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
