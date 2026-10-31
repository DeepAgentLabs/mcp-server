# Roadmap

See [ROADMAP_AUDIT.md](ROADMAP_AUDIT.md) for an evidence-based audit of the
claims below against actual source, tests, and release metadata (dated
2026-09-11). It confirmed the phase statuses here are accurate with one
correction: Phase 3d's `sidecar.*` tools are real and tested but were never
released — they landed in commits after the `v0.2.0` tag with no
`CHANGELOG.md` entry or version bump. The "Release Status" line and Phase 3d
entry below have been updated accordingly; see the audit for full detail.

## Release Status

Release version: `0.5.1` (2026-10-31) — see [CHANGELOG.md](CHANGELOG.md). It adds local
`tower.runbook*` tools for Control Tower 0.9 runbooks ([guide](docs/tower-0.9-runbooks.md)).
`0.5.0` (2026-10-31) completes
Phase 5 with hosted access control: per-key tool permissions (allow/deny globs,
expiry, task scope) enforced at dispatch, revocation and policy re-checked for
queued calls, retries and existing connections, correlated
`mcp.access-decision.v1` evidence, `core.access_status`, and the
`deep-agentic-core-mcp-admin` operator CLI ([guide](docs/access-control.md)).
Hosted image pins and sibling dependency ranges are unchanged.
`0.4.1` (2026-10-19) added Sidecar 0.9 discovery and manual AWS deployment.
The 0.4.0 release completed Phase 4: `core.compare_runs`, a fail-closed `core.release_check`
over Lens, Evals and Chaos evidence, `core.incident_summary` and
`core.export_report` ([guide](docs/unified-workflows.md)). Hosted image pins and
sibling dependency ranges are unchanged.
`0.4.3` adds read-only `lens.optimization_analyze` and pins the hosted images to `agenticlens` 0.11.0.
`0.3.14` syncs the bundled native Evals schemas to `agentic-evals` 0.9.0 and pins
it in the hosted images. `0.3.13` pinned them to `agentic-chaos` 0.8.0.
`0.3.12` adds read-only `lens.routing_decide` and pins the hosted images to `agenticlens` 0.10.0.
`0.3.11` adds `lens.modelfit_recommend` for AgenticLens 0.9.0 (v0.7 ModelFit)
and pins the hosted images to `agenticlens` 0.9.0.
`0.3.10` pins the hosted images to `agentic-chaos` 0.7.0.
`0.3.9` adds `lens.suite_from_traces` and `lens.suite_check` for AgenticLens
0.8.0 (v0.6 test-suite and dataset management) and pins the hosted images to
`agenticlens` 0.8.0.
`0.3.8` adds offline `evals.validate_artifact` against the published Evals 0.7.2
report and gate schemas.
`0.3.7` moves the hosted images to `agentic-chaos` 0.6.0. Its AIOS run export
adds call counts and the escaped error to the producer extension; MCP tools are
unchanged.
`0.3.5` adds `lens.diagnose_run` and `lens.score_analysis` for AgenticLens
0.7.0 (v0.5 diagnosis) and pins the hosted images to `agenticlens` 0.7.0 and
`agentic-chaos` 0.5.3.

`0.3.3` completed Phase 3: provenance on every `lens.analyze_workflow`
finding (3a), AIOS run export and a script allow/deny policy for chaos
experiments (3b), and `spec_version`-routed validation with rule-cited
conformance reports (3c). That release paired with sibling patch releases
`agenticlens` 0.6.1, `agentic-chaos` 0.5.1 and `ai-operations-spec` 0.5.1.
v0.3.2 verified Chaos v0.5 compatibility; v0.3.1 corrected installed Sidecar API
discovery. The 2026-09-11 audit above describes the earlier `0.2.0` release state.

- **Phase 0: Foundation** ✅ Complete
- **Phase 1: Minimal MCP Server** ✅ Complete — `core.health`/`core.version`
  shipped in `0.1.2`
- **Phase 2: Session Management & Diagnostics** ✅ Complete — session state,
  rich `core.health` diagnostics, tool metadata/annotations, `core.verify`,
  and real `prompts/list`/`prompts/get` support all shipped in `0.2.0`
- **Phase 3a: AgenticLens Integration** ✅ Complete — five `lens.*` tools
  (`0.1.3`/`0.2.0`); every `lens.analyze_workflow` finding carries verified
  artifact/step/span provenance in `0.3.3`
- **Phase 3b: Agentic Chaos Integration** ✅ Complete — `chaos.list_faults`
  (`0.1.3`), `chaos.run_experiment` (`0.2.0`); AIOS run export,
  `chaos.export_aios_run`, and the script allow/deny policy in `0.3.3`
