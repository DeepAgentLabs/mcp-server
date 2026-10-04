# Roadmap

See [ROADMAP_AUDIT.md](ROADMAP_AUDIT.md) for an evidence-based audit of the
claims below against actual source, tests, and release metadata (dated
2026-09-11). It confirmed the phase statuses here are accurate with one
correction: Phase 3d's `sidecar.*` tools are real and tested but were never
released — they landed in commits after the `v0.2.0` tag with no
`CHANGELOG.md` entry or version bump. The "Release Status" line and Phase 3d
entry below have been updated accordingly; see the audit for full detail.

## Release Status

Release version: `0.3.0` (2026-10-04) — see [CHANGELOG.md](CHANGELOG.md).
This release includes HTTP/signup support and Sidecar discovery tools; the
2026-09-11 audit above describes the earlier `0.2.0` release state.

- **Phase 0: Foundation** ✅ Complete
- **Phase 1: Minimal MCP Server** ✅ Complete — `core.health`/`core.version`
  shipped in `0.1.2`
- **Phase 2: Session Management & Diagnostics** ✅ Complete — session state,
  rich `core.health` diagnostics, tool metadata/annotations, `core.verify`,
  and real `prompts/list`/`prompts/get` support all shipped in `0.2.0`
- **Phase 3a: AgenticLens Integration** 🏗️ In progress — `lens.analyze_workflow`
  shipped in `0.1.3`; `lens.report_summary`, `lens.compare_runs`,
  `lens.slo_summary`, and `lens.audit_report` shipped in `0.2.0`
- **Phase 3b: Agentic Chaos Integration** ✅ Complete — `chaos.list_faults`
  shipped in `0.1.3`; `chaos.run_experiment` shipped in `0.2.0`
- **Phase 3d: Agentic Sidecar Discovery** ✅ Complete — `sidecar.status` and
  `sidecar.module_inventory` are included in `0.3.0` as discovery/readiness
  tools. The upstream decision runtime remains unimplemented.
- **Phase 3c: AI Operations Specification Conformance** 🏗️ In progress —
  `spec.validate_artifact` and schema resources shipped in `0.1.3`, ahead of
  where this roadmap originally planned them; remaining work still blocked on
  upstream (see below)
- **Phase 4: Unified Workflows** 🚧 Planned
- **Phase 5: Publishing and Adoption** 🚧 Planned
- **Phase 6: Operational Intelligence** 🚧 Planned

## Local and Hosted Delivery Status

The project maintains one codebase with two entry points: local stdio through
`deep-agentic-core-mcp` and optional multi-user Streamable HTTP through
`deep-agentic-core-mcp-http`. Hosted HTTP uses bearer keys and Redis-backed
user-scoped workflow state; the AWS signup service stores user records and key
hashes in DynamoDB. Remote chaos execution remains disabled.

As of 2026-10-04, the hosted service is running at
`https://mcp.deepagentlabs.io/mcp` with signup at `https://mcp.deepagentlabs.io`.
Transport/signup and Sidecar discovery are included in the `0.3.0` release.

- **Package publishing:** version tags run the full CI matrix and packaging
  checks before publishing to PyPI, creating the GitHub Release, and publishing
  MCP Registry metadata. Adoption work remains in Phase 5.
- **AWS continuous deployment:** the first main-triggered deployment was
  verified successfully on 2026-10-04. Starting with `0.3.0`, AWS deployment
  follows successful PyPI publication in the version-tag release workflow.
  Pushes/merges to `main` and manual CI checks do not deploy AWS.
- **Remaining delivery work:** continue Phase 5 registry/adoption work, and
  improve release rollback and hosted operational coverage. Keep package and
  hosted deployment versions aligned through the shared release tag.

See [CONTRIBUTING.md](CONTRIBUTING.md) for release steps and
[deploy/aws/CI-CD.md](deploy/aws/CI-CD.md) for AWS deployment behavior.

## Cross-Project Dependencies

This server is an orchestration layer across sibling projects, so roadmap
status should explicitly account for upstream and downstream dependencies.

- `agenticlens`
  Provides workflow analysis, evaluation, comparison, and reporting behavior
  surfaced through `lens.*` tools.
- `agentic-chaos`
  Provides resilience/fault injection behavior surfaced through `chaos.*`
  tools.
