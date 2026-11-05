"""Optional real Tower 0.11 acceptance; CI installs the published API extra explicitly."""

import json
import socket
import threading
import time

import pytest

pytest.importorskip("agenticops_control_tower")
uvicorn = pytest.importorskip("uvicorn")

from agenticops_control_tower.api.http import create_app  # noqa: E402

from deep_agentic_core_mcp.server import handle_call_tool  # noqa: E402


async def test_published_tower_contract_roundtrip(monkeypatch):
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_REMOTE", raising=False)
    monkeypatch.setenv("AGENTICOPS_TOWER_READ_TOKEN", "reader")
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    monkeypatch.setenv("AGENTICOPS_TOWER_URL", f"http://127.0.0.1:{sock.getsockname()[1]}")
    app = create_app(read_token="reader", write_token="writer", detection_interval_seconds=0)
    server = uvicorn.Server(uvicorn.Config(app, log_level="error"))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 10
        while not server.started:
            if not thread.is_alive() or time.monotonic() >= deadline:
                pytest.fail("Tower server did not start")
            time.sleep(0.01)
        result = await handle_call_tool("tower.capability_contract", {})
        payload = json.loads(result[0].text)
        assert payload["ok"]
        assert payload["data"]["contract_version"] == "tower.capabilities.v1"
        assert payload["data"]["maturity"] == "candidate"
        assert set(payload["data"]["schemas"]) == {"registration", "heartbeat", "agent"}
        monkeypatch.setenv("AGENTICOPS_TOWER_READ_TOKEN", "invalid")
        result = await handle_call_tool("tower.capability_contract", {})
        assert json.loads(result[0].text) == {"ok": False, "error": "Tower HTTP 401"}
    finally:
        server.should_exit = True
        thread.join(timeout=10)
        sock.close()
    assert not thread.is_alive()