- **Phase 3d: Agentic Sidecar Discovery** ✅ Complete — `sidecar.status` and
  `sidecar.module_inventory` are included in `0.3.0` as discovery/readiness
  tools. Sidecar has a local decision runtime; MCP integration with its
  enforcement and live operator controls remains planned.
- **Phase 3c: AI Operations Specification Conformance** ✅ Complete —
  `spec.validate_artifact` and schema resources (`0.1.3`); `spec_version`
  routing per the v0.5 compatibility rules, rule-cited conformance reports, and
  catalog resources in `0.3.3`
- **Phase 4: Unified Workflows** ✅ Complete — unified comparison,
  fail-closed release-check, incident-summary and report-export tools in
  `0.4.0`; local Tower connector since `0.3.6`
- **Phase 5: Publishing and Adoption** ✅ Complete — PyPI, GitHub Release and
  MCP Registry release automation; hosted access control (tool-level
  permissions, revocation at dispatch, correlated denial evidence, operator
  revocation path) in `0.5.0`. Hosted Tower credentials, an authenticated
  Sidecar stop/revoke bridge and the shared AIOS evidence format moved to
  Phase 6 on 2026-10-31 because each depends on sibling work first
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
Since `0.4.3` the hosted image installs `agenticlens` 0.11.0 (`0.4.2` installed Lens 0.10.0 and `agentic-evals` 0.10.0). Since `0.3.14` it installed `agentic-evals` 0.9.0, `agentic-chaos`
0.8.0, and the `ai-operations-spec` 0.5.1 schemas and catalogs, fetched at a
pinned commit and checksum-verified. (`0.3.12` installed Chaos 0.7.0; `0.3.9`–`0.3.10` installed Lens 0.8.0; `0.3.7`–`0.3.8` installed Lens 0.7.0; `0.3.5`–`0.3.6` installed Chaos 0.5.3;
`0.3.4` installed Lens 0.6.1 and Chaos 0.5.1.) Chaos is installed only for its exporter and fault catalog; HTTP still
rejects `chaos.run_experiment`. `tests/test_hosted_image.py` keeps these pins in step with
the adapters. All Phase 3 features are therefore available both locally and
hosted, except chaos execution, which stays local-only.

- **Package publishing:** version tags run the full CI matrix and packaging
  checks before publishing to PyPI, creating the GitHub Release, and publishing
  MCP Registry metadata. Adoption work remains in Phase 5.
- **AWS continuous deployment:** the first main-triggered deployment was
  verified successfully on 2026-10-04. Starting with `0.3.0`, AWS deployment
  follows successful PyPI publication in the version-tag release workflow.
  Pushes/merges to `main` and manual CI checks do not deploy AWS.
- **Remaining delivery work:** Phase 6 containment integrations (hosted Tower
  credentials, Sidecar stop/revoke bridge, AIOS access evidence), release
  rollback and hosted operational coverage. Hosted access control shipped in
  `0.5.0`. Keep package and
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
  exposes installed API readiness and module inventory. Sidecar v0.7 adds local
  task status/audit/operator APIs; exposing them through MCP requires a separate
  authenticated task-scoped bridge. Discovery is not a live task connection.
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

### Phase 3 sibling dependencies (recorded for `0.3.3`)

| Item | Depends on | Validate in |
|---|---|---|
| 3a finding provenance | `agenticlens>=0.6.1` (model-swap and chaos-impact findings name their step) | `tests/test_lens_provenance.py`; agenticlens `tests/test_recommendation_provenance.py` |
| 3b AIOS run export | `agentic-chaos>=0.5.1` (`agentic_chaos.export.to_aios_run`) | `tests/test_chaos_aios_export.py`; chaos `tests/test_export_aios.py` (v0.4 schema + spec semantic checker) |
| 3b script policy | none (server-local) | `tests/test_chaos_script_policy.py` |
| Lens diagnosis tools (`0.3.5`) | `agenticlens>=0.7.0` (`agenticlens.diagnosis`, `analyze_scores`) | `tests/test_lens_diagnosis.py`; agenticlens `tests/test_diagnosis_engine.py`, `tests/test_score_analysis.py` |
| Lens suite tools (`0.3.9`) | `agenticlens>=0.8.0` (`agenticlens.suites`) | `tests/test_lens_suites.py`; agenticlens `tests/test_suites_*.py` |
| Lens ModelFit tool (`0.3.11`) | `agenticlens>=0.9.0` (`agenticlens.modelfit`) | `tests/test_lens_modelfit.py`; agenticlens `tests/test_modelfit_*.py`, `tests/test_examples_modelfit.py` |
| 3c version routing and conformance | `ai-operations-spec>=0.5.1` (`specification/v0.4/conformance-rules.json`, `specification/v0.5/compatibility.json`) | `tests/test_spec_conformance.py`; spec `tests/test_conformance_catalogs.py` |

