# Changelog

All notable changes to this project will be documented here.

This project follows [Semantic Versioning](https://semver.org/).

## 0.2.0 - 2026-08-08

### Added

- `core.verify` tool checking agenticlens, agentic-chaos, and ai-operations-spec connectivity.
- `core.session_state` tool exposing the in-memory session's stored artifacts and call history.
- In-memory session store (`services/session.py`) so `lens.analyze_workflow` -> `lens.report_summary`
  -> `lens.compare_runs` -> `chaos.run_experiment` can share artifacts without the client resending
  them; tools accept an optional `session_id` argument.
- `lens.report_summary` tool rendering a Markdown workflow report via AgenticLens's `MarkdownExporter`.
- `lens.compare_runs` tool wrapping AgenticLens's baseline/candidate trace comparison and regression
  detection.
- `lens.slo_summary` tool applying release-gate style SLO thresholds to an evaluation report.
- `lens.audit_report` tool returning case-by-case evaluation detail, optionally with an HTML report.
- `chaos.run_experiment` tool running a workspace-sandboxed target script inside a chaos session and
  reporting the resulting fault events (mirrors the agentic-chaos CLI's `chaos run`).
- `examples/chaos_target.py`, a minimal `chaos_call()`-instrumented script for `chaos.run_experiment`.
- Real `prompts/list` and `prompts/get` handlers, with prompt arguments and rendered templates
  (previously the prompt registry existed but was never wired into the server).
- Tool metadata (`category`, `prerequisites`, `expected_duration`, `mutates_session`) on every tool,
  surfaced to MCP hosts via `Tool.annotations`/`Tool._meta`.
- `core.health` now returns adapter availability/version, loaded tool/resource/prompt counts, the
  resolved workspace root, and recent successful-call timestamps, instead of just `{"status": "ok"}`.
- `docs/tools.md`, a generated tool reference (name, description, category, prerequisites, expected
  duration, mutation/side-effect flags, and full input schema per tool) produced by
  `scripts/generate_tools_doc.py` from `tools/registry.py`, so it can't drift out of sync with what
  `tools/list` actually returns. `make docs` regenerates it; `make docs-check` fails if it's stale.

### Changed

- Adapters (`adapters/agenticlens.py`, `adapters/agentic_chaos.py`, `adapters/ai_operations_spec.py`)
  now import their sibling repo defensively: a missing/broken sibling no longer crashes server boot,
  it surfaces as `"available": false` through `core.verify`/`core.health` and a structured tool error.

### Fixed

- `chaos.run_experiment`'s `timeout_seconds` now actually bounds wall-clock time. It previously ran
  the worker thread inside a `with ThreadPoolExecutor(...)` block, whose `__exit__` calls
  `shutdown(wait=True)` and blocked for the thread to finish regardless of the timeout having already
  fired.
- `server.py` no longer indexes `SCHEMA_DOCUMENTS` directly when building the schemas resources
  (`SCHEMA_DOCUMENTS["workflow.schema.json"]`, etc.); a missing/broken `ai-operations-spec` sibling
  used to raise `KeyError` at import time, crashing server boot before `core.verify` could report it
  as unavailable. `ai_operations_spec.py` now exposes `schema_resource_content()`/
  `list_schema_resources()` that both derive from what actually loaded, so `resources/list` and
  `resources/read` degrade consistently with everything else.
- `examples/sample_workflow.json` previously failed `Workflow` validation outright (missing
  `start_time`) and was too thin to exercise the recommendation engine even if fixed. It's now a
  valid, richer workflow (6 steps, real metrics) that produces real `lens.analyze_workflow`/
  `lens.report_summary` recommendations (excessive retrieved chunks, a duplicate tool call, long
  conversation history) instead of an empty or erroring result.
- `handle_call_tool` now catches any exception a tool handler raises (e.g. a pydantic
  `ValidationError` from malformed workflow/run input) and returns a structured
  `{"ok": false, "error": ...}` payload instead of letting it propagate past the MCP dispatch boundary.

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
