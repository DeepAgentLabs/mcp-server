"""Readiness observations must not become unearned operational verdicts."""

import json
from importlib.metadata import PackageNotFoundError

from deep_agentic_core_mcp.server import handle_call_tool
from deep_agentic_core_mcp.services import compatibility


def test_missing_and_different_versions_are_explicit(monkeypatch):
    def version(name):
        if name == "agenticlens":
            raise PackageNotFoundError(name)
        return "99.0.0"

    monkeypatch.setattr(compatibility.metadata, "version", version)
    report = compatibility.compatibility_report()
    assert report["local_distributions"]["agenticlens"] == {
        "baseline_version": "0.14.0",
        "installed_distribution_version": None,
        "status": "not_installed",
    }
    assert report["local_distributions"]["mcp"]["status"] == "different_version"
    assert "ok" not in report
    assert "passed" not in report


async def test_compatibility_dispatch_is_read_only_and_has_no_prerequisites(monkeypatch):
    baseline = compatibility.compatibility_report()["baseline"]
    monkeypatch.setattr(compatibility.metadata, "version", baseline["packages"].__getitem__)
    result = await handle_call_tool("core.compatibility", {})
    report = json.loads(result[0].text)
    assert report["baseline"]["maturity"] == "candidate"
    assert all(x["status"] == "baseline_match" for x in report["local_distributions"].values())
    from deep_agentic_core_mcp.tools.registry import list_tools

    entry = next(x for x in list_tools() if x["name"] == "core.compatibility")
    assert entry["prerequisites"] == []
    assert entry["mutates_session"] is False