Each dependency degrades rather than breaking boot. With an older agenticlens,
unattributed findings report `provenance.resolved=false`. With
`agentic-chaos` 0.5.0 (still exercised by the pinned CI lane), experiments run
but return `aios_export.available=false`. With a spec checkout that predates
the catalogs, `conformance.catalog_available=false`, but issues still carry
their rule IDs.

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

Status: complete in 0.3.3. `lens.analyze_workflow` and the `agenticlens`
adapter layer shipped in 0.1.3; `lens.report_summary`, `lens.compare_runs`,
`lens.slo_summary`, and `lens.audit_report` shipped in 0.2.0, each backed by
real `agenticlens` capability (`MarkdownExporter`, `comparison.runner`,
`evaluation.gate`, `evaluation.html_report`) rather than reimplemented logic.
0.3.3 closes the provenance criterion below.

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
- ✅ every finding includes source provenance (step, span, artifact) — each
  recommendation's `provenance` block names the artifact (`workflow_id` when
  the artifact carries one, plus a canonical-JSON `sha256` digest), the workflow
  step (`id`, `name`, `type`, `index`, `id_in_artifact`), the evidence span IDs
  and sources, and the producer. `resolved` is true only when that step and
  every cited span exist in the artifact. `provenance_summary` counts resolved
  findings. Upstream, `agenticlens` 0.6.1 makes every default recommender name
  its step (model swap and chaos impact did not before).
- the analyzed artifact remains traceable to the AI Operations Specification
  contract

No open Phase 3a work remains.

## Phase 3b: Agentic Chaos Integration

Status: complete. 0.3.3 closes the two remaining criteria: AIOS conversion
and the script allow/deny policy. `chaos.list_faults` and the
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
- ✅ chaos results are convertible to AI Operations Specification artifacts —
  `chaos.run_experiment` attaches `aios_run`, a v0.4-draft Run produced by
  `agentic-chaos`'s own exporter (`>=0.5.1`, so the mapping stays with the
  producer). The result is validated through the same path as
  `spec.validate_artifact` (`aios_export.aligned`, rule-cited `issues`).
  `chaos.export_aios_run` converts a saved or session report without running
  code, so it is also offered over HTTP.
- [x] script-path allow/deny-list for `chaos.run_experiment`, layered on top
  of the existing workspace-root confinement: the opt-in
  `DEEP_AGENTIC_CORE_MCP_ALLOWED_SCRIPT_GLOBS` allowlist plus
  `DEEP_AGENTIC_CORE_MCP_DENIED_SCRIPT_GLOBS`. Deny always wins, and
  `.venv`, `site-packages` and `.git` paths are always denied. `core.health`
  reports the active policy. The policy narrows what local stdio clients can
  run. It is not a sandbox, and HTTP still rejects execution (see Known
  Limitations).

## Phase 3d: Agentic Sidecar Discovery

Status: complete, included in `0.3.0`. The tools were implemented after the
`v0.2.0` tag (see the historical [ROADMAP_AUDIT.md](ROADMAP_AUDIT.md)).
Sidecar has an implemented decision runtime and v0.7 local operations APIs.
This MCP phase exposes installed API discovery/readiness without creating or
connecting a live task or proxying operator controls.

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
- MCP clients can distinguish package importability, installed runtime APIs and
  the absence of a live task/control connection
- the server surfaces installed module inventory without reimplementing sidecar
  logic locally

## Phase 3c: AI Operations Specification Conformance

Status: complete in 0.3.3 — the upstream blockers below closed in
`ai-operations-spec` 0.5.1.

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

Delivered in 0.3.3 (previously blocked upstream):

- ✅ versioned/multi-version support. Schema sets load per `spec_version`
  marker from the spec's `specification/v0.5/compatibility.json`, and every
  artifact is validated against the set its own marker names. Following the v0.5
  consumer rules, an unpublished marker is rejected, never re-validated
  against a different version. The response's `compatibility` block gives the
  decision and the cited row (`AIOS-0.5-V01`–`V06`). Today the spec publishes
  one set (`0.4-draft`). A set published for another marker is reported as
  `published_unchecked_versions` and its artifacts are rejected until this server
  implements that version's rules; nothing is ever checked with v0.4 rules by mistake.
- ✅ conformance-style reporting. `conformance` lists every rule from
  `specification/v0.4/conformance-rules.json` with `pass` / `fail` /
  `not_evaluated` / `not_applicable` status, and labels each issue with its
  rule ID (`AIOS-0.4-P01`–`P12`, `X01`, `U02`, `E01`, ...). Process
  obligations are never reported as passing. Server presentation (`ok`,
  `claim`, `schema_errors`, `semantic_errors`, `server`) is kept separate and
  labeled as such. The semantic checks now also enforce P12 (retry attempt
  identity and linking) and X01 for Workflow references.
