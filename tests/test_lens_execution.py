"""MCP delegates evidence verification with host trust, never caller trust."""

import json
from copy import deepcopy
from pathlib import Path

import pytest

from deep_agentic_core_mcp.server import handle_call_tool
from deep_agentic_core_mcp.tools.lens_evidence import execution_verify

FIXTURE = Path(__file__).parent / "fixtures" / "lens-execution-bundle.json"
KEY = b"execution-demo-key-at-least-32-bytes"


def trust(monkeypatch, tmp_path):
    path = tmp_path / "keys.json"
    path.write_text(json.dumps({"test": KEY.hex()}))
    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_LENS_TRUST_STORE", str(path))


@pytest.mark.asyncio
async def test_server_verifies_and_redacts(monkeypatch, tmp_path):
    trust(monkeypatch, tmp_path)
    bundle = json.loads(FIXTURE.read_text())
    content = await handle_call_tool(
        "lens.execution_verify", {"bundle": bundle, "run_id": "run-evidence"}
    )
    payload = json.loads(content[0].text)
    assert payload["ok"] is True
    assert payload["verification"]["status"] == "verified"
    assert payload["causal_links"][0]["decision_id"] == "decision-1"
    assert "private" not in json.dumps(payload)


def test_host_trust_missing_or_invalid(monkeypatch, tmp_path):
    args = {"bundle": json.loads(FIXTURE.read_text()), "run_id": "run-evidence"}
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_LENS_TRUST_STORE", raising=False)
    assert execution_verify(args)["verification"]["status"] == "unknown"
    assert execution_verify({**args, "trusted_keys": {"test": KEY.hex()}})["ok"] is False
    trust(monkeypatch, tmp_path)
    changed = deepcopy(args)
    changed["bundle"]["artifact"]["events"].pop()
    result = execution_verify(changed)
    assert result["ok"] is False
    assert result["verification"]["status"] == "failed"
    assert result["causal_links"] == []
    assert execution_verify({**args, "run_id": "other"})["ok"] is False
    assert execution_verify({"bundle": {}, "run_id": "run-evidence"})["ok"] is False


@pytest.mark.asyncio
async def test_hosted_permission_denies_before_verification(monkeypatch):
    from deep_agentic_core_mcp.server import _TOOL_DISPATCH
    from deep_agentic_core_mcp.services.access_policy import AccessPolicy, Principal
    from deep_agentic_core_mcp.services.remote_sessions import MemorySessionStore

    def forbidden_handler(arguments):
        raise AssertionError("Denied request must not reach Lens or trust store")

    monkeypatch.setitem(_TOOL_DISPATCH, "lens.execution_verify", forbidden_handler)
    content = await handle_call_tool(
        "lens.execution_verify",
        {"bundle": {}, "run_id": "test"},
        owner="alice",
        store=MemorySessionStore(),
        authorizer=lambda: Principal("alice", AccessPolicy(allow=["core.*"])),
    )
    assert json.loads(content[0].text)["access_denied"] is True
