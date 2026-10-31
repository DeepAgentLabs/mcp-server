# deep-agentic-core-mcp

`deep-agentic-core-mcp` is the shared MCP server layer for the DeepAgentLabs
ecosystem. It is designed to expose a single MCP interface that combines:

- `agenticlens` style workflow inspection, profiling, and analysis
- `agentic-chaos` style resilience testing and fault-injection workflows
- `agentic-sidecar` style supervision-readiness and module-surface discovery
- authenticated local Control Tower investigation, read-only fleet posture access and (since
  0.5.1) Control Tower 0.9 runbook tools

It sits above the **AI Operations Workflow Specification**, exposing a unified
MCP-native control surface over the shared operational model used by the
reference implementations.

The goal is one MCP server, one package, and one registry identity rather than
separate MCP servers for each product surface.

<!-- mcp-name: io.github.DeepAgentLabs/deep-agentic-core-mcp -->

## Connect and use

Start with the [user and developer guide](docs/user-guide.md) for hosted signup,
MCP client connection, workflow analysis, evaluation reports, and local chaos/
Sidecar capabilities. Run [the Python workflow example](examples/hosted_workflow.py)
to send an exported workflow to the hosted service. The guide documents current
integration availability and distinguishes implemented tools from future runtime work.

## Idea

This project is the control plane between LLM hosts and the existing Python
libraries:

- `agenticlens` remains the core profiling and analysis engine
- `agentic-chaos` remains the core chaos and resilience engine
- `agentic-sidecar` remains the core decision-supervision and governance engine
- `agenticops-control-tower` 0.7.0 provides the operator-facing control plane
- the `AI Operations Workflow Specification` remains the shared data contract
- `deep-agentic-core-mcp` becomes the MCP-native interface that hosts can call

That means MCP clients can connect once and access observability, chaos,
sidecar discovery, and later Control Tower-aligned operations surfaces through
one server.

## What This Server Should Eventually Do

Planned capability areas:

- profile an agentic workflow and return structured telemetry summaries
- analyze workflow artifacts and surface optimization recommendations
- run controlled chaos experiments against target workflows
- expose installed Sidecar decision/runtime capabilities and module inventory;
  package readiness is distinct from a live task connection
- eventually expose Control Tower inventory and operator-facing control
  surfaces once that sibling package ships them
- compare normal versus chaos runs
- expose shared resources such as workflow schemas, run metadata, and saved
  reports

## Design Principles

- One MCP identity: publish a single server to the MCP Registry
- Python-first: package and publish through PyPI
- Thin orchestration layer: reuse `agenticlens`, `agentic-chaos`, and
  `agentic-sidecar` instead of re-implementing their logic
- Local-first: work well as a stdio MCP server for developer workflows —
  this matters because `chaos.run_experiment` executes real code (see
  [SECURITY.md](SECURITY.md)), so this server is meant for trusted,
  local/stdio use; authenticated HTTP deployments disable code execution
- Dual transport, one tool surface: the optional Streamable HTTP transport
  (below) reuses stdio tools/resources/prompts, with remote script execution
  excluded

## Agentic Chaos v0.5 compatibility (MCP 0.3.2)

Install `agentic-chaos>=0.5.0` alongside the server to discover streaming,
authentication, and context-length faults through `chaos.list_faults`.
The existing local stdio `chaos.run_experiment` tool runs
[`examples/chaos_stream_target.py`](examples/chaos_stream_target.py) with
`faults=["stream_cut"]` and returns the native degraded event. Real sibling
integration tests cover the catalog and experiment path. Chaos remains optional;
no hard sibling dependency is introduced. Hosted HTTP rejects chaos execution.

