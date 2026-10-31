# Changelog

All notable changes to this project will be documented here.

This project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## 0.4.5 - 2026-10-31

### Fixed

- `spec.validate_artifact` now fails a Step whose `ended_at` precedes its
  `started_at` under `AIOS-0.4-P04`, as the Run-level check already did.
- An artifact type the declared marker does not publish (for example a
  provenance record labeled `0.4-draft`) is rejected with an
  `AIOS-0.5-V03` compatibility decision instead of an accept decision
  beside the error.

### Added

- `tests/test_spec_conformance_suite.py` runs the AIOS v0.6.1 portable
  conformance suite from the sibling checkout: `0.4-draft` cases must match
  the expected outcome and rule citations, and `0.6-draft` provenance cases
  must be rejected under `AIOS-0.5-V03`. See `docs/aios-0.6.1.md`.

## 0.4.4 - 2026-10-31

### Added

- Agentic Chaos 0.9.0 (roadmap v0.9 Resilience Probes & Resilience Score)
  compatibility: `chaos.export_aios_run` passes a scored report's derived
  `resilience_score` measurement and its probe/score producer extension
  through unchanged (`tests/test_chaos_aios_export.py`). Probes, scoring and
  run history stay Python/CLI capabilities; no new MCP tool, and hosted HTTP
  still rejects `chaos.run_experiment`. See `docs/chaos-0.9.md`.

### Changed

- Hosted images pin `agentic-chaos==0.9.0` and `agentic-sidecar==0.9.1`;
  `tests/test_hosted_image.py` requires Chaos 0.9.0 or later.

## 0.4.3 - 2026-10-31

### Added

- AgenticLens 0.11.0 (roadmap v0.9 Optimization Intelligence) compatibility:
  read-only `lens.optimization_analyze` ranks evidence-backed optimizations from
  supplied `Run` traces (prompt caching and compression, retrieval pruning and
  reranking, memory summarization, tool caching, retry policy, redundant steps,
  unnecessary handoffs, quality-cost trade-offs) with projected benefit,
  confidence and quality risks kept separate. It never writes a decision ledger
  or changes anything. Older Lens installs degrade only this tool with an
  explicit `agenticlens>=0.11.0` unavailable error.

### Changed

- Hosted images pin `agenticlens==0.11.0`; `tests/test_hosted_image.py` requires
  at least 0.11.0.

## 0.4.2 - 2026-10-31

### Added

- Agentic Evals 0.10.0 compatibility: hosted images and the development
  dependency pin `agentic-evals==0.10.0`. `spec.validate_artifact` reports Runs
  carrying Evals AIOS evaluation evidence as aligned, and
  `tests/test_evals_aios_evidence.py` checks this, including an orphaned
  evaluation cited as `AIOS-0.4-P08`. The bundled native Evals schemas are
  unchanged (Evals 0.10.0 ships the same documents). See
  `docs/evals-0.10-aios-evidence.md`.
- PostgreSQL (Supabase) storage for hosted API keys, per-user sessions and
  signup limits, selected by `DEEP_AGENTIC_CORE_MCP_DATABASE_URL`. The Render
  Blueprint now uses it instead of Render Key Value; `deploy/supabase/schema.sql`
  creates the private schema and least-privilege service role. Its connection
  pool is sized from the request concurrency limit and closed on shutdown or
  failed startup.

### Changed

- Key rotation/revocation conflicts raise `KeyConflictError` for every backend.
- Fix transport and signup test fixtures that leaked remote mode into later tests.

- Roadmap only, decided after the 0.4.0 release: Phase 4 (Unified Workflows) is
  now complete as of 0.4.0, which its release notes below still call the first
  slice. The access-containment items (tool-level permissions, revocation at
  dispatch, stop/revoke, denial evidence, hosted Tower credentials) move to
  Phase 5.

## 0.4.1 - 2026-10-19

- Discover installed Sidecar 0.9 task-authority, revocation and redacted-evidence
  APIs without constructing a task or exposing runtime controls.
- Pin Sidecar 0.9.0 in standalone hosted image recipes; native evidence remains
  compatible and no new remote authority API is claimed.
