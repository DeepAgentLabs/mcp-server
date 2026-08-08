# Roadmap

## Vision

Build one public MCP server for the DeepAgentLabs ecosystem that unifies:

- workflow observability from `agenticlens`
- resilience testing from `agentic-chaos`

The result should feel like a coherent platform surface rather than two loosely
connected products.

The product boundary should mirror the PyPI ecosystem:

- `agenticlens` observes, evaluates, explains, and recommends
- `agentic-chaos` injects, validates, tests, and proves resilience
- `deep-agentic-core-mcp` exposes those capabilities through one MCP-native
  control surface

At a high level, this MCP server should let a host or agent interact with the
ecosystem in terms of developer needs, not repo boundaries. The surface should
eventually make it easy to:

- inspect a run
- analyze prompts, tools, and retrieval
- compare workflows
- run chaos experiments
- summarize incidents and reliability findings
- expose readiness evidence through one MCP-native interface

The MCP server should treat the **AI Operations Specification** as the
canonical contract for ecosystem data exchange.

That means:

- MCP tools should read AI Operations Specification artifacts such as
  `workflow.json`
- MCP responses should be grounded in the same operational objects and semantic
  events
- exports or derived reports should come from the shared specification rather
  than package-specific hidden formats

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

## Phase 2: Session Management & Diagnostics

Goals:

- add lightweight in-memory session state so sequential tool calls share context
- expand `core.health` into rich diagnostics (adapter availability, dependency
  versions, loaded tools/resources, config validation, last successful runs)
- add tool metadata and annotations (category, prerequisites, expected duration,
  whether the tool mutates session state)
- implement prompt registry support — expose reusable prompt templates as MCP
  prompts/resources for analysis, comparison, and experiment workflows
- add integration verification flow — a `core.verify` tool that checks
  agenticlens and agentic-chaos connectivity and reports readiness

Success criteria:

- `lens.profile` → `chaos.run` → `lens.compare` can share a session without
  the client resending artifacts
- `core.health` returns structured diagnostics, not just `{"status": "ok"}`
- MCP clients can discover tool categories, prerequisites, and output types
- a new contributor can run `core.verify` and see what's connected

## Phase 3: AgenticLens Integration

- wire `agenticlens` into the MCP server through adapter functions
- expose a first analysis-oriented tool surface
- support reading workflow JSON artifacts
- support operational-intelligence features as they land in `agenticlens`
- return provenance-rich responses so MCP clients get explainable outputs

Possible tools:

- `lens.analyze_workflow`
- `lens.report_summary`
- `lens.compare_runs`
- `lens.slo_summary`
- `lens.audit_report`

Success criteria:

- a saved workflow artifact can be analyzed through MCP
- recommendations are returned in a host-friendly schema
- every finding includes source provenance (step, span, artifact)
- the analyzed artifact remains traceable to the AI Operations Specification
  contract

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
- chaos results are readable as or convertible to AI Operations Specification
  artifacts

## Phase 4: Unified Workflows

Goals:

- combine observability and chaos into joined workflows
- compare baseline and chaos runs
- expose reusable resources and prompts
- surface incident, evaluation, and readiness evidence through one interface
- expose a high-level control surface for the main developer questions:
  what happened, what changed, what failed, and is this workflow ready

Possible tools:

- `core.compare_runs`
- `core.export_report`
- `core.incident_summary`
- `core.release_check`

## Phase 5: Publishing and Adoption

Goals:

- verify PyPI packaging
- publish to PyPI
- authenticate with the MCP Registry
- publish `server.json`
- add CI for package build and registry publishing

## Phase 6: Operational Intelligence

Goals:

- add guided onboarding wizard for first-time setup
- add saved artifact browsing through MCP resources
- add explainable report recall and session history
- add report and investigation narrative generation

## Open Questions

- Which MCP Python SDK will be the long-term foundation?
- Should the first release depend on local sibling checkouts or published PyPI
  releases only?
- Should `deep-agentic-core-mcp` be a thin wrapper package or eventually own
  workflow orchestration logic directly?
- Is stdio-only enough for v0, or do we want a remote deployment path early?

## Capability North Star

Over time, the MCP surface should expose the ecosystem around a few clear
domains:

- run and workflow analysis
- LLM, prompt, and context analysis
- tool, MCP, and retrieval analysis
- agent and memory analysis
- reliability and incident analysis
- resilience testing and chaos execution
- evaluation and readiness reporting

Developers contributing to the MCP server should be able to ask:

`Which AI Operations Specification object or artifact does this tool read,
return, or transform?`
