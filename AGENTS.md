## deep-agentic-core-mcp Development Reference

## Build and Run

- Install: `make install` (runs `uv sync --extra dev`)
- Run server: `uv run deep-agentic-core-mcp`
- Test: `make test` or `make check` (lint + format + typecheck + test)
- Lint: `make lint`
- Type check: `make typecheck`

## Code Style

- Strict typing (mypy strict mode, Python 3.10+)
- Async-first — all MCP handlers are async
- Line length: 100
- Ruff rules: E, F, I, UP, B, SIM, N
- One purpose per file (separation of concerns)

## Architecture

MCP 2.0 constructor-based handler registration (not decorator-based):

```python
server = Server(
    SERVER_NAME,
    on_list_tools=handle_list_tools,
    on_call_tool=handle_call_tool,
    on_list_resources=handle_list_resources,
)
```

Handlers receive `(ctx: ServerRequestContext, params)` and return typed result
objects (`ListToolsResult`, `CallToolResult`, `ListResourcesResult`).

## Repo Map

| Path | Purpose |
|------|---------|
| `src/deep_agentic_core_mcp/server.py` | MCP server entrypoint, handler registration, tool dispatch |
| `src/deep_agentic_core_mcp/config.py` | Server identity and shared constants |
| `src/deep_agentic_core_mcp/tools/` | Tool implementations (`core.py`) and registry (`registry.py`) |
| `src/deep_agentic_core_mcp/resources/` | MCP resource definitions and catalog |
| `src/deep_agentic_core_mcp/prompts/` | Reusable prompt templates, wired into `prompts/list`/`prompts/get` |
| `src/deep_agentic_core_mcp/schemas/` | Request/response contracts |
| `src/deep_agentic_core_mcp/services/` | Shared orchestration logic |
| `src/deep_agentic_core_mcp/adapters/` | Integration boundaries to agenticlens and agentic-chaos |
| `tests/` | Pytest tests (asyncio_mode=auto) |
| `scripts/generate_tools_doc.py` | Generates `docs/tools.md` from `tools/registry.py` |
| `docs/tools.md` | **Generated** — never hand-edit, run `make docs` |
| `server.json` | MCP Registry metadata |
| `Makefile` | Local dev automation |

## Entry Points

- Console script: `deep-agentic-core-mcp` → `server.py:main()`
- Server boot: `run_server()` → `stdio_server()` → `server.run()`

## Adding a New Tool

1. Add implementation in `tools/` (return a dict)
2. Register in `tools/registry.py` (name, description, and the metadata
   fields: `category`, `prerequisites`, `expected_duration`, `mutates_session`)
3. Add handler entry in `server.py` `_TOOL_DISPATCH`
4. Add test in `tests/test_server.py`
5. Run `make docs` to regenerate `docs/tools.md`

## Package Boundaries

- This server is a **thin orchestration layer** — reuse agenticlens and
  agentic-chaos logic, don't reimplement it
- All tools should read/return AI Operations Specification-compatible artifacts
- MCP types come from `mcp.types` (re-exports `mcp_types`)

## Pre-push Checklist

Run `make check` before every push. It runs: lint → format-check → typecheck → test.
If `tools/registry.py` changed, also run `make docs-check` (regenerates
`docs/tools.md` and fails if that changed anything you didn't commit) —
not part of `check` itself so the default gate stays fast.

## Release

1. Bump version in `pyproject.toml`, `src/deep_agentic_core_mcp/__init__.py`, and `CHANGELOG.md`
2. Commit: `git commit -am "release: vX.Y.Z"`
3. Tag: `git tag vX.Y.Z`
4. Push: `git push origin main --tags`
5. Create a GitHub Release — the workflow publishes to PyPI and the MCP Registry
