"""Inspect the candidate baseline without installing optional sibling packages.

Run: uv run python examples/compatibility_check.py
Version differences are observations; core.verify separately checks adapter readiness.
"""

import asyncio
import json

from deep_agentic_core_mcp.server import handle_call_tool


async def main() -> None:
    result = await handle_call_tool("core.compatibility", {})
    print(json.dumps(json.loads(result[0].text), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