The example is a repository file, not a wheel-installed asset. Clone the
`v0.3.2` source into a `mcp-server` directory and set
`DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT` to its parent directory before starting
the server. The [user guide](docs/user-guide.md#chaos-v05-streaming-with-mcp-032)
provides exact setup commands. CI checks both the pinned Chaos `v0.5.0` tag
and the latest sibling checkout.

See [the user guide](docs/user-guide.md#chaos-v05-streaming-with-mcp-032) and
[the Chaos v0.5 API guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/main/docs/v0.5.md).

## Phase 3 completion (MCP 0.3.3)

- **Finding provenance (3a):** every `lens.analyze_workflow` recommendation has
  a `provenance` block. It names the artifact (`workflow_id`, canonical
  `sha256` digest), the workflow step (`id`, `name`, `type`, `index`), the
  evidence span IDs and the producer. `resolved` is true only when all of these
  exist in the artifact you sent, and `provenance_summary` counts how many do.
  Needs `agenticlens>=0.6.1` for model-swap and chaos-impact findings.
- **Chaos results as AIOS runs (3b):** `chaos.run_experiment` attaches
  `aios_run`, an AI Operations v0.4-draft Run built by `agentic-chaos>=0.5.1`'s
  own exporter and checked by the spec adapter (`aios_export.aligned`).
  `chaos.export_aios_run` converts a saved or session report without running
  any code.
- **Script policy (3b):** `DEEP_AGENTIC_CORE_MCP_ALLOWED_SCRIPT_GLOBS` and
  `DEEP_AGENTIC_CORE_MCP_DENIED_SCRIPT_GLOBS` narrow which workspace scripts
  `chaos.run_experiment` may run. Deny wins, and `.venv`, `site-packages` and
  `.git` are always denied.
- **Version routing and conformance (3c):** `spec.validate_artifact`
  validates against the schema set the artifact's `spec_version` names and
  rejects markers it has no schema for, citing the applicable v0.5 rule
  (`AIOS-0.5-V01`…`V06`). Its `conformance` section lists every
  `AIOS-0.4-*` rule with a status, separate from server presentation. Needs
  `ai-operations-spec>=0.5.1` for the rule and compatibility catalogs.

Run [`examples/phase3_walkthrough.py`](examples/phase3_walkthrough.py) from a
workspace checkout to see all four end to end.

Since `0.3.4` the hosted service at `https://mcp.deepagentlabs.io/mcp` ships
the same sibling versions and spec catalogs, so provenance, conformance reports
and `chaos.export_aios_run` behave the same hosted as locally. Only
`chaos.run_experiment` stays local-only.

## AgenticLens 0.7.0 diagnosis tools (MCP 0.3.5)

- **`lens.diagnose_run`** — send a trace `Run` (and optional `baseline` runs)
  and get AgenticLens's diagnosis report: failure-taxonomy diagnoses with
  confidence and supporting spans, the faulty step and agent with ranked
  candidates, the incident timeline, robust anomalies against the baseline,
  guardrail status (`budget` caps spans, depth, and time), and an
  investigation narrative in Markdown (`include_narrative`, default true).
- **`lens.score_analysis`** — send an evaluation report and get deterministic
  and model-based scores reported separately, judge cost kept apart from agent
  cost, and the cases where evaluators disagree.

Both need `agenticlens>=0.7.0`; with an older install they return a clear
"unavailable" error and every other Lens tool keeps working. The hosted images
pin `agenticlens==0.11.0` (since MCP 0.4.3) and `agentic-chaos==0.9.0` (since MCP 0.4.4).

## AgenticLens 0.8.0 suite tools (MCP 0.3.9)

- **`lens.suite_from_traces`** — send trace `Run`s plus a suite `name` and
  `version` and get a draft agentic-evals suite: each successful run becomes a
  case expecting its tool trajectory and latency/cost within a margin, marked
  `needs_review`, with PII masked (`mask`, `strategy`). Failed runs come back
  in `skipped` with a reason.
- **`lens.suite_check`** — send a suite and get its summary (splits, domains,
  tags, sources, review status), exact/near/conflicting duplicates, and the
  approval checks AgenticLens would run (review, unmasked PII by type and
  location only, conflicting duplicates), plus `approvable`.

Both are read-only and store nothing; approving into the immutable suite store
stays a local `agenticlens suite approve` step. Both need `agenticlens>=0.8.0`;
older installs get an "unavailable" error while other Lens tools keep working.

## AgenticLens 0.9.0 ModelFit tool (MCP 0.3.11)

- **`lens.modelfit_recommend`** — send one or more experiment reports
  (`agenticlens experiment run --save`), an optional ModelFit `config`
  (categories, constraints, weights, candidate catalog, reference variant)
  and optional `variant_metadata` (provider, deployment, capabilities per
  variant), and get a recommendation per task category: status, model,
  confidence, fallback, per-case savings against the reference, and
  high-severity risks, plus the full ModelFit report and task-level model
  matrix.

Constraints fail closed, so a category with no candidate that provably meets
its limits comes back as `no_feasible_model` in `unfit_category_ids`. Each
source's `sha256` is the digest of the report's canonical JSON. The tool calls
no model and stores nothing. It needs `agenticlens>=0.9.0`; older installs
get an "unavailable" error while other Lens tools keep working.

## Unified workflows (MCP 0.4.0)

`0.4.0` completes Phase 4 (Unified Workflows): `core.compare_runs`,
`core.release_check`, `core.incident_summary` and `core.export_report`, plus the
`resource://workflows/release-check` resource and a `core.release_check`
prompt. MCP judges nothing itself: comparisons come from AgenticLens,
evaluation reports go through the Agentic Evals release gate (every
`GateConfig` threshold, strict by default, unknown keys rejected), and chaos
evidence must be a `chaos.run_experiment` report.

The release check fails closed. Each gate is `passed`, `failed`, `invalid` or
`missing`, and `ready` is true only when all of them pass; by default the
comparison, evaluation and chaos evidence are all required
(`required_evidence` narrows that). Hosted HTTP supports all four tools; pass a
locally produced `chaos_report` because hosted chaos execution stays disabled.
The exported report is MCP-local, not an AIOS artifact. No sibling release or
dependency floor changes. See the [unified workflows guide](docs/unified-workflows.md)
and [`examples/unified_release_check.py`](examples/unified_release_check.py).

## Hosted access control (MCP 0.5.0)

`0.5.0` adds per-key tool permissions to hosted HTTP. Each key can carry allow
and deny tool globs, an expiry and a task scope. The server enforces them at
dispatch, outside the model. Before each handler runs, it re-authenticates the
key and reloads its policy, so a revoked, narrowed or expired key is refused
for queued calls, retries and existing connections as well as new requests.
Calls already running finish. Hosted `tools/list` shows only permitted tools, and
`core.access_status` reports the caller's effective policy.

Denials carry an `mcp.access-decision.v1` record. Every hosted call also logs
`dispatch`/`completion` (or `denial`/`revocation_acknowledged`) records that
share a `correlation_id`. These records are MCP-local, not AIOS artifacts.
Operators use `deep-agentic-core-mcp-admin` to set, inspect or clear a key's
policy, or to revoke it by user ID without the agent's key. Supabase deployments
need the `permissions` column from `deploy/supabase/schema.sql`. Tower's MCP
revocation adapter is unchanged and now also stops queued calls. See
[hosted access control](docs/access-control.md) and
[`examples/hosted_access_status.py`](examples/hosted_access_status.py).

## MCP Surface (current, `0.5.0`)

- `core.health` — rich diagnostics: adapter availability/version, loaded
  tool/resource/prompt counts, workspace root, recent successful calls
- `core.version` — server package version
- `core.verify` — checks agenticlens/agentic-chaos/agentic-sidecar/ai-operations-spec
  connectivity and reports readiness
- `core.session_state` — inspect what the active session has accumulated
- `core.access_status` — the caller's effective hosted access policy and the
  tools it may call now; local stdio reports `enforced: false` (0.5.0)
- `core.compare_runs` — Lens baseline/candidate comparison stored for the
  release check (same behavior as `lens.compare_runs`)
- `core.release_check` — fail-closed readiness from a Lens comparison, an Evals
  report judged by the Evals gate, and a chaos report; missing, malformed or
  failed-call evidence blocks the release
- `core.incident_summary` — regressions, chaos crashes/timeouts, failed cases
  and blocked gates; `no_signals` when nothing failed
- `core.export_report` — the session's evidence as one MCP-local
  `mcp.unified-report.v1` envelope (not an AIOS artifact)
- `lens.analyze_workflow` — run AgenticLens recommendations against a
  workflow artifact
- `lens.report_summary` — render a Markdown workflow report
- `lens.compare_runs` — compare baseline/candidate trace runs for
  regressions
- `lens.slo_summary` — apply release-gate style SLO thresholds to an
  evaluation report
- `evals.validate_artifact` — offline validation of native Evals reports and gate decisions
- `lens.audit_report` — case-by-case evaluation detail, optionally with HTML
- `lens.diagnose_run` — diagnose a trace run: faulty step and agent, timeline,
  anomalies, investigation narrative (`agenticlens>=0.7.0`)
- `lens.score_analysis` — deterministic vs model-based scores, judge cost, and
  evaluator disagreement for an evaluation report (`agenticlens>=0.7.0`)
- `lens.suite_from_traces` — draft regression-suite cases from successful
  trace runs, PII masked (`agenticlens>=0.8.0`)
- `lens.suite_check` — suite summary, duplicates, unmasked PII and approval
  readiness (`agenticlens>=0.8.0`)
- `lens.modelfit_recommend` — per-task-category model recommendations from
  experiment reports under hard constraints (`agenticlens>=0.9.0`)
- `lens.routing_decide` — explain runtime model selection and fallback chains from
  ModelFit evidence without invoking models (`agenticlens>=0.10.0`)
- `lens.optimization_analyze` — rank evidence-backed optimizations from traces with
  separate benefit, confidence and quality risk (`agenticlens>=0.11.0`)
- `chaos.list_faults` — list the supported fault types
- `chaos.run_experiment` — run a workspace-sandboxed, policy-checked target
  script under selected faults and attach an AIOS run export
  ([executes real code — see `SECURITY.md`](SECURITY.md))
- `chaos.export_aios_run` — convert a chaos report into a validated AI
  Operations v0.4-draft run artifact (added in `0.3.3`; no code execution)
- `sidecar.status` — report installed Sidecar runtime APIs separately from
  live task connectivity (added in `0.3.0`)
- `sidecar.module_inventory` — inspect the installed sidecar
  modules, framework adapters, and integration placeholders (added in `0.3.0`)
- `spec.validate_artifact` — validate a workflow/run artifact against the
  schema set its `spec_version` names, with a rule-cited conformance report

Sequential tool calls can share context via an optional `session_id`
argument, backed by an in-memory session store — see `ROADMAP.md` Phase 2.

See [ROADMAP.md](ROADMAP.md) for what's shipped per phase and what's still
open, and [docs/tools.md](docs/tools.md) for full input schemas and
per-tool metadata (generated from `tools/registry.py`, run `make docs` to
refresh it after changing that file).

## Local vs. remote install modes

Container definitions are grouped under [deploy/docker](deploy/docker/README.md).

- **Local:** `pip install deep-agentic-core-mcp`, then run
  `deep-agentic-core-mcp` over stdio. Local session behavior is unchanged.
- **Self-hosted multi-user HTTP (`0.3.0`+):** install with
  `pip install 'deep-agentic-core-mcp[http]'`, then run `deep-agentic-core-mcp-http`.
  Provision a unique bearer key per user
  and a Redis URL before startup. Missing configuration prevents startup.
- **Hosted AWS signup:** open [mcp.deepagentlabs.io](https://mcp.deepagentlabs.io)
  to generate a user identity and MCP key; connect your MCP client to
  `https://mcp.deepagentlabs.io/mcp` with its bearer key.
  DynamoDB stores user records and key hashes; keys work immediately and can be
  replaced or revoked through the page. No password or email verification is used.
  Save the key: it cannot be recovered. See [the AWS guide](deploy/aws/README.md).

The HTTP service uses stateless MCP transport at `/mcp` and Redis-backed
workflow sessions scoped to the authenticated user. Users can reuse the same
`session_id` without accessing each other's artifacts. HTTP calls cannot run
`chaos.run_experiment`, even if the local remote-chaos override is set.

See [the remote hosting guide](docs/remote-hosting.md) and `render.yaml` for Render deployment, configuration,
container builds, AWS deployment requirements, client headers, limits, and
credential rotation. `create_app()` also accepts explicit credentials, a
session backend, and allowed hosts/origins for integrations and tests.
`MemorySessionStore` is an explicit development option; the CLI requires Redis.

## Repository Layout

```text
mcp-server/
├── README.md
├── ROADMAP.md
├── pyproject.toml
├── server.json
├── .gitignore
├── docs/
│   ├── architecture.md
│   └── tools.md          # generated - see scripts/generate_tools_doc.py
├── examples/
│   ├── sample_workflow.json
│   ├── provenance_workflow.json
│   ├── phase3_walkthrough.py
│   └── chaos_target.py
├── scripts/
│   └── generate_tools_doc.py
├── src/
│   └── deep_agentic_core_mcp/
│       ├── __init__.py
│       ├── server.py
│       ├── transport_http.py
│       ├── config.py
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── registry.py
│       ├── resources/
│       │   ├── __init__.py
│       │   └── catalog.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── tooling.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── registry.py
│       │   └── session.py
│       ├── adapters/
│       │   ├── __init__.py
│       │   ├── agentic_chaos.py
│       │   ├── agenticlens.py
│       │   ├── agentic_sidecar.py
│       │   └── ai_operations_spec.py
│       └── tools/
│           ├── __init__.py
│           ├── registry.py
│           ├── chaos.py
│           ├── core.py
│           ├── lens.py
│           ├── sidecar.py
│           └── spec.py
└── tests/
    ├── test_chaos_aios_export.py
    ├── test_chaos_script_policy.py
    ├── test_degraded_boot.py
    ├── test_imports.py
    ├── test_lens_provenance.py
    ├── test_spec_conformance.py
    ├── test_registry.py
    ├── test_server.py
    └── test_session.py
```

## MCP-Oriented Structure

This repository should have all of the standard layers we expect for a useful
MCP server:

- `tools/` for callable MCP tools and their registration metadata
- `resources/` for readable assets such as fault catalogs, templates, and
  workflow examples
- `prompts/` for reusable prompt templates exposed through the server
- `schemas/` for typed request and response contracts
- `services/` for shared orchestration logic that keeps tool modules thin,
  including the in-memory session store (`services/session.py`)
- `adapters/` for integration boundaries to `agenticlens`, `agentic-chaos`,
  `agentic-sidecar`, and `ai-operations-spec` — each degrades to
  `"available": false` rather than crashing server boot if its sibling repo is
  missing

## Packaging and Publishing Model

One repository supports both the local Python package and the hosted HTTP service.
The stdio entry point remains available without the optional HTTP dependencies.
HTTP transport and signup support are included from `0.3.0`; the earlier
PyPI `0.2.0` release provides local stdio.

| Workflow | Trigger | Result |
|---|---|---|
| `.github/workflows/ci.yml` | Pull request | Tests Python 3.10–3.13 and builds distributions; no AWS deployment |
| `.github/workflows/ci.yml` | Push/merge to `main`, or manual run | Runs tests and package checks; no AWS deployment |
| `.github/workflows/release-pypi.yml` | Push a `v*` version tag | Runs checks, publishes to PyPI, creates the GitHub Release, publishes MCP Registry metadata; no AWS deployment |

A push to `main` does not publish to PyPI or deploy AWS. Version-tag releases
publish packages using PyPI Trusted Publishing. AWS deployment is an explicit
manual operator action from 0.4.1. See
[CONTRIBUTING.md](CONTRIBUTING.md) for releases and
[the AWS CI guide](deploy/aws/CI-CD.md) for deployment setup and limits.

For PyPI-based verification, the `mcp-name` marker above must match the
`name` field in `server.json`.

## What's Next

Phase 2 (session management, rich diagnostics, tool annotations, prompt
registry, `core.verify`) is complete as of `0.2.0`, and Phase 3 (3a AgenticLens,
3b Agentic Chaos, 3c AI Operations Specification, 3d Sidecar discovery) is
complete as of `0.3.3`. What's still open (see [ROADMAP.md](ROADMAP.md) for
full detail):

- **Sidecar runtime controls**: richer control surfaces require an
  authenticated, task-scoped runtime bridge
- **Phase 5 (Publishing and Adoption)** — complete in 0.5.0: automated
  publishing plus hosted access control (per-key tool permissions, revocation
  at dispatch, correlated denial evidence, operator revocation)
- **Control Tower coordination** — local connector tools ship in 0.3.6 for
  Tower 0.7.0; hosted per-user credential binding moves to Phase 6
- **Phase 6** — containment integrations (hosted Tower credentials, Sidecar
  stop/revoke bridge, AIOS access evidence) and operational intelligence features

## Development

A `Makefile` provides shorthand for common tasks:

```bash
make install     # install dev dependencies
make check       # run all quality gates (lint + format + typecheck + test)
make test-cov    # tests with coverage report
make docs        # regenerate docs/tools.md from tools/registry.py
make docs-check  # fail if docs/tools.md is out of date
make help        # list all available targets
```

## Notes

This scaffold assumes the intended GitHub namespace is
`io.github.deepagentlabs/deep-agentic-core-mcp`. If the final publishing
account or org changes, update:

- the `mcp-name` marker in this README
- `server.json`
- any repository URLs in `pyproject.toml`

## Operational safety roadmap

See [planned safety acceptance criteria](ROADMAP.md#access-containment-and-evidence-planned-extensions) for responsibilities and
dependencies. These additions do not claim implemented end-to-end containment
or integrity protection.

### Sidecar v0.7 compatibility

With Sidecar installed, `sidecar.status` detects its public decision, plan,
runtime-event, audit and local operator APIs. `runtime_ready` means the decision
API is installed; `runtime_connected=false` and `mcp_runtime_controls=false`
make clear that these MCP discovery tools do not attach to an active task.
`sidecar.module_inventory` lists adapter files, including placeholders; their
presence does not certify framework support. No Sidecar dependency is required
for MCP startup. An unavailable package produces an unavailable response.

For live task controls, use Sidecar's authenticated local OperatorServer/CLI
interface described in its
[v0.7.0 live operations guide](https://github.com/DeepAgentLabs/agentic-sidecar/blob/v0.7.0/docs/live-operations.md).
Sidecar v0.7.0 is published separately. This patch improves discovery without
enabling remote stop/revoke through MCP.

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

## Control Tower 0.6.0 connector (MCP 0.3.6)

Local stdio exposes twelve `tower.*` tools over the actual authenticated Tower
HTTP API: inventory/status/versions/posture/evidence, incidents, detection,
investigation, preview, execute and verify. Configure `AGENTICOPS_TOWER_URL`
(a trusted HTTP(S) origin), `AGENTICOPS_TOWER_READ_TOKEN`, and optionally the
separate `AGENTICOPS_TOWER_WRITE_TOKEN`. No Tower package import is required.
Without Tower, all other tools work; Tower tools return structured unavailable.

The `tower.investigation` prompt directs the host model to cite record IDs and
artifact references, preserve uncertainty and missing evidence, recommend only
the supported staging runbook, and leave approval to a human through Tower's
HTTP/CLI. Approval credentials are never accepted by tool arguments or exposed
through an approval tool. Execution is subject to Tower's exact-preview approval.
The model provider remains the client's choice; none is bundled.

Hosted/remote MCP rejects Tower tools until per-user Tower credential binding
exists. Local tokens cannot be borrowed by hosted tenants. Redirects are refused,
responses are limited to 1 MiB and an isolated HTTP worker enforces a ten-second
total deadline. A timeout may leave an action result unknown; inspect the Tower
incident before retrying. URLs and tokens
come only from trusted server environment. The Tower optional connector extra
must use MCP >=0.3.6; other producer floors remain unchanged.

For setup, request JSON and both resolved/escalated native Lens/Evals walkthroughs,
see [Tower's connector guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/main/docs/mcp-connector.md)
and [incident guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/main/docs/incident-recovery.md).
Use `tower.agents` with `status=unhealthy`, `tower.versions` with an explicit
minimum, or `tower.evidence` with `source=agentic-sidecar` to inspect high-risk
posture without replacing native producer decisions.

## Native Evals contract validation — MCP 0.3.8

Published Evals report and gate schemas (0.7.2 at MCP 0.3.8; 0.9.0 since MCP 0.3.14) are now enforced in the native
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

MCP 0.3.14 bundles the Evals 0.9.0 native report and gate schemas, so
`evals.validate_artifact` enforces the new optional judge summary, live-target
summary and per-case `target_status` fields. Validation stays offline and
structural; MCP never recomputes a gate or treats an unavailable judgment as a
pass. Hosted images pin `agentic-evals==0.9.0`. See
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

AgenticLens 0.9.0 delivers its v0.7 milestone: `agenticlens.modelfit` and
`agenticlens modelfit` recommend a model per task category from recorded
experiment reports, under hard quality, cost, latency, safety, provider and
deployment constraints that fail closed, with confidence, explanations,
alternatives, provider-diverse fallbacks, savings tied to the experiment
evidence, quality risks and a task-level model matrix.

MCP 0.3.11 adds the read-only `lens.modelfit_recommend` tool over supplied
reports and pins hosted images to `agenticlens==0.9.0`. Running experiments
stays a local `agenticlens experiment run` step; ModelFit recommends and does
not route traffic.

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

## Control Tower 0.8.0 live operations

See [operator compatibility and ownership](docs/tower-0.8-live-operations.md) for
periodic detection, durable alerts, acknowledgements and joined incident console
views. Existing native contracts and optional dependency ranges remain compatible;
no runtime or patch release is required here.

## Control Tower 0.9.0 runbooks (MCP 0.5.1)

Local stdio adds eight `tower.runbook*` tools (twenty `tower.*` tools in total).
Reader tools list installed runbooks, recommendations for an incident and
execution history. Writer tools preview a catalog version with string
parameters, execute the exact human-approved digest, cancel and verify. There is
still no approval or revocation tool: a human approves through Tower HTTP/CLI
with the separate approver credential. Recommendations come only from installed
runbook versions, and hosted MCP still refuses Tower tools. See the
[runbook tools guide](docs/tower-0.9-runbooks.md).

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
