"""Show a hosted key's effective access policy, then try one tool against it."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import urllib.request
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", default="core.version", help="Tool to try after the status")
    args = parser.parse_args()
    url = os.environ.get("MCP_URL", "https://mcp.deepagentlabs.io/mcp")
    key = os.environ.get("MCP_API_KEY") or getpass.getpass("MCP API key: ")
    if not url.startswith("https://"):
        raise ValueError("Use an HTTPS MCP endpoint")

    def call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        request = urllib.request.Request(
            url,
            data=json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": name, "arguments": arguments},
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
        if "error" in envelope:
            raise RuntimeError(str(envelope["error"]))
        return dict(json.loads(envelope["result"]["content"][0]["text"]))

    status = call("core.access_status", {})
    print(json.dumps({"access_status": status}, indent=2))
    result = call(args.tool, {})
    if result.get("access_denied"):
        # Denials carry the correlated mcp.access-decision.v1 record.
        print(json.dumps({"denied": result["access_decision"]}, indent=2))
    else:
        print(json.dumps({args.tool: result}, indent=2))


if __name__ == "__main__":
    main()
