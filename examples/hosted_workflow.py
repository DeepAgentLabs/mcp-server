"""Analyze an exported workflow using the hosted stateless JSON MCP endpoint."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import urllib.request
from pathlib import Path
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--session-id", default="demo-run")
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
        result = envelope["result"]
        if result.get("isError"):
            raise RuntimeError("MCP tool call failed: " + str(result["content"]))
        payload = dict(json.loads(result["content"][0]["text"]))
        if payload.get("ok") is False or "error" in payload:
            raise RuntimeError(str(payload.get("error", "Tool failed")))
        return payload

    artifact = json.loads(args.artifact.read_text())
    analysis = call("lens.analyze_workflow", {"artifact": artifact, "session_id": args.session_id})
    report = call("lens.report_summary", {"session_id": args.session_id})
    print(json.dumps({"analysis": analysis, "report": report}, indent=2))


if __name__ == "__main__":
    main()