- `agentic-sidecar`
  Provides decision-supervision and governance behavior. Today the MCP server
  only exposes discovery/readiness information because the sidecar runtime is
  still scaffold-only upstream; richer `sidecar.*` control surfaces depend on
  that package shipping real runtime behavior first.
- `ai-operations-spec`
  Provides the canonical artifact model and validation rules surfaced through
  `spec.*` tools and used as the ecosystem exchange contract.
- `agenticops-control-tower`
  Provides the future operator-facing control plane. Once that sibling package
  ships real APIs, MCP should expose those surfaces as connectors rather than
  reimplementing control-plane behavior locally.

For roadmap work, distinguish:

- `Depends on`: a sibling capability or spec milestone that must exist first.
- `Blocked by`: a hard upstream constraint that prevents shipping the feature.
- `Coordinate with`: sibling repos whose docs, examples, or contracts should
  be updated together.
- `Validate in`: sibling CLIs, fixtures, or adapters that should be checked
  before the item is marked done.

## Definition of Done

A roadmap item is done only when all applicable work is complete:

- implementation is merged and reachable through the intended MCP tool,
  prompt, or resource surface
- tests cover the behavior, including integration boundaries where practical
- user-facing examples and generated docs are added or updated
- `README.md` and this roadmap are updated when the feature changes user
  expectations or milestone status
- sibling-project dependencies and end-to-end checks are recorded for any
  cross-repo tool surface
- release metadata (`pyproject.toml`,
  `src/deep_agentic_core_mcp/__init__.py`, `CHANGELOG.md`) is updated when the
  work is part of a release-ready change set

## Vision

Build one public MCP server for the DeepAgentLabs ecosystem that unifies:

- workflow observability from `agenticlens`
- resilience testing from `agentic-chaos`
- decision-supervision surfaces from `agentic-sidecar`

The result should feel like a coherent platform surface rather than two loosely
connected products.

The product boundary should mirror the PyPI ecosystem:

- `agenticlens` observes, evaluates, explains, and recommends
- `agentic-chaos` injects, validates, tests, and proves resilience
- `agentic-sidecar` governs, challenges, and escalates agent decisions
- `agenticops-control-tower` operates the deployed ecosystem through a control
  plane
- `deep-agentic-core-mcp` exposes those capabilities through one MCP-native
  control surface

At a high level, this MCP server should let a host or agent interact with the
ecosystem in terms of developer needs, not repo boundaries. The surface should
eventually make it easy to:

- inspect a run
- analyze prompts, tools, and retrieval
- compare workflows
- run chaos experiments
- inspect sidecar readiness and governance surface
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

Status: complete

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

Status: complete — `core.health` and `core.version` shipped in 0.1.2.

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

Status: complete, shipped in 0.2.0. In-memory session state
(`services/session.py`, `core.session_state`), rich `core.health`
diagnostics, tool metadata/annotations, `core.verify`, and real
`prompts/list`/`prompts/get` support (the 0.1.3 prompt registry was data
only and was never wired into the server) all landed together.

Goals:

- ✅ add lightweight in-memory session state so sequential tool calls share context
- ✅ expand `core.health` into rich diagnostics (adapter availability, dependency
  versions, loaded tools/resources/prompts, workspace root, last successful calls)
- ✅ add tool metadata and annotations (category, prerequisites, expected duration,
  whether the tool mutates session state)
- ✅ implement prompt registry support — `prompts/list`/`prompts/get` are wired
  into the server, with real arguments and rendered templates
- ✅ add integration verification flow — a `core.verify` tool that checks
  agenticlens, agentic-chaos, agentic-sidecar, and ai-operations-spec
  connectivity and reports readiness

Success criteria:

- ✅ `lens.analyze_workflow` → `lens.compare_runs` → `chaos.run_experiment` can
  share a session (via an optional `session_id` argument) without the client
  resending artifacts — the roadmap's original `lens.profile`/`chaos.run`
  names don't exist as MCP tools, so this is verified against the tool names
  that actually ship
- ✅ `core.health` returns structured diagnostics, not just `{"status": "ok"}`
- ✅ MCP clients can discover tool categories, prerequisites, and output types
  (via `Tool._meta`/`Tool.annotations`)
- ✅ a new contributor can run `core.verify` and see what's connected
- as a prerequisite for the above, adapters now degrade instead of crashing
  server boot when a sibling repo is missing/broken (`AdapterUnavailableError`,
  per-adapter `probe()`) — `core.verify`/`core.health` couldn't report
  "not connected" otherwise

