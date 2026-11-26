# AI Reference capability index

This index opens the [AI Reference (robust)](https://deepagentlabs.io/agentic-sidecar/docs/llms-full.md). In that generated raw Markdown file, **Full reference** identifies an included topic section; **Source** links to its maintained document. Use the [Developer Guide (simple)](developer-guide.md#capability-index) for short workflows.

## Capability index

| Capability | Included scope | Detailed reference |
| --- | --- | --- |
| Decision Gate and enforcement | Evaluate seven outcomes, then enforce through governed dispatch. | <a href="#governance-and-evaluator-behavior">Full reference</a> · [Source](governance.md) |
| Policy and risk rules | Apply ordered allow/deny policies and tool/argument risk classifications. | <a href="#configuration">Full reference</a> · [Source](configuration.md) |
| Intent constraints | Bind user constraints to tool arguments, catch intent drift and retain intent identity and expiry. | <a href="#core-supervision-features">Full reference</a> · [Source](features.md) |
| Budget accounting | Track explicit cost/tokens and pause at configured ceilings. | <a href="#governance-and-evaluator-behavior">Full reference</a> · [Source](governance.md) |
| Plan review and Critic | Review supplied plans, unnecessary steps, contradictions and unsupported assumptions. | <a href="#governance-and-evaluator-behavior">Full reference</a> · [Source](governance.md) |
| Offline and live judges | Use MockJudge or optional OpenAI/Anthropic providers with limits and usage accounting. | <a href="#governance-and-evaluator-behavior">Full reference</a> · [Source](governance.md) |
| Human in the loop: approvals and escalation | Approve once, reject, modify intent, replan or stop a suspended proposal. | <a href="#governance-and-evaluator-behavior">Full reference</a> · [Source](governance.md) |
| Custom hooks and failure policies | Extend decision evaluation while preserving mandatory checks and explicit failure behavior. | <a href="#core-supervision-features">Full reference</a> · [Source](features.md) |
| Framework and MCP adapters | Govern sync/async tools in LangGraph, AutoGen, CrewAI, OpenAI Agents, Google ADK and MCP. | <a href="#framework-and-ecosystem-integrations">Full reference</a> · [Source](integrations.md) |
| Task runtime and execution lifecycle | Track proposals, decisions, dispatch reservations, completion and failure. | <a href="#live-runtime-and-operator-controls">Full reference</a> · [Source](live-operations.md) |
| Operator server and Control Room | Watch a task live and pause, resume, replan, stop or restart it, with remote approvals. | <a href="#live-runtime-and-operator-controls">Full reference</a> · [Source](live-operations.md) |
| Emergency stop, cancellation and revocation | Latch dispatch stop, invalidate old decisions, cancel owned async calls and revoke host-owned access. | <a href="#live-runtime-and-operator-controls">Full reference</a> · [Source](live-operations.md) |
| Control Tower fleet operations | Join Sidecar evidence to fleet incidents and stop many deployments through one approved bulk action. | <a href="#control-tower-integration-and-emergency-stop">Full reference</a> · [Source](control-tower-integration.md) |
| Audit journal and restoration | Persist immutable hash-chained events, verify snapshots and restore stopped state. | <a href="#live-runtime-and-operator-controls">Full reference</a> · [Source](live-operations.md) |
| Shared/exclusive supervision | Compose agent-specific context and mandatory guardrails without weakening shared rules. | <a href="#shared-and-exclusive-supervision">Full reference</a> · [Source](scoped-supervision.md) |
| Context privacy and lifecycle | Authorize readers, deliver defensive copies, update, expire and revoke context. | <a href="#authority-privacy-and-validation-evidence">Full reference</a> · [Source](v0.9.md) |
| Redacted evidence and operator readers | Expose allowlisted summaries separately from privileged native artifacts. | <a href="#authority-privacy-and-validation-evidence">Full reference</a> · [Source](v0.9.md) |
| Task authority and delegation | Require grants, narrow child permissions and enforce ancestor expiry/revocation at dispatch. | <a href="#authority-privacy-and-validation-evidence">Full reference</a> · [Source](v0.9.md) |
| Native interchange contracts | Validate intent, decision, audit, scope and transfer wrappers against five candidate schemas. | <a href="#native-contracts-and-intent-transfer">Full reference</a> · [Source](v0.10.md) |
| Cross-agent intent transfer | Serialize narrowed proposals and receive them against a trusted live parent registry. | <a href="#native-contracts-and-intent-transfer">Full reference</a> · [Source](v0.10.md) |
| Native correlation and Lens | Export correlated decisions and attach them to exact Lens run/trace/span identities. | <a href="#framework-and-ecosystem-integrations">Full reference</a> · [Source](integrations.md) |
| Chaos recovery supervision | Evaluate recovery proposals linked to native fault events without executing the tool. | <a href="#framework-and-ecosystem-integrations">Full reference</a> · [Source](integrations.md) |
| AIOS audit projections | Project public native audit identifiers and outcomes into a draft operational artifact. | <a href="#aios-operational-audit-exports">Full reference</a> · [Source](aios-0.8-operational-artifacts.md) |
| Narration and CLI | Display standalone or measured runtime status and use six CLI commands. | <a href="#cli-reference">Full reference</a> · [Source](cli-reference.md) |
| Supervision benchmarks and acceptance | Reproduce synthetic paired dispatch measurements with explicit validation limits. | <a href="#authority-privacy-and-validation-evidence">Full reference</a> · [Source](v0.9.md) |
| Configuration and limitations | Configure roles, optional integrations and trusted-host boundaries. | <a href="#limitations">Full reference</a> · [Source](limitations.md) |

## How to use the robust reference

1. Choose a capability, then read its detailed prerequisites, workflow, output contract and limitations.
2. Consult **Source declarations: src/agentic_sidecar/...** for current statically extracted signatures, model fields and exports across the entire package. Extraction does not import or execute Sidecar. Undocumented helpers remain internal; their appearance does not promote them to public APIs.
3. Consult **Data contract: schemas/v1/...** for the five exact native JSON Schemas. Native wrappers, journal events, correlation projections, redacted summaries and AIOS operational artifacts are distinct formats. A serialized ALLOW or IntentTransfer grants no authority on its own.
4. Use package metadata and current declaration sources for installed-version APIs. Version-labelled guides record a feature's origin; historical compatibility notes apply only to their stated versions. Package 1.0.x does not promote draft/candidate schemas or establish live-provider or production acceptance.
5. Preserve trusted-host boundaries: actor/reader identity, grants, registry, operator credentials, tool dispatch and approval handling come from the host. Observe is not enforcement, fail_open is explicit, and stop/revocation cannot undo previously dispatched side effects.
6. Check `ai-docs-manifest.json` before ingestion: it records every selected source and normalized hash plus the generated reference checksum. Published example outputs and synthetic benchmark counts are not production measurements.

## Maintaining coverage

`docs/ai-docs.json` selects detailed topic/integration guides, every package Python module and all five native schemas. Keep both indexes and the CLI inventory aligned with new user-facing capabilities. From the repository root, regenerate using the shared sibling documentation checkout and Python 3.11 or newer:

```bash
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project agentic-sidecar
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project agentic-sidecar --check
```

The shared site build publishes the robust pack verbatim as a raw Markdown download. The manifest also records downloadable guide examples.
