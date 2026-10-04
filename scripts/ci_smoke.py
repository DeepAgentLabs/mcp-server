"""Check the hosted service with a dedicated CI user's key; never print it."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


def main() -> None:
    origin = os.environ.get("MCP_ORIGIN", "https://mcp.deepagentlabs.io").rstrip("/")
    key = os.environ["MCP_API_KEY"]
    with urllib.request.urlopen(origin + "/healthz", timeout=30) as response:
        assert response.status == 200
    try:
        urllib.request.urlopen(
            urllib.request.Request(
                origin + "/mcp", data=b"{}", headers={"Content-Type": "application/json"}
            ),
            timeout=30,
        )
    except urllib.error.HTTPError as error:
        assert error.code == 401, error.code
    else:
        raise RuntimeError("Unauthenticated request was accepted")
    request = urllib.request.Request(
        origin + "/mcp",
        data=json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "core.health", "arguments": {}},
            }
        ).encode(),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2025-11-25",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        envelope = json.loads(response.read())
    assert not envelope["result"].get("isError")
    payload = json.loads(envelope["result"]["content"][0]["text"])
    assert payload["adapters"]["agenticlens"]["available"]
    assert payload["adapters"]["ai_operations_spec"]["available"]
    print("Verified HTTPS health, authentication enforcement, and MCP integration readiness")


if __name__ == "__main__":
    main()
