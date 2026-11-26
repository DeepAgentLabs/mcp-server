# API Reference (detailed)

**Version:** 1.1.1

The server's public interface is the MCP protocol: tools, resources and prompt templates, served over local stdio or authenticated HTTP. This page lists every interface in one place. For each tool's exact input schema, prerequisites and examples, see the [generated tool catalog](tools.md).

Call tools from an initialized MCP client (`tools/call`), not as shell commands. Hosted keys see only the tools their access policy allows, and dispatch rechecks that policy on every call.

---

## MCP protocol methods

| Method | What it returns |
| --- | --- |
| `tools/list` | The 56 tools below, with input schemas (filtered by access policy when hosted) |
| `tools/call` | A tool's JSON result |
| `resources/list` | Reference, schema, documentation and authorized session resources |
| `resources/read` | One resource's content |
| `prompts/list` | The six prompt templates and their arguments |
| `prompts/get` | A rendered prompt message |

---

## Tools

"Duration" is the registered expectation (`instant`, `fast` or `slow`). "Changes session" means the call stores results in the named session for later tools such as `core.release_check`.

### Core (`core.*`, 15 tools)

| Tool | What it does | Duration | Changes session |
| --- | --- | --- | --- |
| `core.access_status` | Report the calling hosted key's effective access policy: allow and deny globs, task scope, expiry, and the tools it may call right now | instant | no |
| `core.compare_runs` | Compare baseline and candidate trace runs for regressions, storing the comparison for core.release_check | fast | yes |
| `core.compatibility` | Inspect the packaged candidate acceptance matrix and local installed distribution versions | instant | no |
| `core.docs_catalog` | Discover all seven DeepAgentLabs products, bundled documentation versions, commit-pinned sources and resource URIs | fast | no |
| `core.docs_read` | Read the robust AI reference for a product or cited section: APIs, CLI, configuration, schemas and complete examples | fast | no |
| `core.docs_search` | Search robust AI references across all seven products, optionally filtered by product | fast | no |
| `core.export_report` | Export the session's workflow, analysis, comparison, chaos, release-check and incident evidence as one MCP-local JSON envelope (mcp.unified-report.v1; not an AIOS artifact) | instant | no |
| `core.health` | Return rich server diagnostics: adapter availability, loaded tools/resources/prompts, and recent successful calls | instant | no |
| `core.incident_summary` | Collect regressions, chaos crashes or timeouts, failed evaluation cases and blocked release gates from supplied or session evidence for investigation | fast | yes |
| `core.onboard` | Read-only setup steps with sibling readiness | fast | no |
| `core.release_check` | Decide release readiness from a Lens comparison, an Evals report (judged by the Evals release gate) and a chaos.run_experiment report | fast | yes |
| `core.report_recall` | Browse saved artifacts and history with source-cited investigation notes | fast | no |
| `core.session_state` | Inspect the artifacts and call history accumulated in a session | instant | no |
| `core.verify` | Check connectivity to agenticlens, agentic-chaos, agentic-sidecar, and ai-operations-spec, and report readiness | instant | no |
| `core.version` | Return the current server package version | instant | no |

### AgenticLens (`lens.*`, 13 tools)

| Tool | What it does | Duration | Changes session |
| --- | --- | --- | --- |
| `lens.analyze_workflow` | Analyze an AgenticLens-compatible workflow artifact | fast | yes |
| `lens.audit_report` | Return case-by-case evaluation detail for an audit trail | fast | no |
| `lens.compare_runs` | Compare baseline and candidate trace runs for regressions | fast | yes |
| `lens.diagnose_run` | Diagnose a trace run: failure taxonomy, faulty step and agent with confidence and supporting spans, incident timeline, anomalies against optional baseline runs, and an investigation narrative | fast | no |
| `lens.execution_verify` | Verify a Lens AIOS execution bundle with host-configured keys | fast | no |
| `lens.modelfit_recommend` | Recommend a model per task category from supplied AgenticLens experiment reports, under hard quality, cost, latency, safety, provider and deployment constraints that fail closed | fast | no |
| `lens.optimization_analyze` | Rank evidence-backed optimizations from AgenticLens Run traces: prompt caching and compression, retrieval pruning and reranking, memory summarization, tool caching, retry policy, redundant steps, unnecessary handoffs and quality-cost trade-offs between variants | fast | no |
| `lens.report_summary` | Render a Markdown workflow report and recommendation summary | fast | yes |
| `lens.routing_decide` | Explain a model route from a saved ModelFit report and routing policy | fast | no |
| `lens.score_analysis` | Report deterministic and model-based scores separately, judge cost (kept apart from agent cost), and evaluator disagreement for an evaluation report | fast | no |
| `lens.slo_summary` | Apply release-gate style SLO thresholds to an evaluation report | fast | no |
| `lens.suite_check` | Check a test suite before approval: counts by split, domain, tag, source and review status; exact, near and conflicting duplicates; unmasked PII (types and locations only); and the approval checks AgenticLens would run | fast | no |
| `lens.suite_from_traces` | Convert successful trace runs into a draft regression suite: each case expects the run's tool trajectory and latency/cost within a margin, is marked needs_review, and has PII masked unless 'mask' is false | fast | no |

