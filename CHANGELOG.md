# Changelog

All notable changes to this project will be documented here.

This project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

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