- Remove automatic AWS deployment from the release pipeline. Package/GitHub/MCP
  Registry publication remains; existing deployment scripts are manual operator tools.
- Document Sidecar authority, privacy, evidence and ownership boundaries.

## 0.4.0 - 2026-10-19

First Phase 4 (Unified Workflows) slice. No sibling release, dependency range
or hosted image pin changes.

### Added

- `core.compare_runs`, `core.release_check`, `core.incident_summary` and
  `core.export_report`, the `resource://workflows/release-check` resource and a
  `core.release_check` prompt (contributed in #40).
- `core.release_check` fails closed. Evaluation reports go through the Evals
  release gate, the same path as `lens.slo_summary`, so every `GateConfig`
  threshold applies (strict by default) and unknown threshold keys are rejected.
  Comparisons are validated with the Lens comparison model and chaos evidence
  must be a `chaos.run_experiment` report. `required_evidence` (default: all
  three kinds) makes absent evidence a blocking `missing` gate. Each gate reports
  `passed`, `failed`, `invalid` or `missing` with reasons and observed values.
- `core.incident_summary` reports regressions, chaos crashes or timeouts, failed
  evaluation cases and blocked release gates, and `no_signals` when nothing failed.
- `core.export_report` returns an MCP-local `mcp.unified-report.v1` envelope
  naming its generator; it is not an AIOS artifact.
- `docs/unified-workflows.md` and `examples/unified_release_check.py`.

### Changed

- `core.compare_runs` and `lens.compare_runs` share one code path, and
  `lens.compare_runs` now returns invalid runs as a structured error.
- Correct the Sidecar 0.8.5 discovery status in `docs/integrations.md` and add
  the Agentic Evals integration.

## 0.3.14 - 2026-10-19

Pairs with Agentic Evals 0.9.0 (roadmap v0.9 judge reliability, cost and
live-target resilience).

### Changed

- Re-sync the bundled native Evals report and gate schemas from
  `agentic-evals==0.9.0`, so `evals.validate_artifact` and the Lens report tools
  enforce the new optional judge summary, live-target summary and per-case
  `target_status` fields. Reports from Evals 0.7.2 to 0.8.0 still validate.
- Pin the published AWS/Render images to `agentic-evals==0.9.0` alongside
  Lens 0.10.0 and Chaos 0.8.0. No MCP tool is added or changed.
- Document Evals 0.9.0 validation: structural only, with no gate
  recomputation, and an unavailable judgment never treated as a pass.

## 0.3.13 - 2026-10-18

Pairs with Agentic Chaos 0.8.0 (roadmap v0.8 workflows, declarative
experiments and explosion radius).

### Changed

- Pin the published AWS/Render images to Chaos 0.8.0. Existing MCP tool
  boundaries are unchanged.
- `chaos.export_aios_run` passes through the workflow summary that Chaos 0.8
  adds to merged workflow reports. No new MCP tool is added.
- Document Chaos 0.8 workflow evidence and its limits. Hosted HTTP still
  rejects `chaos.run_experiment`.

## 0.3.12 - 2026-10-18

Pairs with AgenticLens 0.10.0 (roadmap v0.8 advisory runtime routing).

### Added

- Read-only `lens.routing_decide`: selection explanations, fallback chains,
  constraint rejections, confidence, policy/report hashes from saved ModelFit
  evidence. Never executes model callbacks or writes a routing audit file.
- Graceful per-tool unavailability with older Lens and routing boundary tests.

### Fixed

- Workspace checkout imports now precede stale sibling virtualenv installations.

### Changed

- Hosted AWS/Render images pin `agenticlens==0.10.0`; Chaos stays at 0.7.0.

## 0.3.11 - 2026-10-18

Pairs with `agenticlens` 0.9.0 (v0.7 ModelFit).

### Added

- `lens.modelfit_recommend`: recommend a model per task category from one or
  more supplied experiment reports, with an optional ModelFit `config` and
  per-variant `variant_metadata` (provider, deployment, capabilities). Returns
  a compact recommendation per category (status, model, confidence, fallback,
  per-case savings, high-severity risks), `unfit_category_ids`, and the full
  ModelFit report with its task-level model matrix. Each source's `sha256` is
  the digest of the report's canonical JSON.
- The tool is read-only: it calls no model and stores nothing. It needs
  `agenticlens>=0.9.0` and reports "unavailable" on older installs without
  affecting other tools.

### Changed

- Hosted AWS and Render images pin `agenticlens==0.9.0` (was 0.8.0).

## 0.3.10 - 2026-10-17

### Changed

- Pin published AWS/Render images to Chaos 0.7.0; preserve existing MCP tool boundaries.
- Document advanced Chaos evidence compatibility and synthetic containment limits.

## 0.3.9 - 2026-10-17

Pairs with `agenticlens` 0.8.0 (v0.6 test-suite and dataset management).

### Added

- `lens.suite_from_traces`: convert trace runs into a draft agentic-evals
  suite. Successful runs become `needs_review` cases expecting their tool
  trajectory and latency/cost within a margin; PII is masked by default
  (`redact`, or `hash` with a random per-call salt unless `salt` is given);
  failed runs are returned in `skipped` with a reason.
- `lens.suite_check`: suite summary, exact/near/conflicting duplicates, and
  the approval checks AgenticLens runs (review, unmasked PII by type and
  location only, conflicting duplicates), with `approvable` and a value-free
  `pii` scan listing each unmasked value's case, field and type.
- Both tools are read-only and store nothing. They need `agenticlens>=0.8.0`
  and report "unavailable" on older installs without affecting other tools.

### Changed

- Hosted AWS and Render images pin `agenticlens==0.8.0` (was 0.7.0).

## 0.3.8 - 2026-10-17

### Added

- Offline validation against the exact published Evals 0.7.2 report and gate
  schemas, with pinned upstream parity tests and packaged schema resources.
- Native JSON boundary tests for nested invalid scores, failed gates, unknown
  additive fields, unsupported versions and value-free diagnostics.

### Changed

- Report consumers reject malformed/partial native artifacts before projecting
  or analyzing them. Send full JSON reports rather than summary-only objects.
- New read-only `evals.validate_artifact` works over stdio and authenticated HTTP.
- Lens report analysis/audit/SLO tools validate input; produced SLO gates validate too.

## 0.3.7 - 2026-10-17

Pairs with `agentic-chaos` 0.6.0 (pytest plugin and chaos contracts).

### Changed

- Hosted AWS and Render images pin `agentic-chaos==0.6.0` (was 0.5.3).
  `chaos.export_aios_run` output now carries `calls: {recorded, dropped}` and,
  when a target crashed, `unhandled_error` in the `io.deepagentlabs.agentic-chaos`
  extension. The run, steps and evidence are unchanged.
- No MCP tool, schema or transport change. Chaos contracts and the pytest
  plugin are not exposed as MCP tools; HTTP still rejects `chaos.run_experiment`.
  `agentic-chaos>=0.5.1` remains the floor for AIOS export.

## 0.3.6 - 2026-10-17

### Added

- Twelve local `tower.*` tools over the authenticated Control Tower 0.6.0 HTTP
  API, covering inventory, evidence, investigation and approved staging recovery.
- Separate configured reader/writer authority, fixed origin, encoded target IDs,
  refused redirects, bounded requests/responses and secret-safe failures.
- `tower.investigation` prompt with citations, explicit uncertainty, untrusted
  evidence boundaries and separate human approval through Tower HTTP/CLI.
- Hosted Tower calls are rejected until per-user credential binding exists.
  Tower remains optional and other MCP tools work without it.


## 0.3.5 - 2026-10-13

Pairs with `agenticlens` 0.7.0 (v0.5 advanced evaluation and diagnosis) and
`agentic-chaos` 0.5.3.

### Added

- `lens.diagnose_run`: AgenticLens diagnosis of a trace run (failure taxonomy,
  faulty step and agent, incident timeline, anomalies against optional
  baseline runs, guardrail status, investigation narrative). Accepts
  `config` (rule thresholds and budgets) and `budget` (analysis caps).
- `lens.score_analysis`: deterministic vs model-based scores, judge cost kept
  separate from agent cost, and evaluator disagreement for an evaluation
  report.
- Both tools are read-only and need `agenticlens>=0.7.0`; with an older
  install they report the missing capability and other Lens tools keep
  working.

### Changed

- The AWS and Render images pin `agenticlens==0.7.0` and
  `agentic-chaos==0.5.3`; the hosted-image test requires Lens 0.7.0.

## 0.3.4 - 2026-10-13

Brings the hosted service up to the Phase 3 feature set. 0.3.3 shipped the
server code, but the hosted images still used the earlier sibling versions.

### Fixed

- The AWS and Render images pin `agenticlens==0.6.1`, so every hosted
  `lens.analyze_workflow` finding resolves its step provenance (model-swap and
  chaos-impact findings were unresolved with 0.5.0).
- The AWS and Render images install `agentic-chaos==0.5.1`, so the hosted
  `chaos.export_aios_run` and `chaos.list_faults` work. HTTP still rejects
  `chaos.run_experiment`; no target script runs on the hosted service.
- `scripts/fetch_schema_assets.py` fetches the `ai-operations-spec` v0.5.1
  assets into a spec-root layout: the three v0.4 schemas plus
  `conformance-rules.json` and `compatibility.json`, each checksum-verified at a
  pinned commit. Hosted `spec.validate_artifact` now returns the full
  rule-by-rule conformance report, and the catalog resources are listed.
- The workspace image and build helper copy `agentic-chaos` and the spec
  catalogs from sibling checkouts.

### Added

- `tests/test_hosted_image.py` fails if the hosted images fall behind the
  sibling versions or spec assets the adapters need.

### Changed

- Release package, MCP Registry metadata, and runtime version as `0.3.4`.

## 0.3.3 - 2026-10-13

Completes Phase 3 (3a AgenticLens, 3b Agentic Chaos, 3c AI Operations
Specification). Pairs with sibling patch releases `agenticlens` 0.6.1,
`agentic-chaos` 0.5.1 and `ai-operations-spec` 0.5.1. Every sibling stays an
optional dependency and degrades instead of failing boot.

### Added

- **Finding provenance (3a).** Each `lens.analyze_workflow` recommendation now
  has a `provenance` block:
  - the artifact: `workflow_id` when the artifact carries one, plus a
    `sha256` digest of its canonical JSON
  - the workflow step: `id`, `id_in_artifact`, `name`, `type`, `index`
  - evidence span IDs and sources, and the producer
  - `resolved`, true only when the step and every span exist under IDs the
    artifact itself carries (IDs AgenticLens generates do not count)

  `provenance_summary` counts resolved findings and lists unresolved ones by
  title.
- **AIOS run export (3b).** `chaos.run_experiment` attaches `aios_run`, an AI
  Operations v0.4-draft Run built by `agentic-chaos`'s own exporter
  (`>=0.5.1`), with `aios_export` reporting its validation (`aligned`,
  rule-cited `issues`, `claim`). New arguments: `export_aios` (default true)
  and `workflow_id`. With an older `agentic-chaos`, the result reports
  `aios_export.available=false`.
- **`chaos.export_aios_run` tool.** Converts a saved report, or the session's
  last experiment, into a validated AIOS run without running code, so it is
  also listed over HTTP.
- **Script allow/deny policy (3b)** for `chaos.run_experiment`:
  - `DEEP_AGENTIC_CORE_MCP_ALLOWED_SCRIPT_GLOBS` (opt-in allowlist) and
    `DEEP_AGENTIC_CORE_MCP_DENIED_SCRIPT_GLOBS`, matched against the
    workspace-relative path
  - deny wins, and `.venv`, `site-packages` and `.git` are always denied, at the
    workspace root or nested
  - `core.health` reports the active policy as `chaos_script_policy`
- **Version routing (3c).** `spec.validate_artifact` validates against the
  schema set the artifact's `spec_version` names, loaded from the spec's
  `specification/v0.5/compatibility.json`. Unpublished, malformed or missing
  markers are rejected rather than re-validated against another version.
  `compatibility` reports the decision and the v0.5 rule (`AIOS-0.5-V01`–`V06`).
  Only markers this server implements rules for (`0.4-draft`) are loaded. Any
  other set the spec publishes appears as `published_unchecked_versions`, and its
  artifacts are rejected rather than checked with the wrong rules.
- **Rule-cited conformance (3c).** `spec.validate_artifact` returns a
  `conformance` report:
  - every rule from `specification/v0.4/conformance-rules.json`, with
    `pass` / `fail` / `not_evaluated` / `not_applicable` status
  - each issue labeled with its rule ID (`AIOS-0.4-P01`–`P12`, `X01`, `U02`,
    `E01`)

  Server presentation fields are separated and labeled in `server.note`.
- New semantic checks: P12 (retry attempts keep distinct identities and link to
  the prior attempt) and X01 (Workflow references must be `external`).
- Resources `resource://specs/aiops/v0.4/conformance-rules` and
  `resource://specs/aiops/v0.5/compatibility`. Schema resources are now
  generated for every loaded schema set.
- `core.verify`/`core.health` report `supported_versions` and catalog
  availability for the spec adapter, and `aios_export` for the chaos adapter.
- `examples/phase3_walkthrough.py` and `examples/provenance_workflow.json`.

### Changed

- `spec.validate_artifact` skips semantic checks when schema validation fails
  (`semantic_checked: false`), so they no longer crash on missing fields the
  schema already reported. Semantic rules then show `not_evaluated`.
- The draft-alignment claim cites the 2026-10-13 observation date.
- Release package, MCP Registry metadata, and runtime version as `0.3.3`.

## 0.3.2 - 2026-10-12

### Added

- Verify Agentic Chaos v0.5 fault catalog discovery and streaming experiment
  events through the existing MCP tools with real sibling integration tests.
- Offline `examples/chaos_stream_target.py` and usage documentation for local
  stdio streaming experiments. New faults are discovered dynamically from the
  optional installed Chaos package; hosted HTTP continues to reject execution.

### Changed

- Release package, MCP Registry metadata, and runtime version as `0.3.2`.
- Pin a dedicated CI job to Chaos `v0.5.0` alongside latest-sibling coverage;
  document source-checkout and explicit workspace setup for wheel installations.
- Document Chaos v0.5 compatibility without adding a hard sibling dependency or
  claiming new MCP profile/provider configuration APIs.

## 0.3.1 - 2026-10-12

### Fixed

- Exercise all v0.7 discovery capabilities and module inventory with a fake
  package/tree in credential-free CI; link to the published Sidecar v0.7.0 guide.

- Sidecar discovery detects installed decision and v0.7 operations APIs instead
  of hardcoding scaffold/runtime-not-ready status. Explicit connection/control
  flags prevent installed capabilities from being mistaken for a live MCP task.
- Module inventory reports installed modules separately from missing planned
  modules; regenerated tool descriptions retain placeholder support boundaries.

## 0.3.0 - 2026-10-04

### Added

- GitHub Actions AWS deployment after successful version-tag PyPI publication, with scoped
  deployment credentials, immutable images, change-set safeguards, and MCP smoke checks.
- Optional CloudFront custom-domain HTTPS configuration and explicit browser
  origin compatibility during domain migration.
- AWS signup portal with generated user identities, DynamoDB-backed hashed API
  keys, immediate rotation/revocation, shared signup limits, and existing-key migration.
- Authenticated multi-user Streamable HTTP transport, per-user Redis workflow
  state, bounded storage with expiry, request/concurrency limits, and Host/Origin
  validation. Stateless transport supports multiple workers without affinity.
- HTTP installation extra, deployment guide, analysis/validation container, and
  filtered container build helper. HTTP never exposes chaos script execution.
- Tool dispatch runs synchronous work off the event loop. AgenticLens evaluation
  integration now uses its public API re-exports.
- `sidecar.status` and `sidecar.module_inventory` tools, wiring `agentic-sidecar`
  into the MCP server through a degrading adapter (Phase 3d). These report
  connectivity and scaffold/module inventory only, since the `agentic-sidecar`
  decision runtime is not implemented upstream yet.

### Fixed

- MCP initialization now reports the package version instead of an empty string.

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
