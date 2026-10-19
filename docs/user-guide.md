# Using the DeepAgentLabs MCP server

This guide covers connecting an assistant, integrating your application, and
choosing hosted versus local tools. For exact tool arguments see the generated
[tool reference](https://github.com/DeepAgentLabs/mcp-server/blob/main/docs/tools.md); operators should use [AWS hosting](https://github.com/DeepAgentLabs/mcp-server/blob/main/deploy/aws/README.md).

## 1. Get a key and connect

Visit https://mcp.deepagentlabs.io/signup, enter a display name, and save or
download your key. There is no password, verified email, or recovery flow.
Anyone holding a key can access that user's sessions. Each signup creates an
independent identity, even if display names match.

Configure your assistant's MCP connection:

| Setting | Value |
| --- | --- |
| Transport | Streamable HTTP |
| Server URL | `https://mcp.deepagentlabs.io/mcp` |
| Header | `Authorization: Bearer <your-key>` |

Your client must support remote HTTP MCP connections and custom authorization
headers. Generic configuration below illustrates the fields; use your client's
supported configuration format rather than assuming these keys are universal:

```json
{
  "type": "http",
  "url": "https://mcp.deepagentlabs.io/mcp",
  "headers": {"Authorization": "Bearer <your-key>"}
}
```

A client requiring OAuth discovery/login instead of custom bearer headers needs
an additional integration: this server currently authenticates MCP API keys.
Start by asking your assistant to call `core.health` and list available tools.
`core.verify` checks every adapter, so its overall `ok` can be false when optional
integrations are absent, even while hosted analysis works.

## 2. Understand what is available

Hosted availability below reflects the `0.3.9` hosted image (2026-10-17). Call `core.health` for the
current status; a tool appearing in the catalog does not guarantee its optional
package is installed.

| Capability | Hosted server | Local server |
| --- | --- | --- |
| AgenticLens analysis and Markdown reports (with finding provenance) | Available (AgenticLens 0.8.0) | Requires AgenticLens installation (`>=0.6.1` for step provenance on every finding) |
| AgenticLens run diagnosis and score analysis (`lens.diagnose_run`, `lens.score_analysis`) | Available (AgenticLens 0.8.0) | Requires `agenticlens>=0.7.0` |
| AgenticLens suite drafting and approval checks (`lens.suite_from_traces`, `lens.suite_check`) | Available (AgenticLens 0.8.0; nothing stored) | Requires `agenticlens>=0.8.0` |
| AgenticLens ModelFit recommendations (`lens.modelfit_recommend`) | Available (AgenticLens 0.9.0; nothing stored, no model called) | Requires `agenticlens>=0.9.0` |
| Baseline/candidate run comparison | Available | Requires AgenticLens installation |
| Evaluation-report SLO gates and audit/HTML reports | Available through `lens.*` | Requires AgenticLens installation |
| AI Operations artifact validation (`spec_version` routing, rule-cited conformance) | Available, including the rule and compatibility catalogs | Requires canonical schema assets (`ai-operations-spec>=0.5.1` for rule IDs) |
| Converting a chaos report to an AIOS run (`chaos.export_aios_run`) | Available (Agentic Chaos 0.6.0; no code runs) | Available with `agentic-chaos>=0.5.1` |
| Agentic Chaos fault listing | Available (Agentic Chaos 0.6.0) | Available with Agentic Chaos installed |
| Native Agentic Evals artifact validation | Available through `evals.validate_artifact` | Available from bundled schemas |
| Control Tower investigation and recovery connector | Local only, with configured Tower credentials | Requires authenticated local Tower service |
| Executing chaos experiments | Disabled and excluded from the HTTP catalog | Available over trusted local stdio |
| Sidecar status and module discovery | Package not installed in the hosted image | Available with Sidecar installed; discovery only |
| Sidecar runtime supervision / decision gates | No MCP execution tools implemented | No MCP execution tools implemented |
| Running agentic-evals suites, targets, or judges | No dedicated MCP tools implemented | Run the package's own API/CLI |

The MCP server consumes artifacts your application supplies. Connect your
workflow to the appropriate tracing/evaluation libraries in your application,
then send exported artifacts to MCP. Connecting an assistant alone does not
instrument your running agents or grant access to their local files.

## 3. Analyze a workflow

An AgenticLens workflow artifact contains a name, timestamps, and steps with
metrics. See [the complete example](https://github.com/DeepAgentLabs/mcp-server/blob/main/examples/sample_workflow.json).

Ask your assistant:

> Call lens.analyze_workflow with this workflow JSON and session_id
> "refund-agent-v1". Then call lens.report_summary using the same session_id,
> without resending the artifact. Explain the recommendations and cost/latency findings.

Equivalent tool arguments:

```json
{"artifact": "<replace with the actual workflow JSON object>", "session_id": "refund-agent-v1"}
```

The artifact must be an object, not the placeholder string above or a local
filename. Follow with:

```json
{"session_id": "refund-agent-v1"}
```

for `lens.report_summary` or `core.session_state`.

Each recommendation in the `lens.analyze_workflow` response has a `provenance`
block showing where it came from:

```json
{
  "artifact": {"workflow_id": "wf-provenance", "workflow_name": "...", "digest": "sha256:..."},
  "step": {"id": "retrieve", "id_in_artifact": true, "name": "Retriever", "type": "retriever", "index": 0},
  "span_ids": ["retrieve"],
  "evidence_sources": ["workflow.step"],
  "resolved": true,
  "producer": {"name": "agenticlens", "version": "0.6.1", "optimization_type": "rag_top_k_reduction"}
}
```

`resolved` is true only when the step and every cited span exist in the
artifact you sent. The digest is a SHA-256 of the artifact's canonical JSON, so
you can confirm which input a finding refers to. It is traceability, not tamper
evidence. `provenance_summary` lists any unresolved findings by title.

### Validate AI Operations artifacts

`spec.validate_artifact` reads the artifact's `spec_version` and validates it
against that version's published schemas. An artifact declaring a version the
server has no schemas for is rejected; it is never checked against a different
version. `compatibility` gives the decision and the v0.5 rule that applies
(`AIOS-0.5-V02` for the current `0.4-draft` artifacts). `conformance` lists
every AI Operations rule with `pass`, `fail`, `not_evaluated` (process
obligations, or semantic rules when the schema already failed) or
`not_applicable`, and each issue carries the rule it violates:

```json
{"rule_id": "AIOS-0.4-P05", "message": "rel-1 references missing object step-9"}
```

Fields outside `conformance` (`ok`, `claim`, `schema_errors`,
`semantic_errors`) are this server's presentation, not specification rules.
The catalogs themselves are MCP resources:
`resource://specs/aiops/v0.4/conformance-rules` and
`resource://specs/aiops/v0.5/compatibility`.

Sessions are scoped to the authenticated user. Two users can use
`refund-agent-v1` without sharing data. Reusing a session ID within one account
shares that account's context. Hosted sessions expire after one hour of
inactivity and are limited to 100 sessions / 4 MiB of state per user. Save returned
reports in your own storage when you need durable history.

## 4. Integrate with your agentic application

Use your framework's MCP client to discover tools and call them with JSON
arguments. Keep the key in your application's secret configuration, outside
prompts and model-visible tool arguments. Use one user key for each intended
identity; all applications sharing a key also share its workflow context.

A typical application sequence is:

1. Run your agent and collect its trace/workflow artifact through your normal instrumentation.
2. Call `lens.analyze_workflow` with the artifact and a run-specific `session_id`.
3. Call `lens.report_summary` using the same session ID.
4. Persist returned analysis/report content alongside your run records.
5. Compare baseline and candidate runs with `lens.compare_runs` before release.

The repository includes a runnable Python HTTP example specifically for this
server's stateless JSON transport:

```bash
export MCP_URL=https://mcp.deepagentlabs.io/mcp
# The script prompts privately for a key if MCP_API_KEY is not set.
python examples/hosted_workflow.py examples/sample_workflow.json --session-id demo-run
```

The example sends your supplied artifact and prints analysis plus a Markdown
report. It does not call an LLM or execute your workflow. In CI, supply
`MCP_API_KEY` through your CI secret store. Treat network errors and HTTP 503 as
transient; respect HTTP 429 Retry-After. A successful HTTP response can still
contain an MCP error or a tool payload with `ok: false`; inspect both.
Concurrent mutations to one user's sessions can return a retryable conflict.

## 5. Evals, regression comparison, and release gates

Run `agentic-evals` in your own application or CI to execute suites/judges. This
MCP server has no `evals.run` tool. It exposes AgenticLens evaluation-report
consumers:

- `lens.slo_summary`: `{"report": <EvaluationReport object>, "thresholds": {"min_pass_rate": 0.95}}`
- `lens.audit_report`: `{"report": <EvaluationReport object>, "include_html": true}`
- `lens.diagnose_run`: `{"run": <Run trace object>, "baseline": [<Run>, ...], "config": {"max_cost_usd": 0.05}, "budget": {"max_spans": 5000}}`
- `lens.score_analysis`: `{"report": <EvaluationReport object>}`
- `lens.suite_from_traces`: `{"runs": [<Run object>, ...], "name": "prod-regression", "version": "1.0.0", "strategy": "hash"}`
- `lens.suite_check`: `{"suite": <agentic-evals TestSuite object>, "threshold": 0.85}`
- `lens.modelfit_recommend`: `{"reports": [<ExperimentReport object>], "config": {"defaults": {"min_pass_rate": 0.85}, "categories": [{"id": "orders", "tags": ["orders"]}]}, "variant_metadata": {"mid-b": {"provider": "provider-b"}}}`
- `lens.compare_runs`: `{"baseline": [<Run object>], "candidate": [<Run object>], "session_id": "release-check"}`

Use JSON conforming to AgenticLens's `EvaluationReport` or `Run` models. Validate
compatibility when exporting from agentic-evals; do not assume any arbitrary
scoring result or console output is a compatible report. `spec.validate_artifact`
uses the canonical AI Operations artifact schemas, which are a different
contract from these AgenticLens input models. Check the tool's expected schema.
Your CI/application must enforce the returned gate decision; an MCP gate report
does not deploy or block a release automatically.

## 6. Chaos and Sidecar on your own machine

For chaos execution, run the stdio MCP server on the machine or trusted
workspace containing your target script and installed sibling libraries.
The usual MCP client command is `deep-agentic-core-mcp`; install the MCP package
and required ecosystem packages in that command's Python environment. The repo's
local workspace setup is described in [README](https://github.com/DeepAgentLabs/mcp-server/blob/main/README.md).

Call `core.health`, then `chaos.list_faults` to discover supported faults.
Call `chaos.run_experiment` with a script path inside the configured workspace,
selected faults, timeout, and session ID. It executes real code; review
[SECURITY.md](https://github.com/DeepAgentLabs/mcp-server/blob/main/SECURITY.md). A server-relative path refers to the machine
[SECURITY.md](https://github.com/DeepAgentLabs/mcp-server/blob/main/SECURITY.md). To limit which scripts it may run, set
`DEEP_AGENTIC_CORE_MCP_ALLOWED_SCRIPT_GLOBS` (for example
`my-agent/chaos/*.py`) and optionally `DEEP_AGENTIC_CORE_MCP_DENIED_SCRIPT_GLOBS`
in the server's environment. Deny wins, and `.venv`, `site-packages` and `.git`
are always denied.

With `agentic-chaos>=0.5.1` the result also includes `aios_run`, the experiment
as an AI Operations v0.4-draft Run, and `aios_export.aligned`, the outcome of
validating it. Pass `"workflow_id"` to link the run to a Workflow definition, or
`"export_aios": false` to skip the export. `chaos.export_aios_run` converts a
saved report, or the session's last experiment, without running anything:

```json
{"session_id": "stream-demo", "workflow_id": "customer-support"}
```

A server-relative path refers to the machine
running that server, not automatically to a remote client's filesystem.

Export normal and chaos run artifacts locally, then send compatible baseline
and candidate run objects to the hosted `lens.compare_runs` tool if desired.
Install/connect Sidecar locally to inspect `sidecar.status` and
`sidecar.module_inventory`. These tools describe package/runtime readiness and
installed modules and public API capabilities; they do not supervise live decisions
through MCP. Sidecar v0.7 local status/audit/operator APIs are reported when installed,
while runtime_connected and mcp_runtime_controls remain false.

## 7. Manage access

Return to the signup page and open “Already have a key?” to inspect your account,
replace its key, or revoke it. Replacement keeps the user ID and workflow
sessions; update every client using the old key. Revocation closes access to
that account. Requests already in progress may finish. Lost keys cannot be
recovered in the current signup flow.

| Problem | Check |
| --- | --- |
| HTTP 401 | Missing, wrong, replaced, or revoked bearer key |
| HTTP 403/421 | Browser Origin or Host is not allowed; operators must configure exact trusted values |
| HTTP 429 | Request/concurrency or signup limits; respect Retry-After |
| HTTP 503 | Authentication/session storage unavailable; retry later |
| Adapter unavailable | Check `core.health`; use a local install for optional packages |
| Workflow/report input rejected | Use the model expected by that tool; inspect `ok` and `error` |

### Chaos v0.5 streaming with MCP 0.3.2

Install `agentic-chaos>=0.5.0` in the local MCP server environment. The catalog
includes four streaming faults and auth/context-length errors dynamically.
The example lives in the source repository; installing the PyPI wheel alone
does not create it. Prepare a trusted local workspace before starting the stdio
server (use your chosen Python environment):

```bash
mkdir -p chaos-workspace
cd chaos-workspace
git clone --branch v0.3.2 https://github.com/DeepAgentLabs/mcp-server.git mcp-server
python -m pip install 'deep-agentic-core-mcp==0.3.2' 'agentic-chaos>=0.5.0'
export DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT="$PWD"
deep-agentic-core-mcp
```

For an MCP host that launches the server itself, put the same absolute workspace
path in its server environment configuration. Setting the variable in another
terminal does not change an already-running host's environment. Your own target
scripts can also live anywhere inside that configured workspace.

Then call `chaos.run_experiment` with:

```json
{
  "script": "mcp-server/examples/chaos_stream_target.py",
  "faults": ["stream_cut"],
  "timeout_seconds": 30,
  "session_id": "stream-demo"
}
```

The example uses `chaos_stream()` under the runner-owned session. Default
`stream_cut` delivers one chunk, closes the source, and returns a native event
with `outcome="degraded"` and `detail.chunks_delivered=1`. The script succeeds;
that does not mean its output quality is acceptable. Apply downstream checks
as appropriate. Paths are resolved inside the server's workspace.

Profiles and provider patch helpers remain Python/CLI APIs in Chaos; the MCP
request schema exposes fault names rather than those configuration surfaces.
Hosted HTTP continues to reject `chaos.run_experiment`. MCP 0.3.3 adds the AIOS
run export described in section 6 (requires `agentic-chaos>=0.5.1`).

## Native Evals validation

Use `evals.validate_artifact` for reports or gate decisions. This offline tool
works without Lens. See [the contract guide](evals-report-contract.md).
