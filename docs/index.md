# MCP Server

How can an MCP client or coding agent use every DeepAgentLabs capability through one server?

## What it does

The server exposes 56 tools, documentation and schema resources, and six prompt templates over local stdio or hosted HTTP. They are grouped by area below. Each area links to its detailed guide; for runnable steps, see the [developer guide](developer-guide.md).

### 1. Core: cross-product checks and server basics (`core.*`, 15 tools)

- **Health, version and status**
    - `core.health`, `core.version`, `core.verify` (are the integrations connected)
    - `core.access_status`: the calling hosted key's effective permissions
- **Setup**
    - `core.onboard`: read-only setup steps with sibling readiness
- **Release checks**
    - `core.release_check`: fail-closed readiness from comparison, Evals and Chaos evidence
    - `core.compatibility`: installed versions against the packaged candidate matrix
    - `core.compare_runs`: baseline versus candidate runs, stored for the release check
- **Incidents and reports**
    - `core.incident_summary`, `core.export_report`
    - `core.report_recall` (saved reports with cited notes), `core.session_state`
- **Documentation for all seven products**
    - `core.docs_catalog`, `core.docs_search`, `core.docs_read`

Guides: [Unified workflows](unified-workflows.md) ·
[Release readiness](release-readiness.md) · [Tool reference](tools.md#core)

### 2. AgenticLens: analyse agent workflows (`lens.*`, 13 tools)

- **Analyse and diagnose**
    - `lens.analyze_workflow`, `lens.diagnose_run`, `lens.compare_runs`
- **Optimise**
    - `lens.optimization_analyze`
    - `lens.modelfit_recommend` (which model fits each task)
    - `lens.routing_decide`
- **Score and report**
    - `lens.score_analysis`, `lens.slo_summary`
    - `lens.report_summary`, `lens.audit_report`
- **Test suites**
    - `lens.suite_check`, `lens.suite_from_traces`
- **Evidence**
    - `lens.execution_verify`: verify an execution bundle with host-held trust keys

Guides: [Lens integration](integrations.md#agenticlens) ·
[Lens execution evidence](lens-execution-evidence.md) · [Tool reference](tools.md#agenticlens-lens)

### 3. Agentic Chaos: fault injection (`chaos.*`, 3 tools)

- **Faults**
    - `chaos.list_faults`
- **Experiments**
    - `chaos.run_experiment`: trusted local scripts only; hosted HTTP always refuses it
- **Export**
    - `chaos.export_aios_run`: turn a chaos report into an AIOS run

Guides: [Chaos integration](integrations.md#agentic-chaos) ·
[Configuration](configuration.md#local-chaos-script-policy) · [Tool reference](tools.md#agentic-chaos-chaos)

### 4. Agentic Evals: report validation (`evals.*`, 1 tool)

- `evals.validate_artifact`: check an eval report or gate decision against its schema

Guides: [Evals report contract](evals-report-contract.md) · [Tool reference](tools.md#native-evals-evals)

### 5. Agentic Sidecar: supervision inventory (`sidecar.*`, 2 tools)

- `sidecar.status`, `sidecar.module_inventory`
- Live stop and revoke run through a separate operator route, not a model tool

Guides: [Sidecar integration](integrations.md#agentic-sidecar) ·
[Phase 6 containment](phase6-containment.md) · [Tool reference](tools.md#agentic-sidecar-sidecar)

### 6. AI Operations Specification: artifact validation (`spec.*`, 1 tool)

- `spec.validate_artifact`: check an artifact against the AIOS schemas (v0.4, v0.6 and v0.8)
- Schema and rule-catalog resources are bundled for offline use

Guides: [Coordinated v1 readiness](coordinated-v1-readiness.md) ·
[Resources and prompts](resources-and-prompts.md) · [Tool reference](tools.md#ai-operations-specification-spec)

### 7. Control Tower: fleet operations (`tower.*`, 21 tools)

- **Fleet**
    - `tower.status`, `tower.agents`, `tower.posture`, `tower.versions`
    - `tower.capability_contract`
- **Incidents and evidence**
    - `tower.detect`, `tower.incidents`, `tower.incident`, `tower.investigate`
    - `tower.evidence`: an agent's evidence history
- **Recovery actions**
    - `tower.preview`, then `tower.execute`
    - A human must approve the exact preview in Tower first
    - `tower.verify`: confirm recovery with fresh Lens and Evals evidence
- **Runbooks**
    - `tower.runbooks`, `tower.runbook_recommendations`, `tower.runbook_preview`
    - `tower.runbook_execute`, `tower.runbook_execution`, `tower.runbook_executions`
    - `tower.runbook_verify`, `tower.runbook_cancel`

Guides: [Tower runbooks](tower-0.9-runbooks.md) ·
[Tower compatibility](tower-0.10-compatibility.md) · [Tool reference](tools.md#control-tower-tower)

### 8. Built-in AI-readable documentation for all seven products

The server bundles the full documentation for every DeepAgentLabs product, written for AI agents to read. GitHub Copilot, OpenAI Codex, Claude Code, Cursor or any MCP-compatible coding agent can use it to explore, understand, integrate and build with these tools from natural-language requests, without anyone navigating the documentation by hand.

- **Products covered**
    - AgenticLens, Agentic Evals, Agentic Chaos, Agentic Sidecar, Control Tower,
      the AI Operations Specification and this MCP server
- **Discover, search and read**
    - `core.docs_catalog`, `core.docs_search` and `core.docs_read`
    - Every answer cites its source commit, checksum and line
- **Resources**
    - `resource://docs/catalog`
    - `resource://docs/{product}/reference`, `/index`, `/manifest` and `/license`
- **Guided build prompt**
    - `core.build_with_ecosystem` has the agent read the right docs before it writes integration code
- **Works offline**
    - No extra packages, network access or API keys are needed to read the docs locally

Guides: [Build with the seven-product AI reference](ecosystem-ai-reference.md)

### 9. Resources and prompt templates

- **Resources**
    - Sample workflow, chaos fault catalog and release-check guide
    - AIOS JSON schemas and conformance-rule catalogs
    - Saved sessions per user: `resource://sessions/{id}`
- **Prompts (six templates)**
    - `core.build_with_ecosystem`, `core.release_check`, `tower.investigation`
    - `lens.workflow_summary`, `lens.compare_summary`, `chaos.experiment_brief`

Guides: [Resources and prompts](resources-and-prompts.md)

### 10. Local and hosted operation

- **Transports**
    - Local stdio: `deep-agentic-core-mcp`
    - Authenticated Streamable HTTP: `deep-agentic-core-mcp-http` (`[http]` extra)
- **Keys and access**
    - Sign-up, key rotation and self-revocation
    - Per-key allow and deny lists, expiry and task scope, enforced at dispatch
    - Operator CLI: `deep-agentic-core-mcp-admin`
- **Storage and isolation**
    - Per-user sessions on memory, Redis or PostgreSQL, with quotas
    - Per-user Control Tower credentials held by the host
- **Evidence**
    - Access-decision logs and AIOS audit-event projections

Guides: [Remote hosting](remote-hosting.md) · [Hosted access control](access-control.md) ·
[Configuration](configuration.md) · [CLI reference](cli-reference.md)

## What you need

An MCP client or coding agent, the server installed (or a hosted key), and the optional DeepAgentLabs packages for the capabilities you use.

## Start here

Connect locally and call `core.version`, `core.compatibility` and `core.verify`: [follow the quickstart](developer-guide.md#quickstart).

## Limits

- Installed versions, adapter readiness and runtime health are separate checks.
- Optional producer tools report unavailable until that package is installed in the server environment.
- MCP cannot grant human approval for Tower recovery actions.
- Hosted HTTP always refuses `chaos.run_experiment`.

See [Limitations](limitations.md).

## Documentation

- [Developer Guide (simple)](developer-guide.md): short task workflows and a capability index
- [API Reference (detailed)](api-reference.md): every tool, resource, prompt, endpoint and entry point
- [AI Readable Documentation](ai-reference-index.md): the full reference as one file for AI tools, with source declarations and schemas