### Agentic Chaos (`chaos.*`, 3 tools)

| Tool | What it does | Duration | Changes session |
| --- | --- | --- | --- |
| `chaos.export_aios_run` | Convert a chaos report into an AI Operations v0.4-draft run artifact (via agentic-chaos>=0.5.1) and validate it with rule-cited conformance | fast | no |
| `chaos.list_faults` | List the supported fault types for chaos experiments | instant | no |
| `chaos.run_experiment` | Run a workspace-sandboxed target script under selected chaos faults and report the resulting events | slow | yes |

### Agentic Evals (`evals.*`, 1 tools)

| Tool | What it does | Duration | Changes session |
| --- | --- | --- | --- |
| `evals.validate_artifact` | Validate native evaluation reports or gate decisions against the published Evals 1.0 schemas | fast | no |

### Agentic Sidecar (`sidecar.*`, 2 tools)

| Tool | What it does | Duration | Changes session |
| --- | --- | --- | --- |
| `sidecar.module_inventory` | List installed modules, framework adapter files, and integration placeholders present in agentic-sidecar | instant | no |
| `sidecar.status` | Report whether agentic-sidecar is importable and whether its decision runtime APIs are installed; no live task connection is implied | instant | no |

### AI Operations Specification (`spec.*`, 1 tools)

| Tool | What it does | Duration | Changes session |
| --- | --- | --- | --- |
| `spec.validate_artifact` | Validate an AIOS artifact against the schema set its `spec_version` names (v0.5 compatibility rules), returning a conformance report that cites AI Operations rule IDs separately from server presentation | fast | no |

### Control Tower (`tower.*`, 21 tools)

| Tool | What it does | Duration | Changes session |
| --- | --- | --- | --- |
| `tower.agents` | Registered agents, filtered by status, environment or capability | fast | no |
| `tower.capability_contract` | Tower capability descriptor, schemas and status meanings | fast | no |
| `tower.detect` | Open an incident from an agent's evidence record | fast | no |
| `tower.evidence` | An agent's evidence history, optionally by source | fast | no |
| `tower.execute` | Run a recovery action whose exact preview a human approved | fast | no |
| `tower.incident` | Read one incident | fast | no |
| `tower.incidents` | List incidents | fast | no |
| `tower.investigate` | Assemble a cited investigation for an incident | fast | no |
| `tower.posture` | Evidence freshness and availability posture | fast | no |
| `tower.preview` | Preview a permitted recovery action for human approval | fast | no |
| `tower.runbook_cancel` | Cancel a runbook run between steps | fast | no |
| `tower.runbook_execute` | Run an approved runbook preview | slow | no |
| `tower.runbook_execution` | Read one runbook run | fast | no |
| `tower.runbook_executions` | Runbook runs for an incident | fast | no |
| `tower.runbook_preview` | Preview a runbook run for an incident, for human approval | fast | no |
| `tower.runbook_recommendations` | Runbooks recommended for an incident | fast | no |
| `tower.runbook_verify` | Verify a runbook run's outcome with fresh Lens and Evals evidence | fast | no |
| `tower.runbooks` | List installed versioned runbooks | fast | no |
| `tower.status` | Fleet status, optionally for one environment | fast | no |
| `tower.verify` | Verify an incident's recovery with fresh Lens and Evals evidence | fast | no |
| `tower.versions` | Agents whose reported capability version meets a minimum | fast | no |

---

## Resources