## Phase 3a: AgenticLens Integration

Status: in progress — `lens.analyze_workflow` and the `agenticlens` adapter
layer shipped in 0.1.3; `lens.report_summary`, `lens.compare_runs`,
`lens.slo_summary`, and `lens.audit_report` shipped in 0.2.0, each backed by
real `agenticlens` capability (`MarkdownExporter`, `comparison.runner`,
`evaluation.gate`, `evaluation.html_report`) rather than reimplemented logic.

- wire `agenticlens` into the MCP server through adapter functions
- expose a first analysis-oriented tool surface
- support reading workflow JSON artifacts
- support operational-intelligence features as they land in `agenticlens`
- return provenance-rich responses so MCP clients get explainable outputs

Possible tools:

- [x] `lens.analyze_workflow` — shipped in 0.1.3
- [x] `lens.report_summary` — shipped in 0.2.0
- [x] `lens.compare_runs` — shipped in 0.2.0
- [x] `lens.slo_summary` — shipped in 0.2.0
- [x] `lens.audit_report` — shipped in 0.2.0

Success criteria:

- a saved workflow artifact can be analyzed through MCP
- recommendations are returned in a host-friendly schema
- every finding includes source provenance (step, span, artifact) — not yet
  verified against `lens.analyze_workflow`'s current response shape
- the analyzed artifact remains traceable to the AI Operations Specification
  contract

Remaining work: this phase is functionally complete against agenticlens's
current API surface; provenance verification above is still open.

## Phase 3b: Agentic Chaos Integration

