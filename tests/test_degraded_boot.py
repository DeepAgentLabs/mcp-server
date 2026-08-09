"""Verify the server boots and stays inspectable when a sibling repo is unavailable.

Runs in a fresh subprocess rather than monkeypatching the current process:
`ai_operations_spec.py` (like the other adapters) resolves its sibling repo
and loads schema documents at *import* time, so the only faithful way to
exercise "the sibling repo is missing" is to make that true before
`deep_agentic_core_mcp.server` is first imported.
"""

import json
import subprocess
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Points `adapters.workspace_root()` at an empty temp directory before any
# adapter module is imported, so every sibling-repo lookup (agenticlens,
# agentic-chaos, ai-operations-spec) fails to find its repo - without
# touching the real sibling directories on disk.
_SCRIPT = textwrap.dedent(
    """
    import asyncio
    import json
    import sys
    import tempfile
    from pathlib import Path

    sys.path.insert(0, "src")
    import deep_agentic_core_mcp.adapters as adapters_pkg

    adapters_pkg.workspace_root = lambda: Path(tempfile.mkdtemp())

    import deep_agentic_core_mcp.server as server_module  # must not raise

    async def main() -> None:
        verify = json.loads((await server_module.handle_call_tool("core.verify", {}))[0].text)
        health = json.loads((await server_module.handle_call_tool("core.health", {}))[0].text)
        validate = json.loads(
            (
                await server_module.handle_call_tool(
                    "spec.validate_artifact", {"artifact": {"artifact_type": "workflow"}}
                )
            )[0].text
        )
        schema_resource_uris = [r.uri for r in server_module.RESOURCES if "schema" in r.uri]
        print(json.dumps({
            "verify": verify,
            "health_status": health["status"],
            "validate": validate,
            "schema_resource_uris": schema_resource_uris,
        }))

    asyncio.run(main())
    """
)


def test_server_boots_and_degrades_when_sibling_repos_are_missing() -> None:
    result = subprocess.run(
        [sys.executable, "-c", _SCRIPT],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr

    output = json.loads(result.stdout.strip().splitlines()[-1])
    assert output["verify"]["ok"] is False
    assert output["verify"]["adapters"]["ai_operations_spec"]["available"] is False
    assert output["health_status"] == "degraded"

    # The crash this test guards against: server.py used to index
    # SCHEMA_DOCUMENTS["workflow.schema.json"] directly at import time, which
    # raised KeyError (not a caught AdapterUnavailableError) as soon as the
    # sibling repo's schemas weren't loaded - before core.verify could ever
    # run. Reaching this point at all is most of what this test proves;
    # these assertions confirm the *degraded* behavior is also correct.
    assert output["validate"]["ok"] is False
    assert "unavailable" in output["validate"]["error"]
    assert output["schema_resource_uris"] == []
