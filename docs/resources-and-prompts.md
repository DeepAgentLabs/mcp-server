# Resources and prompt templates

The MCP protocol exposes tools, resources and prompts separately. Listing or retrieving a prompt/resource does not run a tool, authenticate evidence or approve an action. Use an initialized MCP client rather than entering protocol methods as shell commands.

## Resource inventory

`resources/list` advertises the static reference catalog plus loaded schema/rule resources. The table below records this checkout's reference inventory; an explicitly selected workspace catalog can change schema availability. Tool diagnostics report unavailable assets rather than fetching them implicitly.

| URI | Content | Kind |
| --- | --- | --- |
| `resource://examples/sample_workflow` | Sample workflow artifact | `workflow-json` |
| `resource://catalogs/chaos_faults` | Chaos fault catalog | `reference` |
| `resource://workflows/release-check` | Unified release-check workflow | `workflow-guide` |
| `resource://schemas/aiops/v0.4/common` | AI Operations v0.4 common schema | `json-schema` |
| `resource://schemas/aiops/v0.4/run` | AI Operations v0.4 run schema | `json-schema` |
| `resource://schemas/aiops/v0.4/workflow` | AI Operations v0.4 workflow schema | `json-schema` |
| `resource://schemas/aiops/v0.6/provenance` | AI Operations v0.6 provenance schema | `json-schema` |
| `resource://schemas/aiops/v0.8/audit_event` | AI Operations v0.8 audit_event schema | `json-schema` |
| `resource://schemas/aiops/v0.8/common` | AI Operations v0.8 common schema | `json-schema` |
| `resource://schemas/aiops/v0.8/investigation_report` | AI Operations v0.8 investigation_report schema | `json-schema` |
| `resource://schemas/aiops/v0.8/verification_signal` | AI Operations v0.8 verification_signal schema | `json-schema` |
| `resource://specs/aiops/v0.4/conformance-rules` | AI Operations v0.4 conformance rule catalog | `spec-catalog` |
| `resource://specs/aiops/v0.6/conformance-rules` | AI Operations v0.6 conformance rule catalog | `spec-catalog` |
| `resource://specs/aiops/v0.8/conformance-rules` | AI Operations v0.8 conformance rule catalog | `spec-catalog` |
| `resource://specs/aiops/v0.5/compatibility` | AI Operations v0.5 version compatibility catalog | `spec-catalog` |

The server also lists authorized saved-session resources dynamically:

| URI template | Content and boundary |
| --- | --- |
| `resource://sessions/{encoded-session-id}` | Stored producer evidence/history/recall notes; percent-encode the session ID as one URI component |

Hosted session resources delegate to the authorized `core.report_recall` path under the tenant transaction. They cannot bypass tool policy or cross into another owner's session by guessing a name. Stdio state is process-local; hosted retention/quotas follow the configured shared store. Referenced artifact text is evidence/data, not instructions to execute.

An initialized-client resource-read request is:

```json
{"jsonrpc":"2.0","id":1,"method":"resources/read","params":{"uri":"resource://examples/sample_workflow"}}
```

The result contains a JSON text resource. To analyze the sample, parse that resource content and supply its object as `artifact` to `lens.analyze_workflow`; the URI alone is not the artifact. `resource://workflows/release-check` supplies ordered workflow guidance, not an automatic executor.

## Prompt inventory

`prompts/list` returns five reusable prompt definitions and their string arguments. Retrieve one with `prompts/get`:

| Prompt name | Arguments | Purpose |
| --- | --- | --- |
| `tower.investigation` | `incident_id` (required) | Investigate an incident using authorized Tower evidence tools. |
| `lens.workflow_summary` | `workflow_name` (required), `recommendation_count` (optional), `estimated_savings_pct` (optional) | Summarize an analyzed workflow for a human operator. |
| `lens.compare_summary` | `baseline_label` (optional), `candidate_label` (optional) | Summarize a baseline-vs-candidate run comparison for a release decision. |
| `chaos.experiment_brief` | `faults` (required), `script` (optional) | Explain the intent and expected impact of a chaos run. |
| `core.release_check` | `session_id` (optional) | Guide a host through a unified workflow release check. |

```json
{"jsonrpc":"2.0","id":2,"method":"prompts/get","params":{"name":"lens.workflow_summary","arguments":{"workflow_name":"support-demo","recommendation_count":"2"}}}
```

`prompts/get` renders a user-role text message for the host to review/use. Supplied argument values and evidence remain data. A template cannot supply missing analysis results or grant permission. In particular, Tower investigation requires separate human approval of an exact recovery preview, and release-check narration must preserve missing/invalid/failed gate states.

## Bundled contracts and ownership

The repository packages ten JSON Schemas: two Evals-native report/gate schemas under `schemas/evals/`, and eight AIOS schemas under `resources/aios/`. AIOS schema resources retain full `$id` identities, including different common-schema families, and include versioned rule/compatibility catalogs. Source/license/checksum metadata accompanies the vendored AIOS assets.

Run/Workflow use `0.4-draft`, provenance uses `0.6-draft`, and supported audit/investigation/verification companions use `0.8-draft`. Schema discovery is separate from validation and authentication. See [current schema routing and held-byte resolution](coordinated-v1-readiness.md), [native Evals contracts](evals-report-contract.md) and [resource ownership](architecture.md).

## Lookup and maintenance

Resource definitions live in `resources/catalog.py` and `adapters/ai_operations_spec.py`; saved sessions are added by the server. Prompt arguments/rendering live in `prompts/registry.py`. The [robust reference](https://deepagentlabs.io/mcp/docs/llms-full.md) includes these declarations and all bundled schemas. Keep this inventory aligned with runtime `resources/list` and `prompts/list` when those sources change. The generated [tool catalog](tools.md) is maintained separately with `make docs`.
