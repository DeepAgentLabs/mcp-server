# Roadmap

## Vision

Build one public MCP server for the DeepAgentLabs ecosystem that unifies:

- workflow observability from `agenticlens`
- resilience testing from `agentic-chaos`

The result should feel like a coherent platform surface rather than two loosely
connected products.

## Phase 0: Foundation

Status: current

Goals:

- define project identity and packaging
- define MCP registry metadata
- set the package and source tree structure
- identify the first tool contracts

Deliverables:

- `README.md`
- `ROADMAP.md`
- `pyproject.toml`
- `server.json`
- initial `src/` and `tests/` layout

## Phase 1: Minimal MCP Server

Goals:

- create a runnable stdio MCP server
- expose `core.health`
- expose `core.version`
- return stable JSON payloads

Success criteria:

- local start command works
- host can discover at least one tool
- smoke tests cover imports and server boot

## Phase 2: AgenticLens Integration

Goals:

- wire `agenticlens` into the MCP server through adapter functions
- expose a first analysis-oriented tool surface
- support reading workflow JSON artifacts

Possible tools:

- `lens.analyze_workflow`
- `lens.report_summary`

Success criteria:

- a saved workflow artifact can be analyzed through MCP
- recommendations are returned in a host-friendly schema

## Phase 3: Agentic Chaos Integration

Goals:

- wire `agentic-chaos` into the MCP server through adapter functions
- expose fault listing and experiment execution
- return structured experiment results

Possible tools:

- `chaos.list_faults`
- `chaos.run_experiment`

Success criteria:

- a target script or workflow can be exercised with selected faults
- results can be summarized alongside normal run output

## Phase 4: Unified Workflows

Goals:

- combine observability and chaos into joined workflows
- compare baseline and chaos runs
- expose reusable resources and prompts

Possible tools:

- `core.compare_runs`
- `core.export_report`

## Phase 5: Publishing and Adoption

Goals:

- verify PyPI packaging
- publish to PyPI
- authenticate with the MCP Registry
- publish `server.json`
- add CI for package build and registry publishing

## Open Questions

- Which MCP Python SDK will be the long-term foundation?
- Should the first release depend on local sibling checkouts or published PyPI
  releases only?
- Should `deep-agentic-core-mcp` be a thin wrapper package or eventually own
  workflow orchestration logic directly?
- Is stdio-only enough for v0, or do we want a remote deployment path early?
