# Changelog

All notable changes to this project will be documented here.

This project follows [Semantic Versioning](https://semver.org/).

## 0.1.3 - 2026-08-07

### Added

- `lens.analyze_workflow` tool backed by AgenticLens recommendation engine.
- `chaos.list_faults` tool exposing the agentic-chaos fault registry.
- `spec.validate_artifact` tool for structural and semantic validation against AI Operations v0.4 draft.
- MCP resource endpoints for AI Operations v0.4 schemas (workflow, run, common).
- `resources/read` handler returning resource contents.
- Adapter layer for sibling repos (agenticlens, agentic-chaos, ai-operations-spec).

### Changed

- Tool dispatch now passes arguments through to handlers.
- `inputSchema` on advertised tools reflects actual argument schemas.
- Switched from `AnyUrl` to plain string for resource URIs.
- Server handlers registered via `add_request_handler` instead of decorators.

## 0.1.2 - 2026-07-28

### Added

- Initial MCP server with `core.health` and `core.version` tools.
- Tool registry, resource catalog, and prompt catalog scaffolding.
- stdio transport via `mcp` SDK.
- CI workflow and PyPI Trusted Publishing.
