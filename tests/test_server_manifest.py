"""The MCP registry manifest must advertise the package version being released."""

import json
from pathlib import Path

from deep_agentic_core_mcp import __version__

MANIFEST = Path(__file__).resolve().parents[1] / "server.json"


def test_server_manifest_versions_match_package() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["version"] == __version__
    assert {package["version"] for package in manifest.get("packages", [])} <= {__version__}