- ✅ resource coverage. Resources are generated for every loaded schema set,
  plus `resource://specs/aiops/v0.4/conformance-rules` and
  `resource://specs/aiops/v0.5/compatibility`.

Future spec milestones (new schema sets, frozen markers) need a newer
`ai-operations-spec` and an MCP release that adds that version's checker.

## Phase 4: Unified Workflows

Status: ✅ complete as of `0.4.0`. The unified workflows compose existing
Lens, Evals, Chaos and session APIs, and the local Control Tower connector has
shipped since `0.3.6`. The access-containment items (authenticated
stop/revoke, tool-level authorization, correlated denial evidence) were moved
to Phase 5 on 2026-10-19: they protect hosted users rather than add workflows,
and they depend on spec, Sidecar and Tower work first.

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

Delivered in `0.4.0` ([guide](docs/unified-workflows.md)):

- `core.compare_runs` — the `lens.compare_runs` path, stored for the release check
- `core.release_check` — fails closed: evaluation reports go through the Evals
  release gate (every `GateConfig` threshold, unknown keys rejected),
  comparisons are validated with the Lens comparison model, chaos evidence must
  be a `chaos.run_experiment` report, and `required_evidence` (default: all
  three) turns absent evidence into a blocking `missing` gate
- `core.incident_summary` — failure signals only, including blocked gates
- `core.export_report` — MCP-local `mcp.unified-report.v1` envelope, not an
  AIOS artifact; a shared release-evidence artifact would be specified in
  `ai-operations-spec` first
- `resource://workflows/release-check` and the `core.release_check` prompt
- [`examples/unified_release_check.py`](examples/unified_release_check.py)

The Control Tower tools ship as `tower.*` (local stdio only) rather than the
`control_tower.*` names sketched above.

Control Tower integration notes:

- `deep-agentic-core-mcp` should connect to `agenticops-control-tower` as a
  control-plane connector, not reimplement control-plane logic locally
- first scope should mirror `agenticops-control-tower`'s planned MCP
  connector direction: inventory, health, version, and posture queries
- write-capable Control Tower actions should come only after the sibling
  package exposes stable authorization and audit semantics

## Phase 5: Publishing and Adoption

Status: ✅ complete as of `0.5.0` ([guide](docs/access-control.md)).

Publishing goals (in place):

- ~~verify PyPI packaging~~ ✅
- ~~publish to PyPI~~ ✅ version-tag releases
- ~~authenticate with the MCP Registry~~ ✅
- ~~publish `server.json`~~ ✅
- ~~add CI for package build and registry publishing~~ ✅ `release-pypi.yml`

