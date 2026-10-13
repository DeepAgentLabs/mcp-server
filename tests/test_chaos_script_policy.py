"""Phase 3b: allow/deny glob policy layered on chaos.run_experiment's workspace confinement."""

import json
from pathlib import Path

import pytest

from deep_agentic_core_mcp import config
from deep_agentic_core_mcp.server import handle_call_tool

TARGET = "mcp-server/examples/chaos_target.py"


async def _run(script: str) -> dict:
    result = await handle_call_tool(
        "chaos.run_experiment",
        {"script": script, "faults": ["silent_degradation"], "export_aios": False},
    )
    return json.loads(result[0].text)


async def test_default_policy_allows_workspace_scripts() -> None:
    assert (await _run(TARGET))["ok"] is True


async def test_allowlist_rejects_scripts_outside_it(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(config.ALLOWED_SCRIPT_GLOBS_ENV, "agentic-chaos/examples/*")

    payload = await _run(TARGET)

    assert payload["ok"] is False
    assert "not in the configured allowlist" in payload["error"]


async def test_allowlist_admits_matching_scripts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(config.ALLOWED_SCRIPT_GLOBS_ENV, " other/*.py , mcp-server/examples/* ")

    assert (await _run(TARGET))["ok"] is True


async def test_deny_wins_over_allow(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(config.ALLOWED_SCRIPT_GLOBS_ENV, "mcp-server/*")
    monkeypatch.setenv(config.DENIED_SCRIPT_GLOBS_ENV, "*/chaos_target.py")

    payload = await _run(TARGET)

    assert payload["ok"] is False
    assert "denied by script policy glob '*/chaos_target.py'" in payload["error"]


@pytest.mark.parametrize(
    "relative",
    [
        "proj/.venv/lib/x.py",
        ".venv/x.py",
        "proj/.git/hooks/x.py",
        ".git/hooks/x.py",
        "site-packages/x.py",
        "proj/lib/site-packages/x.py",
    ],
)
async def test_installed_and_vcs_scripts_are_denied_by_default(
    relative: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    script = tmp_path / relative
    script.parent.mkdir(parents=True)
    script.write_text("print('should never run')\n")
    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT", str(tmp_path))

    payload = await _run(relative)

    assert payload["ok"] is False
    assert "denied by script policy" in payload["error"]


def test_default_deny_globs_cover_installed_packages_and_vcs() -> None:
    policy = config.script_policy()
    assert policy["allowed"] == ()
    for glob in ("*/.venv/*", "*/site-packages/*", "*/.git/*"):
        assert glob in policy["denied"]


async def test_health_reports_the_active_policy(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(config.DENIED_SCRIPT_GLOBS_ENV, "secret/*")

    health = json.loads((await handle_call_tool("core.health", {}))[0].text)

    assert "secret/*" in health["chaos_script_policy"]["denied"]
    assert health["chaos_script_policy"]["allowed"] == []