| URI | Content |
| --- | --- |
| `resource://examples/sample_workflow` | Sample workflow artifact for `lens.analyze_workflow` |
| `resource://catalogs/chaos_faults` | Chaos fault catalog |
| `resource://workflows/release-check` | Ordered release-check guide |
| `resource://schemas/aiops/v0.4/{common,run,workflow}` | AIOS v0.4 JSON schemas |
| `resource://schemas/aiops/v0.6/provenance` | AIOS v0.6 provenance schema |
| `resource://schemas/aiops/v0.8/{common,audit_event,investigation_report,verification_signal}` | AIOS v0.8 JSON schemas |
| `resource://specs/aiops/{v0.4,v0.6,v0.8}/conformance-rules` | AIOS conformance-rule catalogs |
| `resource://specs/aiops/v0.5/compatibility` | AIOS version compatibility catalog |
| `resource://docs/catalog` | The seven products' documentation versions, source commits and URIs |
| `resource://docs/{product}/reference` | A product's full AI-readable reference (Markdown) |
| `resource://docs/{product}/index` | A product's capability index (Markdown) |
| `resource://docs/{product}/manifest` | Source selection and checksums (JSON) |
| `resource://docs/{product}/license` | The product's license notice |
| `resource://sessions/{encoded-session-id}` | Saved evidence and history for one of your sessions |

Product IDs: `agenticlens`, `agentic-evals`, `agentic-chaos`, `agentic-sidecar`, `agenticops-control-tower`, `ai-operations-spec`, `mcp-server`. See [Resources and prompts](resources-and-prompts.md) and [Build with the seven-product AI reference](ecosystem-ai-reference.md).

---

## Prompt templates

| Prompt | Arguments | Purpose |
| --- | --- | --- |
| `core.build_with_ecosystem` | `task` (required), `products` | Build from the product references using search and complete reads |
| `core.release_check` | `session_id` | Walk a host through the unified release check |
| `tower.investigation` | `incident_id` (required) | Investigate an incident with Tower evidence tools |
| `lens.workflow_summary` | `workflow_name` (required), `recommendation_count`, `estimated_savings_pct` | Summarize an analyzed workflow for an operator |
| `lens.compare_summary` | `baseline_label`, `candidate_label` | Summarize a baseline-versus-candidate comparison |
| `chaos.experiment_brief` | `faults` (required), `script` | Explain the intent and expected impact of a chaos run |

Prompts return text only. They don't run tools or grant approval.

---

## HTTP endpoints (hosted)

Served by `deep-agentic-core-mcp-http` (install the `[http]` extra).

| Route | Method | Purpose |
| --- | --- | --- |
| `/mcp` | Streamable HTTP | MCP endpoint; requires a bearer key and MCP protocol headers |
| `/healthz` | GET | Storage readiness (not every optional adapter) |
| `/signup`, `/api/signup` | GET, POST | Create a hosted identity and one-time key, when a signup store is configured |
| `/api/account` | GET, POST, DELETE | Read the profile, replace the key or self-revoke, using the current key |
| `/control/tasks/{task_id}/stop` | POST | Operator-only Sidecar stop/revoke; needs separate operator credentials and host bindings |

See [Remote hosting](remote-hosting.md) and [Hosted access control](access-control.md).

---

## Console entry points

| Command | Purpose |
| --- | --- |
| `deep-agentic-core-mcp` | Local stdio MCP server |
| `deep-agentic-core-mcp-http` | Authenticated Streamable HTTP server |
| `deep-agentic-core-mcp-admin show USER_ID` | Read a user's state and effective access policy |
| `deep-agentic-core-mcp-admin set-permissions USER_ID` | Replace the stored access policy |
| `deep-agentic-core-mcp-admin clear-permissions USER_ID` | Restore the default hosted surface |
| `deep-agentic-core-mcp-admin revoke USER_ID` | Revoke a user's key |

See [CLI reference](cli-reference.md) and [Configuration](configuration.md).

---

## Python integration points

These are for hosts embedding the server. They aren't MCP tools.

| Symbol | Purpose |
| --- | --- |
| `transport_http.create_app(...)` | Build the HTTP app, optionally with Sidecar stop/revoke bindings |
| `adapters.ai_operations_spec.resolve_provenance(record, subjects)` | Resolve AIOS provenance against bytes the caller holds, without fetching URIs |
| `services.access_evidence.export_audit_event(...)` | Project access observations to an AIOS `0.8-draft` audit event |

See [Coordinated v1 readiness](coordinated-v1-readiness.md), [Phase 6 containment](phase6-containment.md) and [AIOS 0.8 operational artifacts](aios-0.8-operational-artifacts.md).
