"""Read Tower 0.10's candidate contract through a locally configured MCP connector.

Set AGENTICOPS_TOWER_URL and AGENTICOPS_TOWER_READ_TOKEN on the MCP process.
Run: uv run python examples/tower_capability_contract.py
"""

import asyncio
import json

from deep_agentic_core_mcp.server import handle_call_tool


async def main():
    result = await handle_call_tool("tower.capability_contract", {})
    payload = json.loads(result[0].text)
    print(json.dumps(payload, indent=2))
    if not payload.get("ok"):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
