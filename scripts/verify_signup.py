"""Verify public signup, independent sessions, rotation and revocation over HTTPS.

Creates two temporary identities and revokes their keys on completion.
Credentials stay in memory and are never printed or written to disk.
"""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("origin")
    args = parser.parse_args()
    origin = args.origin.rstrip("/")
    if not origin.startswith("https://"):
        raise ValueError("Use the deployed HTTPS origin")

    def request(
        path: str, method: str = "GET", data: dict[str, Any] | None = None, key: str = ""
    ) -> dict[str, Any]:
        headers = {"Content-Type": "application/json", "Origin": origin}
        if key:
            headers["Authorization"] = "Bearer " + key
        if path == "/mcp":
            headers.pop("Origin")  # MCP desktop clients do not send a browser Origin.
            headers.update(
                {
                    "Accept": "application/json, text/event-stream",
                    "MCP-Protocol-Version": "2025-11-25",
                }
            )
        req = urllib.request.Request(
            origin + path,
            method=method,
            data=json.dumps(data).encode() if data is not None else None,
            headers=headers,
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            assert response.headers["Cache-Control"] == "no-store" or path == "/mcp"
            return dict(json.loads(response.read()))

    def tool(key: str, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        result = request(
            "/mcp",
            "POST",
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments or {}},
            },
            key,
        )
        assert not result["result"].get("isError"), "MCP tool returned an error"
        payload = dict(json.loads(result["result"]["content"][0]["text"]))
        assert payload.get("ok", True), "MCP tool reported a failure"
        return payload

    def denied(key: str) -> None:
        try:
            tool(key, "core.version")
        except urllib.error.HTTPError as error:
            assert error.code == 401, error.code
        else:
            raise RuntimeError("Inactive key was accepted")

    active: list[str] = []
    try:
        with urllib.request.urlopen(origin + "/signup", timeout=30) as response:
            assert response.status == 200
            assert "Create your MCP key" in response.read().decode()
        users = []
        for _ in range(2):
            user = request("/api/signup", "POST", {"display_name": "Deployment check"})
            active.append(user["api_key"])
            assert user["mcp_url"] == origin + "/mcp", "Signup returned a different MCP endpoint"
            users.append(user)
        assert users[0]["user_id"] != users[1]["user_id"]
        artifact = json.loads(
            (Path(__file__).resolve().parents[1] / "examples/sample_workflow.json").read_text()
        )
        tool(active[0], "lens.analyze_workflow", {"artifact": artifact})
        own = tool(active[0], "core.session_state")
        other = tool(active[1], "core.session_state")
        assert own["has_workflow"]
        assert any(item["tool"] == "lens.analyze_workflow" for item in own["history"])
        assert not other["has_workflow"]
        assert not other["history"], "User sessions were not isolated"
        old = active[0]
        replacement = request("/api/account", "POST", key=old)
        active[0] = replacement["api_key"]
        assert replacement["user_id"] == users[0]["user_id"]
        denied(old)
        assert tool(active[0], "core.session_state")["history"], "Rotation lost user state"
        for key in list(active):
            request("/api/account", "DELETE", key=key)
            active.remove(key)
            denied(key)
    finally:
        for key in active:
            request("/api/account", "DELETE", key=key)
    print(
        "Verified public signup, distinct users, isolated MCP sessions, key rotation and revocation"
    )


if __name__ == "__main__":
    main()
