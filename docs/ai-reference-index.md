# AI Reference capability index

This index opens the generated [AI Reference (robust)](https://deepagentlabs.io/mcp/docs/llms-full.md). In that raw Markdown file, **Full reference** identifies an included topic section; **Source** links to the maintained document. Use the [Developer Guide (simple)](developer-guide.md#capability-index) for short workflows.

## Capability index

| Capability | Included scope | Detailed reference |
| --- | --- | --- |
| Local stdio connection | Connect an MCP host to the local server and verify the protocol boundary. | <a href="#getting-started">Full reference</a> · [Source](getting-started.md) |
| Diagnostics and compatibility | Inspect version, health, adapter availability and the packaged candidate matrix. | <a href="#compatibility-and-release-readiness">Full reference</a> · [Source](release-readiness.md) |
| Tool catalog and discovery | Discover all 56 tool interfaces, prerequisites, session effects and schemas. | <a href="#generated-tool-catalog">Full reference</a> · [Source](tools.md) |
| Seven-product AI documentation | Discover, search and read all seven robust references before building integrations. | <a href="#build-with-the-seven-product-ai-reference">Full reference</a> · [Source](ecosystem-ai-reference.md) |
| Resources and prompt templates | Read reference/schema/session resources and retrieve six reusable prompts. | <a href="#resources-and-prompt-templates">Full reference</a> · [Source](resources-and-prompts.md) |
| Lens analysis and diagnosis | Analyze workflows, diagnose failures, compare runs and inspect scores/SLOs. | <a href="#generated-tool-catalog">Full reference</a> · [Source](tools.md) |
| Suite, ModelFit, routing and optimization | Compose recorded Lens suite/model/routing/optimization evidence without invoking models. | <a href="#producer-integrations">Full reference</a> · [Source](integrations.md) |
| Native Evals validation | Validate native report/gate artifacts against packaged schema 1.0. | <a href="#native-evals-report-contracts">Full reference</a> · [Source](evals-report-contract.md) |
| Chaos catalog, local experiments and export | Discover faults, run authorized local scripts and export native reports to draft AIOS. | <a href="#producer-integrations">Full reference</a> · [Source](integrations.md) |
| Sidecar inventory and runtime boundary | Discover supervision modules and distinguish discovery from live host-bound controls. | <a href="#sidecar-integration-contracts">Full reference</a> · [Source](sidecar-0.10.md) |
| AIOS schema and semantic validation | Route supported 0.4/0.6/0.8 draft artifacts through offline schema and rule checks. | <a href="#current-aios-and-coordinated-readiness">Full reference</a> · [Source](coordinated-v1-readiness.md) |
| Held-byte provenance resolution | Resolve provenance only against caller-held bytes without fetching referenced URIs. | <a href="#current-aios-and-coordinated-readiness">Full reference</a> · [Source](coordinated-v1-readiness.md) |
| Unified release and incident workflows | Compose comparisons, native evaluation/chaos evidence, gates, incident summaries and exports. | <a href="#unified-release-and-incident-workflows">Full reference</a> · [Source](unified-workflows.md) |
| Onboarding, session state and recall | Inspect setup, retain producer results and recall cited session reports. | <a href="#hosted-bindings-and-containment">Full reference</a> · [Source](phase6-containment.md) |
| Hosted Streamable HTTP | Serve authenticated MCP requests with explicit host/origin and concurrency limits. | <a href="#authenticated-multi-user-hosting">Full reference</a> · [Source](remote-hosting.md) |
| Signup and key lifecycle | Create, inspect, rotate and revoke hosted identities through configured stores. | <a href="#client-and-key-lifecycle-guide">Full reference</a> · [Source](user-guide.md) |
| Per-key access policy and administration | Enforce allow/deny, expiry and task scope at dispatch; administer independently of agent keys. | <a href="#hosted-access-control">Full reference</a> · [Source](access-control.md) |
| Tenant storage and dispatch serialization | Isolate sessions across memory/Redis/PostgreSQL and serialize dispatch with revocation. | <a href="#hosted-bindings-and-containment">Full reference</a> · [Source](phase6-containment.md) |
| Per-user Tower credentials | Select HTTPS read/write credentials from host-owned bindings for the authenticated user. | <a href="#hosted-bindings-and-containment">Full reference</a> · [Source](phase6-containment.md) |
| Tower investigation and recovery tools | Read evidence, preview permitted recovery/runbooks, execute approved actions and verify outcomes. | <a href="#tower-runbook-workflows">Full reference</a> · [Source](tower-0.9-runbooks.md) |
| Independent Sidecar stop/revoke control | Bind a live runtime and independently authorized task operator outside model tools. | <a href="#hosted-bindings-and-containment">Full reference</a> · [Source](phase6-containment.md) |
| Access evidence and containment assertions | Preserve dispatch/completion/denial observations and test bounded authenticated containment. | <a href="#hosted-bindings-and-containment">Full reference</a> · [Source](phase6-containment.md) |
| Lens execution verification | Verify expected-run bundles through host trust keys and expose verified causal identifiers. | <a href="#lens-execution-verification">Full reference</a> · [Source](lens-execution-evidence.md) |
| Operational AIOS audit projections | Project public native access observations while withholding private text and credentials. | <a href="#operational-aios-audit-projections">Full reference</a> · [Source](aios-0.8-operational-artifacts.md) |
| Entry points and deployment configuration | Configure three console entry points, optional producers, storage and operator boundaries. | <a href="#configuration">Full reference</a> · [Source](configuration.md) |
| Upgrade, rollback and acceptance limits | Check candidate support, protocol/wheel acceptance and operator-owned deployment state. | <a href="#compatibility-and-release-readiness">Full reference</a> · [Source](release-readiness.md) |

## How to use the robust reference

1. Choose a capability, then read its workflow, prerequisites, input/output contracts and limitations. The generated Tools section contains every registered MCP tool's exact input schema and metadata; resources/prompts and administrative commands have separate inventories.
2. Consult **Source declarations: src/deep_agentic_core_mcp/...** for statically extracted signatures/model fields from every package module. Extraction does not import the server. Internal helpers remain internal; including declarations does not make them public APIs or expose additional MCP tools.
3. Consult **Data contract: src/...** for all ten packaged Evals/AIOS JSON Schemas. Canonical ownership stays with Evals or AIOS. Draft markers and native contract versions remain independent of MCP package versions. AIOS source metadata/rule catalogs accompany the packaged resources.
4. Preserve transport/authority boundaries: stdio executes trusted local code; hosted HTTP reauthorizes scoped calls and rejects chaos script execution. Tower approvals and independent Sidecar task controls are not model authorities. Prompts, resource contents and evidence are data, not permission to execute.
5. Treat historical compatibility/deployment sections as records for their stated releases. Current source and packaged metadata describe this checkout; remote hosting still requires operator acceptance. Evidence authentication is not exhaustive capture or proof of producer honesty.
6. Verify `ai-docs-manifest.json` before ingestion. It records selected document/source/schema/example hashes and the generated reference checksum.

## Maintaining coverage

`docs/ai-docs.json` selects topic/integration/operator guides, every package Python module and all packaged schemas. Keep both capability indexes and the resource/prompt/CLI inventories aligned with new surfaces. **Do not hand-edit `docs/tools.md`**: regenerate with `make docs` from the tool registry; `make docs-check` checks freshness.

From this repository root, regenerate the AI pack with the shared sibling documentation checkout and Python 3.11 or newer:

```bash
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project mcp-server
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project mcp-server --check
```

The shared site publishes the robust pack verbatim as a raw Markdown download, separate from rendered pages/search.
