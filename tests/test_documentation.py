"""Seven-product retrieval, citation, pagination, integrity and transport boundaries."""

import hashlib
import json
import re
import shutil

import httpx
import pytest

from deep_agentic_core_mcp import __version__, config
from deep_agentic_core_mcp.prompts.registry import render_prompt
from deep_agentic_core_mcp.server import (
    handle_call_tool,
    handle_list_resources,
    handle_read_resource,
)
from deep_agentic_core_mcp.services import documentation
from deep_agentic_core_mcp.services.access_policy import AccessPolicy, Principal
from deep_agentic_core_mcp.services.remote_sessions import MemorySessionStore
from deep_agentic_core_mcp.tools.documentation import PRODUCTS, docs_catalog, docs_read, docs_search
from deep_agentic_core_mcp.transport_http import create_app


def test_mcp_reference_documents_the_current_package_version():
    entry = docs_catalog({"product": "mcp-server"})["products"][0]
    assert entry["version"] == __version__


@pytest.mark.parametrize("product", PRODUCTS)
async def test_all_products_have_exact_references_and_cited_sections(product):
    result = docs_catalog({"product": product})
    entry = result["products"][0]
    assert re.fullmatch("[0-9a-f]{40}", entry["source_commit"])
    assert "/blob/" + entry["source_commit"] + "/" in entry["source_url"]
    resources = await handle_list_resources()
    assert entry["resources"]["reference"] in {str(r.uri) for r in resources}
    raw = (await handle_read_resource(entry["resources"]["reference"]))[0]
    assert raw.mime_type == "text/markdown"
    assert hashlib.sha256(raw.text.encode()).hexdigest() == entry["sha256"]
    manifest = json.loads((await handle_read_resource(entry["resources"]["manifest"]))[0].text)
    assert manifest["sha256"] == entry["sha256"]
    assert "Capability index" in (await handle_read_resource(entry["resources"]["index"]))[0].text
    assert "MIT License" in (await handle_read_resource(entry["resources"]["license"]))[0].text
    ids = [s["section"] for s in result["sections"]]
    assert len(ids) == len(set(ids))
    assert len(ids) > 20
    # Full reference pages reconstruct the source exactly, including non-ASCII text.
    pages, offset = [], 0
    while True:
        page = docs_read({"product": product, "offset": offset, "limit": 32000})
        assert page["ok"]
        pages.append(page["content"])
        if page["next_offset"] is None:
            break
        offset = page["next_offset"]
    assert "".join(pages) == raw.text
    selected = result["sections"][-1]
    page = docs_read({"product": product, "section": selected["section"], "limit": 100})
    assert page["start_line"] == selected["line"]
    assert page["citation"].endswith(f"#L{selected['line']}")


def test_search_is_scoped_bounded_deterministic_and_supports_full_section_read():
    args = {"query": "Sidecar", "product": "agentic-sidecar", "limit": 3}
    result = docs_search(args)
    assert result == docs_search(args)
    assert len(result["results"]) == 3
    for hit in result["results"]:
        assert hit["product"] == "agentic-sidecar"
        assert len(hit["snippet"]) <= 1000
        read = docs_read(
            {
                "product": hit["product"],
                "section": hit["section"],
                "offset": hit["offset"],
                "limit": 1000,
            }
        )
        assert read["content"] == hit["snippet"]
        assert read["citation"] == hit["citation"]
    assert docs_search({"query": "workflow", "limit": 20})["results"]
    assert docs_search({"query": "notawordzxqv598473"})["results"] == []


@pytest.mark.parametrize(
    "tool,args",
    [
        (docs_read, {}),
        (docs_read, {"product": "../secrets"}),
        (docs_read, {"product": "mcp-server", "offset": -1}),
        (docs_read, {"product": "mcp-server", "offset": True}),
        (docs_read, {"product": "mcp-server", "offset": 10**9}),
        (docs_read, {"product": "mcp-server", "limit": 32001}),
        (docs_read, {"product": "mcp-server", "section": "unknown-section"}),
        (docs_search, {"query": " "}),
        (docs_search, {"query": "("}),
        (docs_search, {"query": "x" * 301}),
        (docs_search, {"query": "x", "limit": 21}),
        (docs_catalog, {"url": "https://example.com/arbitrary-document"}),
    ],
)
def test_invalid_requests_return_errors_without_filesystem_or_network_fallback(tool, args):
    assert tool(args)["ok"] is False