Hosted access control (moved from Phase 4; see
[Access containment and evidence](#access-containment-and-evidence-planned-extensions)):

- ~~tool-level permissions per hosted key (allow/deny lists, optional task
  scope and expiry), enforced in `handle_call_tool`, configurable first through
  the key-store configuration and then in the hosted user store~~ ✅ `0.5.0`:
  `services/access_policy.py`; environment `{key, permissions}` entries,
  Supabase `mcp.users.permissions` and DynamoDB `USER#` `permissions`
- ~~revocation and permissions re-checked at dispatch, covering queued calls,
  retries and existing sessions; in-flight calls are not cancelled~~ ✅ `0.5.0`:
  re-authorized after the user's session lock is acquired
  (`tests/test_access_dispatch.py`)
- ~~correlated access-denial, revocation-acknowledgement and dispatch/completion
  evidence for Tower~~ ✅ `0.5.0` as the MCP-local `mcp.access-decision.v1`
  record. The shared format in `ai-operations-spec` moves to Phase 6
- ~~an independent operator path~~ ✅ `0.5.0`: `deep-agentic-core-mcp-admin
  revoke|set-permissions` by user ID with store credentials. Tower's existing
  `MCPAccessRevoker` now also stops queued calls
- authenticated Sidecar stop/revoke bridge → Phase 6 (**depends on** a Sidecar
  task-scoped runtime control API reachable from MCP)
- per-user Tower credentials so hosted MCP can serve `tower.*` tools → Phase 6
  (**coordinate with** `agenticops-control-tower` hosted authentication)

Delivered in `0.5.0`:

- `core.access_status` — the caller's policy, expiry, task scope and permitted tools
- hosted `tools/list` filtered by the caller's policy
- `deep-agentic-core-mcp-admin` — `show`, `set-permissions`, `clear-permissions`, `revoke`
- [`examples/hosted_access_status.py`](examples/hosted_access_status.py)
- CI runs the PostgreSQL store tests against a `postgres:16` service

## Phase 6: Operational Intelligence

Goals:

- containment integrations moved from Phase 5: hosted `tower.*` with per-user
  Tower credentials; an authenticated Sidecar stop/revoke bridge; emitting the
  AIOS access-evidence format once `ai-operations-spec` defines it (replacing or
  mapping `mcp.access-decision.v1`)

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
- **`chaos.run_experiment` is not sandboxed.** Workspace confinement plus the
  `0.3.3` allow/deny glob policy limit *which* scripts run, but not what a
  script can do once running. The tool still doesn't authenticate or
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

## Access containment and evidence (planned extensions)

Added 2026-10-11; moved from Phase 4 to Phase 5 on 2026-10-19. Hosted bearer authentication, key replacement/revocation and
remote chaos restrictions exist. They do not terminate running agents or revoke
unrelated downstream credentials.

- [x] Phase 5 (`0.5.0`): enforce access outside the LLM at dispatch, including
      queued calls, retries and existing sessions after revocation. The effective
      revocation point is the dispatch re-check after the session lock; in-flight
      calls are not cancelled. Authenticated Sidecar stop/revoke → Phase 6.
- [x] Phase 5 (`0.5.0`): deterministic tool-level authorization and delegated task
      scopes; denied tools are rejected regardless of model or client requests.
      Tests cover cross-user access, direct-call bypass and revoked/expired authority.
- [x] Keep an independently authorized operator revocation path after the agent's
      key is revoked (`deep-agentic-core-mcp-admin revoke`); local stdio trust is
      documented separately from hosted HTTP auth (`docs/access-control.md`).
- [ ] Phase 3a/6: expose producer policy/action correlation and Lens integrity
      verification, including failed/unknown status. Schema validity is not
      cryptographic verification. **Blocked by** `agenticlens`: integrity-protected
      export/verification is still an open item on its roadmap, so there is no
      producer API to expose yet. This is a planned safety extension; it is not
      part of the core Phase 3a scope that `0.3.3` completes (finding provenance
      is digest-based traceability, not tamper evidence).
- [x] Phase 5 (`0.5.0`): emit correlated access denials, revocation
      acknowledgements and dispatch/completion evidence (MCP-local
      `mcp.access-decision.v1`). Phase 6: the shared AIOS format for Tower and
      containment scoring.
- [ ] Validate with Chaos/Evals fixtures for revoked keys, denied tools, injected
      instructions, queued dispatch and incomplete evidence. Preserve the remote
      arbitrary-chaos execution restriction until sandbox requirements are met.

Shared authority/evidence semantics belong in AI Operations Specification;
MCP remains the access/composition layer, not a second policy or audit engine.

## Sidecar 0.8 interoperability

MCP server 0.3.5 retains connectivity, discovery and transport ownership.
Sidecar 0.8 adds a client adapter and a separate-process MCP 2.3.0 gateway example
with server-side enforcement. This does not enable remote operator bridging
in this server or expose shared/exclusive configuration through public tools.

Sidecar 0.8 provides Shared/Exclusive context-only, guardrails-only or combined
configuration, explicit host context delivery and mandatory guardrail composition.
Exclusive rules cannot weaken shared restrictions. Cross-framework privacy,
revocation and delegated authority remain v0.9 validation; stable schemas remain
v1.0. Native correlated Lens readback requires Lens 0.7.1. All sibling packages
stay optional; no dependency floor is increased without a runtime requirement.
See the [Sidecar integration contract](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/integrations.md).

## Tower connector delivered in 0.3.6

The first Phase 4 Control Tower integration ships alongside Tower 0.7.0, which
combines its Phase 6/6A: twelve local stdio tools over real authenticated HTTP
queries and incident transitions, separate reader/writer credentials, and a cited
investigation prompt. Human approval stays in Tower HTTP/CLI. Hosted calls are
rejected until per-user Tower credentials exist. MCP remains usable without Tower.
Unified cross-engine workflows shipped in `0.4.0`, completing Phase 4. Hosted
Tower credentials and access containment are Phase 5 work.
See [setup](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/main/docs/mcp-connector.md).

## Native Evals contract validation — MCP 0.3.8

Published Evals 0.7.2 report and gate schemas are now enforced in the native
consumer paths. Validation runs offline using bundled upstream contracts;
invalid artifacts fail with field-level diagnostics. Native verdicts and
AIOS conformance remain distinct. See [behavior, examples and migration](docs/evals-report-contract.md).

Agentic Evals 0.7.2 publishes native report (`schema_version: "1.0"`) and
gate-decision JSON Schemas, with offline `report_schema()` and
`gate_decision_schema()` accessors. Contract 1.x evolves additively; readers
should tolerate unknown fields. MCP spec.validate_artifact validates AIOS artifacts, not the native Evals schemas. Dedicated Evals tools and AIOS evaluation evidence export remain future work.

See the [contract, examples and compatibility policy](https://github.com/DeepAgentLabs/agentic-evals/blob/main/docs/report-contract.md). Existing dependency
ranges remain sufficient; using the new accessors directly requires
`agentic-evals>=0.7.2`. This documentation alignment needs no sibling patch release.

## AgenticLens 0.8.0 suite management

AgenticLens 0.8.0 delivers its v0.6 milestone: `agenticlens.suites` and
`agenticlens suite` build regression suites from CSV/JSON imports, production
traces and user feedback. It masks PII by default before storage (`--no-mask`
opts out), detects duplicates and
conflicting labels, adds synthetic variations and stable splits, records
reviews, and approves suites into immutable, hash-verified versions that CI
verifies, exports and evaluates. Suites stay plain agentic-evals `TestSuite`
files.

MCP 0.3.9 adds two read-only, artifact-in/artifact-out tools:
`lens.suite_from_traces` (draft cases from successful runs, PII masked by
default, skipped runs with reasons) and `lens.suite_check` (summary,
duplicates, unmasked-PII locations and the approval checks Lens would run).
Neither stores anything; approval and the immutable store stay local CLI/API
operations. Hosted images pin `agenticlens==0.8.0`.

See the [suite management guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.8.0/docs/suite-management.md).

## Evals 0.8.0 CLI interoperability

Evals 0.8.0 CLI JSON reports and gate decisions retain the 0.7.2 wire contract and validate with `evals.validate_artifact`. The bundled upstream 0.7.2 schemas and pinned contract-test dependency remain the compatibility baseline. JUnit and Markdown are presentation formats, not native validator inputs. This release adds no MCP execution tool or runtime dependency.

See [CLI usage and compatibility](docs/evals-0.8-cli.md).

## Evals 0.9.0 judge reliability (MCP 0.3.14)

Evals 0.9.0 adds optional judge (`summary.judge`), live-target (`summary.live`)
and per-case `target_status` fields to native report schema 1.0. MCP 0.3.14
re-syncs the bundled upstream schemas from `agentic-evals==0.9.0` (the
contract-test dev pin) and pins the hosted images to it, so
`evals.validate_artifact` enforces the new fields offline. No tool is added or
changed; validation never recomputes a gate. See
[the compatibility note](docs/evals-0.9-judge-reliability.md).

## Evals 0.10.0 evaluation evidence

Agentic Evals 0.10.0 exports evaluation reports as AIOS `0.4-draft`
`evaluation` evidence merged into an existing Run. `spec.validate_artifact`
reports those Runs as aligned (`AIOS-0.4-P08` passing), and a new test checks
this against the installed Evals. MCP 0.4.2 pins `agentic-evals==0.10.0` in
hosted images and development. Native schemas are unchanged, so
`evals.validate_artifact` needs no sync. See
[the compatibility note](docs/evals-0.10-aios-evidence.md).

## Chaos 0.7.0 interoperability

Chaos 0.7.0 adds sequential fault cascades, deterministic monotonic breaking-point
search, synthetic response poisoning (including prompt/tool-response instruction
and policy-bypass payloads), and explicit-price retry cost estimates. Native
child event IDs and fault types remain intact; cascade IDs/stages and poisoning
strategy/payload/seed are additive event detail. Existing report readers and
AIOS exports remain compatible.

See the [v0.7 guide and offline synthetic example](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.7.0/docs/v0.7.md).
The example includes observed synthetic dispatches and a bypassed negative
control. Injection or recovery alone does not prove containment. No new shared
schema, automatic adapter, hosted execution capability or containment guarantee
is introduced.

MCP 0.3.10 pins published images to Chaos 0.7.0. The existing registry discovers poisoned_response; trusted local scripts can use cascade/search APIs. No new MCP tools are added. Hosted HTTP continues to reject chaos.run_experiment.

## Control Tower 0.7.0 fleet operations

Tower 0.7.0 adds frozen environment/capability targeting, bulk desired settings,
separate approval, durable per-target results and bounded stop/MCP-revocation
acknowledgement through Python, HTTP and CLI. No fleet atomicity or automatic
rollback/resume is claimed. Timed-out/requested commands need host reconciliation.

Local MCP 0.3.6 investigation tools remain compatible. Tower 0.7 bulk endpoints are Python/HTTP/CLI-only: MCP exposes no new fleet write or approval tools, and hosted Tower restrictions remain in force.

Existing optional dependency ranges remain sufficient. No sibling runtime or
native evidence schema changes are required; this documentation alignment needs
no patch release. See the [operator guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.7.0/docs/fleet-operations.md).

See the [local Tower compatibility guide](docs/tower-0.7-fleet-operations.md) for the operator workflow and package boundaries.

## AgenticLens 0.9.0 ModelFit

AgenticLens 0.9.0 delivers its v0.7 milestone: per-task-category model
recommendations from recorded experiment reports, under hard quality, cost,
latency, safety, provider and deployment constraints that fail closed, with
confidence, explanations, alternatives, provider-diverse fallbacks, savings
tied to the experiment evidence, quality risks and a task-level model matrix.

MCP 0.3.11 adds the read-only, artifact-in/artifact-out `lens.modelfit_recommend`
tool and pins hosted images to `agenticlens==0.9.0`. Experiment execution and
runtime routing stay outside MCP; the tool stores nothing.

See the [ModelFit guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.9.0/docs/modelfit.md).

## AgenticLens 0.11.0 optimization (MCP 0.4.3)

`lens.optimization_analyze` ranks evidence-backed optimizations from supplied
AgenticLens `Run` traces: prompt caching and compression, retrieval pruning and
reranking, memory summarization, tool caching, retry policy, redundant steps,
unnecessary handoffs and quality-cost trade-offs between variants. Each
opportunity carries run/span evidence, projected benefit with its basis,
confidence with reasons, and quality risks kept separate. It is advisory and
read-only: it never writes a decision ledger, evaluates outcomes or changes a
prompt, model or tool. Record decisions and evaluate adopted changes with the
local `agenticlens optimize decide|outcome` CLI. Older Lens installs degrade
only this tool with an explicit `agenticlens>=0.11.0` unavailable error.

```json
{
  "traces": [{"...": "complete AgenticLens Run objects with unique run_id"}],
  "config": {"monthly_runs": 30000},
  "baseline_variant_id": "large"
}
```

Hosted images pin `agenticlens==0.11.0`. See the
[Lens optimization guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.11.0/docs/optimization.md).

## AgenticLens 0.10.0 routing (MCP 0.3.12)

`lens.routing_decide` explains a route from a supplied ModelFit `report`,
`request` (`request_id`, `category_id`) and optional routing `policy`. It returns
constraints, confidence, ranked targets, fallback chain and policy/report hashes.
It is read-only in **every mode**, including `enforce`: no model invocation,
callbacks, human approval execution or audit-file writes. `executed` is always
false. An unrouteable decision stays blocked/escalated in the native result.
Older Lens installs degrade only this tool with an explicit unavailable error.

```json
{
  "report": {"...": "supply the complete ModelFit report"},
  "request": {"request_id": "opaque-123", "category_id": "orders"},
  "policy": {"minimum_confidence": "medium"}
}
```

Hosted images pin `agenticlens==0.10.0` and retain `agentic-chaos==0.7.0`.
The workspace source takes precedence over stale copies in sibling virtualenvs.
See the [Lens routing guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.10.0/docs/routing.md)
for callback execution and audit boundaries. Sidecar authority, Tower approvals,
Evals scoring, Chaos faults and AIOS shared schemas remain independently owned.

## Chaos 0.8.0 interoperability

Chaos 0.8.0 adds:

- multi-stage chaos workflows: steps, steady-state health checks, parallel
  branches, approval gates that can be resumed, and reusable templates
- declarative YAML/JSON/TOML experiments, with validation that never executes
  targets and cron schedule previews
- `Scope` explosion-radius control (steps, providers and exclusions) on every
  built-in fault and `cascade()`; custom faults get it by calling
  `BaseFault.__init__`, setting `scope` or overriding `in_scope()`
- a topology fuzzer that weights fault placement by fan-out

Native event IDs and fault types are unchanged. Workflow provenance
(`detail.workflow`) and an optional `ChaosReport.workflow` summary are
additive. A workflow's steps merge into one native report for contracts and
AIOS export.

See the [v0.8 guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.8.0/docs/v0.8.md)
and the [offline examples](https://github.com/DeepAgentLabs/agentic-chaos/tree/v0.8.0/examples/workflows).
Workflow statuses, health checks and fuzz outcomes are resilience evidence.
They are not scores, release gates or proof of containment. No new shared
schema, automatic adapter or hosted execution capability is introduced.

MCP 0.3.13 pins the published images to Chaos 0.8.0. `chaos.export_aios_run`
carries the workflow summary of merged reports in the producer extension, and
the existing registry discovers faults. Workflows, experiments and fuzzing
are Python/CLI orchestration, not new MCP tools. Hosted HTTP continues to
reject `chaos.run_experiment`, so no experiment target is executed by the
hosted service.

## Sidecar 0.9.0 interoperability

Task-authority/delegation and reader-safe summaries are available in Sidecar.
See [compatibility and ownership boundaries](docs/sidecar-0.9.md). Existing
native decisions/correlation stay compatible; no new normative schema is claimed.

## AIOS v0.6 examples and extension guidance

See [AIOS v0.6 compatibility](docs/aios-v0.6.md) for canonical examples,
namespace rules and native contract boundaries. AIOS artifacts remain
`0.4-draft`; no runtime dependency bump or package release is required.

## Control Tower 0.8.0 integration alignment

Tower Phase 8 implements periodic detection, alerts, attributed lifecycle audit
and incident console views. Existing local authenticated tower.* investigation/recovery tools remain compatible. New alert and joined-view endpoints are Tower API/CLI surfaces, not new MCP tools. Hosted Tower credentials remain separate work.

See [compatibility and operator example](docs/tower-0.8-live-operations.md).
No sibling runtime change or patch release is required.

## Chaos 0.9.0 interoperability

Chaos 0.9.0 adds:

- resilience probes: `HttpProbe`, `ResponseQualityProbe`, `LatencyProbe` and
  `FunctionProbe` check steady state before chaos, while faults are active and
  after recovery. By default no fault is injected when a pre-chaos probe
  fails; `require_steady_state=False` runs the chaos anyway and leaves the
  score inconclusive
- a 0-100 resilience score built from recovery, probe, latency,
  retry-efficiency and cost evidence, with per-fault verdicts. Components a
  run cannot show (for example latency without a baseline) are left out and
  the remaining weights renormalized. The score is inconclusive (`null`) after
  a failed pre-chaos probe, for dry runs, when no fault fired, or when no
  component can be computed
- a local run-history store for score trends, with `max_runs` and
  `max_age_days` retention, and a `--min-score` CI gate
- probes and scoring on chaos workflows, experiment files and the pytest marker

Native event IDs and fault types are unchanged. `ChaosReport.probes`,
`ChaosReport.resilience` and the matching `WorkflowReport` fields are optional
and additive. When a score was computed, AIOS exports add a derived
`resilience_score` measurement; inconclusive runs export none. Probe results
and the score breakdown stay in the `io.deepagentlabs.agentic-chaos`
producer extension.

See the [v0.9 guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.9.0/docs/v0.9.md)
and the [offline demo](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.9.0/examples/chaos_resilience_demo.py).
The resilience score summarizes the evidence of one chaos run. It is not an
Evals score, a release-gate decision, a deployment health signal or proof of
containment. No new shared schema, automatic adapter or hosted execution
capability is introduced.

MCP 0.4.4 pins the published images to Chaos 0.9.0. `chaos.export_aios_run` passes the `resilience_score` measurement and the producer extension through unchanged, and the existing registry discovers faults. Probes, scoring and history are Python/CLI capabilities, not new MCP tools. Hosted HTTP continues to reject `chaos.run_experiment`, so the hosted service neither executes experiment targets nor calls probe endpoints.

## AIOS v0.6.1 provenance and conformance suite (MCP 0.4.5)

MCP 0.4.5 runs the AIOS v0.6.1 portable conformance suite in CI and matches
every `0.4-draft` case. It now fails Steps that end before they start
(`AIOS-0.4-P04`) and rejects an artifact type the declared marker does not
publish under `AIOS-0.5-V03`. `0.6-draft` provenance records are reported as
published but unchecked and are rejected, never validated against v0.4. See
[AIOS v0.6.1 compatibility](docs/aios-0.6.1.md).

## Hosted access control (MCP 0.5.0)

Phase 5 closes with per-key tool permissions enforced at dispatch. Sibling
impact:

| Sibling | Impact | Validate in |
| --- | --- | --- |
| `agenticops-control-tower` | `MCPAccessRevoker` interface unchanged; revocation now also stops queued calls. `>=0.3.6,<1` admits 0.5.0 | Tower `tests/` with `--with deep-agentic-core-mcp==0.5.0` |
| `ai-operations-spec` | No schema change. A shared access-evidence object is a future spec proposal | `tests/test_spec_conformance_suite.py` unchanged |
| `agentic-sidecar` | No change; the stop/revoke bridge is Phase 6 | — |
| `agenticlens`, `agentic-evals`, `agentic-chaos` | Documentation only; hosted pins unchanged | `tests/test_hosted_image.py` |

## Control Tower 0.9.0 runbook tools (MCP 0.5.1)

Tower Phase 9 ships versioned runbooks with exact-digest approval, bounded steps,
compensation, cancellation, reconciliation and verified recovery. MCP 0.5.1 adds
local `tower.runbooks`, `tower.runbook_recommendations`,
`tower.runbook_executions`, `tower.runbook_execution`, `tower.runbook_preview`,
`tower.runbook_execute`, `tower.runbook_cancel` and `tower.runbook_verify`.
Approval stays human-only through Tower; hosted MCP keeps rejecting Tower tools
until per-user credential binding (Phase 6). Tower's existing
`deep-agentic-core-mcp>=0.3.6,<1` range admits 0.5.1, so no Tower change is needed.
See [runbook tools](docs/tower-0.9-runbooks.md).

