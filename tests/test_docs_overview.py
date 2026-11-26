"""The public overview and API reference stay in step with the registered surface."""

import json
import re
from pathlib import Path

from deep_agentic_core_mcp import __version__
from deep_agentic_core_mcp.prompts.registry import list_prompts
from deep_agentic_core_mcp.tools.registry import list_tools

DOCS = Path(__file__).resolve().parents[1] / "docs"


def _tool_names() -> set[str]:
    return {tool["name"] for tool in list_tools()}


def test_api_reference_lists_every_registered_tool_and_prompt():
    text = (DOCS / "api-reference.md").read_text(encoding="utf-8")
    assert f"**Version:** {__version__}" in text
    listed = set(re.findall(r"^\| `([a-z]+\.[a-z_]+)` \|", text, re.MULTILINE))
    prompts = {prompt["name"] for prompt in list_prompts()}
    assert listed == _tool_names() | prompts


def test_overview_names_every_registered_tool():
    text = (DOCS / "index.md").read_text(encoding="utf-8")
    missing = sorted(name for name in _tool_names() if f"`{name}`" not in text)
    assert not missing


def test_human_docs_state_the_current_tool_count():
    count = len(_tool_names())
    for name in ("index.md", "developer-guide.md", "cli-reference.md", "api-reference.md"):
        text = (DOCS / name).read_text(encoding="utf-8")
        stated = {int(a or b) for a, b in re.findall(r"(?:all|server exposes) (\d+) tool|\b(\d+)(?: registered|-tool)", text)}
        assert stated <= {count}, (name, stated)


def test_sidebar_matches_the_product_documentation_layout():
    entries = json.loads((DOCS / "navigation.json").read_text(encoding="utf-8"))
    assert [next(iter(entry.values())) for entry in entries] == [
        "index.md",
        "developer-guide.md",
        "api-reference.md",
        "ai-reference-index.md",
    ]
