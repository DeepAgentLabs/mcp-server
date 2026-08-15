## deep-agentic-core-mcp Development Reference

## Ecosystem Context

### Role in DeepAgentLabs

`deep-agentic-core-mcp` is the MCP-native control surface for DeepAgentLabs. It
exposes spec-aligned operational artifacts and selected capabilities from the
ecosystem through a unified interface for hosts, agents, and external systems.

### Owns

- MCP server wiring, handler registration, tool/resource exposure, and transport
  boundaries
- Thin orchestration that composes capabilities from sibling packages without
  redefining their core logic
- The contract for how DeepAgentLabs capabilities are presented through MCP

### Does Not Own

- The canonical operational model or schema definitions — those belong in
  `ai-operations-spec`
- Primary instrumentation, trace analysis, or evaluation logic — those belong
  in `agenticlens`
- Fault injection and resilience simulation logic — those belong in
  `agentic-chaos`
- Agent-decision supervision or governance policy logic — those belong in
  `agentic-sidecar`

### Integrates With

- `ai-operations-spec` so returned artifacts and tool semantics align with the
  shared contract
- `agenticlens` as a source of analysis, provenance, and workflow evidence
- `agentic-chaos` as a source of resilience and degradation workflows
- `agentic-sidecar` when supervised-decision capabilities need MCP exposure in
  the future. At the ecosystem-role level, Sidecar is the **SUPERVISE** layer,
  while its concrete functionality spans both supervision and governance.

### Current Roadmap Focus

The next major work is provenance verification on `lens.analyze_workflow`,
multi-version AIOS schema support, and more unified observability-plus-chaos
workflows. Changes here should strengthen composition and interoperability, not
duplicate implementation logic from sibling repos.

### Before You Build Here

- Prefer adapting and exposing sibling-package behavior over rebuilding it in
  server-local modules
- If a new concept changes artifact meaning or shape across the ecosystem,
  update `ai-operations-spec` first
- Keep this package thin: MCP is the access layer, not the place to invent a
  second analysis engine, chaos engine, or policy runtime

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

## Feature Completion Expectations

- Every behavior change must include tests.
- User-facing tools and workflows must include or update examples in
  `README.md`, generated tool docs, or test fixtures that demonstrate expected
  usage.
- When a roadmap item or milestone meaningfully changes status, update
  `README.md` and the roadmap document in the same change.
- If that milestone or release changes the public ecosystem story, also update
  the shared org-profile docs in the `.github` repository:
  `profile/README.md` and, when relevant, `profile/ROADMAP.md`.
- When work is packaged as a release-ready change, also update
  `pyproject.toml`, `src/deep_agentic_core_mcp/__init__.py`, and
  `CHANGELOG.md`.

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
3. Tag: create an annotated `vX.Y.Z` tag and use the latest `CHANGELOG.md`
   release section as the tag description
4. Push: `git push origin main --tags`
5. Create a GitHub Release — the workflow publishes to PyPI and the MCP Registry
