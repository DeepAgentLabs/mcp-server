"""Exercise an installed wheel over stdio from an empty workspace, without siblings.

Run with the wheel installed: python -I scripts/smoke_protocol.py
"""

import asyncio
import json
import sys
import tempfile
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

import deep_agentic_core_mcp


async def main() -> None:
    installed = Path(deep_agentic_core_mcp.__file__).resolve()
    assert installed.parent != Path(__file__).resolve().parents[1] / "src/deep_agentic_core_mcp"
    with tempfile.TemporaryDirectory(prefix="mcp-wheel-") as workspace:
        server = StdioServerParameters(
            command=sys.executable,
            args=["-I", "-c", "from deep_agentic_core_mcp.server import main; main()"],
            cwd=workspace,
            env={"DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT": workspace},
        )
        async with stdio_client(server) as streams, ClientSession(*streams) as client:
            initialized = await client.initialize()
            assert initialized.server_info.version == deep_agentic_core_mcp.__version__
            tools = await client.list_tools()
            assert {"core.compatibility", "core.verify", "core.version"} <= {
                tool.name for tool in tools.tools
            }
            result = await client.call_tool("core.compatibility", {})
            assert not result.is_error
            report = json.loads(result.content[0].text)
            assert report["baseline"]["baseline_id"] == "mcp-0.7"
            for package, observation in report["local_distributions"].items():
                if package != "mcp":
                    assert observation["status"] == "not_installed", package
            version = await client.call_tool("core.version", {})
            assert json.loads(version.content[0].text)["version"] == initialized.server_info.version
            verified = await client.call_tool("core.verify", {})
            assert not json.loads(verified.content[0].text)["ok"]
            assert (await client.list_prompts()).prompts
            prompt = await client.get_prompt(
                "lens.workflow_summary", {"workflow_name": "wheel-smoke"}
            )
            assert "wheel-smoke" in prompt.messages[0].content.text
            resources = await client.list_resources()
            assert resources.resources
            await client.read_resource("resource://examples/sample_workflow")
    print(
        "Installed wheel: initialize, tools, compatibility, degraded boot, prompts and resources OK"
    )


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), timeout=60))
