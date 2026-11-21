# MCP Server developer guide

Use this simple guide to choose a capability and connect a client to the DeepAgentLabs MCP server. The [AI Reference (robust)](https://deepagentlabs.io/mcp/docs/llms-full.md) includes detailed operational guides, the generated tool catalog, current package declarations and all ten bundled schemas. Local stdio and hosted HTTP have different execution and authorization boundaries.

[Capability index](#capability-index) · [Quickstart](#quickstart) · [Configuration](#settings) · [Troubleshooting](#troubleshooting) · [Reference](#reference)

## Capability index

Each row links to a short workflow below, with detailed references for configuration, contracts and limitations.

| Capability | What you can do |
| --- | --- |
| [Local stdio connection](#stdio) | Connect an MCP host to the local server and verify the protocol boundary. |
| [Diagnostics and compatibility](#diagnostics) | Inspect version, health, adapter availability and the packaged candidate matrix. |
| [Tool catalog and discovery](#tools) | Discover all 53 tool interfaces, prerequisites, session effects and schemas. |
| [Resources and prompt templates](#resources) | Read reference/schema/session resources and retrieve five reusable prompts. |
| [Lens analysis and diagnosis](#lens) | Analyze workflows, diagnose failures, compare runs and inspect scores/SLOs. |
| [Suite, ModelFit, routing and optimization](#intelligence) | Compose recorded Lens suite/model/routing/optimization evidence without invoking models. |
| [Native Evals validation](#evals) | Validate native report/gate artifacts against packaged schema 1.0. |
| [Chaos catalog, local experiments and export](#chaos) | Discover faults, run authorized local scripts and export native reports to draft AIOS. |
| [Sidecar inventory and runtime boundary](#sidecar) | Discover supervision modules and distinguish discovery from live host-bound controls. |
| [AIOS schema and semantic validation](#validation) | Route supported 0.4/0.6/0.8 draft artifacts through offline schema and rule checks. |
| [Held-byte provenance resolution](#provenance) | Resolve provenance only against caller-held bytes without fetching referenced URIs. |
| [Unified release and incident workflows](#release-checks) | Compose comparisons, native evaluation/chaos evidence, gates, incident summaries and exports. |
| [Onboarding, session state and recall](#sessions) | Inspect setup, retain producer results and recall cited session reports. |
| [Hosted Streamable HTTP](#http) | Serve authenticated MCP requests with explicit host/origin and concurrency limits. |
| [Signup and key lifecycle](#keys) | Create, inspect, rotate and revoke hosted identities through configured stores. |
| [Per-key access policy and administration](#access) | Enforce allow/deny, expiry and task scope at dispatch; administer independently of agent keys. |
| [Tenant storage and dispatch serialization](#storage) | Isolate sessions across memory/Redis/PostgreSQL and serialize dispatch with revocation. |
| [Per-user Tower credentials](#tower-bindings) | Select HTTPS read/write credentials from host-owned bindings for the authenticated user. |
| [Tower investigation and recovery tools](#tower) | Read evidence, preview permitted recovery/runbooks, execute approved actions and verify outcomes. |
| [Independent Sidecar stop/revoke control](#stop) | Bind a live runtime and independently authorized task operator outside model tools. |
| [Access evidence and containment assertions](#containment) | Preserve dispatch/completion/denial observations and test bounded authenticated containment. |
| [Lens execution verification](#execution) | Verify expected-run bundles through host trust keys and expose verified causal identifiers. |
| [Operational AIOS audit projections](#audit) | Project public native access observations while withholding private text and credentials. |
| [Entry points and deployment configuration](#settings) | Configure three console entry points, optional producers, storage and operator boundaries. |
| [Upgrade, rollback and acceptance limits](#acceptance) | Check candidate support, protocol/wheel acceptance and operator-owned deployment state. |

## Quickstart

Requires Python 3.10 or newer in an activated virtual environment:

```bash
python -m pip install deep-agentic-core-mcp
```

Merge this entry into your MCP client's existing configuration. Use the executable's full path when the client cannot see your environment:

```json
{
  "mcpServers": {
    "deep-agentic-core": {
      "command": "deep-agentic-core-mcp",
      "args": []
    }
  }
}
```

[Download mcp-client.json](guide/examples/mcp-client.json)

Restart/reconnect the client, then request these **MCP tool calls** (not shell commands):

```text
core.version {}
core.compatibility {}
core.verify {}
```

Expect diagnostics with explicit optional-adapter availability. Missing producer packages do not mean the base server failed to connect. See [client connection](getting-started.md).

## Usage

Repository examples require a source checkout. Tool-call fragments run in an initialized MCP client; file paths, credentials, endpoints, runtime bindings and native artifacts must be supplied by the host. Optional producers run in the server environment, not automatically in the client environment.

<span id="stdio"></span>

### Local stdio connection

Run `deep-agentic-core-mcp` through the client's stdio configuration. The local process retains trusted workspace access and process-local workflow state. Restart after installing a producer or changing its environment. The base package supports diagnostics, prompts, resources and bundled spec validation without optional sibling packages. See [startup configuration](configuration.md#local-stdio) and [protocol interfaces](resources-and-prompts.md).

<span id="diagnostics"></span>

### Diagnostics and compatibility

Use `core.health`, `core.version`, `core.verify` and `core.compatibility`. Compatibility reports installed distribution observations against packaged acceptance pins; it does not prove the imported source, remote host readiness or current operator acceptance. `core.onboard` returns read-only setup steps. See [candidate matrix, degraded operation and protocol smoke](release-readiness.md).

<span id="tools"></span>

### Tool catalog and discovery

Use MCP `tools/list` to inspect the current surface. The [generated catalog](tools.md) covers all 53 registered tools, exact input schemas, prerequisites, expected duration and session mutations. Hosted discovery is filtered by access policy, and dispatch rechecks authorization; hiding a tool is not the enforcement mechanism. A listed tool can still report an unavailable producer.

<span id="resources"></span>

### Resources and prompt templates

Use MCP `resources/list` / `resources/read` for the sample workflow, fault catalog, release-check guide, AIOS schemas/rule catalogs and authorized saved sessions. Use `prompts/list` / `prompts/get` for five templates: `tower.investigation`, `lens.workflow_summary`, `lens.compare_summary`, `chaos.experiment_brief` and `core.release_check`.

Prompt retrieval supplies text; it does not execute tools or approve recovery. See [the complete resource and prompt inventory, arguments and protocol examples](resources-and-prompts.md).

<span id="lens"></span>

### Lens analysis and diagnosis

Install AgenticLens in the server environment, restart, and verify availability. Read `resource://examples/sample_workflow`; pass that JSON object as `artifact` to `lens.analyze_workflow` with a chosen session ID, then call `lens.report_summary` for that session. Structured run tools provide comparison, diagnosis, score analysis, evidence auditing and SLO summaries.

Use the exact artifact family each tool requests: profiling workflows, structured runs and evaluation reports differ. See [Lens tool schemas](tools.md) and [producer integration contracts](integrations.md#agenticlens).

<span id="intelligence"></span>

### Suite, ModelFit, routing and optimization

`lens.suite_from_traces` converts recorded runs into regression cases; `lens.suite_check` inspects suites. `lens.modelfit_recommend` reads experiment evidence, `lens.routing_decide` explains eligible routing, and `lens.optimization_analyze` reads recorded traces for opportunities. These tools compose Lens APIs and do not invoke provider models or silently adopt recommendations. See [inputs and output limits](tools.md) and [Lens integration](integrations.md).

<span id="evals"></span>

### Native Evals validation

`evals.validate_artifact` validates native evaluation-report or gate JSON with packaged schema 1.0. Schema validity does not mean a case passed or a release is approved. JUnit/Markdown are presentation formats, not native validator inputs. See [native report/gate contracts](evals-report-contract.md) and [tool input schema](tools.md).

<span id="chaos"></span>

### Chaos catalog, local experiments and export

`chaos.list_faults` discovers producer-supported faults. `chaos.run_experiment` executes a trusted local instrumented script under workspace confinement, configured path globs and timeout limits. `chaos.export_aios_run` maps a native report to a draft AIOS Run.

Hosted HTTP always rejects arbitrary chaos script execution. For hosted release checks, supply a report produced at an authorized local boundary. See [Chaos integration](integrations.md#agentic-chaos), [local script policy](configuration.md#local-chaos-script-policy), and [transport limits](limitations.md).

<span id="sidecar"></span>

### Sidecar inventory and runtime boundary

`sidecar.status` and `sidecar.module_inventory` expose installation/module diagnostics. They do not discover or govern arbitrary running agents. Live stop/revoke requires the explicit independent operator bridge below, bound to the process owning the actual runtime. Sidecar retains pre-action policy/authority/approval ownership. See [Sidecar contracts](sidecar-0.10.md), [integration inventory](integrations.md#agentic-sidecar) and [bridge setup](phase6-containment.md).

<span id="validation"></span>

### AIOS schema and semantic validation

`spec.validate_artifact` routes by the declared marker: Run/Workflow `0.4-draft`, provenance `0.6-draft`, and supported operational companions `0.8-draft`. Bundled schemas/catalogs resolve offline; an explicitly selected workspace catalog is authoritative. Results distinguish schema, semantic and unchecked process/cross-artifact obligations.

See [current validation and resource families](coordinated-v1-readiness.md), [tool input schema](tools.md) and [bundled schema inventory](resources-and-prompts.md). Package release numbers do not promote draft conformance.

<span id="provenance"></span>

### Held-byte provenance resolution

The Python adapter `resolve_provenance(record, held_subject_bytes)` resolves only bytes explicitly held by the caller. It does not fetch URIs, execute artifacts or authenticate conclusions merely because references resolve. Identity, digest and content validity remain separate results. This is a Python integration capability, not an additional MCP tool. See [adapter contract and offline cases](coordinated-v1-readiness.md).

<span id="release-checks"></span>

### Unified release and incident workflows

Use `core.compare_runs`, `core.release_check`, `core.incident_summary` and `core.export_report` to combine producer-owned evidence. A release-check fragment for an initialized MCP client is:

```json
{
  "session_id": "release-42",
  "evaluation_report": {"...": "replace with a complete native Evals report"},
  "required_evidence": ["evaluation"],
  "thresholds": {"min_pass_rate": 0.95}
}
```

The report placeholder must be replaced; it is not runnable evidence. Comparison and chaos evidence may be supplied or recalled from the session; native Evals evidence is supplied explicitly. Default required evidence is comparison, evaluation and chaos. Missing/invalid/failed gates block readiness. Incident summaries preserve failure signals without inventing causality, and report export uses MCP-local `mcp.unified-report.v1`, not AIOS. See [full workflow, statuses and examples](unified-workflows.md).

<span id="sessions"></span>

### Onboarding, session state and recall

```text
core.onboard {}
core.session_state {"session_id":"release-42"}
core.report_recall {"session_id":"release-42"}
```

`core.report_recall {}` lists saved sessions; scoped recall returns stored results, recent history and deterministic cited notes, without fresh scoring. `resource://sessions/{encoded-session-id}` exposes the same authorized evidence. Unknown recall IDs do not create new reports. See [onboarding/recall and source citations](phase6-containment.md#onboarding-saved-artifacts-and-recall).

<span id="http"></span>

### Hosted Streamable HTTP

Install `deep-agentic-core-mcp[http]`, configure a key store plus shared session storage, and launch `deep-agentic-core-mcp-http`. The endpoint is `/mcp`; requests carry a bearer key and MCP protocol headers. Configure public host/origin rules and process-level request/concurrency limits. `/healthz` checks storage readiness, not all optional adapters.

The base CLI refuses missing authentication/storage configuration. In-memory sessions are available only through explicit embedding/test configuration. See [configuration](configuration.md#hosted-http) and [complete hosting setup, containers and operator-owned deployment](remote-hosting.md). This guide does not deploy a service.

<span id="keys"></span>

### Signup and key lifecycle

Deployments with the configured database/DynamoDB signup store expose `/signup` for generated user identities and one-time keys. Profile, replacement and self-revocation require the current key; replacing a key preserves stable user/session ownership. Display names are unverified labels, and keys are not recoverable. Environment-key changes require worker restarts; stored lifecycle changes apply through the key store. See [client/key workflow](user-guide.md) and [store choices](remote-hosting.md).

<span id="access"></span>

### Per-key access policy and administration

Host-owned policies configure `allow`, `deny`, `expires_at` and task scope. Deny wins. Hosted tools are reauthorized after acquiring the session dispatch transaction, so queued calls/retries observe revocation and narrowed permissions. `core.access_status` explains effective permissions when allowed by the policy.

The separate administrator CLI uses store credentials, not the agent bearer key:

```bash
deep-agentic-core-mcp-admin show USER_ID
```

`set-permissions`, `clear-permissions` and `revoke` mutate operator-owned access; use the documented exact user and policy. See [administration/dispatch semantics](access-control.md) and [all four admin commands](cli-reference.md).

<span id="storage"></span>

### Tenant storage and dispatch serialization

Hosted session names are isolated by authenticated owner. Redis takes session precedence over PostgreSQL; with no Redis, a configured database can hold sessions, keys and signup limits. Session quotas are 100 sessions and 4 MiB serialized state per user, with a one-hour idle TTL. Rate/concurrency counters remain per worker.

Dispatch/revocation share owner-specific serialization. Redis uses a non-expiring guard and bounded acquisition; crashes require operator reconciliation before clearing an orphan. PostgreSQL uses transaction locking; memory is single-process only. See [storage setup and quotas](remote-hosting.md) and [dispatch guards and recovery limits](phase6-containment.md#shared-redis-dispatch-guard).

<span id="tower-bindings"></span>

### Per-user Tower credentials

Configure `DEEP_AGENTIC_CORE_MCP_TOWER_BINDINGS` on the host with per-user HTTPS origins and separate read/write credentials. Selection uses the reauthenticated caller identity at dispatch, with no credential or origin accepted as tool arguments. Missing bindings fail closed; write tools need a write token. Approval remains human-only in Tower. See [binding shape, reload and redirect rules](phase6-containment.md#hosted-tower-credentials).

<span id="tower"></span>

### Tower investigation and recovery tools

`tower.*` exposes status, agents, versions, posture, incidents/evidence, detection/investigation, permitted recovery preview/execute/verify and runbook discovery/preview/execution/cancellation. `tower.capability_contract` discovers the remote contract. Use the generated schemas to select exact IDs and parameters.

MCP cannot grant human approval. Execution consumes separately approved Tower previews, and successful execution alone does not establish verified recovery. See [runbook workflows](tower-0.9-runbooks.md), [capability readiness](tower-0.10-compatibility.md), and [all Tower tool inputs](tools.md).

<span id="stop"></span>

### Independent Sidecar stop/revoke control

The embedding host supplies a live `SidecarBridge`/`TaskBinding`, `TaskKeyRevoker` and an independent `operator_store` to `transport_http.create_app`. Operator credentials are exact-task scoped and separate from agent credentials. POST `/control/tasks/{task_id}/stop` is an operator route, not a model-callable MCP tool.

The bridge acknowledges only effective native stop/access revocation with successful evidence persistence. Unsupported bindings, failures, in-flight work and cooperative cancellation remain explicit. Already-reserved calls may finish. See [complete host binding, receipt, retry and scope semantics](phase6-containment.md#authenticated-sidecar-stoprevoke-bridge).

<span id="containment"></span>

### Access evidence and containment assertions

Hosted access logs preserve `mcp.access-decision.v1` dispatch, completion, denial and rejected-revocation observations with correlation and task identity; credentials and tool arguments are omitted. Dispatch means admission, not completion. A per-call denial is not proof that every downstream credential was revoked.

The paired Chaos/Lens/Evals acceptance path verifies explicitly scoped ordered snapshots and includes bypassed-authorizer negative controls. Completeness remains producer-declared. See [native access evidence](access-control.md#denials-and-evidence), [assertion setup and acceptance cases](phase6-containment.md#evidence-and-native-assertions), and [reusable containment scoring](evals-0.11-containment.md).

<span id="execution"></span>

### Lens execution verification

`lens.execution_verify` accepts an actual Lens ExecutionBundle plus an expected `run_id`. Configure `DEEP_AGENTIC_CORE_MCP_LENS_TRUST_STORE` as a protected host JSON key-ID → hex-key map; callers cannot supply keys, trust paths or precomputed verdicts. The server delegates authenticated snapshot, conformance and mapping checks to Lens.

Only verified evidence exposes causal IDs. Failed, unknown and incomplete evidence remain distinct, without raw payload exposure. This tool neither signs nor executes evidence. See [key setup, rotation, coverage and required Lens capability](lens-execution-evidence.md).

<span id="audit"></span>

### Operational AIOS audit projections

Python `services.access_evidence.export_audit_event(...)` projects native public access observations with supplied public target/actor context to an AIOS `0.8-draft` audit event. It preserves native identity/correlation while withholding private subject/tool/reason text. Dispatch maps to started, denial to denied, and completion follows the observed outcome or unknown.

This adds no automatic remote export or enforcement. See [current projection contract](aios-0.8-operational-artifacts.md), [public-target example](coordinated-v1-readiness.md) and `examples/operational_artifacts.py` in the checkout.

<span id="settings"></span>

## Entry points and deployment configuration

The package installs `deep-agentic-core-mcp` (stdio), `deep-agentic-core-mcp-http` (authenticated HTTP with `[http]`) and `deep-agentic-core-mcp-admin` (operator key policy/revocation). Optional producers must be installed/configured in the server's selected environment. Workspace-root settings may select explicit sibling sources/catalogs over installed/bundled defaults.

See [environment variables and precedence](configuration.md), [entry points/admin syntax](cli-reference.md), [HTTP/storage setup](remote-hosting.md) and [limitations](limitations.md). Package publication does not deploy AWS or update an existing service.

<span id="acceptance"></span>

### Upgrade, rollback and acceptance limits

Record actual version, compatibility observations, policy and binding configuration without credentials. Use fresh pinned environments or immutable image digests, verify protocol/tool/storage behavior, and run explicit operator deployment acceptance. On rollback, reconcile in-flight effects and dispatch guards before restoring the prior environment; do not restore revoked credentials.

See [acceptance matrix and upgrade/rollback sequence](release-readiness.md), [current AIOS changes](coordinated-v1-readiness.md), and [hosted boundaries](limitations.md). Independent review, live/deployment acceptance and stable schema/API freezing remain separate from package milestones.

## Troubleshooting

Check the client's executable/environment, optional adapter readiness and selected workspace root. For hosted denials, inspect key policy/store availability and task binding, then retry only after the owner resolves guard/revocation state. Use the [troubleshooting guide](troubleshooting.md); do not weaken hosted authorization to repair a local connection.

## Reference

- [Generated 53-tool catalog](tools.md), [resources/prompts](resources-and-prompts.md), and [entry points/admin CLI](cli-reference.md).
- [AI Reference (robust)](https://deepagentlabs.io/mcp/docs/llms-full.md) and [capability/source index](ai-reference-index.md).
- [Source manifest and checksums](ai-docs-manifest.json).