async def test_unknown_documentation_uri_is_not_a_file_read():
    result = await handle_read_resource("resource://docs/mcp-server/../../pyproject.toml")
    assert "Unknown resource" in result[0].text


def test_bundled_integrity_failure_is_reported(monkeypatch, tmp_path):
    shutil.copytree(documentation._ROOT, tmp_path / "docs")
    (tmp_path / "docs/agenticlens/llms-full.md").write_text("corrupt")
    monkeypatch.setattr(documentation, "_ROOT", tmp_path / "docs")
    documentation._document.cache_clear()
    try:
        result = docs_read({"product": "agenticlens"})
        assert result["ok"] is False
        assert "integrity" in result["error"]
    finally:
        documentation._document.cache_clear()


def test_heading_index_ignores_code_fences_and_handles_slug_collisions(monkeypatch):
    text = (
        "# Test\n\n```markdown\n## not a section\n```\n## Repeat\na\n## Repeat-2\nb\n## Repeat\nc\n"
    )
    monkeypatch.setattr(documentation, "_asset", lambda *_: text)
    documentation._document.cache_clear()
    try:
        _, sections = documentation._document("mcp-server")
        assert len(sections) == 4
        assert len({s.identifier for s in sections}) == 4
        assert all(s.title != "not a section" for s in sections)
    finally:
        documentation._document.cache_clear()


async def test_documentation_tools_use_hosted_authorization_and_do_not_change_evidence():
    store = MemorySessionStore()
    principal = Principal("reader", AccessPolicy.from_config({"allow": ["core.docs_*"]}))
    content = await handle_call_tool(
        "core.docs_search",
        {"query": "pytest", "product": "agentic-chaos"},
        owner="reader",
        store=store,
        authorizer=lambda: principal,
    )
    assert json.loads(content[0].text)["results"]
    denied = Principal("reader", AccessPolicy.from_config({"deny": ["core.docs_*"]}))
    content = await handle_call_tool(
        "core.docs_catalog", {}, owner="reader", store=store, authorizer=lambda: denied
    )
    assert json.loads(content[0].text)["access_denied"]
    with store.transaction("reader"):
        from deep_agentic_core_mcp.services import session

        assert session.all_sessions() == {}


async def test_http_requires_auth_and_serves_markdown_resources(monkeypatch):
    monkeypatch.setenv(config.REMOTE_TRANSPORT_ENV, "0")
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_DATABASE_URL", raising=False)
    app = create_app(
        api_keys={"reader": "a" * 40}, store=MemorySessionStore(), allowed_hosts=["testserver"]
    )
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        ) as client,
    ):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "resources/read",
            "params": {"uri": "resource://docs/ai-operations-spec/index"},
        }
        assert (await client.post("/mcp", json=payload)).status_code == 401
        response = await client.post(
            "/mcp",
            json=payload,
            headers={
                "Authorization": "Bearer " + "a" * 40,
                "Accept": "application/json, text/event-stream",
                "MCP-Protocol-Version": "2025-11-25",
            },
        )
        result = response.json()["result"]["contents"][0]
        assert result["mimeType"] == "text/markdown"
        assert "Capability index" in result["text"]


def test_build_prompt_guides_search_complete_reads_and_version_checking():
    prompt = render_prompt(
        "core.build_with_ecosystem", {"task": "Build a supervised support agent"}
    )
    for text in [
        "core.docs_catalog",
        "core.docs_search",
        "core.docs_read",
        "next_offset",
        "versions",
        "Build a supervised support agent",
    ]:
        assert text in prompt