Status: complete, shipped in 0.2.0. `chaos.list_faults` and the
`agentic-chaos` adapter layer shipped in 0.1.3; `chaos.run_experiment`
shipped in 0.2.0, running a workspace-sandboxed target script inside a real
`chaos_session()` (mirroring the agentic-chaos CLI's `chaos run`), with a
`timeout_seconds` guard and a documented limitation that Python cannot force
-kill the worker thread on timeout.

Goals:

- ✅ wire `agentic-chaos` into the MCP server through adapter functions
- ✅ expose fault listing and experiment execution
- ✅ return structured experiment results

Possible tools:

- [x] `chaos.list_faults` — shipped in 0.1.3
- [x] `chaos.run_experiment` — shipped in 0.2.0

Success criteria:

- ✅ a target script or workflow can be exercised with selected faults
- ✅ results can be summarized alongside normal run output
- chaos results are readable as or convertible to AI Operations Specification
  artifacts — still open; `chaos.run_experiment`'s output is `ChaosReport`-shaped
  but not yet run through `spec.validate_artifact`
- [ ] script-path allow/deny-list for `chaos.run_experiment`, layered on top
  of the existing workspace-root confinement — an opt-in instance-level
  allowlist (e.g. `MCP_SERVER_ALLOWED_SCRIPT_GLOBS`) plus a deny-list, modeled
  on `devops-open-agent`'s layered MCP-server allowlist/whitelist/blacklist
  pattern; tracked as a prerequisite for widening `chaos.run_experiment`
  exposure beyond trusted local stdio clients (see Known Limitations)

## Phase 3d: Agentic Sidecar Discovery

Status: complete, included in `0.3.0`. The tools were implemented after the
`v0.2.0` tag (see the historical [ROADMAP_AUDIT.md](ROADMAP_AUDIT.md)).
`agentic-sidecar` remains a scaffold upstream, so this phase exposes discovery
and readiness information rather than a decision runtime.

Goals:

- wire `agentic-sidecar` into the MCP server through a degrading adapter
- expose a first `sidecar.*` surface that is honest about scaffold vs runtime
- let MCP hosts discover the sidecar module/adapters/integrations footprint
  without importing the sibling repo themselves

Tools:

- [x] `sidecar.status`
- [x] `sidecar.module_inventory`

Success criteria:

- `core.verify` and `core.health` report `agentic-sidecar` separately from the
  other siblings
- MCP clients can distinguish "package importable" from "runtime implemented"
- the server surfaces current scaffold inventory without reimplementing sidecar
  logic locally

## Phase 3c: AI Operations Specification Conformance

Status: in progress — delivered ahead of where this roadmap had it planned.

Goals:

- wire `ai-operations-spec` into the MCP server through adapter functions
- expose structural and semantic artifact validation
- expose the specification's schemas as MCP resources so hosts can fetch the
  contract directly instead of vendoring copies

Delivered in 0.1.3:

- `spec.validate_artifact` tool, validating workflow/run artifacts against
  the AI Operations v0.4 draft
- MCP resource endpoints for the v0.4 workflow, run, and common schemas
- a `resources/read` handler returning resource contents
- an `ai-operations-spec` adapter layer

Remaining work (re-checked during the 0.2.0 pass, still blocked upstream):

- validation coverage beyond the v0.4 draft (versioned/multi-version support)
  — `ai-operations-spec`'s `v0.1`–`v0.3` directories don't have populated
  `schemas/` yet, only `v0.4` does, so there's nothing to switch between
- conformance-style reporting that distinguishes spec-defined pass/fail rules
  from server-specific presentation, mirroring `agenticlens`'s own
  conformance direction — no defined conformance-rule format exists upstream
  to wire against yet
- resource coverage for additional artifact and schema types as the
  specification grows

## Phase 4: Unified Workflows

Goals:

- combine observability and chaos into joined workflows
- compare baseline and chaos runs
- expose reusable resources and prompts
- surface incident, evaluation, and readiness evidence through one interface
- expose a high-level control surface for the main developer questions:
  what happened, what changed, what failed, and is this workflow ready
- define the first Control Tower integration path once
  `agenticops-control-tower` ships a real control API, starting with
  read-only operator queries and keeping authorization-sensitive write
  operations out of scope until audit/auth boundaries are clear

Possible tools:

- `core.compare_runs`
- `core.export_report`
- `core.incident_summary`
- `core.release_check`
- `control_tower.list_agents`
- `control_tower.list_unhealthy_agents`
- `control_tower.capability_summary`

Control Tower integration notes:

- `deep-agentic-core-mcp` should connect to `agenticops-control-tower` as a
  control-plane connector, not reimplement control-plane logic locally
- first scope should mirror `agenticops-control-tower`'s planned MCP
  connector direction: inventory, health, version, and posture queries
- write-capable Control Tower actions should come only after the sibling
  package exposes stable authorization and audit semantics

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
- ~~Is stdio-only enough for v0, or do we want a remote deployment path early?~~
  Resolved: an optional Streamable HTTP transport (`transport_http.py`, the
  `http` extra) now ships alongside stdio, sharing the same tool surface.
  HTTP now requires per-user bearer credentials and shared Redis state,
  enforces user isolation and storage quotas, and uses stateless transport.
  AWS infrastructure now includes a DynamoDB-backed public key signup portal,
  immediate key rotation/revocation, and migration of existing user identities.
  Verified email signup, account recovery, OAuth onboarding, and billing remain future work.

## Known Limitations

- ~~Tool handlers are synchronous and block the event loop.~~ Resolved:
  `handle_call_tool` now runs each handler via `asyncio.to_thread()`, so a
  slow call (notably `chaos.run_experiment`) no longer blocks the event loop
  from serving other concurrent clients — a precondition for the Streamable
  HTTP transport added below.
- **`chaos.run_experiment` has no allowlist beyond workspace-path
  confinement.** Any script inside the workspace root can still be executed
  under stdio/local use, and the tool still doesn't authenticate or
  authorize the calling client itself (see `SECURITY.md`). The remote-transport
  gate disables this tool by default. Authenticated HTTP dispatch now always
  rejects execution, including with the legacy remote-chaos override enabled.
  Isolated workers and explicit authorization remain prerequisites for a
  future remote execution feature.

## Documentation Backlog

Identified while writing `docs/tools.md` in `0.2.0` and re-flagged by a
subsequent review; deliberately deferred rather than missed. All three are
about *using* the server (a new integrator's first fifteen minutes), not
about the tool surface itself, which `docs/tools.md` already covers:

- **`docs/getting-started.md`** — install + MCP client config (e.g. Claude
  Desktop) + a first `core.health`/`lens.analyze_workflow` call, walked
  through end to end.
- **Session workflow walkthrough** — `lens.analyze_workflow` ->
  `lens.compare_runs` -> `chaos.run_experiment` sharing a `session_id`.
  Phase 2's headline feature (see above); currently only demonstrated in
  test code (`tests/test_server.py`), not in any doc a new integrator would
  read.
- **Prompts overview** — what the 3 shipped prompts (`lens.workflow_summary`,
  `lens.compare_summary`, `chaos.experiment_brief`) actually render, given an
  example set of arguments. Currently only discoverable by reading
  `prompts/registry.py` directly.

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
