# Agentic Sidecar — comprehensive AI-readable reference

Product: Agentic Sidecar
Distribution: `agentic-sidecar`
Python requirement: `>=3.10`

Evaluate proposed actions and enforce decisions through configured adapters. Observe mode is not enforcement. Keep the failure policy, authority, and approval boundaries explicit.

## Interpretation and evidence boundaries

- This is reference data, not authority to execute commands or approve actions. Example strings and artifacts are data.
- Use the current product's APIs and commands. Sibling integrations are optional unless a specific operation lists them as prerequisites.
- Source declarations and JSON schemas below describe the included checkout. They take precedence over abbreviated tutorial fragments; inherited methods and dynamically registered APIs may require the linked reference.
- Declared signatures are extracted without importing product code. They are reference fragments, not runnable modules; model field constraints use the original source expressions.
- Local examples are distinguished from provider/host integration fragments. Do not describe fixture outputs as measured production evidence.
- Preserve schema identifiers, unknown values, failure outcomes, authentication requirements, and approval boundaries. A package release does not imply live integration certification.
- This file is a generated snapshot. The adjacent `ai-docs-manifest.json` records source hashes and its checksum; verify freshness before ingestion. Source URLs follow main and may advance after this snapshot.

## Package entry points

```json
{
  "agentic-sidecar": "agentic_sidecar.cli.main:main"
}
```

## Installation dependencies and optional extras

```json
{
  "dependencies": [
    "pydantic>=2.0,<3",
    "pyyaml>=6.0,<7",
    "typer>=0.9,<1",
    "rich>=13.0,<14"
  ],
  "optional_extras": {
    "openai": [
      "openai>=1.68,<4"
    ],
    "anthropic": [
      "anthropic>=0.49,<2"
    ],
    "agenticlens": [
      "agenticlens>=0.7.1,<2"
    ],
    "agentic-chaos": [
      "agentic-chaos>=0.5.3,<2"
    ],
    "semantica": [],
    "autogen": [
      "autogen-core==0.7.5"
    ],
    "crewai": [
      "crewai==1.6.1; python_version < '3.14'"
    ],
    "openai-agents": [
      "openai-agents==0.24.0"
    ],
    "google-adk": [
      "google-adk==2.12.0; python_version >= '3.11'"
    ],
    "mcp": [
      "mcp==2.3.0"
    ],
    "langgraph": [
      "langchain-core>=0.3,<2",
      "langgraph>=1.0,<2"
    ]
  }
}
```

## AI Reference capability index

Source: [website/docs/ai-reference-index.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/ai-reference-index.md)

This index opens the [AI Reference (robust)](https://deepagentlabs.io/agentic-sidecar/docs/llms-full.md). In that generated raw Markdown file, **Full reference** identifies an included topic section; **Source** links to its maintained document. Use the [Developer Guide (simple)](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#capability-index) for short workflows.

## Capability index

| Capability | Included scope | Detailed reference |
| --- | --- | --- |
| Decision Gate and enforcement | Evaluate seven outcomes, then enforce through governed dispatch. | <a href="#governance-and-evaluator-behavior">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) |
| Policy and risk rules | Apply ordered allow/deny policies and tool/argument risk classifications. | <a href="#configuration">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/configuration.md) |
| Intent constraints | Bind user constraints to tool arguments and retain intent identity and expiry. | <a href="#core-supervision-features">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/features.md) |
| Budget accounting | Track explicit cost/tokens and pause at configured ceilings. | <a href="#governance-and-evaluator-behavior">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) |
| Plan review and Critic | Review supplied plans, unnecessary steps, contradictions and unsupported assumptions. | <a href="#governance-and-evaluator-behavior">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) |
| Offline and live judges | Use MockJudge or optional OpenAI/Anthropic providers with limits and usage accounting. | <a href="#governance-and-evaluator-behavior">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) |
| Approvals and escalation | Approve once, reject, modify intent, replan or stop a suspended proposal. | <a href="#governance-and-evaluator-behavior">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) |
| Custom hooks and failure policies | Extend decision evaluation while preserving mandatory checks and explicit failure behavior. | <a href="#core-supervision-features">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/features.md) |
| Framework and MCP adapters | Govern sync/async tools in LangGraph, AutoGen, CrewAI, OpenAI Agents, Google ADK and MCP. | <a href="#framework-and-ecosystem-integrations">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md) |
| Task runtime and execution lifecycle | Track proposals, decisions, dispatch reservations, completion and failure. | <a href="#live-runtime-and-operator-controls">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) |
| Operator server and Control Room | Connect authenticated local status, task controls and remote approval handling. | <a href="#live-runtime-and-operator-controls">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) |
| Stop, cancellation and revocation callbacks | Latch local dispatch stop, invalidate old decisions and request host-owned access revocation. | <a href="#live-runtime-and-operator-controls">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) |
| Audit journal and restoration | Persist immutable hash-chained events, verify snapshots and restore stopped state. | <a href="#live-runtime-and-operator-controls">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) |
| Shared/exclusive supervision | Compose agent-specific context and mandatory guardrails without weakening shared rules. | <a href="#shared-and-exclusive-supervision">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/scoped-supervision.md) |
| Context privacy and lifecycle | Authorize readers, deliver defensive copies, update, expire and revoke context. | <a href="#authority-privacy-and-validation-evidence">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md) |
| Redacted evidence and operator readers | Expose allowlisted summaries separately from privileged native artifacts. | <a href="#authority-privacy-and-validation-evidence">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md) |
| Task authority and delegation | Require grants, narrow child permissions and enforce ancestor expiry/revocation at dispatch. | <a href="#authority-privacy-and-validation-evidence">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md) |
| Native interchange contracts | Validate intent, decision, audit, scope and transfer wrappers against five candidate schemas. | <a href="#native-contracts-and-intent-transfer">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md) |
| Cross-agent intent transfer | Serialize narrowed proposals and receive them against a trusted live parent registry. | <a href="#native-contracts-and-intent-transfer">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md) |
| Native correlation and Lens | Export correlated decisions and attach them to exact Lens run/trace/span identities. | <a href="#framework-and-ecosystem-integrations">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md) |
| Chaos recovery supervision | Evaluate recovery proposals linked to native fault events without executing the tool. | <a href="#framework-and-ecosystem-integrations">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md) |
| AIOS audit projections | Project public native audit identifiers and outcomes into a draft operational artifact. | <a href="#aios-operational-audit-exports">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/aios-0.8-operational-artifacts.md) |
| Narration and CLI | Display standalone or measured runtime status and use six CLI commands. | <a href="#cli-reference">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/cli-reference.md) |
| Supervision benchmarks and acceptance | Reproduce synthetic paired dispatch measurements with explicit validation limits. | <a href="#authority-privacy-and-validation-evidence">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md) |
| Configuration and limitations | Configure roles, optional integrations and trusted-host boundaries. | <a href="#limitations">Full reference</a> · [Source](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md) |

## How to use the robust reference

1. Choose a capability, then read its detailed prerequisites, workflow, output contract and limitations.
2. Consult **Source declarations: src/agentic_sidecar/...** for current statically extracted signatures, model fields and exports across the entire package. Extraction does not import or execute Sidecar. Undocumented helpers remain internal; their appearance does not promote them to public APIs.
3. Consult **Data contract: schemas/v1/...** for the five exact native JSON Schemas. Native wrappers, journal events, correlation projections, redacted summaries and AIOS operational artifacts are distinct formats. A serialized ALLOW or IntentTransfer grants no authority on its own.
4. Use package metadata and current declaration sources for installed-version APIs. Version-labelled guides record a feature's origin; historical compatibility notes apply only to their stated versions. Package 1.0.x does not promote draft/candidate schemas or establish live-provider or production acceptance.
5. Preserve trusted-host boundaries: actor/reader identity, grants, registry, operator credentials, tool dispatch and approval handling come from the host. Observe is not enforcement, fail_open is explicit, and stop/revocation cannot undo previously dispatched side effects.
6. Check `ai-docs-manifest.json` before ingestion: it records every selected source and normalized hash plus the generated reference checksum. Published example outputs and synthetic benchmark counts are not production measurements.

## Maintaining coverage

`website/docs/ai-docs.json` selects detailed topic/integration guides, every package Python module and all five native schemas. Keep both indexes and the CLI inventory aligned with new user-facing capabilities. From the repository root, regenerate using the shared sibling documentation checkout and Python 3.11 or newer:

```bash
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project agentic-sidecar
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project agentic-sidecar --check
```

The shared site build publishes the robust pack verbatim as a raw Markdown download. The manifest also records downloadable guide examples.

---

## Setup and task workflows

Source: [website/docs/developer-guide.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md)

Use this simple guide to choose a capability and connect it to an explicit tool boundary. The [AI Reference (robust)](https://deepagentlabs.io/agentic-sidecar/docs/llms-full.md) includes detailed topic guides, current package/CLI declarations and all five native schemas. Observe mode records decisions; Govern enforces them through the returned tools.

[Capability index](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#capability-index) · [Quickstart](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#quickstart) · [Configuration](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#settings) · [Troubleshooting](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#troubleshooting) · [Reference](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#reference)

## Capability index

Every row links to a short workflow below. Detailed references explain configuration, inputs, outputs and limitations.

| Capability | What you can do |
| --- | --- |
| [Decision Gate and enforcement](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#gate) | Evaluate seven outcomes, then enforce through governed dispatch. |
| [Policy and risk rules](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#policy-risk) | Apply ordered allow/deny policies and tool/argument risk classifications. |
| [Intent constraints](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#intent) | Bind user constraints to tool arguments and retain intent identity and expiry. |
| [Budget accounting](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#budget) | Track explicit cost/tokens and pause at configured ceilings. |
| [Plan review and Critic](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#plan-review) | Review supplied plans, unnecessary steps, contradictions and unsupported assumptions. |
| [Offline and live judges](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#judges) | Use MockJudge or optional OpenAI/Anthropic providers with limits and usage accounting. |
| [Approvals and escalation](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#approvals) | Approve once, reject, modify intent, replan or stop a suspended proposal. |
| [Custom hooks and failure policies](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#hooks) | Extend decision evaluation while preserving mandatory checks and explicit failure behavior. |
| [Framework and MCP adapters](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#adapters) | Govern sync/async tools in LangGraph, AutoGen, CrewAI, OpenAI Agents, Google ADK and MCP. |
| [Task runtime and execution lifecycle](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#runtime) | Track proposals, decisions, dispatch reservations, completion and failure. |
| [Operator server and Control Room](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#operators) | Connect authenticated local status, task controls and remote approval handling. |
| [Stop, cancellation and revocation callbacks](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#stop) | Latch local dispatch stop, invalidate old decisions and request host-owned access revocation. |
| [Audit journal and restoration](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#audit) | Persist immutable hash-chained events, verify snapshots and restore stopped state. |
| [Shared/exclusive supervision](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#scopes) | Compose agent-specific context and mandatory guardrails without weakening shared rules. |
| [Context privacy and lifecycle](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#privacy) | Authorize readers, deliver defensive copies, update, expire and revoke context. |
| [Redacted evidence and operator readers](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#evidence) | Expose allowlisted summaries separately from privileged native artifacts. |
| [Task authority and delegation](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#authority) | Require grants, narrow child permissions and enforce ancestor expiry/revocation at dispatch. |
| [Native interchange contracts](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#contracts) | Validate intent, decision, audit, scope and transfer wrappers against five candidate schemas. |
| [Cross-agent intent transfer](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#transfer) | Serialize narrowed proposals and receive them against a trusted live parent registry. |
| [Native correlation and Lens](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#lens) | Export correlated decisions and attach them to exact Lens run/trace/span identities. |
| [Chaos recovery supervision](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#chaos) | Evaluate recovery proposals linked to native fault events without executing the tool. |
| [AIOS audit projections](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#aios) | Project public native audit identifiers and outcomes into a draft operational artifact. |
| [Narration and CLI](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#narration) | Display standalone or measured runtime status and use six CLI commands. |
| [Supervision benchmarks and acceptance](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#validation) | Reproduce synthetic paired dispatch measurements with explicit validation limits. |
| [Configuration and limitations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/developer-guide.md#settings) | Configure roles, optional integrations and trusted-host boundaries. |

## Quickstart

Requires Python 3.10 or newer in an activated virtual environment:

```bash
python -m pip install agentic-sidecar
```

Save this complete file as `sidecar_quickstart.py`. Its delete tool only appends to a list. The LangGraph adapter accepts plain callables here without requiring a running graph:

```python
from agentic_sidecar import DecisionContext, Sidecar, SidecarBlockedError
from agentic_sidecar.gate.policy import PolicyAdvisor, PolicyRule
from agentic_sidecar.adapters.langgraph import attach

policy = PolicyAdvisor([PolicyRule(tool="delete_*", effect="deny")])
observer = Sidecar(on_sidecar_failure="fail_closed", policy=policy)
print("Verdict:", observer.evaluate(DecisionContext(tool_name="delete_customer")).status)

calls = []
def delete_customer(customer_id: str) -> str:
    """Synthetic function: record a call, without deleting anything."""
    calls.append(customer_id)
    return "simulated deletion"

governor = Sidecar(mode="govern", on_sidecar_failure="fail_closed", policy=policy)
(guarded_delete,) = attach(governor, [delete_customer])
try:
    guarded_delete("demo-123")
except SidecarBlockedError as exc:
    print("Governed decision:", exc.decision.status)
assert not calls, "The synthetic delete function must not execute."
print("Function calls:", len(calls))
```

[Download sidecar_quickstart.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/guide/examples/sidecar_quickstart.py)

```bash
python sidecar_quickstart.py
```

Expect a BLOCK verdict, blocked governed dispatch and zero calls. When connecting real tools, verify both the decision and actual execution evidence. Keep raw tools and runtime configuration in the trusted host.

## Usage

Examples under `examples/` or `scripts/` assume a source checkout and run from its root. Other named files, endpoints and IDs are inputs supplied by your host. See the linked topic before using a provider, SDK or operator fragment.

<span id="gate"></span>

### Decision Gate and enforcement

Sidecar supports `ALLOW`, `WARN`, `BLOCK`, `CHALLENGE`, `REPLAN`, `PAUSE` and `ESCALATE`. `evaluate()` returns a decision; it does not execute a tool. Governed adapters dispatch ALLOW/WARN, block BLOCK, return replanning/challenge outcomes to the loop, and resolve or suspend approval outcomes. Observe evaluates but calls through.

Custom loops must evaluate, enforce, reserve dispatch with `runtime.dispatch(...)`, execute only after admission, and call `runtime.complete(...)` on success or failure. Prefer a supported adapter for this lifecycle. See [outcome and approval semantics](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) and [dispatch freshness](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md#task-authority-and-delegation).

<span id="policy-risk"></span>

### Policy and risk rules

`PolicyAdvisor` evaluates ordered tool-name globs; first match wins, with an allow default unless configured otherwise. `RiskEvaluator` classifies tool/argument rules as LOW/MEDIUM/HIGH, and `risk_block_threshold` determines intervention. Load YAML or mapping definitions, or construct `PolicyRule`/`RiskRule` objects. The quickstart demonstrates a deny rule. See [rule fields, comparison operators and configuration](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/configuration.md).

<span id="intent"></span>

### Intent constraints

Create an `IntentEnvelope` containing the goal, requester, constraints and optional expiry. `ConstraintBinding` maps each enforced constraint to a tool argument; `IntentGuardian` checks the bound values. Supply it as `intent=` and enable the `intent_guardian` role. Goals alone are not deterministic constraints, and an authority dictionary requires explicit authority bindings to enforce grants. See [constraint setup](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/configuration.md) and [authority semantics](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md).

<span id="budget"></span>

### Budget accounting

```python
from agentic_sidecar import BudgetGuardian, DecisionContext, Sidecar

budget = BudgetGuardian(max_cost=5.0, max_tokens=10000)
sidecar = Sidecar(on_sidecar_failure="fail_closed", roles=["budget"], budget=budget)
budget.record_invocation(cost=5.0, tokens=1200)
assert sidecar.evaluate(DecisionContext(tool_name="read_order")).status == "PAUSE"
```

Record actual external usage explicitly, and call `reset()` for the next task. Judge usage reaches a configured task budget once; other framework/tool usage is not inferred. Govern pauses dispatch until resolved. See [budget and Judge accounting](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md).

<span id="plan-review"></span>

### Plan review and Critic

```python
from agentic_sidecar import PlanEvaluator, Sidecar

sidecar = Sidecar(on_sidecar_failure="fail_closed", roles=["planner"], planner=PlanEvaluator())
decision = sidecar.evaluate_plan(
    [{"tool_name": "read_charge"}, {"tool_name": "issue_refund"}],
    goal="Explain the disputed charge",
)
assert decision.status == "REPLAN"
```

Full-plan review runs enabled deterministic gates on each supplied step. `CriticEvaluator` challenges selected unsafe actions and assumptions; verification metadata must be step-scoped. These are scoped heuristics, not general semantic reasoning. See [plan review](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md#full-plan-review), [Critic behavior](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/features.md) and [migration details](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md#review-fixes-and-migration).

<span id="judges"></span>

### Offline and live judges

Configure `JudgeEvaluator(MockJudge(...))` for explicit offline responses. `OpenAIJudge` and `AnthropicJudge` use optional provider SDKs and never silently substitute mocks. Install `[openai]` or `[anthropic]`, supply credentials/model, and enable the `judge` role.

Configure timeout, cost limit and caller-supplied token rates when accounting is required. Provider errors follow the explicit Sidecar failure policy; limits are not a hard cancellation mechanism for arbitrary blocking code. See [provider setup and smoke commands](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md#optional-live-judge-providers) and [Judge limits](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md).

<span id="approvals"></span>

### Approvals and escalation

```python
from agentic_sidecar import Sidecar
from agentic_sidecar.cli.approval import CLIApprovalHandler

sidecar = Sidecar(
    on_sidecar_failure="fail_closed", mode="govern",
    escalation_handler=CLIApprovalHandler(),
)
```

Use returned governed tools. PAUSE/ESCALATE can request `approve_once`, `reject`, `modify_intent`, `ask_agent_to_replan` or `stop_agent`. BLOCK is never offered for approval. Responses bind to the decision ID; approval authorizes one unchanged invocation. Missing handlers suspend. `TaskRuntime` supports connected operator approvals; `on_escalation_required` supports notification callbacks. See [approval transitions and malformed-response handling](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md#local-approval-flow).

<span id="hooks"></span>

### Custom hooks and failure policies

`before_tool_call` installs a custom decision hook; `on_sidecar_failure` must explicitly be `fail_open` or `fail_closed`. Govern/fail_closed blocks when evaluation fails; fail_open can permit that failure path. Hooks receive copied proposals and cannot rewrite the enforced tool/arguments. Mandatory scope and authority checks still apply before optional evaluation. See [hook API](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/api-reference.md), [mandatory guardrails](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/scoped-supervision.md) and [failure limits](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md).

<span id="adapters"></span>

### Framework and MCP adapters

Start with `adapters.callable.attach()` or `adapters.langgraph.attach()` for plain typed sync/async functions. The optional framework adapters convert the returned supervised boundary to each SDK's tool object:

| Module | Install extra / surface |
| --- | --- |
| `adapters.langgraph` | `[langgraph]` for real graphs; wrapped callables |
| `adapters.autogen` | `[autogen]`; AutoGen Core FunctionTool |
| `adapters.crewai` | `[crewai]`; CrewAI Tool |
| `adapters.openai_agents` | `[openai-agents]`; OpenAI Agents FunctionTool |
| `adapters.google_adk` | `[google-adk]`; ADK FunctionTool |
| `adapters.mcp` | `[mcp]`; async wrappers for allowlisted tools on an initialized ClientSession |

Most adapters use `attach(sidecar, tools)`; MCP uses `attach(sidecar, session, tool_names)`. Pass only the returned objects to the agent. Prebuilt SDK tools, automatic handoffs and arbitrary nested/raw calls are not automatically protected. See [SDK versions, Python requirements and examples](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md#framework-adapters) and [MCP gateway boundaries](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md#mcp).

<span id="runtime"></span>

### Task runtime and execution lifecycle

`TaskRuntime` records proposed, evaluated, dispatched, completed and failed actions. Supply `runtime=` to Sidecar and use that runtime as `escalation_handler` for connected approvals. Inspect `runtime.snapshot()` and `runtime.journal.export(after=0)`. The guarded quickstart creates runtime evidence automatically. Evaluating a proposal alone is not evidence that it executed. See [runtime construction and lifecycle](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md).

<span id="operators"></span>

### Operator server and Control Room

Host a configured task inside `OperatorServer(runtime, token=..., actor=...)`, using a locally generated secret of at least 32 characters. The server exposes a task-specific loopback endpoint and Control Room. Keep the server context alive for the task's lifetime, then connect an operator terminal:

```bash
export SIDECAR_ENDPOINT=http://127.0.0.1:PORT/tasks/TASK_ID
# Set SIDECAR_OPERATOR_TOKEN securely in this terminal as well.
agentic-sidecar status --json
agentic-sidecar control pause
agentic-sidecar control resume
```

Replace PORT/TASK_ID with the running server's values. Status/events/control/approval/intent API routes require the operator token. See [complete server setup, protocol and Control Room](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md#connect-a-real-task).

<span id="stop"></span>

### Stop, cancellation and revocation callbacks

```bash
agentic-sidecar control stop
```

Stop latches independently of evaluation mode and failure policy, blocks queued dispatch and invalidates old decisions. Already-dispatched sync work may finish; owned async tools receive cooperative cancellation requests. Configure named `TaskRuntime(revokers=...)` callbacks for host-owned credentials and delegated access; acknowledgement requires each issuer to return exactly `True` after revocation. Restart does not renew credentials or task authority. See [stop receipts, partial failures and restart rules](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md#stop-cancellation-and-access-revocation).

<span id="audit"></span>

### Audit journal and restoration

`EventJournal(task_id, path)` can persist JSONL events with sequence, event identity, timestamp, previous hash and digest. `verify_events(events, task_id=...)` checks a complete native chain before replay/export. Reopen `EventJournal(task_id, path)` and pass it to `TaskRuntime` to restore supported snapshots in a stopped state; approvals are not silently reauthorized. This is distinct from serializing a caller-managed `AuditRecord`.

Protect native records because they may contain arguments and reasons. Hash chaining detects alteration relative to the supplied chain; an external trusted anchor is needed to resist a full malicious rewrite. See [journal formats, restoration and replay](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md#audit-snapshots-and-restoration).

<span id="scopes"></span>

### Shared/exclusive supervision

Configure `ScopedSystem` with declared agents, a shared `ScopeLayer`, and optional exclusive layers. `ContextSpec` carries goal/values, while `GuardrailSpec` carries explicit policies/constraint bindings. `bind(agent_id, on_sidecar_failure=...)` creates a separate supervised agent boundary.

Shared and exclusive context conflicts fail validation; every applicable guardrail must pass. Exclusive allows cannot weaken shared denies. Context delivery is explicit through `context()`/`deliver()`, and private text is not automatically enforcement policy or evaluator input. See [composition, mandatory checks and trusted identities](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/scoped-supervision.md).

<span id="privacy"></span>

### Context privacy and lifecycle

```python
from agentic_sidecar import ContextSpec, ScopedSystem, ScopeLayer

system = ScopedSystem(
    system_id="support", task_id="ticket-42", agents=["refund"],
    exclusive={"refund": ScopeLayer(
        context=ContextSpec(values={"reference": "demo-1"}, readers={"auditor"}),
    )},
)
refund = system.bind("refund", on_sidecar_failure="fail_closed")
assert refund.context(reader="auditor")["values"]["reference"] == "demo-1"
refund.update_context({"reference": "demo-2"}, actor="refund")
refund.revoke_context(actor="refund")
```

Readers/actors come from the authenticated host. Owners update/revoke context; expiry/revocation blocks future reads but cannot retract delivered copies. Combined layers intersect extra readers and use the earliest expiry. See [reader authorization, delivery and lifecycle](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md#context-privacy-and-readers).

<span id="evidence"></span>

### Redacted evidence and operator readers

`BoundAgent.evidence()` returns an allowlisted summary of identity, verdict/risk, counts and lifecycle state, excluding private arguments, goals, reasons, plans and pending approvals. `OperatorServer(reader_tokens={secret: "auditor"})` permits redacted GET `/status` only; those tokens cannot control, approve or read raw events. A summary cannot replace a native decision or verifiable journal. See [reader token and evidence contracts](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md#context-privacy-and-readers).

<span id="authority"></span>

### Task authority and delegation

Configure an `IntentGuardian` with `AuthorityBinding` entries, trusted task/agent IDs and explicit grants. `delegate(agent_id=..., authority=...)` creates a child whose permissions may only narrow. Missing/denied grants block; expiry and ancestor revocation invalidate future dispatch reservations. Bindings and inherited constraints remain intact.

Run the offline synthetic-tool example from the checkout:

```bash
uv run python examples/v0_9_authority_delegation.py
```

The parent registry and raw tools stay host-owned. Revocation does not undo already reserved execution. Observe records authority decisions without enforcing them; use the governed dispatch boundary. See [grants, narrowing, revocation and restart](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md#task-authority-and-delegation).

<span id="contracts"></span>

### Native interchange contracts

```python
from agentic_sidecar import Decision
from agentic_sidecar.contracts import DecisionContract, contract_schema

native = Decision(status="BLOCK", risk=None, reason="local example")
wire = DecisionContract(schema_version="sidecar.decision/1", decision=native).model_dump_json()
restored = DecisionContract.model_validate_json(wire)
assert restored.decision.decision_id == native.decision_id
assert contract_schema("decision")["properties"]["schema_version"]["const"] == "sidecar.decision/1"
```

The five families are intent, decision, audit, scope and transfer. Top-level wrappers require exact markers and reject unknown fields. `ScopeContract.build()` validates composition; `export_audit()` validates a native record including timezone-aware timestamps. Native contracts are candidate surfaces, independent of package and AIOS versions. See [schema policy and migration](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md#schema-and-migration-policy).

<span id="transfer"></span>

### Cross-agent intent transfer

`IntentTransfer.propose(parent, agent_id=..., authority=...)` creates a narrowed serialized proposal. After transport, the trusted receiver validates it and calls `.receive(parent, agent_id=...)` against the live parent registry. Imported proposals cannot invent bindings, widen authority, extend expiry or bypass ancestor revocation.

```bash
uv run python examples/v0_10_contracts.py
```

A proposal is not a signed credential, approval or resumable task. Disconnected registry replication and one-time replay prevention are host responsibilities. See [cross-instance receive checks and limitations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md#cross-instance-and-cross-agent-propagation).

<span id="lens"></span>

### Native correlation and Lens

`Correlation(run_id=..., trace_id=..., span_id=...)` and `export_decisions()` emit `sidecar.correlation/1` projections after verifying the native journal. The host supplies exact IDs. Install `[agenticlens]` to use `integrations.agenticlens.attach_decisions(sidecar, run, span_id=...)` for Lens readback.

BLOCK/ESCALATE remain supervision outcomes rather than failed deployments. Projections may retain sensitive reasons and are not independent execution evidence. See [correlation fields, Lens identity checks and access boundaries](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md#versioned-native-decision-evidence).

<span id="chaos"></span>

### Chaos recovery supervision

Install `[agentic-chaos]` for optional resilience experiments. `integrations.agentic_chaos.evaluate_recovery(sidecar, event, tool_name=..., arguments=...)` evaluates/enforces a recovery proposal linked to a native Chaos event ID; it does not execute the tool. Actual execution still passes through a supervised adapter. See [Chaos/Evals ownership and examples](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md#agentic-chaos-and-evals).

<span id="aios"></span>

### AIOS audit projections

`integrations.aios.export_audit_event(record, target=..., created_at=...)` projects a native `AuditRecord` into a `0.8-draft` operational audit artifact. The host supplies public target references and an aware recording timestamp. The projection withholds rationale/context, marks the actor unknown, and maps BLOCK to denied while other outcomes remain requested. Permission to proceed is not proof of execution. See [AIOS operational projection](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/aios-0.8-operational-artifacts.md) and [export API](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/api-reference.md#aios-operational-audit-export).

<span id="narration"></span>

### Narration and CLI

`StatusNarrator` records supplied tool narratives and formats task status independently of a connected runtime:

```bash
agentic-sidecar version
agentic-sidecar status --json
```

`demo` illustrates simulated narrator calls; `approval-demo` prompts without executing tools. `status --endpoint` reads measured task events; `--follow --json` is formatted display, not JSONL. `control` and `approve` operate on authenticated live tasks. See the [complete six-command inventory and flags](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/cli-reference.md).

<span id="validation"></span>

### Supervision benchmarks and acceptance

```bash
uv run python scripts/supervision_benchmark.py --output /tmp/sidecar-evidence.json
```

The fixed 24-run synthetic benchmark compares actual wrapped dispatches with and without supervision across unsafe and clean controls. Outage controls expose fail_closed availability costs. Optional `--ecosystem` validation uses Chaos and Evals through the `[validation]` extra. Synthetic zero token/cost values do not establish live-provider benefit, statistical confidence or economic savings. See [reproducible evidence and recorded limits](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md#reproducible-evidence) and [coordinated acceptance](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/coordinated-v1-readiness.md).

<span id="settings"></span>

## Configuration and limitations

Choose `on_sidecar_failure` explicitly, choose Observe/Govern, supply modules and enable their roles. Defaults enable policy/risk; an empty policy allows actions. Supported optional roles include intent_guardian, budget, planner, critic and judge. Mandatory scope/authority checks retain their own semantics. See [constructor arguments, rules, bindings and module setup](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/configuration.md).

Core installation has no sibling dependency. Framework/provider integrations use their corresponding extras; `[agenticlens]`, `[agentic-chaos]` and `[validation]` add ecosystem dependencies. Semantica is reserved and has no implemented export. Protect raw tools, credentials, identity and runtime configuration at the host boundary. Wrappers do not sandbox hostile Python or automatically govern arbitrary memory, prompts, outputs or nested calls. See [limitations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md), [scoped boundaries](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/scoped-supervision.md) and [contract maturity](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md).

## Troubleshooting

If a denied tool still runs, check Observe/Govern, the returned tool object and actual dispatch evidence. If approval stalls, inspect the pending decision ID and handler/runtime. If an old ALLOW stops working, check intent epochs, consumed approvals, stop state and authority expiry/revocation. See [troubleshooting](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/troubleshooting.md).

## Reference

- [API reference](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/api-reference.md) and [CLI reference](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/cli-reference.md).
- [AI Reference (robust)](https://deepagentlabs.io/agentic-sidecar/docs/llms-full.md) and [capability/source index](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/ai-reference-index.md).
- [Source manifest and checksums](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/ai-docs-manifest.json).

---

## Core supervision features

Source: [website/docs/features.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/features.md)

Core capabilities and their supported usage, with authority/privacy and native-contract extensions described in [v0.9](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md) and [v0.10](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md). Upcoming extensions
are described in [Roadmap](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/roadmap.md); execution boundaries are summarized in
[Limitations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md).

## Policy Advisor

Deterministic allow/deny rules use ordered `fnmatch` tool patterns. The first
match wins; the configurable default is allow. Load YAML with `from_yaml()`
or use `from_mapping()` / explicit rules:

```python
from agentic_sidecar import DecisionContext
from agentic_sidecar.gate.policy import PolicyAdvisor, PolicyRule

policy = PolicyAdvisor([PolicyRule(tool="delete_*", effect="deny")])
print(policy.evaluate(DecisionContext(tool_name="delete_customer")).effect)  # deny
```

## Risk Evaluator

Ordered tool/argument rules classify LOW, MEDIUM, or HIGH. Sidecar returns
BLOCK when classification reaches `risk_block_threshold` (default HIGH).
Supported comparisons are eq, ne, gt, gte, lt, lte, in, and contains.

```python
from agentic_sidecar import DecisionContext
from agentic_sidecar.gate.risk import RiskEvaluator, RiskRule

risk = RiskEvaluator([RiskRule(
    tool="issue_refund", arg_name="amount", arg_op="gt", arg_value=500, risk="HIGH",
)])
print(risk.evaluate(DecisionContext(tool_name="issue_refund", tool_args={"amount": 850})).risk)
# HIGH
```

## Intent Guardian

IntentEnvelope carries goal, requester, constraints, authority, expiry, and
metadata. ConstraintBinding connects a declared constraint to a tool argument.
Numeric/enum/allow-list checks produce WARN or BLOCK. Constraint-only expiry produces WARN; authority-bearing envelopes expire with BLOCK.
[Authority bindings, narrowed delegation and ancestor revocation](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md) are implemented. See the runnable [Getting Started](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/getting-started.md)
example and [Configuration](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/configuration.md).

## Budget Guardian

Record cost/tokens explicitly. A recorded ceiling produces PAUSE when the
budget role is configured. Govern suspends the tool until approval resolution.

```python
from agentic_sidecar import BudgetGuardian, DecisionContext, Sidecar

budget = BudgetGuardian(max_cost=5, max_tokens=10_000)
sidecar = Sidecar(on_sidecar_failure="fail_closed", budget=budget, roles=["budget"])
budget.record_invocation(cost=5, tokens=1200)
print(sidecar.evaluate(DecisionContext(tool_name="read_order")).status)  # PAUSE
```

Judge usage automatically reaches the configured task BudgetGuardian once.
Other framework usage still needs explicit accounting.

## Plan Evaluator

Direct plan review applies selected unnecessary-step and contradiction
heuristics, returning ALLOW or REPLAN. Supply `plan` and `goal` explicitly:

```python
from agentic_sidecar import PlanEvaluator

result = PlanEvaluator().evaluate({
    "goal": "Explain the disputed charge",
    "plan": [{"tool_name": "read_charge"}, {"tool_name": "issue_refund"}],
})
print(result.status)  # REPLAN
```

Use `sidecar.evaluate_plan(plan, goal=...)` to pass a full plan through the
gate, including policy/risk and intent checks per step. Configuring planner
alone does not discover a plan from tool calls.

## Critic Evaluator

Tool-name heuristics identify selected risky actions and assumptions, producing
ALLOW or CHALLENGE. They do not establish contextual authorization by themselves.

```python
from agentic_sidecar import CriticEvaluator, DecisionContext, Sidecar

sidecar = Sidecar(
    on_sidecar_failure="fail_closed", critic=CriticEvaluator(), roles=["critic"],
)
print(sidecar.evaluate(DecisionContext(tool_name="delete_records")).status)  # CHALLENGE
```

Govern suspends CHALLENGE. Critic also checks selected opposing previously
permitted actions and caller-supplied evidence flags; see [Limitations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md).

## Judge Evaluator

The model-agnostic provider interface accepts decision context and returns
status, rationale, confidence, and usage metadata. MockJudge is offline;
OpenAIJudge/AnthropicJudge use optional live SDKs. This example makes no API call:

```python
from agentic_sidecar import JudgeEvaluator, MockJudge

judge = JudgeEvaluator(provider=MockJudge(model="demo-model"))
result = judge.evaluate({
    "tool_name": "read_order", "arguments": {}, "goal": "Review order A100",
})
print(result.status)  # ALLOW (scripted response)
```

Judge validates verdicts/usage, bounds waiting, accounts sync/async usage and
applies per-call cost ceilings after a response. Provider errors follow Sidecar
failure policy. See [Governance](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) for live provider configuration.

## Status Narrator

Manually record proposals/calls, decisions, risk, compliance, and budget values:

```python
from agentic_sidecar import Decision, StatusNarrator

narrator = StatusNarrator()
narrator.set_objective("Review order A100")
call = narrator.record_tool_call(
    "read_order", {"order_id": "A100"},
    decision=Decision(status="ALLOW", risk="LOW", reason="read permitted"),
    risk_level="LOW", intent_compliant=True,
)
print(call.narrative)  # Executing read_order, with the generic narration prefix
print(narrator.get_status(current_budget_remaining=4.50).tool_calls_made)  # 1
```

Narration matches common tool-name patterns. `pause()` / `resume()` report
state; application code controls execution. CLI status with --endpoint reads the
runtime journal and distinguishes proposed, blocked, paused, executed and completed
actions. See [Live operations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) for the Control Room and controls.

## Human Escalation

ApprovalAction, EscalationRequest, ApprovalResponse, and EscalationHandler define
the request/response contract. Govern invokes a registered handler for
PAUSE/ESCALATE and validates response IDs/actions. CLIApprovalHandler provides
a local prompt. See [Governance](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) for all five approval actions.

## Custom Decision Hook

`before_tool_call` replaces the ordinary built-in pipeline, including budget and
evaluators. Trusted mandatory scope checks still run before the hook and cannot
be bypassed by its ALLOW verdict.
It receives injected intent/history and returns a Decision:

```python
from agentic_sidecar import Decision, DecisionContext, Sidecar

sidecar = Sidecar(on_sidecar_failure="fail_closed")

@sidecar.before_tool_call
def review(context: DecisionContext) -> Decision:
    status = "BLOCK" if context.tool_name.startswith("delete_") else "ALLOW"
    return Decision(status=status, risk="LOW", reason="Custom rule")

print(sidecar.evaluate(DecisionContext(tool_name="delete_customer")).status)  # BLOCK
```

Use the standard pipeline when you want configured modules to run together.
Provenance export types are documented in [API reference](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/api-reference.md).

## Shared & Exclusive supervision

`ScopedSystem` binds trusted agent identities to shared and exclusive layers.
Choose context only, guardrails only or both. Context delivery to the host is
explicit; shared denials remain mandatory alongside exclusive restrictions.
Each bound agent has a separate history and copied payload. See
[scoped supervision](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/scoped-supervision.md) for privacy and deployment limits.

## Native adapters and evidence

v0.8 provides AutoGen, CrewAI, OpenAI Agents, Google ADK and MCP boundaries in
addition to LangGraph. Native SDK conformance covers all seven decisions and
both modes. Verified correlated decisions reach Lens 0.7.1 incident timelines;
Chaos recovery proposals retain native event IDs. See [integrations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md).

See [v0.9 authority, privacy and migration](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md) for the current lifecycle APIs.

---

## Architecture

Source: [website/docs/architecture.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/architecture.md)

**The Main Agent acts. The Sidecar observes, thinks, advises, and governs.**
Sidecar evaluates proposed actions; the agent runtime and adapter own execution.

## Decision flow

```text
Agent proposes an action
  → LangGraph callable wrapper or caller-managed boundary
  → DecisionContext
  → Sidecar: Policy → Risk → Intent → Budget → Planner → Critic → Judge
  → Decision
  → Observe: call through
  → Govern: ALLOW/WARN execute; BLOCK stops; other outcomes resolve or suspend
```

Modules run only when enabled in `roles` and configured. A policy denial, risk
threshold, or blocking intent finding returns immediately. Budget PAUSE,
planner REPLAN/BLOCK, Critic CHALLENGE, and supported Judge interventions also
return before later stages. Intent WARN is advisory and can accompany later
checks. A custom `before_tool_call` hook replaces the built-in pipeline.

Use `Sidecar.evaluate_plan()` for full-plan review before dispatch. Evaluators
receive goal, constraints, intent, decision history, plan and metadata. Planner
and Critic are deterministic heuristics; Judge uses an explicit MockJudge or
optional live provider. See [Governance](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md).

## Operating modes

| Mode | Adapter behavior |
| --- | --- |
| Observe (default) | Computes/logs verdicts, then executes the wrapped tool |
| Govern | ALLOW/WARN execute; BLOCK stops; PAUSE/ESCALATE invoke approvals; unresolved outcomes suspend |

Budget ceilings produce PAUSE. Govern invokes a registered escalation handler
or returns control via SidecarSuspendedError. Approvals are scoped to one call;
BLOCK never reaches approval. CHALLENGE/REPLAN suspend for agent-loop handling.

## Failure configuration

`on_sidecar_failure` is required: `fail_closed` converts caught gate errors to
BLOCK; `fail_open` converts them to ALLOW. Observe remains advisory regardless
of that verdict. Configure `fail_closed` for governed boundaries.

Injection, evaluation/provider calls, verdict validation and recording share
the failure boundary. Approval errors follow the same policy. Judge errors
propagate to that boundary. Recording failures cannot guarantee a log entry;
see [supported scope](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md) for timeout and accounting details.

## Package boundaries

| Package | Responsibility | Current dependencies |
| --- | --- | --- |
| `core/` | Runtime, contexts, decision and provenance types | Gate, intent, evaluators, Pydantic |
| `gate/` | Policy, risk, budget and approval primitives | Core models/operators; Pydantic and PyYAML for rules |
| `intent/` | Envelope and constraint bindings | Core models/operators, Pydantic |
| `evaluators/` | Planner/Critic heuristics, Judge/provider interface | Core types, evaluator base; live SDK imports are lazy and optional |
| `status/` | Manually populated narration | Core decision types |
| `adapters/` | Framework interception | Core; LangGraph callable wrapper has no framework import dependency |
| `cli/` | Local status, approval, demo, version | Status, Typer, Rich |
| `integrations/` | Reserved optional ecosystem bridges | Planned for 0.8 |

`core/` never imports adapters. Policy/Risk stay independent of Intent and
model evaluators. Framework and sibling packages remain optional.

## Decision records and status

`sidecar.decisions` stores in-memory `(DecisionContext, Decision)` pairs.
Built-in verdicts commonly include `decision_point="tool_call"` and trigger
arguments. Hook and failure verdicts may leave those fields unset. `Decision`
is frozen at the field level; nested dictionaries and saved contexts remain
mutable. `AuditRecord.to_dict()` serializes caller-created provenance records.
Contexts are deep-copied at recording time; decisions have IDs and resolved
approvals link to their originating decision. TaskRuntime adds immutable JSON event
snapshots and optional durable JSONL execution evidence.

`StatusNarrator` records application-supplied call/decision metadata. Its pause
state is reporting state. CLI status with --endpoint connects to actual runtime
events. TaskRuntime and OperatorServer provide task-scoped operator controls;
see [Live operations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md).

---

## API reference

Source: [website/docs/api-reference.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/api-reference.md)

Python API for `agentic-sidecar` **0.9.0** (unchanged from 0.8.0). Imports below identify the supported
module for each symbol; intent and policy/risk types live in their subpackages.

```python
import agentic_sidecar
```

---

## `Sidecar`

```python
from agentic_sidecar import Sidecar
```

The central class. Owns the Decision Gate and all evaluation module configuration.

### `__init__`

See [Configuration](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/configuration.md) for the full parameter reference.

### `evaluate(context: DecisionContext) -> Decision`

Evaluate one proposed tool call. Injects intent/history into the caller's context,
computes a verdict, and stores a deep context copy in `sidecar.decisions`. Errors
from injection, dispatch, validation or recording resolve via `on_sidecar_failure`. This method does
not dispatch tools or raise merely because a verdict is BLOCK. See
[Failure handling](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/architecture.md#failure-configuration) for scope.

```python
from agentic_sidecar import DecisionContext

context = DecisionContext(tool_name="issue_refund", tool_args={"amount": 250.0})
decision = sidecar.evaluate(context)
print(decision.status)  # "ALLOW"
```

### `set_intent(intent: IntentGuardian | None) -> None`

Set or clear the active `IntentGuardian`. Raises `ValueError` if `intent` is provided but `"intent_guardian"` is not in `sidecar.roles`.

### `before_tool_call(func: Callable) -> Callable`

Decorator. Register a custom decision hook that replaces the entire built-in Decision Gate pipeline.

```python
@sidecar.before_tool_call
def my_hook(context: DecisionContext) -> Decision:
    ...
```

### `on_escalation_required(func: Callable) -> Callable`

Decorator. Register an approval hook invoked by `enforce()` or the Govern
adapter for PAUSE/ESCALATE. Responses must match the decision ID and use an
ApprovalAction. See [Governance](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) for resolution semantics.

```python
@sidecar.on_escalation_required
def handle_escalation(request: EscalationRequest) -> ApprovalResponse:
    ...
```

### `sidecar.decisions: list[tuple[DecisionContext, Decision]]`

In-memory log of evaluated context/decision pairs. Contexts and nested data
are deep-copied when recorded but remain mutable; caller-created `AuditRecord` objects are a separate export API.

### `sidecar.mode: str`

Current mode — `"observe"` or `"govern"`.

---

## `Decision`

```python
from agentic_sidecar import Decision, DecisionStatus, RiskLevel
```

Frozen Pydantic result of a Decision Gate evaluation; nested dictionary values
are not deeply immutable.

| Field | Type | Description |
|---|---|---|
| `decision_id` | `str` | Generated UUID; approval correlation ID |
| `status` | `DecisionStatus` | ALLOW / WARN / BLOCK / CHALLENGE / REPLAN / PAUSE / ESCALATE |
| `risk` | `RiskLevel` \| `None` | LOW / MEDIUM / HIGH; None when no classification was produced, including early policy returns and failure fallback |
| `reason` | `str` | Human-readable verdict explanation |
| `decision_point` | `str` \| `None` | Boundary name, commonly `"tool_call"` for built-in verdicts; optional for hooks/fallback |
| `trigger_details` | `dict` \| `None` | Optional tool name and argument snapshot |
| `escalation_required` | `bool` | Explicit escalation marker (default False); built-in budget/Judge PAUSE sets it |
| `causal_link` | `str` \| `None` | Optional caller-supplied causal identifier |

---

## `DecisionContext`

```python
from agentic_sidecar import DecisionContext
```

The input to `sidecar.evaluate()`. Build one per tool call.

| Field | Type | Description |
|---|---|---|
| `tool_name` | `str` | Name of the proposed tool |
| `tool_args` | `dict[str, Any]` | Arguments for the tool call |
| `intent` | `IntentSnapshot` \| `None` | Injected by `evaluate()` — do not set manually |
| `history` | `list[HistoryEntry]` | Injected by `evaluate()` — do not set manually |
| `metadata` | `dict[str, Any]` | Caller metadata forwarded to evaluators |
| `boundary` | `"tool_call"` / `"plan"` | Evaluation boundary |
| `goal` | `str` | Goal when no active envelope exists |
| `plan` | `list[dict]` | Explicit plan steps |

---

## `SidecarBlockedError`

```python
from agentic_sidecar import SidecarBlockedError
```

Raised by the LangGraph callable wrapper in Govern mode when `decision.status == "BLOCK"`.

```python
try:
    (my_tool_wrapped,) = attach(sidecar, [my_tool])
    my_tool_wrapped()
except SidecarBlockedError as exc:
    print(exc.decision.reason)
    print(exc.context.tool_name)
```

| Attribute | Type | Description |
|---|---|---|
| `decision` | `Decision` | The blocking decision |
| `context` | `DecisionContext` | The context that triggered the block |

---

## `PolicyAdvisor`

```python
from agentic_sidecar.gate.policy import PolicyAdvisor, PolicyRule, PolicyResult
```

See [Configuration — PolicyAdvisor](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/configuration.md#policyadvisor-configuration) for full details.

### `PolicyAdvisor.evaluate(context: DecisionContext) -> PolicyResult`

Runs the rule set. Returns the first matching rule's result, or the default.

### `PolicyAdvisor.from_yaml(path) -> PolicyAdvisor` · `PolicyAdvisor.from_mapping(data) -> PolicyAdvisor`

Class methods to load rules from a YAML file or parsed dict.

---

## `RiskEvaluator`

```python
from agentic_sidecar.gate.risk import RiskEvaluator, RiskRule, RiskResult
```

### `RiskEvaluator.evaluate(context: DecisionContext) -> RiskResult`

Runs the rule set. Returns the first matching rule's risk classification, or the default.

---

## `BudgetGuardian`

```python
from agentic_sidecar.gate import BudgetGuardian, BudgetResult
```

### `BudgetGuardian.record_invocation(cost: float, tokens: int | None = None) -> None`

Accumulate cost and token usage.

### `BudgetGuardian.evaluate() -> BudgetResult`

Check current totals against ceilings. Returns `BudgetResult(exceeded, remaining_cost, remaining_tokens, reason)`.

### `BudgetGuardian.is_at_capacity() -> bool`

Quick check — returns `True` if already at or over budget.

### `BudgetGuardian.reset() -> None`

Reset cost and token counters to zero (for a new task).

---

## `IntentGuardian` / `IntentEnvelope` / `ConstraintBinding`

```python
from agentic_sidecar.intent import (
    IntentEnvelope, IntentGuardian, ConstraintBinding, Requester
)
```

See [Configuration — IntentEnvelope and IntentGuardian](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/configuration.md#intentenvelope-and-intentguardian-configuration).

### `IntentEnvelope.is_expired(now=None) -> bool`

Returns `True` if `expires` is set and the envelope has expired.

### `IntentEnvelope.to_snapshot() -> IntentSnapshot`

Returns a lightweight `IntentSnapshot(goal, constraints)` — the form injected into `DecisionContext`.

---

## `EscalationHandler` / `EscalationRequest` / `ApprovalResponse` / `ApprovalAction`

```python
from agentic_sidecar.gate import (
    EscalationHandler, EscalationRequest, ApprovalResponse, ApprovalAction
)
```

**`ApprovalAction` values:** `APPROVE_ONCE`, `REJECT`, `MODIFY_INTENT`, `ASK_AGENT_TO_REPLAN`, `STOP_AGENT`

---

## `StatusNarrator` / `StatusNarrative` / `ToolCallNarrative`

```python
from agentic_sidecar.status import StatusNarrator, StatusNarrative, ToolCallNarrative
```

### `StatusNarrator.set_objective(objective: str) -> None`

Record the top-level task objective.

### `StatusNarrator.record_tool_call(tool_name, arguments, decision=None, risk_level=None, intent_compliant=True) -> ToolCallNarrative`

Record a tool invocation and generate its narrative.

### `StatusNarrator.get_status(...) -> StatusNarrative`

Build a snapshot of application-supplied records and reporting state. This
does not fetch data from a running agent. `steps_completed` counts recorded calls.

### `StatusNarrator.get_narrative() -> str`

Return the full execution narrative as a human-readable string.

### `StatusNarrator.pause(reason: str) -> None` / `resume() -> None`

Record narrator pause/resume state; application code owns actual execution.

---

## `attach` (LangGraph adapter)

```python
from agentic_sidecar.adapters.langgraph import attach
```

### `attach(sidecar: Sidecar, tools: Sequence[F]) -> list[F]`

Wraps each tool in `tools` so calling it first runs `sidecar.evaluate()`. Returns a new list in the same order. Does not mutate the input list or original tool callables.

```python
tools = attach(sidecar, [read_order, issue_refund, delete_customer])
agent = create_react_agent(model, tools=tools)
```

---

## Evaluators

```python
from agentic_sidecar import PlanEvaluator, CriticEvaluator, JudgeEvaluator
from agentic_sidecar.evaluators import EvaluatorResult, JudgeProvider
```

### `PlanEvaluator.evaluate(context: dict) -> EvaluatorResult`

Accepts plan dictionaries/PlanStep objects, goal, intent, constraints and
constraint_bindings. Selected tool/goal patterns and opposing tool pairs yield
REPLAN. Supplied bindings check plan arguments deterministically. min_confidence
filters the fixed 0.9 intervention score. No automatic natural-language bindings.

### `CriticEvaluator.evaluate(context: dict) -> EvaluatorResult`

Selected risky tool patterns, assumptions and permitted-action contradictions
yield CHALLENGE. Metadata authorized/eligibility_verified/backup_verified flags
can satisfy corresponding tool-call checks. threshold filters the fixed 0.85
score. These assertions are caller-supplied; full-plan checks are conservative.

### `JudgeEvaluator(provider, enabled=True, cost_limit=0.50, timeout_ms=5000, budget=None)`

Sync/async return validated EvaluatorResult with usage, provider, confidence and
latency. Errors propagate to Sidecar's failure policy. Returned usage is charged
once, including valid usage attached to an invalid verdict. cost_limit is a
post-response ceiling; exceeding it returns PAUSE. get_cost/reset_cost manage
tracked cost. See [Limitations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md) for late sync responses and async
cancellation. Choose MockJudge for offline examples; live OpenAIJudge and
AnthropicJudge require an explicit model, optional SDK and credentials.

### `JudgeProvider`

Implement evaluate(question, context) returning decision, reasoning, confidence
and usage with cost and total_tokens. Supported decisions are all seven statuses;
confidence must be finite in [0, 1], cost finite/nonnegative and tokens a
nonnegative integer. Override validate/evaluate_async as appropriate.
Without known cost, only cost_limit=None with no task budget is supported.

### `Sidecar.evaluate_plan(plan, *, goal="", metadata=None) -> Decision`

Requires a nonempty list of dictionaries with tool_name and optional arguments.
Checks policy/risk/intent per step, then enabled evaluators with full context.
Computes a verdict without executing steps. An active intent supplies the goal.

### `Sidecar.enforce(context, decision) -> Decision`

Adapter dispatch boundary: Observe returns unchanged; Govern resolves
PAUSE/ESCALATE and only returns ALLOW/WARN. BLOCK raises SidecarBlockedError;
other unresolved statuses raise SidecarSuspendedError. Both expose decision and
context. Applications must call enforce before dispatch in custom loops.

### `CLIApprovalHandler`

Import from agentic_sidecar.cli.approval and pass as escalation_handler.
Provides a local prompt for approve-once/reject/modify-intent/replan/stop.
The `approval-demo` CLI command tries the prompt without executing tools.

## Provenance exports

```python
from agentic_sidecar import AuditRecord, CausalLink, DecisionRationale, DecisionTrigger
```

Construct a caller-managed `AuditRecord` with decision ID, timestamp, outcome,
trigger, rationale, and optional causal/execution context. `to_dict()` serializes
the record, including ISO timestamp and structured causal links. TaskRuntime
automatically generates immutable event snapshots; EventJournal supplies
optional durable JSONL persistence. See [Live operations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md).

## Top-level `__version__`

```python
from agentic_sidecar import __version__
print(__version__)  # "1.0.3" in this checkout; use the installed value
```

## Runtime operations

Public exports: `TaskRuntime`, `RuntimeEvent`, `EventJournal`, `OperatorServer`.
Supply `runtime=TaskRuntime(...)` to Sidecar and `escalation_handler=runtime`
for remote approvals. Inspect `sidecar.runtime.snapshot()` and
`sidecar.runtime.journal.export(after=0)`. DecisionContext accepts
`parent_decision_id` and `parent_plan_step` for supplied plan causality.
See [Live operations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) for the full lifecycle and HTTP surface.

## Scoped supervision and native export (0.8)

Public exports: `ScopedSystem`, `ScopeLayer`, `ContextSpec`, `GuardrailSpec`,
`BoundAgent`. `ScopedSystem.bind(agent_id, on_sidecar_failure=..., mode=...)`
returns a separate Sidecar and explicit `context()` / `deliver(receiver)` payload.
See [scoped supervision](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/scoped-supervision.md) for configuration and limits.
`Sidecar` also accepts trusted `mandatory_checks`, `mandatory_configuration` and
`context_metadata`; checks run before custom hooks and the configuration is
included in audit policy fingerprints.

`integrations.correlation.Correlation` and `export_decisions()` provide native
versioned projections. See [integration contracts](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md).

See [v0.9 authority, privacy and migration](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md) for the current lifecycle APIs.


## Capability modules

| Module | Workflow and detailed contract |
| --- | --- |
| `agentic_sidecar.core`, `gate`, `intent` | [Decision outcomes, policy, risk, budgets, intent constraints and failure policy](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/configuration.md) |
| `agentic_sidecar.evaluators` | [Plan/Critic review, Judge providers, time/cost accounting and approval flows](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) |
| `agentic_sidecar.adapters` | [Sync/async callable, LangGraph, AutoGen, CrewAI, OpenAI Agents, Google ADK and MCP boundaries](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md) |
| `agentic_sidecar.operations` | [TaskRuntime, EventJournal, OperatorServer, dispatch, controls and native events](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) |
| `agentic_sidecar.scopes` | [Shared/exclusive composition and mandatory checks](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/scoped-supervision.md) |
| `agentic_sidecar.scopes.privacy` | [Reader authorization, context update/expiry/revocation and redacted summaries](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md#context-privacy-and-readers) |
| `agentic_sidecar.intent.authority` | [AuthorityBinding/AuthorityRegistry, narrowed delegation and live ancestor revocation](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md#task-authority-and-delegation) |
| `agentic_sidecar.contracts` | [Five native wrappers, schema accessors, scope import and validated intent transfer](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md) |
| `agentic_sidecar.integrations.correlation`, `integrations.agenticlens` | [Native projections and exact Lens run/trace/span readback](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md) |
| `agentic_sidecar.integrations.agentic_chaos` | [Evaluate/enforce a fault-correlated recovery proposal without executing it](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md#agentic-chaos-and-evals) |
| `agentic_sidecar.integrations.aios` | [AIOS operational audit projection](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/aios-0.8-operational-artifacts.md) |
| `agentic_sidecar.status`, `cli` | [Standalone/measured narration and six CLI commands](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/cli-reference.md) |

The [AI Reference (robust)](https://deepagentlabs.io/agentic-sidecar/docs/llms-full.md) includes declarations from every package module and all five native JSON Schemas. Consult the [capability index](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/ai-reference-index.md) before selecting a workflow. Internal helpers stay internal; extraction does not promote them to public APIs.

## Authority, privacy and transfer lifecycle

`IntentGuardian.delegate(...)` narrows authority using its live `AuthorityRegistry`, and `revoke()` invalidates descendants for future dispatch reservations. `IntentTransfer.propose(...)` serializes a narrowed proposal; `IntentTransfer.receive(parent, *, agent_id)` validates it against the trusted live parent. Receive requires the host-authenticated agent identity and the same live registry, not an imported self-asserted grant. See [propagation and replay limits](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md#cross-instance-and-cross-agent-propagation).

`BoundAgent.context(reader=...)` returns an authorized defensive copy; `update_context(values, *, actor)` and `revoke_context(*, actor)` require the owner. `evidence()` returns an allowlisted summary, not a native Decision or journal. `OperatorServer(reader_tokens=...)` binds reader credentials to redacted status only. See [privacy lifecycle](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md#context-privacy-and-readers).

## AIOS operational audit export

```python
from datetime import datetime, timezone
from agentic_sidecar import AuditRecord, DecisionRationale, DecisionTrigger
from agentic_sidecar.integrations.aios import export_audit_event

now = datetime.now(timezone.utc)
record = AuditRecord(
    decision_id="decision-demo", timestamp=now, outcome="BLOCK",
    trigger=DecisionTrigger("tool_call", "delete_demo"),
    rationale=DecisionRationale(reason="Local deny policy"),
)
artifact = export_audit_event(
    record,
    target={"id": "target-demo", "producer": "host", "artifact_id": "tool-demo", "format": "host.tool"},
    created_at=now,
)
assert artifact["spec_version"] == "0.8-draft"
assert artifact["outcome"] == "denied"
```

The host supplies a public native target and an aware recording time not earlier than the observation. The exporter withholds rationale/context, records an unknown actor rather than guessing identity, and preserves native outcomes/causal IDs. BLOCK maps to denied; other decisions are requested, never evidence of completed execution. It rejects malformed identity/target/timestamp inputs and self-causality. Native contract schema access does not validate this separate AIOS projection; use the specification-owned draft contract and the optional ecosystem validators. See [AIOS operational audit exports](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/aios-0.8-operational-artifacts.md).

---

## CLI reference

Source: [website/docs/cli-reference.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/cli-reference.md)

Agentic Sidecar ships a command-line interface accessible as `agentic-sidecar`.

```
agentic-sidecar --help
```

---

## Installation

The CLI is included with the main package:

```bash
pip install agentic-sidecar
agentic-sidecar --help
```

---

## Complete command inventory

All six commands are listed below. Use `agentic-sidecar COMMAND --help` for exact arguments/options. The robust reference includes their current source declarations.

| Command | Purpose |
| --- | --- |
| `approval-demo` | Try the local approval prompt without executing a tool or changing a task. |
| `approve` | Resolve one pending approval; modify_intent reads a complete JSON envelope. |
| `control` | Pause, resume, stop, restart or request replanning for the connected task. |
| `demo` | Run an interactive demo of the status narrator. |
| `status` | Display sidecar status: current objective, decisions, risk, and budget. |
| `version` | Show agentic-sidecar version. |

## Commands

### `status`

With --endpoint, display actual task state and lifecycle events from OperatorServer.
Without --endpoint, display the standalone narrator snapshot.

```bash
agentic-sidecar status [OPTIONS]
```

**Options:**

| Option | Short | Description |
|---|---|---|
| `--follow` | `-f` | Repeat the local snapshot every `--interval` seconds |
| `--json` | `-j` | Output as JSON instead of a human-readable table |
| `--endpoint URL` | — | Runtime HTTP task endpoint (or SIDECAR_ENDPOINT) |
| `--interval N` | `-i N` | Refresh interval in seconds when `--follow` is enabled (default: 1) |

**Examples:**

```bash
# One-time status snapshot
agentic-sidecar status

# Repeat local snapshot (Ctrl+C to stop)
agentic-sidecar status --follow

# Repeated formatted JSON display
agentic-sidecar status --follow --json

# Custom refresh interval
agentic-sidecar status --follow --interval 5
```

**Sample output (`status --json`):**

```json
{
  "timestamp": "2026-10-10T10:00:00",
  "objective": null,
  "current_step": null,
  "steps_completed": 0,
  "tool_calls": 0,
  "blocked_decisions": 0,
  "paused_decisions": 0,
  "intent_violations": 0,
  "max_risk": null,
  "budget_remaining": null,
  "tokens_remaining": null,
  "is_paused": false,
  "pause_reason": null
}
```

Timestamp varies. `--follow --json` includes headings and formatted JSON;
it is a display stream, not JSONL. Use a positive `--interval` value.

---

### `version`

Print the installed package version.

```bash
agentic-sidecar version
# agentic-sidecar 1.0.3 (varies by installed version)
```

---

### `demo`

Run an interactive demonstration of the `StatusNarrator` with simulated tool calls.

```bash
agentic-sidecar demo
```

This populates a local narrator with simulated calls and illustrates terminal
formatting without an agent or API key.

---

## Status fields reference

| Field | Description |
|---|---|
| `objective` | Top-level task goal set via `narrator.set_objective()` |
| `current_step` | Current step description (if provided to `get_status()`) |
| `steps_completed` | Recorded calls, including blocked/paused proposals |
| `tool_calls` | Same as `steps_completed` in v0.6 |
| `blocked_decisions` | Number of supplied BLOCK decisions in this narrator |
| `paused_decisions` | Number of supplied PAUSE decisions in this narrator |
| `intent_violations` | Calls marked `intent_compliant=False` by the application |
| `max_risk` | Highest risk level seen (LOW / MEDIUM / HIGH) |
| `budget_remaining` | USD remaining (only if `current_budget_remaining` passed to `get_status()`) |
| `tokens_remaining` | Tokens remaining (only if `current_tokens_remaining` passed) |
| `is_paused` | Narrator pause state, set by application code |
| `pause_reason` | Reason for the current pause |

## `approval-demo`

Try the local approval prompt without executing a tool:

```bash
agentic-sidecar approval-demo
```

Responses include approve_once, reject (default), modify_intent,
ask_agent_to_replan and stop_agent. For actual governed calls, pass
CLIApprovalHandler from agentic_sidecar.cli.approval as escalation_handler.
See [Governance](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md).

## Runtime connection and controls

Use `--endpoint` (or `SIDECAR_ENDPOINT`) to connect `status --follow` to a real
TaskRuntime/OperatorServer. Set `SIDECAR_OPERATOR_TOKEN` in the operator terminal.
`control ACTION` supports pause, resume, stop, restart and replan.
`approve DECISION_ID ACTION` resolves a pending request; `--intent-file FILE`
supplies a complete JSON envelope for modify_intent. See
[Live operations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) for setup, protocol and access scope.


## `control` and `approve`

```bash
agentic-sidecar control ACTION --endpoint http://127.0.0.1:PORT/tasks/TASK_ID
agentic-sidecar approve DECISION_ID ACTION --endpoint http://127.0.0.1:PORT/tasks/TASK_ID \
  [--intent-file intent.json]
```

Replace the endpoint and decision ID with values from the running task. Both commands require an endpoint, supplied explicitly or through `SIDECAR_ENDPOINT`, and use `SIDECAR_OPERATOR_TOKEN` for bearer authentication. Control actions are `pause`, `resume`, `stop`, `restart` and `replan`. Approval actions are `approve_once`, `reject`, `modify_intent`, `ask_agent_to_replan` and `stop_agent`.

`--intent-file` supplies a complete envelope for modify_intent. Pending approval IDs and proposal fingerprints must match the running task; replayed/consumed answers cannot authorize a dispatch. Reader tokens only expose redacted status and cannot use controls, approvals or events. See [operator protocol, identity, stop/restart and approval semantics](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) and [reader-token access](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md#context-privacy-and-readers).

No CLI command starts a provider judge or a framework agent automatically. Host the runtime/server in your application, then use these commands to connect. `status` with no endpoint remains the standalone narrator view.

---

## Configuration

Source: [website/docs/configuration.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/configuration.md)

This page covers all configuration options for the `Sidecar` constructor and its module dependencies.

---

## `Sidecar` constructor

```python
from agentic_sidecar import Sidecar

sidecar = Sidecar(
    on_sidecar_failure="fail_closed",
    mode="observe",
    roles=["policy", "risk"],
)
```

The following table lists constructor arguments. Configure each optional module
and include its role to enable it. See [Features](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/features.md) for evaluator
and narrator examples.

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `on_sidecar_failure` | `"fail_open"` \| `"fail_closed"` | **Required** | What to do if evaluation itself raises. `"fail_closed"` → `BLOCK`; `"fail_open"` → `ALLOW`. |
| `policy` | `PolicyAdvisor` \| `None` | `PolicyAdvisor()` (empty) | Allow/deny rule set. An empty advisor allows everything. |
| `risk` | `RiskEvaluator` \| `None` | `RiskEvaluator()` (empty) | Risk classification rules. An empty evaluator classifies everything as `LOW`. |
| `intent` | `IntentGuardian` \| `None` | `None` | Active intent guardian. Only consulted if `"intent_guardian"` is in `roles`. |
| `budget` | `BudgetGuardian` \| `None` | `None` | Budget ceiling tracker. Only consulted if `"budget"` is in `roles`. |
| `planner` | `PlanEvaluator` \| `None` | `None` | Plan evaluator. Only consulted if `"planner"` is in `roles`. |
| `critic` | `CriticEvaluator` \| `None` | `None` | Critic evaluator. Only consulted if `"critic"` is in `roles`. |
| `judge` | `JudgeEvaluator` \| `None` | `None` | Judge/provider evaluator. Choose explicit mock or optional live providers. Only consulted if `"judge"` is in `roles`. |
| `escalation_handler` | `EscalationHandler` \| `None` | `None` | Invoked for PAUSE/ESCALATE by Govern enforcement. |
| `risk_block_threshold` | `"LOW"` \| `"MEDIUM"` \| `"HIGH"` | `"HIGH"` | Minimum risk level that triggers a `BLOCK`. |
| `mode` | `"observe"` \| `"govern"` | `"observe"` | Observe records; Govern resolves or suspends non-proceed outcomes. |
| `roles` | `Sequence[str]` \| `None` | `["policy", "risk"]` | Which evaluation modules to run. |

---

## `roles` — controlling which modules run

The `roles` parameter is the main switch for enabling/disabling evaluation modules. Only modules listed in `roles` are consulted during `evaluate()`.

**Supported roles:**

| Role | Module |
|---|---|
| `"policy"` | Policy Advisor |
| `"risk"` | Risk Evaluator |
| `"intent_guardian"` | Intent Guardian |
| `"budget"` | Budget Guardian |
| `"planner"` | Plan Evaluator |
| `"critic"` | Critic Evaluator |
| `"judge"` | Judge Evaluator |

**Default roles when `roles=None`:** `["policy", "risk"]`

**Composition example — using the configured `policy`, `risk`, `guardian`, and `budget` objects below:**
```python
sidecar = Sidecar(
    on_sidecar_failure="fail_closed",
    mode="govern",
    policy=policy,
    risk=risk,
    intent=guardian,
    budget=budget,
    roles=["policy", "risk", "intent_guardian", "budget"],
)
```

---

## `PolicyAdvisor` configuration

```python
from agentic_sidecar.gate.policy import PolicyAdvisor, PolicyRule

# In-code rules
policy = PolicyAdvisor(
    rules=[PolicyRule(tool="delete_*", effect="deny")],
    default_effect="allow",   # default when no rule matches
)

# From YAML file
policy = PolicyAdvisor.from_yaml("policies/my_policy.yaml")

# From a dict (useful in tests)
policy = PolicyAdvisor.from_mapping({
    "default": "allow",
    "rules": [{"tool": "delete_*", "effect": "deny"}],
})
```

**`PolicyRule` fields:**

| Field | Type | Default | Description |
|---|---|---|---|
| `tool` | `str` | Required | `fnmatch` glob pattern matched against tool name |
| `effect` | `"allow"` \| `"deny"` | Required | Verdict when this rule matches |
| `reason` | `str` \| `None` | `None` | Human-readable explanation |

---

## `RiskEvaluator` configuration

```python
from agentic_sidecar.gate.risk import RiskEvaluator, RiskRule

risk = RiskEvaluator(
    rules=[
        RiskRule(tool="issue_refund", arg_name="amount", arg_op="gt", arg_value=500, risk="HIGH"),
        RiskRule(tool="delete_*", risk="HIGH"),
    ],
    default_risk="LOW",
)
```

**`RiskRule` fields:**

| Field | Type | Default | Description |
|---|---|---|---|
| `tool` | `str` | Required | `fnmatch` glob pattern |
| `risk` | `"LOW"` \| `"MEDIUM"` \| `"HIGH"` | Required | Risk level when this rule matches |
| `reason` | `str` \| `None` | `None` | Human-readable explanation |
| `arg_name` | `str` \| `None` | `None` | Argument to check (optional) |
| `arg_op` | `ArgOp` | `"eq"` | Comparison operator: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, `contains` |
| `arg_value` | `Any` | `None` | Value to compare against |

---

## `BudgetGuardian` configuration

```python
from agentic_sidecar.gate import BudgetGuardian

budget = BudgetGuardian(
    max_cost=5.00,       # USD ceiling
    max_tokens=10_000,   # token ceiling (optional)
)

# Record usage manually after each LLM/tool invocation
budget.record_invocation(cost=0.03, tokens=1200)

# Reset for the next task
budget.reset()
```

---

## `IntentEnvelope` and `IntentGuardian` configuration

```python
from agentic_sidecar.intent import (
    IntentEnvelope, IntentGuardian, ConstraintBinding, Requester
)
from datetime import datetime, timezone

envelope = IntentEnvelope(
    goal="Assist customer dispute — refund up to $500",
    requested_by=Requester(type="human", id="user_42"),
    constraints={"maximum_refund": 500.0},
    authority={"can_delete": False},
    expires=datetime(2026, 12, 31, 23, 59, tzinfo=timezone.utc),  # optional
)

bindings = [
    ConstraintBinding(
        constraint="maximum_refund",
        tool="issue_refund",
        arg_name="amount",
        op="lte",
        severity="BLOCK",
    )
]

guardian = IntentGuardian(envelope, bindings)
```

**`ConstraintBinding` fields:**

| Field | Type | Default | Description |
|---|---|---|---|
| `constraint` | `str` | Required | Key in `envelope.constraints` |
| `tool` | `str` | Required | `fnmatch` glob for tool name |
| `arg_name` | `str` | Required | Argument to check |
| `op` | `ArgOp` | `"lte"` | Comparison operator |
| `severity` | `"WARN"` \| `"BLOCK"` | `"BLOCK"` | Decision outcome when violated |
| `reason` | `str` \| `None` | `None` | Override the auto-generated reason |

---

Budget counters are shared with the object passed to Sidecar. Record actual
usage explicitly for external calls; Judge usage reaches this budget once.
PAUSE suspends Govern dispatch or invokes the configured approval handler.
See [Governance](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) for provider rates and limit configuration.

## Updating intent at runtime

A long-lived `Sidecar` can serve one `IntentEnvelope` per task. The following
composition pattern assumes configured envelopes, bindings, and an agent.
Use `set_intent()` between tasks and reset the budget separately when appropriate:

```python
# Before task 1
sidecar.set_intent(IntentGuardian(envelope_1, bindings_1))
agent.invoke(task_1)

# Before task 2
sidecar.set_intent(IntentGuardian(envelope_2, bindings_2))
agent.invoke(task_2)

# Clear intent
sidecar.set_intent(None)
```

> **Note:** `set_intent()` raises `ValueError` if you pass an `IntentGuardian` but `"intent_guardian"` is not in `sidecar.roles`.

See [v0.9 authority, privacy and migration](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md) for the current lifecycle APIs.

---

## Governance and evaluator behavior

Source: [website/docs/governance.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md)

These governance enhancements originated in **0.6.1** and remain part of **0.8.0**.
See [Live operations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) for the connected runtime and operator interface.
Govern permits ALLOW/WARN. BLOCK stops. CHALLENGE/REPLAN return control to the
agent loop. PAUSE/ESCALATE invoke a registered handler or suspend when unresolved.
Observe remains advisory.

## Local approval flow

```python
from agentic_sidecar import Sidecar
from agentic_sidecar.cli.approval import CLIApprovalHandler

sidecar = Sidecar(
    on_sidecar_failure="fail_closed", mode="govern",
    escalation_handler=CLIApprovalHandler(),
)
```

Attach configured tools with `adapters.langgraph.attach()`. The handler prompts
when evaluation produces PAUSE/ESCALATE. Try `agentic-sidecar approval-demo`
without executing a tool. You can also register `on_escalation_required`.

| Action | Result |
| --- | --- |
| approve_once | Authorizes this invocation; the next proposal is evaluated and approved separately |
| reject | BLOCK for this proposal |
| modify_intent | Validates a full IntentEnvelope, preserves bindings, reevaluates once; another intervention suspends |
| ask_agent_to_replan | REPLAN; return control to the agent loop |
| stop_agent | BLOCK and stop subsequent proposals on this Sidecar instance |

Responses must reference the request's decision ID. Each resolution gets its
own ID and causal_link to the originating decision. BLOCK is never offered
for approval. Missing handlers suspend, independently of failure mode. Handler
errors/malformed responses follow the configured failure policy.

Custom loops call `evaluate(context)` then `enforce(context, decision)` before
dispatch. Catch SidecarBlockedError/SidecarSuspendedError to handle outcomes;
neither exception executes the proposed tool. Review the offline walkthrough:

```bash
uv run python examples/v0_6_1_governance.py
```

## Full-plan review

```python
from agentic_sidecar import PlanEvaluator, Sidecar

sidecar = Sidecar(on_sidecar_failure="fail_closed", roles=["planner"], planner=PlanEvaluator())
decision = sidecar.evaluate_plan(
    [{"tool_name": "read_charge"}, {"tool_name": "issue_refund"}],
    goal="Explain the disputed charge",
)
assert decision.status == "REPLAN"
```

An active envelope supplies the goal/constraints. Enabled deterministic gates
check every plan step; evaluators receive goal, constraints, history, intent,
plan, bindings and metadata. This boundary reviews a supplied plan without
executing it. Planner/Critic remain scoped heuristics; see [Limitations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md).

## Optional live Judge providers

Install `agentic-sidecar[openai]` or `agentic-sidecar[anthropic]`. Configure the
corresponding API-key environment variable and an explicit accessible model.
OpenAIJudge uses the [Responses API](https://developers.openai.com/api/reference/python/resources/responses/methods/create);
AnthropicJudge uses the [Messages SDK](https://platform.claude.com/docs/en/api/sdks/python).
SDK imports are lazy; each request disables retries and sets a timeout.

`MockJudge` is the explicitly named offline provider. OpenAIJudge and
AnthropicJudge never silently substitute mock responses.

Live providers accept input_cost_per_million/output_cost_per_million in USD.
Supply current model rates when using cost limits or BudgetGuardian. Rates are
not hardcoded. Calculated cost uses supplied token rates and is an estimate,
not a provider billing statement. To test a live contract without cost accounting, explicitly set
cost_limit=None and omit the task budget:

```python
import os
from agentic_sidecar import JudgeEvaluator, OpenAIJudge

# Configure OPENAI_API_KEY and SIDECAR_OPENAI_MODEL before invoking this example.
judge = JudgeEvaluator(OpenAIJudge(model=os.environ["SIDECAR_OPENAI_MODEL"]), cost_limit=None)
```

Judge validates all seven statuses, reasoning, confidence and usage; errors
propagate to Sidecar failure policy. Sync/async share limits, usage and latency
accounting. Configuring Judge and Budget on Sidecar connects returned usage
once; external tool/framework usage still needs record_invocation(). Cost limits
apply after a response. See [timeout/accounting limits](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md).

Run live smoke tests explicitly after configuring credentials and models:

```bash
uv sync --extra openai --extra anthropic
uv run python scripts/smoke_judge_providers.py --provider openai --model YOUR_MODEL
uv run python scripts/smoke_judge_providers.py --provider anthropic --model YOUR_MODEL
```

## Acceptance evidence

Local acceptance: **402 passing tests**, **93% coverage**, eight offline Python
examples and ten notebook cells, strict MkDocs/snippet/link checks, Ruff/mypy,
Actionlint, and wheel/sdist/Twine metadata validation. The full suite also passed
on Python 3.10; CI covers Python 3.10–3.13.

Runtime tests cover all outcomes, Observe/Govern, sync/async interception, all
five approval actions, missing handlers, mismatched IDs, malformed outputs,
injection/recording/provider failures, timeout behavior and accounting. Real
LangGraph StateGraph/ToolNode dispatch is exercised in CI with the optional extra.
Deterministic injected SDK clients verify OpenAI/Anthropic request/usage contracts.

Live smoke status during local validation: **not run for either provider**;
OPENAI_API_KEY and ANTHROPIC_API_KEY were not configured. This is recorded
separately in tests/validation/provider_smoke_status.json. Live evidence remains
an open 0.6.x acceptance item; CI does not require paid API credentials.

Four deterministic fixtures compare guardian off/on with clean controls:

| Scenario | Unsafe proposal | Clean control | Guardian off | Guardian on |
| --- | --- | --- | --- | --- |
| Refund | $850 against $500 limit | $120 | Both ALLOW | Unsafe BLOCK; clean ALLOW |
| Environment | production against staging scope | staging | Both ALLOW | Unsafe BLOCK; clean ALLOW |
| Export | confidential against public allow-list | public | Both ALLOW | Unsafe BLOCK; clean ALLOW |
| Delegation | external against support-team allow-list | support | Both ALLOW | Unsafe BLOCK; clean ALLOW |

**Observed:** 4/4 unsafe proposals caught with guardian on (100%); 0/4 with it
off (0%); 0/4 clean controls falsely blocked (0%). These fixtures validate explicit
bound fields; delegation is an allow-list check, not enforcement of delegated
authority. They make no claims about general model quality or task success.

```bash
uv run pytest tests/validation
uv run python scripts/intent_benchmark.py
```

Release automation validates tag/source/changelog before building and validates
wheel/sdist metadata before publication. CI runs examples, compiles Python doc
fences, checks local file links and builds docs strictly on pull requests.
Pages deployment is limited to main. [Roadmap](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/roadmap.md) tracks remaining work.

## v0.9 lifecycle and evidence

Task authority, reader access, redacted summaries and paired supervision measurements
are available. See [the v0.9 guide](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md) for dispatch-time enforcement, migration
and explicitly synthetic benchmark limits. Plan Critic evidence must be step-scoped.

---

## Shared and exclusive supervision

Source: [website/docs/scoped-supervision.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/scoped-supervision.md)

Added in **0.8.0**. Configure context/intent only, guardrails only, or both.
Shared layers apply to a declared system/task; Exclusive layers apply to named
agents. The trusted harness creates `ScopedSystem`, binds each agent identity,
then gives that agent only its context payload and supervised tools.

```python
from agentic_sidecar import ContextSpec, GuardrailSpec, ScopedSystem, ScopeLayer
from agentic_sidecar.gate.policy import PolicyRule

system = ScopedSystem(
    system_id="support", task_id="ticket-42", agents=["research", "refund"],
    shared=ScopeLayer(
        context=ContextSpec(goal="Resolve billing", values={"customer": "A100"}),
        guardrails=GuardrailSpec(rules=[PolicyRule(tool="delete_*", effect="deny")]),
    ),
    exclusive={"refund": ScopeLayer(
        context=ContextSpec(goal="Prepare refund", values={"transaction": "T100"}),
        guardrails=GuardrailSpec(rules=[PolicyRule(tool="export_*", effect="deny")]),
    )},
)
refund = system.bind("refund", on_sidecar_failure="fail_closed")
payload = refund.context()
# Explicit transport: host writes the payload into this agent's instructions.
refund.deliver(lambda context: print(context["goals"]))
# Pass refund.sidecar to the selected framework adapter's attach().
```

`ContextSpec` carries goal text and structured values; text is not a deterministic
guardrail. Shared and exclusive goals are preserved in order. Equal duplicate
context keys are accepted; conflicting values are rejected during configuration.
Unknown/duplicate agent identities and unknown exclusive targets are rejected.
A single exclusive layer may be assigned to several agent IDs by the host.

`GuardrailSpec` carries ordered tool policies plus optional constraint values and
`ConstraintBinding` entries. Each layer is evaluated independently: an exclusive
allow cannot override a shared deny, or a weaker local limit override a shared
limit. Missing bound arguments and unknown constraint references cannot silently
pass. All mandatory checks precede custom decision hooks; warnings cannot hide a
later denial. The same checks cover full-plan evaluation. Within each policy
layer, first matching rule wins, as in `PolicyAdvisor`.

Each bound agent has a separate Sidecar/history/runtime. Configuration and returned
payloads are copied. Harness-bound IDs overwrite spoofed reserved decision metadata
(`sidecar.scope`, `sidecar.context`); tool arguments never select an identity.
Audit policy fingerprints include shared and exclusive guardrail configuration.

## Limits and responsibilities

This is explicit host integration, not automatic prompt/memory rewriting. SDK
adapters cover returned tool objects, not every framework action, handoff or
retained raw function. Observe mode records without enforcement; fail_open can
permit calls after evaluation failures. Use Govern/fail_closed for containment.

The configuration object and Sidecar belong to the trusted host. In-process Python
wrappers are not process isolation. Run protected tools and credentials in an
enforcing service under a separate identity; restrict agent access to that service.
The [MCP gateway example](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/examples.md) demonstrates a separate-process boundary,
server-side checks and an unavailable raw tool; it does not sandbox a hostile OS
user who can inspect gateway memory/files or change its launch environment.

Only assigned exclusive context is returned through explicit host delivery. In 0.9,
private goals/values are not evaluator/audit metadata. Reader access, context
updates/expiry/revocation, redacted evidence and operator readers are documented in
[v0.9](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md). Framework memory, prompt, result and output transport remain host
responsibilities; there is no process isolation or automatic secret scrubbing.

---

## Live runtime and operator controls

Source: [website/docs/live-operations.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md)

Sidecar now owns a task-local runtime event journal. The LangGraph adapter records
proposals, decisions, actual dispatch reservations, completions and failures.
Evaluation alone never reports successful execution. Local operator controls run
independently of the Judge and use the same runtime as approval resolution.

## Connect a real task

```python
import os
from pathlib import Path
from agentic_sidecar import EventJournal, OperatorServer, Sidecar, TaskRuntime
from agentic_sidecar.adapters.langgraph import attach

runtime = TaskRuntime(journal=EventJournal("order-task", Path("order-task.jsonl")))
sidecar = Sidecar(
    on_sidecar_failure="fail_closed", mode="govern", runtime=runtime,
    escalation_handler=runtime,
)

def read_order(order_id: str) -> str:
    return order_id

with OperatorServer(
    runtime, token=os.environ["SIDECAR_OPERATOR_TOKEN"], actor="local-operator",
) as server:
    print(server.url)
    # Keep this context alive for the lifetime of your agent/graph.
    tools = attach(sidecar, [read_order])
    read_order_tool = tools[0]
    read_order_tool("order-123")
```

Generate a secret of at least 32 characters locally, set `SIDECAR_OPERATOR_TOKEN`
in the application and operator terminal, and keep it out of URLs. Open the
printed task URL for the Control Room and enter the token. The UI displays the
objective, supplied plan, measured intent findings, risk, budget, action lifecycle
and audit events. It exposes pause, resume, stop, explicit restart, intent editing,
replan, and all five per-decision approval actions. The actor is configured by the
server, not trusted from request bodies.

```bash
export SIDECAR_ENDPOINT=http://127.0.0.1:PORT/tasks/order-task
agentic-sidecar status --follow
agentic-sidecar status --follow --json
agentic-sidecar control pause
agentic-sidecar control resume
agentic-sidecar control stop
agentic-sidecar approve DECISION_ID approve_once
agentic-sidecar approve DECISION_ID reject
agentic-sidecar approve DECISION_ID modify_intent --intent-file intent.json
```

`status` without an endpoint retains the standalone narrator demonstration.
With an endpoint it reads real runtime status and new events using a sequence
cursor. `--json` prints formatted JSON snapshots, not JSONL. The live human
narration identifies proposed, blocked, paused, suspended, executed, completed
and failed actions. `completed` counts successful tool returns, not proposals.
A model hook can replace gate stages; missing alignment/risk is reported as
not evaluated rather than invented. Intent findings describe explicit constraint
checks, not a general semantic proof of alignment.

## Local protocol and isolation

The server binds only to `127.0.0.1`; no TLS or public deployment is provided.
Each server holds one task, one token and one configured actor. Use a separate
secret/server per operator trust boundary. Every API read and mutation requires
`Authorization: Bearer TOKEN`. The HTML shell contains no task data or token.
There is no CORS access; cross-origin API requests are rejected. Audit files
contain tool arguments and intent context: protect their filesystem access.
Tools/context must support Pydantic JSON serialization for export.

All routes are prefixed by `/tasks/TASK_ID`:

| Method and suffix | Result |
| --- | --- |
| GET `/status` | Objective, intent, plan, findings, budget, actions, pending approvals, running calls, counters |
| GET `/events?after=N` | Immutable events strictly after sequence N |
| POST `/control` | `{"action":"pause\|resume\|stop\|restart\|replan"}`; submit one action string |
| POST `/approval` | `decision_id`, `action`, optional `modified_intent` and `explanation` |
| POST `/intent` | `{"intent":{...}}` containing a complete IntentEnvelope |

Unknown tasks are rejected. Approval IDs must identify an unresolved request in
this runtime; duplicate/replayed answers are rejected. Approve-once authorizes
one dispatch; authorization is bound to an immutable fingerprint of the evaluated
context, and changed or consumed proposals cannot dispatch. Modify-intent validates
a complete envelope, preserves bindings, and reevaluates the paused proposal.
Runtime intent approvals apply the validated envelope, record the approving actor
and invalidate earlier verdicts before acknowledgement. Direct intent editing also
invalidates earlier verdicts. Approval waiting times out
into REPLAN, including with fail_open. The harness handles replanning and retries;
the operator replan control pauses further dispatch until explicit resume.

## Stop, cancellation and access revocation

Pause/stop share a lock with dispatch reservations. Stop latches before writing
the stop event or invoking external callbacks, independently of evaluation,
approval and failure policy. Once the latch is effective, queued proposals,
approval retries and concurrently evaluated verdicts cannot dispatch. Epochs
invalidate pre-stop/pre-pause decisions, including after explicit restart.
Stop applies to wrapped dispatch in Observe as well as Govern. A broken audit
sink cannot prevent access-revocation callbacks; stop receipts report audit_error
when stop evidence could not be persisted.

Already-dispatched synchronous tools may complete and retain their side effects.
A dispatch event marks admission to execution; stop does not reverse that
admission. Async tools run as owned asyncio tasks and receive cancellation
requests on their own event loop. Cancellation is cooperative: tools can suppress
it. Completion/failure evidence records what actually happened; a request to
cancel is never reported as a completed cancellation. External harnesses can
supply a cancellation callback to `runtime.dispatch(..., cancel=callback)`.

Credential/MCP/session/delegation access belongs to its issuer or gateway. Supply
named `TaskRuntime(revokers={"gateway": revoke_task_access})` callbacks when the
harness grants such access. Each callback must synchronously revoke the root
task's access **and all its sessions and delegated task access**, and return
exactly `True` only after that issuer acknowledges the revocation. Exceptions,
False and other values produce partial failure. The stop receipt reports
`effective_at`, already-running IDs, cancellation requests, per-issuer results,
and `access_revocation`: acknowledged, partial_failure, or not_configured.
`not_configured` acknowledges only the local dispatch stop, never credential
revocation. Revocation failures and in-flight revocations prevent restart.

Explicit restart requires a stopped, idle task and successful configured
revocations; it creates a new decision epoch. It does not renew credentials.
Unwrapped functions and independently created task runtimes remain outside this
boundary. Cross-process isolation and protected-tool gateways are v0.8 work;
a callback contract is not a built-in MCP credential manager. Lens integrity
integration and formal authority handoff remain later milestones.

## Audit snapshots and restoration

Every event has sequence, event_id, task_id, UTC timestamp, kind, payload,
previous_hash and digest. Decision events contain the frozen JSON decision,
trigger, rationale/findings, injected context, proposal_id, policy content/hash,
parent decision link and optional parent_plan_step. Supply
`DecisionContext(parent_decision_id=..., parent_plan_step=...)` when evaluating
steps from a parent plan. Approval records contain actor, action and decision ID;
the resolved decision's causal_link points to the original paused decision.
Dispatch/completion records share invocation_id and decision_id.

`RuntimeEvent` is frozen and stores payload as JSON text. Export returns fresh
nested objects, so mutating exported data or input arguments cannot rewrite the
journal. The older public `sidecar.decisions` list and caller-created AuditRecord
remain compatibility surfaces; the journal is the execution evidence.

The optional JSONL sink writes and fsyncs before publishing an event. New files
use mode 0600; use one writer per task/file. Sink failure follows the configured failure policy. fail_closed prevents dispatch;
fail_open permits execution with missing evidence and reports audit_errors in
status. Stop and stale/consumed decision guards remain enforced independently.
`EventJournal(task_id, path)` restores and checks sequence, identity and hashes.
Malformed partial records and corruption within the retained chain fail restoration.
Removing complete trailing records leaves a valid chain and cannot be detected
without an external trusted head/length checkpoint, which is not provided here.
Hash chaining also cannot detect malicious rewriting by a file owner.
Restored runtimes are stopped and require explicit restart. Uncompleted dispatches
and partial/unacknowledged revocations remain visible and prevent restart;
resolve them in the owning harness rather than claiming completion after a crash.
In a live process, completion/failure always clears running state and cancellation
callbacks, even if writing the final audit event fails. The sink error still
propagates under fail_closed; a later restore may retain unresolved execution
when that final event is missing.

### AI Operations Specification mapping

This is a native Sidecar artifact, not a new normative AIOS schema. Align with
AIOS occurrence/event/evidence conventions, preserving these distinctions:

| Sidecar field | AIOS meaning |
| --- | --- |
| task_id | Producer task correlation; map to the owning Run through explicit deployment attribution |
| decision_id / invocation_id | Distinct supervision and tool-execution occurrences |
| event_id / sequence / timestamp | Producer event identity, ordering and occurrence time |
| causal_link / parent_plan_step | Evidenced causality/plan context; correlation alone is not a causal edge |
| proposed / decision | Proposed work and supervision outcome, not completed execution |
| executed / completed / failed | Dispatch admission and actual tool outcome |
| actor / approval / stop_acknowledged | Operator evidence and access-boundary acknowledgement |

AIOS v0.4 remains an exploratory draft; no formal schema-conformance claim is
made. Control Tower's native `decision` reader accepts the decision inside an
audit event. Attribute it using EvidenceLink with source `agentic-sidecar`, its
source version, registered deployment ID and artifact reference. BLOCK/PAUSE and
other governance outcomes stay separate from deployment health and heartbeat.

## Reproducible acceptance evidence

```bash
uv run pytest tests/test_operations.py
uv run python examples/v0_7_control_room.py
uv run python examples/v0_7_control_room.py --record /tmp/sidecar-recording.json
# For browser operation, configure the token first:
uv run python examples/v0_7_control_room.py --interactive
# Optional local sibling readback, no sibling dependency added to Sidecar:
PYTHONPATH=../agenticops-control-tower/src uv run pytest tests/validation/test_control_tower_native.py
```

The committed `tests/validation/v0_7_lifecycle.json` records one actual HTTP
approval and refund dispatch/completion, followed by a rejection with no second
side effect. Tests cover immutable export/restore, corruption, stop/retry/concurrent
proposals, already-running calls, async cancellation, partial revocation,
issuer-contract session/delegation denial, auth/task isolation, CLI readback,
causal links, approval timeout, and native Control Tower outcome/health separation.
Authenticated OpenAI/Anthropic smoke remains pending credentials, by request;
this limitation is independent of the local operator acceptance evidence.

---

## Authority, privacy and validation evidence

Source: [website/docs/v0.9.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md)

Released as **0.9.0**. These APIs are native Sidecar contracts; AIOS schema
stability remains v1.0 work. Core installation still needs no sibling packages.

## Task authority and delegation

An `AuthorityBinding(authority="refund", tool="refund*")` requires an explicit
`True` grant for matching tools. Configure it on `IntentGuardian` with trusted
`task_id` and `agent_id`. Missing and denied grants block; authority-bearing
envelopes expire with BLOCK rather than the legacy constraint-only expiry WARN.
Bindings are checked even when a custom decision hook replaces optional evaluators.

```python
from agentic_sidecar import AuthorityBinding, Sidecar
from agentic_sidecar.intent import IntentEnvelope, IntentGuardian, Requester

parent = IntentGuardian(
    IntentEnvelope(goal="Resolve billing", requested_by=Requester(id="operator"),
                   authority={"refund": True, "delete": False}),
    authority_bindings=[AuthorityBinding(authority="refund", tool="refund*")],
    task_id="ticket-42", agent_id="supervisor",
)
child = parent.delegate(agent_id="refund-agent", authority={"refund": True})
sidecar = Sidecar(on_sidecar_failure="fail_closed", mode="govern",
                  roles=["intent_guardian"], intent=child)
parent.revoke()  # Descendants and outstanding child authorizations are invalid.
```

Delegation preserves task scope, constraint values and constraint/authority bindings;
permissions may only narrow and expiry cannot extend the parent's. Generic constraints
are preserved exactly because arbitrary operators have no universal ordering. A shared
registry checks all ancestors. Revocation and dispatch reservation use the same lock:
a reservation already made may complete, but none may be made after revocation returns.
Custom agent loops must call `runtime.dispatch(context, sidecar.enforce(context, decision))`
before executing a permitted tool and `runtime.complete(invocation_id)` afterward.
`evaluate()`/`enforce()` alone do not reserve dispatch or guarantee freshness.
The registry is process-local, not a distributed credential service. Use a protected
server/credential issuer for remote enforcement. Trusted hosts must keep registries,
Sidecars and raw tools outside agent-controlled code.

Task stop revokes the active grant and descendants. Restart does not restore authority;
the trusted harness must explicitly issue a new task/grant. Operator MODIFY_INTENT
rejects authority-bearing envelopes; use explicit harness re-delegation instead of
resetting a child grant and losing ancestor revocation. `set_intent()` always invalidates
outstanding decisions. Treat direct mutation of guardian configuration as unsupported.

Native decision context records `sidecar.authority` grant/task/agent/intent and parent
intent IDs. The existing `sidecar.correlation/1` projection is unchanged; correlate
run/trace/span IDs at the host boundary as before.

## Context privacy and readers

`ContextSpec(readers={"auditor"}, expires=aware_datetime)` authorizes additional
readers besides the assigned agent. `BoundAgent.context(reader="auditor")` returns
a defensive copy; unauthorized readers fail. For combined shared/exclusive payloads,
extra readers must be authorized by every contributing layer. Reader and actor
identities are supplied by authenticated harness code, never by agent tool arguments.

`update_context(values, actor=owner)` changes the host-held payload for subsequent
reads; only the owner can update or call `revoke_context(actor=owner)`. Expiry and
revocation block future reads. Updates do not rewrite previously delivered prompts
or weaken independently configured guardrails. Handoffs are explicit host calls.

Private scope goals/values are no longer automatically injected into evaluator context,
logs or native audit events. The agent receives them through `context()`/`deliver()`.
The scope identity remains in metadata; `sidecar.context` is an empty compatibility
marker. Configure constraints explicitly when a private instruction needs enforcement.

`BoundAgent.evidence()` returns an allowlisted redacted summary (IDs, verdict/risk,
counts and lifecycle status). It excludes arguments, goals, reasons, plans, metadata,
findings and pending approval requests. This is not a native Decision artifact or a
hash-verifiable journal; do not send it to a consumer requiring original evidence.

`OperatorServer(..., reader_tokens={long_secret: "auditor"})` permits reader tokens
only on GET `/status`, with the same redacted summary. Reader tokens cannot control,
approve, modify intent or read raw events. The main operator token explicitly grants
full task access; use it only for a task-authorized operator. Existing Control Room
controls require the operator token. Raw journals, arguments/reasons, correlation
exports and full operator views remain privileged and can contain tool-supplied secrets.

Sidecar does not intercept arbitrary framework memory, user-written logs, network
traffic, model prompts, or agent-generated outputs. It does not sandbox hostile Python
or OS users, scrub arbitrary tool arguments, or retract context/results already delivered.
Its adapters do not capture tool results in the journal or implicitly share them across
agents. Protect each agent's prompt/memory/result transport in the host framework.

## Review fixes and migration

- Hooks receive a copied context and cannot rewrite tool name/arguments, boundary or
  plan. Changes resolve through the configured failure policy; original proposal data
  remains intact. Govern/fail_closed blocks such calls. Fail_open remains explicit.
- Plan verdicts retain the highest step risk and risk findings.
- Critic verification evidence belongs on each step's `metadata`, using `authorized`,
  `eligibility_verified` and `backup_verified`. Top-level metadata authorizes only the
  top-level action; it cannot suppress challenges for an entire plan.
- Constraint-only guardians keep existing expiry WARN semantics. Task-authority
  checks are opt-in through bindings. Observe records authority verdicts without
  enforcing them; task stop remains independent of Observe/failure policy.

## Reproducible evidence

```bash
uv run python scripts/supervision_benchmark.py --output /tmp/sidecar-evidence.json
uv run --extra validation python scripts/supervision_benchmark.py --ecosystem --output /tmp/sidecar-ecosystem.json
```

The committed record is `tests/validation/v0_9_supervision.json` in the repository.
It contains 24 fixed synthetic runs: six scenarios, one unsafe proposal and one clean
control per scenario, with and without supervision. Scenarios cover bound constraints,
unnecessary plan steps, unsupported assumptions, MockJudge, a gate outage and a
provider outage. It records actual wrapped dispatches, not just verdicts.

| Variant | Samples | Unsafe dispatches / 6 | False interventions / 6 | Task successes / 12 |
| --- | --- | --- | --- | --- |
| Agent Alone | 12 | 6 | 0 | 6 |
| Sidecar Govern/fail_closed | 12 | 0 | 2 | 10 |

Success means executing a clean proposal or preventing an unsafe proposal. Two clean
outage controls are deliberately counted as false interventions; fail_closed trades
availability for containment. Latency is measured per run and varies by machine.
Token/cost counters are explicitly synthetic zero because there is no live inference.
Improvement per added dollar is undefined at zero cost. No live-model improvement,
statistical confidence, production task success or economic savings are claimed.

`--ecosystem` uses Chaos 0.8 rate-limit injection at the gate, preserves native event
IDs, and asks Evals 0.9 to score supplied success observations (10/12). A failing clean
outage is an expected observation, not a hidden test failure. Generic scoring/gates
remain Evals-owned; resilience injection remains Chaos-owned. Optional model-backed
Planner/Critic reasoning is deferred until evidence justifies its cost.

Runnable examples: `examples/v0_9_authority_delegation.py` and
`examples/v0_9_private_context.py` in the repository.

---

## Native contracts and intent transfer

Source: [website/docs/v0.10.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md)

Sidecar 0.10.0 delivers candidate native interchange contracts, not a stable
AIOS layer or the coordinated ecosystem v1.0 release. The opt-in module
`agentic_sidecar.contracts` exports `IntentContract`, `DecisionContract`,
`AuditContract`, `ScopeContract`, `IntentTransfer`, `contract_schema` and
`export_audit`. Existing constructors and raw serialization remain supported.

## Schema and migration policy

Each wrapper requires an exact `sidecar.<family>/1` marker. The five families
are intent, decision, audit, scope and transfer. `contract_schema(kind)` returns
a fresh offline Draft 2020-12 schema, independent of installed siblings.
Source schemas live in `schemas/v1`; matching copies are published under the
specification repository's `drafts/sidecar-contracts-v1`. Tests compare every
schema to the runtime model. Package versions and contract markers are independent.

Wrap an existing native object rather than inventing identities or timestamps:

```python
from agentic_sidecar import Decision
from agentic_sidecar.contracts import DecisionContract

native = Decision(status="BLOCK", risk=None, reason="gate unavailable")
wire = DecisionContract(schema_version="sidecar.decision/1", decision=native).model_dump_json()
restored = DecisionContract.model_validate_json(wire)
assert restored.decision.decision_id == native.decision_id
```

AuditContract preserves AuditRecord fields; export_audit validates timezone-aware
timestamps. RuntimeEvent/EventJournal hash chaining and sidecar.correlation/1
remain separate, unchanged native formats. An audit wrapper does not verify a
journal; verify_events requires the complete original native chain. Decision,
audit and intent payloads can include privileged arguments, reasons, goals and
metadata. Authorize access before export; use BoundAgent.evidence for redacted
summaries, which cannot be substituted for verifiable native evidence.

Top-level wrappers reject unknown fields and unknown markers. Existing payload
models retain their historical extra-field behavior. Readers must select the
family explicitly and fail on unsupported markers; no automatic downgrade is
performed. During this 0.x candidate phase, incompatible wire changes require
a new marker, migration documentation and compatibility fixtures. New optional
fields in a /1 contract require producer/consumer coordination because strict
readers reject them. No stable public API promise is made before coordinated
v1.0 acceptance; existing 0.9 native APIs remain available in 0.10.

## Shared and Exclusive scope semantics

ScopeContract.build runs the existing ScopedSystem validator before binding.
Shared context reaches all declared agents; exclusive context reaches its assigned
agent. Conflicting values fail instead of overriding. Every applicable guardrail
must pass: an exclusive rule cannot weaken shared restrictions. Combined context
uses the intersection of reader sets and the earliest expiry. Owners retain
access subject to expiry/revocation. Delivery is an explicit host operation;
context is never implicit authority or evaluator input. Updates and revocation
are instance-local; exported configuration does not preserve runtime revocation
state or retract delivered copies. Only trusted hosts may build configuration;
never accept an agent's scope declaration as authorization.

## Cross-instance and cross-agent propagation

Run `uv run python examples/v0_10_contracts.py` for serialized proposal/receive,
separate guardian instances and live ancestor revocation. IntentTransfer.propose
narrows authority; receive compares authenticated receiver identity, parent intent
and grant IDs, task scope, goal, requester and causal parent metadata. The live
registry then verifies unchanged inherited constraints, non-extended expiry,
non-widened authority and the full ancestor revocation/expiry chain. Bindings are
copied from the receiving host's parent guardian, never accepted from the wire.
The child has a new intent and grant identity; ancestor revocation blocks future
reservations. Reserved calls can finish, as in 0.9.

The trusted harness authenticates the `agent_id` supplied to receive and transports
the private proposal. A proposal is neither a signed credential nor an approval.
Receiving requires the same live AuthorityRegistry as the trusted parent, which
may be shared by separate Sidecar/guardian instances in one host. A fresh registry
rejects the unknown parent grant. Disconnected processes, durable grant replication,
replay prevention and remote issuer/revocation protocols are outside this release.
Receiving the same valid proposal can create multiple narrowed grants; hosts that
require one-time delegation must deduplicate it. Importing a grant never resumes
an old TaskRuntime or restores approvals. Check authority at dispatch through the
existing governed adapter; a serialized Decision ALLOW alone permits nothing.

## Compatibility and acceptance

| Boundary | Supported baseline | Evidence / unchanged semantics |
| --- | --- | --- |
| Python | 3.10–3.13 | CI test matrix, standalone install |
| AgenticLens | 0.12.0 | correlation/1 native reader and journal verification |
| Agentic Chaos | 0.10.0 | recovery proposals, native event identity, paired benchmark |
| Agentic Evals | 0.12.0 | validation extra; scoring separate from supervision |
| MCP server | 0.6.0 | Phase 6 bridge; native access receipts unchanged |
| Control Tower | 0.9.0 | optional Sidecar >=0.7,<1 admits 0.10; native reader |
| AI Operations Spec | 0.7.0 | non-normative mapping, draft markers unchanged |
| Framework SDKs | See pyproject optional extras | native adapter CI: AutoGen, CrewAI, OpenAI Agents, Google ADK, MCP, LangGraph |

`tests/test_contracts.py` covers migration, marker rejection, tampering,
propagation, constraints, scope conflicts, reader privacy and ancestor revocation.
Existing adapter, journal, approval and failure-policy tests remain release gates.
`make check`, `make docs-check`, `make examples-check`, `make release-check` and
package build validate the candidate. The fixed paired supervision benchmark
retains its synthetic 24-run configuration and does not establish live-provider
benefit; see the v0.9 acceptance record. Authenticated provider smoke remains open.
Sibling compatibility notes do not add runtime dependencies or require package
patches where native readers and supported ranges are unchanged. MCP standalone
image pins, if advanced, require a patch release of that sibling.

---

## Framework and ecosystem integrations

Source: [website/docs/integrations.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md)

## Framework adapters

All adapters share the same sync/async governed callable boundary. Supply plain,
typed Python functions with docstrings to `attach(sidecar, tools)` and pass the
returned tools to your framework. The core imports no framework SDK.

| Module / install extra | Returned surface | Tested SDK | Python |
| --- | --- | --- | --- |
| `adapters.langgraph` / `langgraph` | Typed callables for LangChain StructuredTool / LangGraph | LangGraph 1.x, LangChain Core 1.x | 3.10+ |
| `adapters.autogen` / `autogen` | AutoGen Core FunctionTool | 0.7.5 | 3.10+ |
| `adapters.crewai` / `crewai` | CrewAI Tool | 1.6.1 | 3.10–3.13 |
| `adapters.openai_agents` / `openai-agents` | OpenAI Agents FunctionTool | 0.24.0 | 3.10+ |
| `adapters.google_adk` / `google-adk` | ADK FunctionTool | 2.12.0 | 3.11+ |

The native SDK conformance job runs on Python 3.12; the core/LangGraph matrix
runs on 3.10–3.13. Other SDK/Python combinations are not independently certified.
SDK extras are pinned to the validated versions. CrewAI and ADK dependencies use
Python markers; an ineligible Python environment will not install that SDK.

```python
from agentic_sidecar import Sidecar
from agentic_sidecar.adapters.autogen import attach

sidecar = Sidecar(on_sidecar_failure="fail_closed", mode="govern")

def read_order(order_id: str) -> str:
    """Read an order."""
    return f"Order {order_id}"

# Install agentic-sidecar[autogen] before running this conversion.
tools = attach(sidecar, [read_order])
```

Observe records all seven verdicts and calls through. Govern executes ALLOW/WARN,
blocks BLOCK, and resolves or suspends PAUSE/ESCALATE/CHALLENGE/REPLAN. All adapters
use the same approval, explicit fail_open/fail_closed, stop and audit paths.
OpenAI tools disable SDK error conversion so governance exceptions propagate.
CrewAI `run()` also runs async callables; the shared async wrapper retains owned
cancellation. Frameworks may convert exceptions into model-visible errors; such
conversion never authorizes the denied tool invocation.

Supported inputs are plain typed callables, not prebuilt SDK tools, injected SDK
context parameters, hosted tools, automatic handoffs or agent-as-tool recursion.
Protect every nested boundary explicitly. Original functions and raw sessions
remain accessible to a trusted host: wrappers are not a sandbox. Use
[scoped supervision](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/scoped-supervision.md) for shared/exclusive composition.

## MCP

`agentic_sidecar.adapters.mcp.attach(sidecar, session, tool_names)` creates async
callables for allowlisted tools on an initialized MCP 2.3.0 `ClientSession`.
The MCP SDK owns transport/discovery. Client-side checks alone cannot contain an
agent holding the raw session. The gateway example also gates the server's tool,
keeps credentials server-side, rejects raw tool names and records actual execution.
See [examples](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/examples.md); production requires a separately secured service identity.

## Versioned native decision evidence

`sidecar.correlation/1` associates each decision with explicit run/trace/span IDs,
logical task/system/agent identity, source journal event, timestamp, policy hash,
boundary, tool name and the original seven-state decision (including causal ID).
The host must supply IDs for the exact session/span; exporting a mixed-span
Sidecar under one span is not automatic correlation.

```python
from agentic_sidecar import DecisionContext, Sidecar
from agentic_sidecar.integrations.correlation import Correlation, export_decisions

sidecar = Sidecar(on_sidecar_failure="fail_closed")
sidecar.evaluate(DecisionContext(tool_name="read"))
records = export_decisions(sidecar, Correlation(
    run_id="run-1", trace_id="trace-1", span_id="span-1",
))
```

Export verifies the complete native journal hash chain first. Projections omit the full DecisionContext; the original Decision trigger details
can contain tool arguments, and reasons can contain sensitive values. Authorize
readers and redact appropriately before exporting beyond that boundary.
A projection is not independently verifiable execution evidence. Hash chains detect
alteration/reordering, not a full rewrite by a malicious producer without an
external trusted anchor. AIOS mapping is a non-normative draft; stable schemas
remain v1.0 work.

## AgenticLens

Lens **0.7.1** provides `agenticlens.integrations.sidecar.attach_decisions(run, records)`
and native journal verification. Sidecar's optional helper
`agentic_sidecar.integrations.agenticlens.attach_decisions(sidecar, run, span_id=...)`
verifies the journal through Lens and exports the matching projection. Install the
`agenticlens` extra. Lens checks exact run/trace/span identity and atomically rejects
invalid/conflicting batches; duplicate records are idempotent. Diagnosis schema 1.1
adds supervision decisions to the timeline. BLOCK does not mark a span/run/deployment
failed; actual dispatch/completion remains native journal evidence.

The extra admits `agenticlens>=0.7.1,<2` since Sidecar 0.8.4, so it installs
alongside Lens 0.9.0 (ModelFit). ModelFit model recommendations carry no
supervision decisions; correlation readback is unchanged.

## Agentic Chaos and Evals

`integrations.agentic_chaos.evaluate_recovery(sidecar, event, tool_name=..., arguments=...)`
checks/enforces a recovery proposal with a native Chaos event ID. It does not execute
it; actual dispatch still uses a supervised adapter. Tested against Chaos 0.5.3 and
0.6.0; the optional `agentic-chaos` extra admits `>=0.5.3,<2` since Sidecar 0.8.1.
Chaos 0.6.0 event IDs and shape are unchanged; its contracts and pytest plugin stay in Chaos.
Gate failure tests cover explicit fail_open/fail_closed; Chaos retains fault injection.
Evals 0.7.2 retains scoring/report ownership; comparative supervision evidence and
delegated authority are described in the [v0.9 guide](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md). No core sibling dependency is introduced.

## Tower, AIOS and Semantica

Tower 0.5.2's existing native decision/journal reader retains producer outcomes and
separate deployment health. MCP 0.3.5's discovery boundary remains separate from a
live runtime. Compatibility checks do not imply remote operator bridging.
AIOS records the correlation convention as a draft, not stable conformance.
`integrations.semantica` and the empty `semantica` extra are reserved; no provenance
export or upstream compatibility is claimed until its API is validated.

## Native Evals report contract

Evals 0.7.2 publishes packaged report and gate JSON Schemas through
`report_schema()` and `gate_decision_schema()`. Contract 1.x evolves additively;
readers should tolerate unknown fields. Native validation does not establish
AIOS conformance or containment. See the
[contract and runnable examples](https://github.com/DeepAgentLabs/agentic-evals/blob/main/docs/report-contract.md).
Existing dependency ranges remain sufficient; importing the new accessors
directly requires `agentic-evals>=0.7.2`.

For Chaos 0.7 cascades and synthetic poisoning, install Sidecar 0.8.3 or later.
See [compatibility and containment limits](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/chaos-0.7.md).

For Chaos 0.8 workflows and experiments, install Sidecar 0.8.5 or later. The
optional extra then admits `>=0.5.3,<0.9`. See [workflow evidence and limits](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/chaos-0.8.md).


## Current native contracts and operational export

The current checkout keeps optional Lens/Chaos dependencies within `<2`; SDK extras and Python markers are declared in `pyproject.toml`. Release-labelled compatibility sections above record the originally tested releases, not an independent certification of every newer installation.

`agentic_sidecar.contracts` provides five candidate native wrapper families plus `contract_schema()` and validated `IntentTransfer` propagation. See [migration and receiving-host checks](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md). `agentic_sidecar.integrations.aios.export_audit_event()` separately projects public native audit identifiers/outcomes into an AIOS `0.8-draft` audit event, withholding rationale and context. See [operational projection details](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/aios-0.8-operational-artifacts.md) and the [export API](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/api-reference.md#aios-operational-audit-export). Native wrappers, `sidecar.correlation/1`, the hash-chained runtime journal and AIOS projections are distinct artifacts.

Authority registries, task identity and raw tools stay owned by the trusted host. Historical references to authority as future work predate the implemented v0.9 lifecycle; shared contract maturity and independent acceptance remain separate release-policy gates. Semantica is reserved and remains unimplemented.

---

## AIOS operational audit exports

Source: [website/docs/aios-0.8-operational-artifacts.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/aios-0.8-operational-artifacts.md)

AIOS repository v0.8.1 distributes the v0.8.0 schema snapshot under MIT.
Run/Workflow remain **0.4-draft**, provenance **0.6-draft**, and operational
companions **0.8-draft**. Independent acceptance and coordinated v1.0 gates remain open.

## Decisions and audit records

Sidecar 0.11.0 ships `integrations.aios.export_audit_event` for native AuditRecord decisions. BLOCK projects to denied; other governance outcomes project to requested, without asserting execution success. Actor remains unknown. Public source identity, observation time and causal/correlation links are preserved; rationale, tool arguments and execution context are withheld. Malformed supplied identity is rejected.

## Adoption and validation

See [coordinated readiness and examples](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/coordinated-v1-readiness.md) for the
public API and migration path. The [canonical schemas and rules](https://github.com/DeepAgentLabs/ai-operations-spec/tree/v0.8.1/specification/v0.8)
define the projection contract. Source and citation presence do not authenticate
a producer or verify its conclusion. Reference URIs are not instructions to
fetch or execute anything. Use Lens or MCP for optional schema and semantic
checks; source/native identity and unavailable/unknown states remain explicit.

## Dependencies and rollback

The implementation is released in the owning package's minor version, with no
AIOS Python runtime dependency. Native contracts retain their own versions.
Disable optional companion emission or pin the preceding package version to
roll back; do not relabel a companion as an older artifact family.

---

## Coordinated readiness

Source: [website/docs/coordinated-v1-readiness.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/coordinated-v1-readiness.md)

Sidecar 0.11.0 adds the optional
`agentic_sidecar.integrations.aios.export_audit_event(record, target=..., created_at=...)`
projection for native AuditRecord values. It requires a host-supplied public
reference and a timezone-aware recording time. BLOCK becomes denied; other
native governance outcomes become requested, never succeeded. Native decision
id, outcome, correlation and parent decision links are preserved. Actor remains
unknown because AuditRecord has no authenticated actor field.

The exporter omits raw arguments, rationale, execution context and private tool
names. Callers remain responsible for using public opaque identifiers in supplied
references and correlation ids. Importing/exporting evidence grants no authority
and does not alter enforcement. Run `python examples/operational_artifacts.py`.

The live provider command now accepts `--require-all`. It exits 2 if a selected
provider was not run and 1 on a failed call. Release acceptance uses
`uv run python scripts/smoke_judge_providers.py --require-all` with both explicit
models and credentials supplied through the environment. Missing credentials
remain not_run, never a passing acceptance record. Provider calls are opt-in;
no model or key is selected automatically.

Migration/rollback: existing native contracts and runtime flows are unchanged.
Optional callers can disable companion emission and pin 0.10.1. Preserve native
audit records; do not reinterpret an ALLOW as dispatch/completion or relabel
0.8-draft evidence as a native Sidecar contract.

Independent acceptance, live/deployment evidence and the stable freeze remain
separate gates. See the [shared release policy](https://github.com/DeepAgentLabs/.github/blob/main/profile/RELEASE_POLICY.md).

## Coordinated 1.0.0 milestone

Version 1.0.0 marks the coordinated DeepAgentLabs milestone on 2026-11-05.
Development and roadmap delivery continue after this release. Existing draft
and candidate schema markers retain their maturity; package versions do not
certify AIOS conformance or production deployment readiness. Independent review,
independent implementations, security/deployment acceptance, live-provider
validation and the stable contract freeze remain tracked follow-up work.
See the [ecosystem release policy](https://github.com/DeepAgentLabs/.github/blob/main/profile/RELEASE_POLICY.md).

---

## Examples

Source: [website/docs/examples.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/examples.md)

The examples target the **0.8.0** API. Historical version labels in filenames
identify their introduction. Run them from the repository root:

```bash
uv sync --extra dev --extra langgraph
```

Every Python example uses local data or scripted responses; no API key is needed.
See the [example catalog](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/examples/README.md)
for links and setup details.

| File under `examples/` | Purpose |
| --- | --- |
| `governed_customer_support_agent.py` | Observe vs Govern with policy/risk/intent checks; reads and within-limit refunds pass, over-limit refunds and deletions receive BLOCK |
| `langgraph_refund_observe_mode.py` | A scripted real LangGraph agent executes tools while Sidecar records advisory verdicts |
| `langgraph_intent_guardian_govern_mode.py` | A scripted real graph blocks $850 and permits $120 under a $500 refund constraint |
| `v0_3_planner_critic_judge.py` | Direct full-plan checks, heuristic Critic, mock Judge, and composed evaluation |
| `v0_3_judge_providers.py` | Mock provider swapping and synthetic usage accounting |
| `v0_4_budget_and_escalation.py` | Manual budget accounting, PAUSE verdict, explicitly invoked approval handler, and audit serialization |
| `v0_7_control_room.py` | Real HTTP approval/rejection, execution lifecycle and Control Room |
| `v0_6_1_governance.py` | Runtime approval, suspension, full-plan review and shared Judge budget |
| `v0_5_status_narration.py` | Manually supplied decisions, compliance/budget values, and narrator pause/resume state |
| `v0_5_cli_guide.md` | Local CLI snapshots, JSON, follow formatting, demo, and version |
| `sidecar_purpose_demo.ipynb` | Interactive deterministic intent constraints for multiple domains |

For example:

```bash
uv run python examples/v0_3_planner_critic_judge.py
uv run python examples/v0_4_budget_and_escalation.py
uv run python examples/langgraph_intent_guardian_govern_mode.py
```

The customer-support example configures a budget but does not spend against it;
use the budget example to see a PAUSE verdict. Its over-limit refund is classified
by Risk before the Intent stage; the dedicated LangGraph Govern example isolates
Intent Guardian behavior.

The budget example handles an approval request in its own application code.
The governance example demonstrates runtime approval and suspension before
dispatch, plus full-plan review and automatic Judge accounting. The v0.7 Control
Room example uses a real local HTTP interface, records approval and rejection,
and counts actual tool effects. Standalone narrator methods update reported state. Provider mock costs are illustrative
values, not measured inference costs. See [supported scope](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md)
and the [roadmap](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/roadmap.md).

For the notebook, install Jupyter separately and run:

```bash
jupyter notebook examples/sidecar_purpose_demo.ipynb
```

---

## End-to-End Use Cases

For complete, step-by-step walkthroughs solving real-world production problems end-to-end (including multi-layer guardrails, LangGraph integration, and policy enforcement), visit the [Agentic Sidecar Use Cases Site](https://deepagentlabs.io/agentic-sidecar/usecases/).


## v0.8 examples

- `examples/v0_8_scoped_agents.py`: two agents, shared context and policy, exclusive
  context/restrictions, explicit host delivery and blocked dispatch.
- `examples/v0_8_framework_agents.py`: host-bound LangGraph research and AutoGen
  refund tools, shared denial and separate exclusive context (requires both extras).
- `examples/v0_8_correlated_evidence.py`: credential-free native evidence export.
- `examples/v0_8_gateway_server.py`: separate-process credential-owning MCP server,
  launched by `tests/test_mcp_gateway.py` with `SIDECAR_RUN_GATEWAY=1`.

Run `uv run python examples/v0_8_scoped_agents.py`; install the `mcp` extra and run
`uv run pytest tests/test_mcp_gateway.py` for the real transport/gateway scenario.
Framework conformance runs through real native SDK dispatch without model calls.

---

## Troubleshooting

Source: [website/docs/troubleshooting.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/troubleshooting.md)

Use the returned verdict, enabled roles, and configured bindings to inspect
behavior before attaching real tools. These notes describe the **0.8.0** API.

## Required failure configuration

Omitting `on_sidecar_failure` raises `TypeError`; an unsupported value raises
`ValueError`. Choose `fail_closed` for governed decision boundaries:

```python
from agentic_sidecar import Sidecar
sidecar = Sidecar(on_sidecar_failure="fail_closed")
```

## Optional modules and roles

Enable a module by passing its instance and including its role. Intent checks
also require a configured envelope and bindings. Passing an IntentGuardian
without `intent_guardian` in roles raises ValueError. Other optional modules
should likewise have matching roles:

```python
from agentic_sidecar import BudgetGuardian, Sidecar
budget = BudgetGuardian(max_cost=5)
sidecar = Sidecar(on_sidecar_failure="fail_closed", budget=budget, roles=["budget"])
budget.record_invocation(cost=5)
```

Supported roles: policy, risk, intent_guardian, budget, planner, critic, judge.

## Inspect a BLOCK decision

Policy denial, risk threshold, and intent constraints can each produce BLOCK.
Read the exception's `decision.reason` and `context` to identify the stage.
Test a proposed action directly without dispatching it:

```python
from agentic_sidecar import DecisionContext
verdict = sidecar.evaluate(DecisionContext(tool_name="issue_refund", tool_args={"amount": 850}))
print(verdict.status, verdict.reason)
```

Observe mode permits execution after a verdict. Use it with controlled tools
when evaluating rules; Govern enforces BLOCK through the adapter.

## Budget and approval handling

Judge usage automatically reaches the configured task budget. Record other
calls explicitly. Govern suspends PAUSE/ESCALATE when no handler exists.
Register on_escalation_required or pass CLIApprovalHandler as escalation_handler.
Base EscalationHandler is an interface; it raises NotImplementedError.

## Planner input

Use `Sidecar.evaluate_plan(plan, goal=...)` for a full-plan gate. Configuring a
planner on tool calls does not discover the plan. The active envelope supplies
goal/constraints; all evaluators receive history/plan/metadata.

## Provider configuration

Use MockJudge for offline scripted examples. OpenAIJudge/AnthropicJudge make
live API calls and require their optional SDK, credentials and an explicit model.
Supply both token rates before enabling cost ceilings or a task budget.
Provider errors and timeouts follow on_sidecar_failure; direct Judge calls raise.
See [Governance](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) for setup and [Limitations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md) for
post-response cost ceilings and cancellation boundaries.

## Local CLI status

`status` starts with a fresh narrator. Zero calls and no objective are expected.
`demo` shows a populated simulated narrator. Creating a narrator in application
code does not connect a separate CLI process. For live status, run an OperatorServer
in the task process and supply its URL through --endpoint or SIDECAR_ENDPOINT;
set the same SIDECAR_OPERATOR_TOKEN in the operator terminal.
Use a positive refresh interval for `--follow`.

## Rule matching

Tool patterns use `fnmatch`, not regular expressions. Rules are ordered;
the first match wins. Argument checks require the exact configured key.

```python
import fnmatch
print(fnmatch.fnmatch("soft_delete", "delete_*"))  # False
print(fnmatch.fnmatch("soft_delete", "*delete*"))  # True
```

Constraint bindings skip undeclared constraints and absent arguments. Bindings
validate the supplied structured values; they do not infer natural-language limits.

## Optional framework and docs setup

The callable wrapper itself does not import LangGraph. To run the real graph
examples, install its extra. To build the site, install the docs extra:

```bash
uv sync --extra dev --extra docs --extra langgraph
uv run mkdocs build --strict
```

For a docs build failure, inspect the first error, verify local links/anchors,
and include new pages in `website/mkdocs.yml` navigation.

---

## Limitations

Source: [website/docs/limitations.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/limitations.md)

Supported scope for the **0.9.0** API. See [Governance](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md) for usage
and validation evidence, and [Roadmap](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/roadmap.md) for future priorities.

## Governance boundary

Observe records verdicts and executes tools. Govern executes ALLOW/WARN only;
BLOCK raises SidecarBlockedError. PAUSE/ESCALATE invoke a registered handler or
raise SidecarSuspendedError when unresolved. CHALLENGE/REPLAN always return
control through SidecarSuspendedError. These exceptions prevent the tool call;
they do not checkpoint, resume, or replan an entire agent workflow.

Approval is local or supplied through the authenticated runtime HTTP interface. Async tools run
evaluation/approval in a worker thread to avoid blocking their event loop.
Cancelling the waiting coroutine cannot cancel a running sync evaluator/prompt.
Use one Sidecar/Judge/Budget per task. Runtime approvals support concurrent
proposals; evaluators and manual budget accounting are not a task transaction.

APPROVE_ONCE authorizes the current invocation only. BLOCK cannot be approved.
MODIFY_INTENT requires a full constraint-only envelope, preserves bindings and reevaluates once;
authority-bearing intents require explicit harness re-delegation;
another intervention returns control without an automatic prompt loop.
STOP_AGENT latches the task; explicit runtime restart is required to run again. REJECT blocks that proposal. REPLAN returns control to the agent loop.

## Deterministic intent and heuristic evaluators

Policy/Risk use ordered tool patterns and argument comparisons. Intent requires
explicit bindings; absent constraints/arguments are skipped. Expiry produces
WARN for constraint-only guardians. Opt-in authority bindings enforce granted/denied
authority and ancestor expiry/revocation at dispatch; see [v0.9](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.9.md).

`evaluate_plan()` checks explicit step dictionaries; it does not discover or
execute the agent's plan. Planner uses selected tool/goal patterns, contradictory
tool pairs and supplied constraint bindings. Critic uses selected risky tool
patterns, previously permitted opposing actions and explicit metadata evidence
flags (`authorized`, `eligibility_verified`, `backup_verified`). These flags are
caller-supplied assertions, not independently verified authorization. History
records verdicts, not successful executions. Heuristics do not establish general
semantic intent or proof of correctness; confidence thresholds filter fixed
heuristic scores. Full-plan Critic review conservatively checks each step.

## Live providers and usage accounting

OpenAIJudge and AnthropicJudge make real optional SDK calls. MockJudge is an
explicit offline fixture. Models and current USD token rates are configured by
the caller. Supply both rates for cost ceilings/task budget accounting; without
rates, use cost_limit=None and no BudgetGuardian. Known returned usage is recorded
once; framework/tool usage outside Judge still needs record_invocation().

Judge cost limits apply after a response and cannot reserve future spend.
Provider-native timeouts disable SDK retries. Judge timeout bounds waiting;
an arbitrary sync call cannot be cancelled and may finish after timeout. Late
sync responses still account usage, and another invocation is refused while
one is outstanding. Native async calls are cancelled at timeout; provider spend
without returned usage cannot be recovered from that cancellation. Malformed
outputs with valid usage still account completed inference before verdict
validation. Unknown or invalid usage never creates invented cost measurements.

Live API smoke results require credentials and an explicit model. Normal CI
uses deterministic SDK contract fixtures. See [acceptance evidence](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/governance.md)
for the recorded live-smoke status.

## Runtime, records and integrations

Failure policy covers injection, evaluator/provider errors, malformed verdicts,
logging/recording and approvals. A failed recorder returns the configured
fallback but cannot guarantee an audit entry -- the already-computed verdict
is discarded, so with `fail_open` a recorder failure after a genuine BLOCK
resolves to ALLOW; `fail_closed` resolves the same failure to BLOCK instead.
A custom before_tool_call hook replaces all built-in stages, including plan
checks, budget and evaluators.

Decision IDs and approval causal links are available. In-memory contexts are
deep-copied at recording time; the public list, its contexts and nested decision
dictionaries remain mutable. The immutable runtime journal records durable execution lifecycle; see
[Live operations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md). AuditRecord remains a caller-created export type.

LangGraph sync/async plain callables are supported. Framework-native tool objects,
additional adapters and optional ecosystem exports target 0.8.

## Narration and CLI

The standalone StatusNarrator remains manually populated. Connected CLI status
reads actual runtime events and execution state; `--follow --json` prints
formatted snapshots, not JSONL. The Control Room uses the same authenticated
HTTP interface. See [Live operations](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/live-operations.md) for task isolation,
stop/cancellation/revocation boundaries and restore behavior.

The package remains Pre-Alpha; stable API/schema guarantees target 1.0.

## Scoped delivery and adapters

v0.8 provides explicit host context delivery and mandatory guardrail composition.
Wrappers cover returned tools only. Private-context isolation across external
memories, outputs and telemetry remains v0.9 validation work; keep journals and
configuration in the trusted host. Semantica export remains conditional. See
[scoped limits](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/scoped-supervision.md#limits-and-responsibilities) and
[validated framework versions](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/integrations.md).

---

## Historical integration note: AIOS v0.6.1 compatibility

Source: [website/docs/aios-0.6.1.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/aios-0.6.1.md)

AI Operations Specification repository v0.6.1 adds the first v0.6.x drafts:

- [provenance records](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.6.1/specification/v0.6/provenance.md): a
  `spec_version: "0.6-draft"`, `artifact_type: "provenance"` companion artifact
  with subjects, source references, derived findings and evidence lineage;
- a [portable conformance suite](https://github.com/DeepAgentLabs/ai-operations-spec/tree/v0.6.1/specification/v0.6/conformance-suite)
  with expected outcomes and rule citations;
- [naming conventions](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.6.1/specification/v0.6/naming-conventions.md).

Run and Workflow artifacts stay `0.4-draft`; the v0.4 schemas and
`AIOS-0.4-*` rule catalog are unchanged, so existing exports remain valid.
Consumers that do not check `0.6-draft` must reject provenance records under
`AIOS-0.5-V03` rather than validate them against v0.4.

## Agentic Sidecar

Decisions, authority grants and the native `sidecar.correlation/1` convention stay native. A provenance finding is descriptive: it grants no authority, cannot approve an action and cannot bypass supervision, whatever its `status` or `confidence`. Sidecar does not emit AIOS `0.6-draft` provenance records. Its native decision
provenance (`AuditRecord`, `CausalLink`, `DecisionRationale` and the
`DecisionTrigger` shapes) is a separate Sidecar-local audit export, not an AIOS
provenance record, and keeps its existing contract.

## Dependencies

No runtime dependency floor changes and no package release are needed for
this documentation alignment. Independent review is still pending; passing the
suite or holding a verified provenance record is not stable conformance and
does not show that any artifact or finding is true. See the
[AIOS ecosystem guide](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.6.1/docs/v0.6.1-ecosystem.md).

---

## Historical integration note: AIOS repository v0.7.0 compatibility

Source: [website/docs/aios-0.7.0.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/aios-0.7.0.md)

AIOS v0.7.0 adds non-normative migration guidance, an OpenTelemetry companion
profile pinned to upstream semantic conventions 1.37.0, tested retry examples,
and a strict MkDocs publishing pipeline. Run/Workflow remain `0.4-draft`;
provenance remains `0.6-draft`. Independent-review gates remain open.

Native decisions, task authority and access evidence keep their current meaning. Authorization does not prove dispatch or completion.

No runtime dependency floor changes or package patch release are required.
This is documentation alignment; it does not add an automatic exporter or
migration adapter. The paired telemetry example is illustrative, not OTLP JSON.

For an offline example, clone AIOS at tag `v0.7.0`, run `uv sync --extra dev`,
then `uv run pytest tests/test_otel_binding.py tests/test_v06_conformance_suite.py`.
Use `make docs` to build its browsable documentation. These are specification
repository checks, not commands supplied by this package.

See the [migration guide](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.7.0/specification/v0.6/migration-guide.md),
[OTel profile](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.7.0/specification/v0.6/otel-binding.md)
and [dependency matrix](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.7.0/docs/v0.7.0-ecosystem.md).

Repository v0.7.0 corrects the next-phase release number; the incorrect
v0.6.2 publication and tag have been removed. Artifact markers and independent-review gates do not change.

---

## Historical integration note: Chaos 0.11 ChaosHub compatibility

Source: [website/docs/chaos-0.11-chaoshub.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/chaos-0.11-chaoshub.md)

Sidecar 0.10.1 widens both optional Chaos ranges to `<0.12` so the 0.11 wheel can be installed. Governance decisions and the live stop/revoke bridge keep their native meaning; recipe execution is caller-owned and does not prove containment.

Chaos 0.11.0 adds six offline framework-neutral starter recipes, explicit
commit-pinned GitHub registry exchange and opt-in installed fault plugins.
Downloads and catalog listing never execute recipe targets. JSON recipes are
also valid YAML and need no YAML extra. `hub push` stages a contribution in a
caller-owned registry checkout for an ordinary reviewed pull request.

## Offline operator example

Run from an agentic-chaos checkout with its instrumented offline target:

```bash
agentic-chaos hub search rag
agentic-chaos hub pull rag-context-poisoning recipe.json
agentic-chaos chaos run examples/chaoshub_app.py --experiment rag-context-poisoning --save hub-report.json
```

The example deliberately emits a synthetic wrong answer. Availability can pass
while resilience stays inconclusive without quality probes or a fidelity judge.
Review target, probe and workflow paths before running downloaded recipes.
Remote access needs an explicit repository and full commit SHA; plugin loading
executes trusted installed code only when explicitly requested. The native
Chaos report and AIOS export formats are unchanged.

See the [ChaosHub guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/4b60f2e8deb7b68a469a10d3219e60fdc3f3c562/docs/v0.11.md)
and [offline app](https://github.com/DeepAgentLabs/agentic-chaos/blob/4b60f2e8deb7b68a469a10d3219e60fdc3f3c562/examples/chaoshub_app.py).
Coordinated ecosystem v1.0 acceptance remains open.

---

## Historical integration note: Chaos 0.7 compatibility

Source: [website/docs/chaos-0.7.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/chaos-0.7.md)

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

Sidecar 0.8.3 widens its optional agentic-chaos extra to >=0.5.3,<0.8. Recovery proposals retain native Chaos event IDs. This packaging patch changes no governance behavior; cross-framework attack containment remains v0.9 validation.

---

## Historical integration note: Chaos 0.8 compatibility

Source: [website/docs/chaos-0.8.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/chaos-0.8.md)

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

Sidecar 0.8.5 widens its optional `agentic-chaos` extra to `>=0.5.3,<0.9`.
Recovery proposals keep native Chaos event IDs, including for events raised
inside workflow steps. Chaos workflow Suspend gates are Chaos-owned approvals,
not Sidecar decisions. This packaging patch changes no governance behavior.
Injecting into Sidecar gate and approval paths remains v0.9 validation.

---

## Historical integration note: Chaos 0.9 compatibility

Source: [website/docs/chaos-0.9.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/chaos-0.9.md)

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

Sidecar 0.9.1 widens its optional `agentic-chaos` extra to `>=0.5.3,<0.10` and its `validation` extra to `>=0.8,<0.10`. Recovery proposals keep native Chaos event IDs in scored reports. A poisoned response that Sidecar contains is still `unverified` in the Chaos score unless a fidelity judge scored it. Sidecar decisions do not feed the score, and the score does not drive Sidecar governance. This packaging patch changes no governance behavior.

---

## Historical integration note: Control Tower 0.6.0 compatibility

Source: [website/docs/control-tower-0.6.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/control-tower-0.6.md)

Tower combines Phase 6 (local MCP connector and investigation) and Phase 6A
(approved staging incident-to-recovery) in a single **0.6.0** release, paired with
MCP **0.3.6**. Sibling packages remain optional; no producer dependency floor or
runtime behavior changes in this documentation alignment.

Sidecar 0.8.0 retains decision-time supervision, dispatch blocking and task
stop/restart ownership. Tower provides a thin optional SidecarContainmentAdapter.
Install an mcp revoker in TaskRuntime to coordinate native MCP key revocation.
Stop does not depend on model approval; explicit human restart still uses
Sidecar stopped/idle/revocation checks. In-flight calls and unsupported downstream
credentials prevent claims of universal containment.

The first supported remediation target is Tower's deterministic local SQLite
staging dependency runtime. Exact-preview approval binds target, dependency,
impact, rollback and recovery criteria. Tower commits a consumed execution claim
before dispatch; duplicates and interrupted actions cannot automatically replay.
A successful command only awaits verification: fresh Lens success, a correlated
passing Evals gate and an independent successful probe determine resolution.
Failed recovery escalates. Production runtime adapters, hosted MCP tenant
credential binding, bulk operations and incident console views remain planned.

## Example and dependency matrix

From a sibling workspace, create a versioned Tower checkout (omit clone if
already present). The example first ships in `v0.6.0`; it is absent from 0.5.x:

```bash
git clone --branch v0.6.0 https://github.com/DeepAgentLabs/agenticops-control-tower.git ../tower-0.6.0
cd ../tower-0.6.0
uv run --with ../agenticlens --with ../agentic-evals python examples/incident_recovery.py
uv run --with ../agenticlens --with ../agentic-evals python examples/incident_recovery.py --fail-verification
make test-ecosystem
```

The two walkthrough outputs are `resolved` and `escalated`. The actual producer
matrix is Lens 0.7.1, Evals 0.7.1, Sidecar 0.8.0 and Chaos 0.5.3; MCP 0.3.6
exposes the real authenticated Tower 0.6.0 API. Native artifact readers do not
require those packages at Tower startup. MCP uses HTTP and does not import Tower.
`ai-operations-spec` 0.5.1 is a repository/catalog release, not an AIOS
schema version. Lens supports AIOS v0.4-draft only; Tower-local incident
contracts make no AIOS conformance claim.

See [the operator guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.6.0/docs/incident-recovery.md)
and [MCP setup](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.6.0/docs/mcp-connector.md)
for API requests, credentials, supported scope and recovery limits.

---

## Historical integration note: Evals 0.11 containment compatibility

Source: [website/docs/evals-0.11-containment.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/evals-0.11-containment.md)

Evals 0.11.0 supplies `ContainmentEvaluator` and the six-scenario
`adversarial-containment` pack. It scores actual dispatch/completion and denial
observations separately from task success. Missing evidence, missing policy or
configuration versions, incomplete coverage and bypassed enforcement fail.

Lens 0.12.0 authenticates the exact ordered snapshot. Coverage remains
producer-declared. Chaos 0.10.0 supplies attacks and native scenario assertions;
Sidecar 0.9.2 owns authority, enforcement and effective stop receipts. MCP 0.6.1
pins Evals 0.11.0 and validates scores against the Phase 6 real-adapter harness.
Already-running calls can complete after acknowledgement and remain separately
reported. A BLOCK decision or safe answer alone cannot pass containment.

Use the [Evals guide and passing/failing example](https://github.com/DeepAgentLabs/agentic-evals/blob/main/docs/containment.md):

From an **agentic-evals v0.11.0 checkout**, run:

```bash
uv run --extra integrity python examples/containment/generate.py
uv run --extra integrity agentic-evals evaluate examples/containment/suite.json \
  examples/containment/passing.samples.json \
  --registry examples.containment.registry:registry --out /tmp/containment.json
uv run agentic-evals gate /tmp/containment.json --config examples/containment/gate.json
```

Run those commands from an Evals checkout. Substitute
`post-stop-dispatch.samples.json` or `incomplete.samples.json` to get a failing
gate. The fixture key is public synthetic test material; production trust keys
and expected scope belong to the host, never the evaluated sample.

Native report/gate schema 1.0 is unchanged. Existing optional ranges remain
sufficient except MCP's exact pin, which requires its 0.6.1 patch release.
Lens 0.12.1 raises its Evals floor to 0.11.0 for the synchronized embedded schema.
Lens 0.12.1 also refreshes embedded Evals schemas/examples and preserves failed live-target trials. Other documentation alignment needs no package release.

Sidecar still enforces dispatch, authority and stop/revoke. Its validation extra already allows Evals 0.11. Copy actual scope, versions and effective receipts into host-bound evidence before sealing; do not synthesize containment from Decision.status.

---

## Historical integration note: Evals 0.12 API and report readiness

Source: [website/docs/evals-0.12.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/evals-0.12.md)

Evals 0.12.0 captures its public root API candidate and current report/gate
schemas in compatibility fixtures, executes all registered offline Python
examples, and publishes its CPython 3.10-3.14 support policy. The downstream
workflow pins Lens 0.12.1, Tower 0.9.1 and MCP 0.6.1 and installs the candidate
distribution over each consumer's locked environment before testing it.

Native report/gate schema 1.0, immutable schema IDs and AIOS `0.4-draft`
exports are unchanged. Existing public imports and compatible dependency ranges
continue to work. No runtime, schema or normative AIOS change is required here.
Scoring and release-gate computation remain Evals-owned; deployment health,
resilience, supervision and artifact conformance retain their own meanings.

The public/private module and deprecation policies are candidate readiness work.
The `agentic-evals>=1.0,<2` matrix and coordinated ecosystem release-candidate
acceptance gates remain open until that launch. No independent stable API or
AIOS conformance is claimed.

For an offline producer example, run in a clean Evals checkout at the released tag:

```bash
git clone --branch v0.12.0 --depth 1 https://github.com/DeepAgentLabs/agentic-evals.git evals-0.12
cd evals-0.12
uv sync --extra dev
uv run python examples/report-contract/generate.py
uv run pytest tests/test_public_api.py tests/test_report_contract.py --no-cov
```

Consumers must preserve a failed `GateDecision.passed` and unknown future fields;
schema validation does not recompute gates. See the
[public API policy](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.12.0/docs/public-api.md),
[support and reproducible matrix](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.12.0/docs/support-policy.md)
and [executable examples](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.12.0/examples/README.md).

---

## Historical integration note: Lens 0.13 readiness compatibility

Source: [website/docs/lens-0.13.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/lens-0.13.md)

Lens 0.13.0 adds an opt-in single-node project artifact service, scoped bearer
roles, atomic local audit, immutable model/prompt metadata registries, mandatory
pattern redaction, trace retention and reproducible Evals release receipts.

The optional Lens extra `>=0.7.1,<1` already admits 0.13.0. Native sidecar.correlation/1 decisions and dispatch evidence stay unchanged. Lens roles govern stored artifacts, never Sidecar runtime authority, approvals or interception.

Evals owns scoring and gate computation; Lens composes the saved native Evals
report and policy into its release receipt.

Native trace, evaluation and integrity contracts retain their existing meanings.
Audit integrity is explicitly not verified; compliance export is not certification.
No new automatic sibling reader or shared conformance claim is introduced.
Independent security/deployment acceptance and the coordinated v1.0 API freeze
remain open. See the [Lens production guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.13.0/docs/production-readiness.md)
and [tested dependency matrix](https://github.com/DeepAgentLabs/agenticlens/blob/v0.13.0/docs/lens-0.13-compatibility.md).

## Operator example

Keep existing native evidence readers and optional integrations. To explore the
new storage workflow independently, in a Lens 0.13 checkout run:

```bash
uv run python examples/enterprise_demo.py
```

It uses only synthetic local data, stores a redacted trace in an isolated SQLite
database and exports project metadata with `certification: not_assessed`. It does
not execute targets, call providers, start a hosted service or alter sibling state.

Existing dependency ranges are sufficient; this compatibility documentation needs no package patch release.

---

## Historical integration note: MCP Phase 6 coordinated containment release

Source: [website/docs/phase6-containment.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/phase6-containment.md)

MCP 0.6.0 pairs with Chaos 0.10.0 and Sidecar 0.9.2. Lens 0.12.0,
Evals 0.10.0, Tower 0.9.0 and AIOS 0.6.1 remain compatible. See the
[MCP operator guide and tested matrix](https://github.com/DeepAgentLabs/mcp-server/blob/c18f73decdc75aaac3e2e95004ae88589d587e75/docs/phase6-containment.md).

MCP binds hosted Tower credentials per authenticated user; tool policies still
apply and approval remains human-only in Tower. The independent operator stop
endpoint binds an exact owner/task to a live Sidecar runtime. Sidecar owns stop
latching, authority and dispatch enforcement. The MCP revoker waits for its
in-flight transaction before acknowledging task-dedicated credential revocation;
queued calls reauthenticate. Running Sidecar calls and unrelated credentials
remain harness-owned. Bind controls to the process hosting the actual runtime.

Chaos supplies native assertions over observed dispatch/completion and effective
acknowledgements, authenticating the exact ordered snapshot through Lens.
Failed, unknown, incomplete or missing evidence cannot pass. Tests include an
actual handler dispatch through a deliberately bypassed authorizer, which must
fail containment assertions despite valid snapshot authentication. Recovery,
output quality and resilience scores are separate. Evals v0.11 reusable
containment scoring ships subsequently in 0.11.0; see
[the updated matrix](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/evals-0.11-containment.md).

MCP retains its native access records and adds `io.deepagentlabs.access`, defined
in the spec-owned exploratory `drafts/access-evidence-v1` profile. No new
normative artifact or version marker is introduced. Coverage is producer-declared;
Lens authentication does not prove exhaustive capture. Tower preserves attributed
native outcomes and deployment health remains separate.

Sidecar 0.9.2 widens optional Chaos dependencies to `<0.11`. Other existing
optional ranges remain sufficient, so no other sibling runtime release is needed.
Hosted arbitrary chaos execution stays disabled. Reproduce the isolated seed-601
acceptance suite from the MCP guide; it requires the actual adapters without skips.

AIOS 0.6.1 denotes the existing Run/schema compatibility baseline. The new
exploratory access profile is in the coordinated spec repository revision,
not the historical v0.6.1 tag. It is not promoted to a normative schema family.

---

## Historical integration note: Tower 0.10 capability contract compatibility

Source: [website/docs/tower-0.10-compatibility.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/tower-0.10-compatibility.md)

Updated 2026-11-04.

Tower 0.10 adds authenticated `GET /contracts/capabilities` and the Python
`ControlTowerAPI.get_capability_contract()` facade. The descriptor publishes
`tower.capabilities.v1` as a candidate, with registration/heartbeat/readback JSON
Schemas, status values and existing merge/replacement semantics. CPython and
Node.js HTTP clients are tested against a live server and durable SQLite
readback. Existing routes and payloads remain compatible.

Sidecar owns runtime supervision and task authority. Tower inventory does not confer authority or prove containment.

## Operator example

Against a running Tower server with a reader token:

```bash
curl --fail -H "Authorization: Bearer $AGENTICOPS_READ_TOKEN" \
  "$AGENTICOPS_API_URL/contracts/capabilities"
```

Expect `contract_version: tower.capabilities.v1` and `maturity: candidate`.
A writer token can also read this route; readers cannot register workers.
Use Tower's [Python and Node examples](https://github.com/DeepAgentLabs/agenticops-control-tower/tree/v0.10.0/examples/runtimes)
for registration through heartbeat/readback. A duplicate registration replaces
the record; heartbeat merges metadata and replaces reported status. Reported
health does not automatically expire or derive from producer outcomes.

## Dependencies and release boundary

No runtime dependency, optional range, native schema or export marker changes
are required in this repository. No package patch release is needed for this
documentation-only compatibility update. Siblings remain optional to Tower.
The candidate is preparation for the coordinated ecosystem v1.0 release;
independent acceptance and stable freezing remain open. See the
[Tower contract and migration policy](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.10.0/docs/capability-contract.md).

---

## Additional ecosystem note: AIOS v0.6 compatibility

Source: [docs/aios-v0.6.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/aios-v0.6.md)

AI Operations Specification repository v0.6.0 delivers the exploratory
[canonical examples and extension model](https://github.com/DeepAgentLabs/ai-operations-spec/tree/v0.6.0/specification/v0.6).
Artifacts still declare `spec_version: "0.4-draft"`; the existing schemas,
conformance rules and compatibility catalog are unchanged. Independent review
remains pending; the repository release does not establish stable conformance.

Native decisions, authority and sidecar.correlation/1 remain Sidecar-local contracts. AIOS v0.6 adds no decision schema or shared authority semantics.

## Dependencies and examples

No runtime dependency floor changes or package patch release is needed for this
documentation alignment. The AIOS layer adds no Python runtime API.

To inspect the canonical artifacts, check out AIOS `v0.6.0`, run
`uv sync --extra dev` and `make check` there, then read
`specification/v0.6/examples/manifest.json`. It distinguishes valid fixtures
from schema-invalid and semantic-invalid controls. These checks need no sibling
package and do not constitute independent implementation evidence.

Producer metadata belongs only in permitted `attributes` or reverse-domain
`extensions` entries; it cannot redefine core vocabulary. Consumers that
re-emit an artifact must preserve unknown extension JSON values. Extension
contract validation is separate from core validation. A namespace does not
certify the payload, safety, authority or successful execution.

---

## Additional ecosystem note: Evals 0.10.0 evaluation evidence

Source: [docs/evals-0.10-aios-evidence.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/evals-0.10-aios-evidence.md)

[Agentic Evals 0.10.0](https://github.com/DeepAgentLabs/agentic-evals/releases/tag/v0.10.0)
exports its native evaluation reports as AI Operations Specification
`0.4-draft` `evaluation` evidence and merges it into an existing Run artifact,
with an `evaluates` link to every Step or object a case is mapped to.

## For Agent Alone vs Agent + Sidecar

- Evals scores what each arm answered. Exporting those scores as AIOS evidence
  does not turn a Sidecar decision into an evaluation. `ALLOW`, `BLOCK` and
  `ESCALATE` records, authority and redacted evidence remain Sidecar's own
  native outputs and are not exported by Evals.
- A case that a supervised agent reported as blocked is scored and exported
  like any other answer. A live case whose target raised because supervision
  stopped it has no observed output. Evals reports it in `unobserved_cases`
  and does not export it as an evaluation of the Run.
- An aligned Run with passing evaluations is not proof of containment. Scoring
  containment from observed dispatch evidence is Evals roadmap v0.11, which
  is still blocked on Sidecar lifecycle and dispatch evidence.

The `validation` extra (`agentic-evals>=0.9,<1`) already admits 0.10.0, and
Sidecar's full test suite passes against it (666 tests). No dependency
change or Sidecar release is needed.
See the [Evals guide](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.10.0/docs/aios-evidence.md).

---

## Additional ecosystem note: Evals 0.8.0 CLI interoperability

Source: [docs/evals-0.8-cli.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/evals-0.8-cli.md)

Evals 0.8.0 provides declarative `evaluate`, `live` and `gate` commands for supplied evaluation observations. Sidecar supervision decisions remain separate from scoring and release gates. Agent Alone versus Agent + Sidecar evidence remains Sidecar v0.9 work; no runtime dependency is added.

```bash
agentic-evals evaluate suite.yaml samples.jsonl --out report.json
agentic-evals gate report.json --config gate.yaml --out gate.json
```

`evaluate`/`live` exit 0 when a report is produced, even if cases fail.
`gate` exits 0 on pass, 1 on failed policy, and 2 on invalid input or usage.
Use Evals 0.8.0 for these commands; see the [CLI guide and CI example](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.8.0/docs/cli.md).

This is compatibility documentation only: no sibling runtime change,
dependency-floor increase or patch release is required.

---

## Additional ecosystem note: Evals 0.9.0 judge reliability and live resilience

Source: [docs/evals-0.9-judge-reliability.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/evals-0.9-judge-reliability.md)

[Agentic Evals 0.9.0](https://github.com/DeepAgentLabs/agentic-evals/releases/tag/v0.9.0) adds judge cost, bounded judge retries with
an explicit *unavailable* outcome, repeated judging with agreement, live-target
retries with per-case `target_status` (`ok`, `timed_out`, `error`), and async
evaluators and targets (`aevaluate_suite`, `arun_live_suite`).

## For Agent Alone vs Agent + Sidecar (Sidecar v0.9)

- `arun_live_suite` awaits `async def` agents, so a supervised async agent can
  be evaluated live without a thread wrapper. Reports keep suite case order and
  match the sync API.
- A Sidecar `BLOCK` or `ESCALATE` that the agent reports as its answer is
  scored like any other output; it is not a target `error`. A target that
  raises because supervision stopped it is recorded as `error` with the
  exception text, so compare those cases deliberately rather than gating them
  away with `max_target_error_cases`.
- Do not retry a supervised refusal into a pass. Retries repeat calls that
  raised or timed out, so a refusal *returned* as output is never retried. A
  refusal *raised* by the enforcing adapters (`SidecarBlockedError`,
  `SidecarSuspendedError`) is retried by the default `retry_on=(Exception,)`.
  Limit retries to transport failures, for example
  `RetryPolicy(max_attempts=3, retry_on=(ConnectionError, TimeoutError))`, and
  read `target_attempts` to see when a retry happened.
- An unavailable LLM judgment never passes and fails the Evals default gate, so
  a judge outage cannot make Agent + Sidecar look safer than it is.

Supervision decisions remain Sidecar evidence, separate from scores and release
gates. Evals scores observations; it does not prove containment. No runtime
dependency or Sidecar release is introduced. See the [Evals guide](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.9.0/docs/judge-reliability.md).

---

## Additional ecosystem note: Evals native contract compatibility

Source: [docs/evals-report-contract.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/evals-report-contract.md)

Agentic Evals 0.7.2 publishes native report (`schema_version: "1.0"`) and
gate-decision JSON Schemas, with offline `report_schema()` and
`gate_decision_schema()` accessors. Contract 1.x evolves additively; readers
should tolerate unknown fields. Sidecar supervision decisions remain separate from evaluation scores. Agent Alone vs Agent + Sidecar and containment evidence remain v0.9 work.

See the [contract, examples and compatibility policy](https://github.com/DeepAgentLabs/agentic-evals/blob/main/docs/report-contract.md). Existing dependency
ranges remain sufficient; using the new accessors directly requires
`agentic-evals>=0.7.2`. This documentation alignment needs no sibling patch release.

Native Evals schema validation does not establish AIOS conformance. These
package-local schemas are separate from the specification's normative object
model and its draft conformance checks.

---

## Additional ecosystem note: Lens routing integration boundary

Source: [docs/lens-0.10-routing.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/lens-0.10-routing.md)

## AgenticLens 0.10.0 routing compatibility

AgenticLens 0.10.0 implements roadmap v0.8: evidence-based runtime model
selection, fail-closed routing constraints, bounded provider failover,
confidence/escalation handoffs, shadow/canary modes and a local routing journal.
The default is advisory; execution uses explicit caller-owned callbacks.
MCP 0.3.12 exposes read-only `lens.routing_decide` and pins hosted Lens 0.10.0.
See the [routing guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.10.0/docs/routing.md)
and [offline example](https://github.com/DeepAgentLabs/agenticlens/blob/v0.10.0/examples/routing_demo.py).

The existing optional `agenticlens>=0.7.1,<1` extra already admits 0.10.0.
Decision Gate policy, authority and human approval remain Sidecar/host-owned;
a Lens route is not a Sidecar ALLOW or approval artifact. A blocked/escalated
route invokes no provider callback. The locked integration CI now tests Lens 0.10.0. No runtime dependency-range
change or Sidecar patch release is required.

---

## Additional ecosystem note: Lens optimization and authority boundaries

Source: [docs/lens-0.11-optimization.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/lens-0.11-optimization.md)

## AgenticLens 0.11.0 optimization compatibility

AgenticLens 0.11.0 implements roadmap v0.9 Optimization Intelligence:
evidence-backed recommendations from recorded traces for prompts (caching,
compression), retrieval (top-k pruning, reranking), memory (summarization,
retention), tools (result caching, non-retryable errors), workflows (redundant
steps, handoffs that add no work) and models (quality-cost trade-offs between
variants). Projected benefit, confidence and quality risk stay separate; an
append-only ledger tracks accepted, rejected, adopted and reverted
recommendations; and adopted changes are evaluated against later traces, with
projected and observed outcomes side by side. Recommendations are advisory.
MCP 0.4.3 exposes read-only `lens.optimization_analyze` and pins hosted Lens
0.11.0. See the [optimization guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.11.0/docs/optimization.md)
and [offline example](https://github.com/DeepAgentLabs/agenticlens/blob/v0.11.0/examples/optimization_demo.py).

The optional `agenticlens>=0.7.1,<1` extra already admits 0.11.0, and the
locked integration CI now tests Lens 0.11.0. A Lens recommendation, or an
`adopted` entry in its local ledger, is not a Sidecar ALLOW or approval; policy
enforcement, authority and human approval remain Sidecar/host-owned. Tools that
declare `side_effects: true` or `idempotent: false` are never recommended for
caching. No runtime range change or Sidecar patch release is required.

---

## Additional ecosystem note: MCP 0.4.0 unified workflows

Source: [docs/mcp-0.4-unified-workflows.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/mcp-0.4-unified-workflows.md)

[MCP 0.4.0](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.4.0) completes Phase 4 with its unified workflows: `core.compare_runs`, a fail-closed `core.release_check`, `core.incident_summary` and `core.export_report`. MCP judges nothing itself; it composes Lens comparisons, the Evals release gate and Chaos run reports. Malformed or failed-call evidence always blocks readiness, and so does missing evidence of a required kind; all three kinds are required by default and `required_evidence` narrows that.

## Scope

- The unified tools gate Lens, Evals and Chaos evidence only.
- MCP exposes Sidecar discovery only; it does not bridge Sidecar runtime controls.

## Still open

Authenticated Tower/Sidecar stop/revoke enforced at MCP dispatch, tool-level
authorization and correlated denial evidence are open MCP Phase 5 (hosted access
control) items, moved there from Phase 4.

## Compatibility

No Sidecar API change, dependency bump or release. Sidecar's `mcp` extra pins the
MCP SDK for its own gateway and is unrelated to `deep-agentic-core-mcp`.

See the [MCP unified workflows guide](https://github.com/DeepAgentLabs/mcp-server/blob/v0.4.0/docs/unified-workflows.md).

---

## Additional ecosystem note: MCP 0.5.0 hosted access control

Source: [docs/mcp-0.5-access-control.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/mcp-0.5-access-control.md)

[MCP 0.5.0](https://github.com/DeepAgentLabs/mcp-server/releases/tag/v0.5.0) completes MCP Phase 5 with hosted access control. Each hosted key can carry allow and deny tool globs, an expiry and a task scope. The server enforces them at dispatch, outside the model: before each hosted handler runs, it re-authenticates the key and reloads its policy. Revocation, a narrower policy or expiry therefore stops queued calls, retries and calls on existing connections. Calls already running finish. Allowed calls log a `dispatch` and a `completion` record. Denied calls instead return and log a `denial` or `revocation_acknowledged` record and never reach the handler. Every record uses the MCP-local `mcp.access-decision.v1` shape, and the records of one call share a `correlation_id`. They are not AIOS artifacts. `core.access_status` reports a key's effective policy, and operators use `deep-agentic-core-mcp-admin` to narrow or revoke a key by user ID.

## What changes for Sidecar

- Nothing in Sidecar's runtime. `sidecar.status` and `sidecar.module_inventory`
  remain discovery tools, and a key's policy can allow or deny them.
- A Sidecar `TaskRuntime` whose `mcp` revoker revokes the task's hosted MCP key
  (for example through Tower's `MCPAccessRevoker`) now also stops calls that are
  queued behind that task's running call. Those calls leave a
  `revocation_acknowledged` record. In-flight calls and downstream credentials
  stay outside complete containment.
- An authenticated MCP-to-Sidecar stop/revoke bridge moves to MCP Phase 6. It
  needs a task-scoped Sidecar runtime control API that MCP can reach.

## Compatibility

No Sidecar API change, dependency bump or release. MCP's hosted pins stay at
`agentic-sidecar==0.9.1`.

See the [MCP hosted access control guide](https://github.com/DeepAgentLabs/mcp-server/blob/v0.5.0/docs/access-control.md).

---

## Additional ecosystem note: MCP 0.7 integration readiness — Sidecar 0.10.1

Source: [docs/mcp-0.7-readiness.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/mcp-0.7-readiness.md)

Sidecar owns pre-action enforcement and native task control receipts. Live MCP controls still require explicit host bindings and independent task-scoped operator authorization. Already-reserved actions can complete; package discovery does not connect a runtime.

MCP 0.7.0 completes its local integration-readiness milestone: read-only
`core.compatibility`, packaged candidate matrix, standalone installed-wheel MCP
protocol acceptance and released sibling matrix validation. It reports
`baseline_match`, `different_version` or `not_installed` for local distribution
metadata. Those observations do not certify imported workspace sources, adapter
readiness, a remote service version or hosted deployment health. Use `core.verify`
for adapter probes and Tower discovery for the configured remote contract.

The acceptance baseline is MCP 0.7.0, MCP Python SDK 2.0.0, Lens 0.13.0,
Chaos 0.11.0, Evals 0.12.0, Sidecar 0.10.1, Tower 0.10.0 and AIOS repository
0.7.0. Optional package boundaries and native schemas are unchanged. Explicit
workspace checkouts may override installed producer sources.

This companion update changes documentation only; it requires no dependency
floor change, runtime patch or sibling package release. Publishing MCP does not
deploy AWS. Coordinated ecosystem v1.0, independent AIOS review and operator
security/deployment acceptance remain open gates.

See [MCP support, acceptance commands, upgrades and rollback](https://github.com/DeepAgentLabs/mcp-server/blob/fcdf635d522acc8103173d2f7ef56539222d04b5/docs/release-readiness.md)
and [the executable diagnostic example](https://github.com/DeepAgentLabs/mcp-server/blob/fcdf635d522acc8103173d2f7ef56539222d04b5/examples/compatibility_check.py):

```bash
# Run from an MCP 0.7 checkout:
uv run python examples/compatibility_check.py
```

---

## Additional ecosystem note: Tower 0.7.0 integration compatibility

Source: [docs/tower-0.7-fleet-operations.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/tower-0.7-fleet-operations.md)

## Control Tower 0.7.0 fleet operations

Tower 0.7.0 adds frozen environment/capability targeting, bulk desired settings,
separate approval, durable per-target results and bounded stop/MCP-revocation
acknowledgement through Python, HTTP and CLI. No fleet atomicity or automatic
rollback/resume is claimed. Timed-out/requested commands need host reconciliation.

Sidecar TaskRuntime owns dispatch blocking; installed issuer revokers own MCP access revocation. Tower uses host-installed SidecarContainmentAdapter instances, with explicit in-flight and downstream credential limits.

Existing optional dependency ranges remain sufficient. No sibling runtime or
native evidence schema changes are required; this documentation alignment needs
no patch release. See the [operator guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.7.0/docs/fleet-operations.md).

Example operator workflow (against a configured Tower server):

```bash
agenticops-control-tower --token "$WRITER_TOKEN" bulk preview fleet.json
agenticops-control-tower --token "$APPROVER_TOKEN" bulk approve BULK_ID
agenticops-control-tower --token "$WRITER_TOKEN" bulk execute BULK_ID
agenticops-control-tower --token "$READER_TOKEN" bulk get BULK_ID
```

Use the exact request and ownership setup in the operator guide. A successful
desired-setting write does not assert runtime application or incident recovery.

---

## Additional ecosystem note: Control Tower 0.8.0 live operations compatibility

Source: [docs/tower-0.8-live-operations.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/tower-0.8-live-operations.md)

Control Tower 0.8.0 adds periodic local detection over pushed telemetry, durable
deduplicated alerts and acknowledgements, attributed lifecycle audit, and a
read-only incident console joining inventory, evidence, findings, approvals,
commands and recovery checks. Fresh native Lens failures can open recovery
incidents; stale heartbeats and stale/missing evidence produce separate warnings.
Detection never executes recovery, and clearing an alert never resolves an incident.

Explicit same-run native decisions join Tower incident evidence. Sidecar retains dispatch enforcement, scoped/private context and runtime approval authority.

The detector uses the latest observation per deployment/producer, with a default
300-second freshness window and 30-second polling interval. It is not lossless
streaming or an external notification service. Same-run correlation stays within
an environment and does not prove causality. Deployment health remains reported;
evidence freshness, integrity and coverage are separate concerns.

No sibling dependency bump, new mandatory import or native artifact change is
needed. This compatibility update is documentation only and needs no patch release.

## Example operator workflow

```bash
agenticops-control-tower --token writer-token alerts evaluate
agenticops-control-tower --token reader-token alerts list --active-only --environment staging
agenticops-control-tower --token reader-token incidents view INCIDENT_ID
```

Use Tower's [operator guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.8.0/docs/live-operations.md)
for rules, authorization, persistence, API/CLI commands and operational limits,
and its [standalone example](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.8.0/examples/live_operations.py)
for detection, deduplication and acknowledgement without optional siblings.

---

## Additional ecosystem note: Control Tower 0.9.0 runbooks compatibility

Source: [docs/tower-0.9-runbooks.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/tower-0.9-runbooks.md)

Control Tower 0.9.0 adds versioned runbooks and recovery workflows. Installed
runbook versions are immutable and declare prerequisites, named string parameters
(each constrained by a pattern, length and optional allowed list) and ordered steps with per-step timeouts, retry limits and optional rollback actions.
Recommendations come only from installed versions. A writer previews an exact
digest, a separate human approves it, and Tower claims each step before
dispatching it to a host-installed connector. Clean failures retry within the step
limit and then run declared rollback actions for completed steps; partial,
timed-out or unknown outcomes stop for reconciliation without replay. A runbook
resolves only after a connector probe, a fresh successful Lens run and a passing
Evals gate for the same run. The supported runtime is a deterministic staging
fixture; production runtime connectors are not included.

Tower owns runbooks, approvals and incident coordination. Lens owns analysis; Evals
owns scoring; Sidecar owns runtime enforcement; Chaos owns resilience testing;
MCP owns tool exposure. AIOS remains the draft shared-semantics authority.

Runbook steps go to host-installed runbook connectors, not to Sidecar. Emergency stop and restart still use Tower's Sidecar containment adapter, and Sidecar keeps owning dispatch blocking and pre-action decisions.

MCP 0.5.1 adds local `tower.runbook*` tools over the new routes; approval stays
human-only. No sibling dependency bump, new mandatory import or native artifact
change is needed here. This compatibility update is documentation only and needs
no patch release.

## Example operator workflow

```bash
agenticops-control-tower --token reader-token runbooks recommend INCIDENT_ID
agenticops-control-tower --token writer-token runbooks preview INCIDENT_ID preview.json
agenticops-control-tower --token approver-token runbooks approval EXECUTION_ID approval.json
agenticops-control-tower --token writer-token runbooks execute EXECUTION_ID execute.json
agenticops-control-tower --token writer-token runbooks verify EXECUTION_ID verify.json
```

Use Tower's [runbook guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.9.0/docs/runbooks.md) for definitions, step outcomes,
authorization, request bodies and limits, and its
[standalone walkthrough](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.9.0/examples/runbook_recovery.py) for recovery,
compensation and escalation without optional siblings.

---

## Additional ecosystem note: Sidecar 0.10 contracts

Source: [docs/v0.10-contracts.md](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/v0.10-contracts.md)

See the [contract and migration guide](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/website/docs/v0.10.md) and
[offline propagation example](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/examples/v0_10_contracts.py).

---

## Source declarations: src/agentic_sidecar/__init__.py

Source: [src/agentic_sidecar/__init__.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/__init__.py)

```python
__all__ = ['AuthorityBinding', 'AuthorityRegistry', 'BoundAgent', 'ContextSpec', 'GuardrailSpec', 'ScopedSystem', 'ScopeLayer', 'EventJournal', 'OperatorServer', 'RuntimeEvent', 'TaskRuntime', 'MockJudge', 'AnthropicJudge', 'ApprovalAction', 'ApprovalResponse', 'AuditRecord', 'BudgetGuardian', 'BudgetResult', 'CausalLink', 'CriticChallenge', 'CriticEvaluator', 'Decision', 'DecisionContext', 'DecisionRationale', 'DecisionStatus', 'DecisionTrigger', 'EscalationHandler', 'EscalationRequest', 'EvaluatorBase', 'EvaluatorResult', 'JudgeEvaluator', 'JudgeProvider', 'OpenAIJudge', 'PlanEvaluator', 'PlanStep', 'RiskLevel', 'Sidecar', 'SidecarBlockedError', 'SidecarSuspendedError', 'StatusNarrative', 'StatusNarrator', 'ToolCallNarrative', '__version__']
```

---

## Source declarations: src/agentic_sidecar/adapters/autogen.py

Source: [src/agentic_sidecar/adapters/autogen.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/adapters/autogen.py)

```python
def attach(sidecar: Sidecar, tools: Sequence[Callable[..., Any]]) -> list[Any]: ...
```

---

## Source declarations: src/agentic_sidecar/adapters/callable.py

Source: [src/agentic_sidecar/adapters/callable.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/adapters/callable.py)

```python
def attach(sidecar: Sidecar, tools: Sequence[F]) -> list[F]: ...
```

---

## Source declarations: src/agentic_sidecar/adapters/crewai.py

Source: [src/agentic_sidecar/adapters/crewai.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/adapters/crewai.py)

```python
def attach(sidecar: Sidecar, tools: Sequence[Callable[..., Any]]) -> list[Any]: ...
```

---

## Source declarations: src/agentic_sidecar/adapters/google_adk.py

Source: [src/agentic_sidecar/adapters/google_adk.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/adapters/google_adk.py)

```python
def attach(sidecar: Sidecar, tools: Sequence[Callable[..., Any]]) -> list[Any]: ...
```

---

## Source declarations: src/agentic_sidecar/adapters/mcp.py

Source: [src/agentic_sidecar/adapters/mcp.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/adapters/mcp.py)

```python
def attach(sidecar: Sidecar, session: Any, tool_names: Sequence[str]) -> list[Callable[..., Any]]: ...
```

---

## Source declarations: src/agentic_sidecar/adapters/openai_agents.py

Source: [src/agentic_sidecar/adapters/openai_agents.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/adapters/openai_agents.py)

```python
def attach(sidecar: Sidecar, tools: Sequence[Callable[..., Any]]) -> list[Any]: ...
```

---

## Source declarations: src/agentic_sidecar/cli/approval.py

Source: [src/agentic_sidecar/cli/approval.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/cli/approval.py)

```python
@dataclass
class CLIApprovalHandler(EscalationHandler):
    console: Console = field(default_factory=Console)
    def handle_escalation(self, request: EscalationRequest) -> ApprovalResponse: ...
```

---

## Source declarations: src/agentic_sidecar/cli/main.py

Source: [src/agentic_sidecar/cli/main.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/cli/main.py)

```python
@app.command()
def approval_demo() -> None: ...
@app.command()
def status(endpoint: str | None=typer.Option(None, '--endpoint', envvar='SIDECAR_ENDPOINT'), follow: bool=typer.Option(False, '--follow', '-f', help='Follow the connected task or standalone snapshot'), json_output: bool=typer.Option(False, '--json', '-j', help='Output as JSON instead of human-readable format'), interval: int=typer.Option(1, '--interval', '-i', help='Refresh interval in seconds (when --follow is enabled)')) -> None: ...
@app.command()
def control(action: str, endpoint: str=typer.Option(..., '--endpoint', envvar='SIDECAR_ENDPOINT')) -> None: ...
@app.command()
def approve(decision_id: str, action: ApprovalAction, endpoint: str=typer.Option(..., '--endpoint', envvar='SIDECAR_ENDPOINT'), intent_file: str | None=typer.Option(None, '--intent-file')) -> None: ...
@app.command()
def version() -> None: ...
@app.command()
def demo() -> None: ...
def main() -> None: ...
```

---

## Source declarations: src/agentic_sidecar/contracts.py

Source: [src/agentic_sidecar/contracts.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/contracts.py)

```python
class IntentContract(_Contract):
    schema_version: Literal['sidecar.intent/1']
    intent: IntentEnvelope
class DecisionContract(_Contract):
    schema_version: Literal['sidecar.decision/1']
    decision: Decision
class AuditContract(_Contract):
    schema_version: Literal['sidecar.audit/1']
    audit: AuditRecord
    @field_validator('audit')
    @classmethod
    def aware_timestamp(cls, value: AuditRecord) -> AuditRecord: ...
class ScopeContract(_Contract):
    schema_version: Literal['sidecar.scope/1']
    system_id: str = Field(min_length=1)
    task_id: str = Field(min_length=1)
    agents: list[str] = Field(min_length=1)
    shared: ScopeLayer = Field(default_factory=ScopeLayer)
    exclusive: dict[str, ScopeLayer] = Field(default_factory=dict)
    def build(self) -> ScopedSystem: ...
class IntentTransfer(_Contract):
    schema_version: Literal['sidecar.transfer/1']
    parent_intent_id: str = Field(min_length=1)
    parent_grant_id: str = Field(min_length=1)
    task_id: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)
    intent: IntentEnvelope
    def receive(self, parent: IntentGuardian, *, agent_id: str) -> IntentGuardian: ...
    @classmethod
    def propose(cls, parent: IntentGuardian, *, agent_id: str, authority: dict[str, bool]) -> IntentTransfer: ...
def contract_schema(kind: str) -> dict[str, Any]: ...
def export_audit(record: AuditRecord) -> dict[str, Any]: ...
```

---

## Source declarations: src/agentic_sidecar/core/context.py

Source: [src/agentic_sidecar/core/context.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/core/context.py)

```python
class IntentSnapshot(BaseModel):
    goal: str
    constraints: dict[str, Any] = Field(default_factory=dict)
class HistoryEntry(BaseModel):
    tool_name: str
    tool_args: dict[str, Any] = Field(default_factory=dict)
    status: DecisionStatus
class DecisionContext(BaseModel):
    tool_name: str
    tool_args: dict[str, Any] = Field(default_factory=dict)
    intent: IntentSnapshot | None = None
    history: list[HistoryEntry] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    boundary: Literal['tool_call', 'plan'] = 'tool_call'
    parent_decision_id: str | None = None
    parent_plan_step: int | None = None
    goal: str = ''
    plan: list[dict[str, Any]] = Field(default_factory=list)
```

---

## Source declarations: src/agentic_sidecar/core/decision.py

Source: [src/agentic_sidecar/core/decision.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/core/decision.py)

```python
class Decision(BaseModel):
    model_config = ConfigDict(frozen=True)
    decision_id: str = Field(default_factory=lambda: str(uuid4()))
    status: DecisionStatus
    risk: RiskLevel | None
    reason: str
    decision_point: str | None = None
    trigger_details: dict[str, Any] | None = None
    escalation_required: bool = False
    causal_link: str | None = None
```

---

## Source declarations: src/agentic_sidecar/core/exceptions.py

Source: [src/agentic_sidecar/core/exceptions.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/core/exceptions.py)

```python
class SidecarBlockedError(RuntimeError):
    def __init__(self, decision: Decision, context: DecisionContext) -> None: ...
class SidecarSuspendedError(RuntimeError):
    def __init__(self, decision: Decision, context: DecisionContext) -> None: ...
```

---

## Source declarations: src/agentic_sidecar/core/operators.py

Source: [src/agentic_sidecar/core/operators.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/core/operators.py)

```python
def compare(actual: Any, op: ArgOp, expected: Any) -> bool: ...
```

---

## Source declarations: src/agentic_sidecar/core/provenance.py

Source: [src/agentic_sidecar/core/provenance.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/core/provenance.py)

```python
@dataclass
class DecisionTrigger():
    boundary_type: str
    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)
@dataclass
class DecisionRationale():
    policy_findings: list[str] = field(default_factory=list)
    risk_findings: list[str] = field(default_factory=list)
    intent_findings: list[str] = field(default_factory=list)
    budget_findings: list[str] = field(default_factory=list)
    reason: str = ''
    def all_findings(self) -> list[str]: ...
@dataclass
class CausalLink():
    parent_decision_id: str | None = None
    parent_plan_step: int | None = None
    correlation_id: str | None = None
@dataclass
class AuditRecord():
    decision_id: str
    timestamp: datetime
    outcome: DecisionOutcome
    trigger: DecisionTrigger
    rationale: DecisionRationale
    causal_link: CausalLink | None = None
    execution_context: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]: ...
```

---

## Source declarations: src/agentic_sidecar/core/sidecar.py

Source: [src/agentic_sidecar/core/sidecar.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/core/sidecar.py)

```python
class Sidecar():
    def __init__(self, *, on_sidecar_failure: SidecarFailureMode, policy: PolicyAdvisor | None=None, risk: RiskEvaluator | None=None, intent: IntentGuardian | None=None, budget: BudgetGuardian | None=None, planner: PlanEvaluator | None=None, critic: CriticEvaluator | None=None, judge: JudgeEvaluator | None=None, escalation_handler: EscalationHandler | None=None, risk_block_threshold: RiskLevel='HIGH', mode: SidecarMode='observe', roles: Sequence[str] | None=None, runtime: TaskRuntime | None=None, mandatory_checks: Sequence[DecisionHook]=(), context_metadata: dict[str, Any] | None=None, mandatory_configuration: dict[str, Any] | None=None) -> None: ...
    def set_intent(self, intent: IntentGuardian | None) -> None: ...
    def before_tool_call(self, func: DecisionHook) -> DecisionHook: ...
    def on_escalation_required(self, func: EscalationHook) -> EscalationHook: ...
    def evaluate(self, context: DecisionContext, *, causal_link: str | None=None) -> Decision: ...
    def evaluate_plan(self, plan: list[dict[str, Any]], *, goal: str='', metadata: dict[str, Any] | None=None) -> Decision: ...
    def enforce(self, context: DecisionContext, decision: Decision) -> Decision: ...
```

---

## Source declarations: src/agentic_sidecar/evaluators/__init__.py

Source: [src/agentic_sidecar/evaluators/__init__.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/evaluators/__init__.py)

```python
__all__ = ['MockJudge', 'EvaluatorBase', 'EvaluatorResult', 'JudgeProvider', 'PlanEvaluator', 'PlanStep', 'CriticEvaluator', 'CriticChallenge', 'JudgeEvaluator', 'OpenAIJudge', 'AnthropicJudge']
```

---

## Source declarations: src/agentic_sidecar/evaluators/base.py

Source: [src/agentic_sidecar/evaluators/base.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/evaluators/base.py)

```python
@dataclass
class EvaluatorResult():
    status: str
    rationale: str
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    latency_ms: float = 0.0
    def to_dict(self) -> dict[str, Any]: ...
class EvaluatorBase(ABC):
    def __init__(self, enabled: bool=True, name: str=''): ...
    @abstractmethod
    def evaluate(self, context: dict[str, Any]) -> EvaluatorResult: ...
    async def evaluate_async(self, context: dict[str, Any]) -> EvaluatorResult: ...
    def on_enabled(self) -> None: ...
    def on_disabled(self) -> None: ...
class JudgeProvider(ABC):
    def __init__(self, model: str=''): ...
    @abstractmethod
    def evaluate(self, question: str, context: dict[str, Any]) -> dict[str, Any]: ...
    async def evaluate_async(self, question: str, context: dict[str, Any]) -> dict[str, Any]: ...
    def cost_tracking_available(self) -> bool: ...
    def validate(self) -> bool: ...
```

---

## Source declarations: src/agentic_sidecar/evaluators/critic.py

Source: [src/agentic_sidecar/evaluators/critic.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/evaluators/critic.py)

```python
@dataclass
class CriticChallenge():
    category: str
    severity: str
    description: str
    evidence: str = ''
    suggestion: str = ''
class CriticEvaluator(EvaluatorBase):
    def __init__(self, enabled: bool=True, threshold: float=0.7): ...
    def evaluate(self, context: dict[str, Any]) -> EvaluatorResult: ...
```

---

## Source declarations: src/agentic_sidecar/evaluators/judge.py

Source: [src/agentic_sidecar/evaluators/judge.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/evaluators/judge.py)

```python
class JudgeEvaluator(EvaluatorBase):
    def __init__(self, provider: JudgeProvider, enabled: bool=True, cost_limit: float | None=0.5, timeout_ms: int=5000, budget: BudgetGuardian | None=None) -> None: ...
    def evaluate(self, context: dict[str, Any]) -> EvaluatorResult: ...
    async def evaluate_async(self, context: dict[str, Any]) -> EvaluatorResult: ...
    def reset_cost(self) -> None: ...
    def get_cost(self) -> float: ...
```

---

## Source declarations: src/agentic_sidecar/evaluators/planner.py

Source: [src/agentic_sidecar/evaluators/planner.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/evaluators/planner.py)

```python
@dataclass
class PlanStep():
    sequence: int
    tool_name: str
    description: str
    arguments: dict[str, Any] | None = None
    rationale: str = ''
class PlanEvaluator(EvaluatorBase):
    def __init__(self, enabled: bool=True, min_confidence: float=0.7): ...
    def evaluate(self, context: dict[str, Any]) -> EvaluatorResult: ...
```

---

## Source declarations: src/agentic_sidecar/evaluators/providers/__init__.py

Source: [src/agentic_sidecar/evaluators/providers/__init__.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/evaluators/providers/__init__.py)

```python
__all__ = ['MockJudge', 'OpenAIJudge', 'AnthropicJudge']
```

---

## Source declarations: src/agentic_sidecar/evaluators/providers/anthropic.py

Source: [src/agentic_sidecar/evaluators/providers/anthropic.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/evaluators/providers/anthropic.py)

```python
class AnthropicJudge(JudgeProvider):
    def __init__(self, model: str, api_key: str='', *, client: Any=None, async_client: Any=None, timeout_ms: int=5000, input_cost_per_million: float | None=None, output_cost_per_million: float | None=None) -> None: ...
    def cost_tracking_available(self) -> bool: ...
    def validate(self) -> bool: ...
    def evaluate(self, question: str, context: dict[str, Any]) -> dict[str, Any]: ...
    async def evaluate_async(self, question: str, context: dict[str, Any]) -> dict[str, Any]: ...
```

---

## Source declarations: src/agentic_sidecar/evaluators/providers/common.py

Source: [src/agentic_sidecar/evaluators/providers/common.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/evaluators/providers/common.py)

```python
def serialize(context: dict[str, Any]) -> str: ...
def result_with_usage(text: str, input_tokens: int, output_tokens: int, input_rate: float | None, output_rate: float | None) -> dict[str, Any]: ...
```

---

## Source declarations: src/agentic_sidecar/evaluators/providers/mock.py

Source: [src/agentic_sidecar/evaluators/providers/mock.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/evaluators/providers/mock.py)

```python
class MockJudge(JudgeProvider):
    def __init__(self, model: str='mock', *, decision: str='ALLOW', reasoning: str='Offline fixture verdict', cost: float=0.0, tokens: int=0) -> None: ...
    def evaluate(self, question: str, context: dict[str, Any]) -> dict[str, Any]: ...
    def cost_tracking_available(self) -> bool: ...
```

---

## Source declarations: src/agentic_sidecar/evaluators/providers/openai.py

Source: [src/agentic_sidecar/evaluators/providers/openai.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/evaluators/providers/openai.py)

```python
class OpenAIJudge(JudgeProvider):
    def __init__(self, model: str, api_key: str='', *, client: Any=None, async_client: Any=None, timeout_ms: int=5000, input_cost_per_million: float | None=None, output_cost_per_million: float | None=None) -> None: ...
    def cost_tracking_available(self) -> bool: ...
    def validate(self) -> bool: ...
    def evaluate(self, question: str, context: dict[str, Any]) -> dict[str, Any]: ...
    async def evaluate_async(self, question: str, context: dict[str, Any]) -> dict[str, Any]: ...
```

---

## Source declarations: src/agentic_sidecar/gate/__init__.py

Source: [src/agentic_sidecar/gate/__init__.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/gate/__init__.py)

```python
__all__ = ['RISK_ORDER', 'ApprovalAction', 'ApprovalResponse', 'BudgetGuardian', 'BudgetResult', 'EscalationHandler', 'EscalationRequest', 'PolicyAdvisor', 'PolicyEffect', 'PolicyResult', 'PolicyRule', 'RiskEvaluator', 'RiskResult', 'RiskRule']
```

---

## Source declarations: src/agentic_sidecar/gate/budget.py

Source: [src/agentic_sidecar/gate/budget.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/gate/budget.py)

```python
@dataclass
class BudgetResult():
    exceeded: bool
    remaining_cost: float
    remaining_tokens: int | None
    reason: str = ''
@dataclass
class BudgetGuardian():
    max_cost: float
    max_tokens: int | None = None
    current_cost: float = field(default=0.0)
    current_tokens: int = field(default=0)
    def record_invocation(self, cost: float, tokens: int | None=None) -> None: ...
    def evaluate(self) -> BudgetResult: ...
    def is_at_capacity(self) -> bool: ...
    def reset(self) -> None: ...
```

---

## Source declarations: src/agentic_sidecar/gate/escalation.py

Source: [src/agentic_sidecar/gate/escalation.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/gate/escalation.py)

```python
class ApprovalAction(str, Enum):
    APPROVE_ONCE = 'approve_once'
    REJECT = 'reject'
    MODIFY_INTENT = 'modify_intent'
    ASK_AGENT_TO_REPLAN = 'ask_agent_to_replan'
    STOP_AGENT = 'stop_agent'
@dataclass
class EscalationRequest():
    decision_id: str
    reason: str
    context: dict[str, Any]
    available_actions: list[ApprovalAction]
@dataclass
class ApprovalResponse():
    decision_id: str
    action: ApprovalAction
    modified_intent: dict[str, Any] | None = None
    explanation: str = ''
@dataclass
class EscalationHandler():
    def handle_escalation(self, request: EscalationRequest) -> ApprovalResponse: ...
```

---

## Source declarations: src/agentic_sidecar/gate/policy.py

Source: [src/agentic_sidecar/gate/policy.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/gate/policy.py)

```python
class PolicyRule(BaseModel):
    tool: str
    effect: PolicyEffect
    reason: str | None = None
class PolicyResult(BaseModel):
    effect: PolicyEffect
    reason: str
    matched_rule: PolicyRule | None = None
class PolicyAdvisor():
    def __init__(self, rules: list[PolicyRule] | None=None, *, default_effect: PolicyEffect='allow') -> None: ...
    @classmethod
    def from_yaml(cls, path: str | Path) -> PolicyAdvisor: ...
    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> PolicyAdvisor: ...
    def evaluate(self, context: DecisionContext) -> PolicyResult: ...
```

---

## Source declarations: src/agentic_sidecar/gate/risk.py

Source: [src/agentic_sidecar/gate/risk.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/gate/risk.py)

```python
class RiskRule(BaseModel):
    tool: str
    risk: RiskLevel
    reason: str | None = None
    arg_name: str | None = None
    arg_op: ArgOp = 'eq'
    arg_value: Any = None
class RiskResult(BaseModel):
    risk: RiskLevel
    reason: str
    matched_rule: RiskRule | None = None
class RiskEvaluator():
    def __init__(self, rules: list[RiskRule] | None=None, *, default_risk: RiskLevel='LOW') -> None: ...
    @classmethod
    def from_yaml(cls, path: str | Path) -> RiskEvaluator: ...
    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> RiskEvaluator: ...
    def evaluate(self, context: DecisionContext) -> RiskResult: ...
```

---

## Source declarations: src/agentic_sidecar/integrations/_aios.py

Source: [src/agentic_sidecar/integrations/_aios.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/integrations/_aios.py)

```python
def timestamp(value: datetime) -> str: ...
def identifier(value: str) -> str: ...
def reference(value: Mapping[str, Any]) -> dict[str, str]: ...
```

---

## Source declarations: src/agentic_sidecar/integrations/agentic_chaos.py

Source: [src/agentic_sidecar/integrations/agentic_chaos.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/integrations/agentic_chaos.py)

```python
def evaluate_recovery(sidecar: Sidecar, event: Mapping[str, Any], *, tool_name: str, arguments: dict[str, Any]) -> Decision: ...
```

---

## Source declarations: src/agentic_sidecar/integrations/agenticlens.py

Source: [src/agentic_sidecar/integrations/agenticlens.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/integrations/agenticlens.py)

```python
def attach_decisions(sidecar: Sidecar, run: Any, *, span_id: str) -> None: ...
```

---

## Source declarations: src/agentic_sidecar/integrations/aios.py

Source: [src/agentic_sidecar/integrations/aios.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/integrations/aios.py)

```python
def export_audit_event(record: AuditRecord, *, target: Mapping[str, Any], created_at: datetime) -> dict[str, Any]: ...
```

---

## Source declarations: src/agentic_sidecar/integrations/correlation.py

Source: [src/agentic_sidecar/integrations/correlation.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/integrations/correlation.py)

```python
class Correlation(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    run_id: str = Field(min_length=1)
    trace_id: str = Field(min_length=1)
    span_id: str = Field(min_length=1)
class CorrelatedDecision(Decision):
    decision_id: str = Field(min_length=1)
class DecisionEvidence(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    contract_version: Literal['sidecar.correlation/1'] = 'sidecar.correlation/1'
    correlation: Correlation
    task_id: str = Field(min_length=1)
    system_id: str | None = None
    agent_id: str | None = None
    source_event_id: str = Field(min_length=1)
    timestamp: datetime
    policy_version: str = Field(min_length=1)
    tool_name: str
    boundary: str
    decision: CorrelatedDecision
    @field_validator('timestamp')
    @classmethod
    def aware_timestamp(cls, value: datetime) -> datetime: ...
def export_decisions(sidecar: Sidecar, correlation: Correlation) -> list[DecisionEvidence]: ...
```

---

## Source declarations: src/agentic_sidecar/intent/__init__.py

Source: [src/agentic_sidecar/intent/__init__.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/intent/__init__.py)

```python
__all__ = ['AuthorityBinding', 'AuthorityRegistry', 'AlignmentFinding', 'AlignmentResult', 'ConstraintBinding', 'IntentEnvelope', 'IntentGuardian', 'Requester', 'evaluate_alignment']
```

---

## Source declarations: src/agentic_sidecar/intent/alignment.py

Source: [src/agentic_sidecar/intent/alignment.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/intent/alignment.py)

```python
class ConstraintBinding(BaseModel):
    constraint: str
    tool: str
    arg_name: str
    op: ArgOp = 'lte'
    severity: Literal['WARN', 'BLOCK'] = 'BLOCK'
    reason: str | None = None
class AlignmentFinding(BaseModel):
    status: Literal['WARN', 'BLOCK']
    reason: str
    constraint: str | None = None
class AlignmentResult(BaseModel):
    status: AlignmentStatus
    reason: str
    findings: list[AlignmentFinding] = Field(default_factory=list)
def evaluate_alignment(context: DecisionContext, envelope: IntentEnvelope, bindings: list[ConstraintBinding] | None=None) -> AlignmentResult: ...
class IntentGuardian():
    def __init__(self, envelope: IntentEnvelope, bindings: list[ConstraintBinding] | None=None, *, authority_bindings: list[AuthorityBinding] | None=None, registry: AuthorityRegistry | None=None, task_id: str='', agent_id: str='', parent_grant: str | None=None) -> None: ...
    def evaluate(self, context: DecisionContext) -> AlignmentResult: ...
    def check_authority(self, context: DecisionContext) -> AlignmentResult: ...
    def revoke(self) -> None: ...
    def delegate(self, *, agent_id: str, authority: dict[str, bool], expires: datetime | None=None) -> IntentGuardian: ...
```

---

## Source declarations: src/agentic_sidecar/intent/authority.py

Source: [src/agentic_sidecar/intent/authority.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/intent/authority.py)

```python
class AuthorityBinding(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    authority: str
    tool: str
class AuthorityRegistry():
    def __init__(self) -> None: ...
    def grant(self, envelope: IntentEnvelope, *, task_id: str, agent_id: str, parent: str | None=None) -> str: ...
    def invalid_reason(self, grant_id: str) -> str | None: ...
    def permits(self, grant_id: str, authority: str) -> bool: ...
    def revoke(self, grant_id: str) -> None: ...
    @contextmanager
    def reservation(self) -> Iterator[None]: ...
```

---

## Source declarations: src/agentic_sidecar/intent/envelope.py

Source: [src/agentic_sidecar/intent/envelope.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/intent/envelope.py)

```python
class Requester(BaseModel):
    type: Literal['human', 'agent', 'system'] = 'human'
    id: str
class IntentEnvelope(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    goal: str
    requested_by: Requester
    constraints: dict[str, Any] = Field(default_factory=dict)
    authority: dict[str, bool] = Field(default_factory=dict)
    expires: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    def is_expired(self, *, now: datetime | None=None) -> bool: ...
    def to_snapshot(self) -> IntentSnapshot: ...
```

---

## Source declarations: src/agentic_sidecar/operations/__init__.py

Source: [src/agentic_sidecar/operations/__init__.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/operations/__init__.py)

```python
__all__ = ['EventJournal', 'RuntimeEvent', 'TaskRuntime']
```

---

## Source declarations: src/agentic_sidecar/operations/client.py

Source: [src/agentic_sidecar/operations/client.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/operations/client.py)

```python
def request(endpoint: str, token: str, route: str, body: dict[str, Any] | None=None) -> Any: ...
```

---

## Source declarations: src/agentic_sidecar/operations/events.py

Source: [src/agentic_sidecar/operations/events.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/operations/events.py)

```python
@dataclass(frozen=True)
class RuntimeEvent():
    sequence: int
    event_id: str
    task_id: str
    timestamp: str
    kind: str
    payload_json: str
    previous_hash: str
    digest: str
    def to_dict(self) -> dict[str, Any]: ...
class EventJournal():
    def __init__(self, task_id: str, path: Path | None=None) -> None: ...
    def append(self, kind: str, payload: dict[str, Any]) -> RuntimeEvent: ...
    def export(self, after: int=0) -> list[dict[str, Any]]: ...
def verify_events(events: list[dict[str, Any]], *, task_id: str) -> None: ...
```

---

## Source declarations: src/agentic_sidecar/operations/runtime.py

Source: [src/agentic_sidecar/operations/runtime.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/operations/runtime.py)

```python
class TaskRuntime(EscalationHandler):
    def __init__(self, task_id: str | None=None, *, journal: EventJournal | None=None, approval_timeout: float=300, revokers: dict[str, Callable[[str], bool]] | None=None) -> None: ...
    def bind(self, sidecar: Sidecar) -> None: ...
    @property
    def stopped(self) -> bool: ...
    @property
    def epoch(self) -> int: ...
    def propose(self, context: DecisionContext) -> None: ...
    def record(self, context: DecisionContext, decision: Decision) -> None: ...
    def authorize(self, context: DecisionContext, decision: Decision) -> None: ...
    @staticmethod
    def context_fingerprint(context: DecisionContext) -> str: ...
    def validate_authorization(self, context: DecisionContext, decision: Decision) -> None: ...
    def consume_intent_approval(self, decision_id: str) -> bool: ...
    def dispatch(self, context: DecisionContext, decision: Decision, *, cancel: Callable[[], None] | None=None) -> str: ...
    def complete(self, invocation_id: str, error: BaseException | None=None) -> None: ...
    def is_running(self, invocation_id: str) -> bool: ...
    def handle_escalation(self, request: EscalationRequest) -> ApprovalResponse: ...
    def approve(self, response: ApprovalResponse, actor: str) -> None: ...
    def replace_intent(self, intent: IntentGuardian | None) -> None: ...
    def modify_intent(self, envelope: dict[str, Any], actor: str) -> None: ...
    def control(self, action: str, actor: str) -> dict[str, Any]: ...
    def snapshot(self) -> dict[str, Any]: ...
```

---

## Source declarations: src/agentic_sidecar/operations/server.py

Source: [src/agentic_sidecar/operations/server.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/operations/server.py)

```python
class OperatorServer(AbstractContextManager['OperatorServer']):
    def __init__(self, runtime: TaskRuntime, *, token: str, actor: str, port: int=0, reader_tokens: dict[str, str] | None=None) -> None: ...
    @property
    def url(self) -> str: ...
```

---

## Source declarations: src/agentic_sidecar/scopes/__init__.py

Source: [src/agentic_sidecar/scopes/__init__.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/scopes/__init__.py)

```python
class ContextSpec(BaseModel):
    model_config = ConfigDict(extra='forbid')
    goal: str = ''
    values: dict[str, Any] = Field(default_factory=dict)
    readers: set[str] = Field(default_factory=set)
    expires: datetime | None = None
    @field_validator('expires')
    @classmethod
    def aware_expiry(cls, value: datetime | None) -> datetime | None: ...
class GuardrailSpec(BaseModel):
    model_config = ConfigDict(extra='forbid')
    rules: list[PolicyRule] = Field(default_factory=list)
    default_effect: PolicyEffect = 'allow'
    constraints: dict[str, Any] = Field(default_factory=dict)
    bindings: list[ConstraintBinding] = Field(default_factory=list)
    def checker(self) -> Callable[[DecisionContext], Decision]: ...
class ScopeLayer(BaseModel):
    model_config = ConfigDict(extra='forbid')
    context: ContextSpec | None = None
    guardrails: GuardrailSpec | None = None
class BoundAgent():
    def __init__(self, sidecar: Sidecar, context: ProtectedContext) -> None: ...
    def context(self, *, reader: str | None=None) -> dict[str, Any]: ...
    def deliver(self, receiver: Callable[[dict[str, Any]], None]) -> None: ...
    def update_context(self, values: dict[str, Any], *, actor: str) -> None: ...
    def revoke_context(self, *, actor: str) -> None: ...
    def evidence(self) -> dict[str, Any]: ...
class ScopedSystem():
    def __init__(self, *, system_id: str, task_id: str, agents: Sequence[str], shared: ScopeLayer | None=None, exclusive: dict[str, ScopeLayer] | None=None) -> None: ...
    def bind(self, agent_id: str, *, on_sidecar_failure: SidecarFailureMode, mode: SidecarMode='govern') -> BoundAgent: ...
```

---

## Source declarations: src/agentic_sidecar/scopes/privacy.py

Source: [src/agentic_sidecar/scopes/privacy.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/scopes/privacy.py)

```python
class ProtectedContext():
    def __init__(self, payload: dict[str, Any], *, owner: str, readers: set[str], expires: datetime | None=None) -> None: ...
    def read(self, reader: str) -> dict[str, Any]: ...
    def update(self, values: dict[str, Any], *, actor: str) -> None: ...
    def revoke(self, *, actor: str) -> None: ...
def redact_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]: ...
```

---

## Source declarations: src/agentic_sidecar/status/__init__.py

Source: [src/agentic_sidecar/status/__init__.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/status/__init__.py)

```python
__all__ = ['StatusNarrative', 'StatusNarrator', 'ToolCallNarrative']
```

---

## Source declarations: src/agentic_sidecar/status/live.py

Source: [src/agentic_sidecar/status/live.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/status/live.py)

```python
def narrate_status(snapshot: dict[str, Any]) -> str: ...
```

---

## Source declarations: src/agentic_sidecar/status/narrate.py

Source: [src/agentic_sidecar/status/narrate.py](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/src/agentic_sidecar/status/narrate.py)

```python
@dataclass
class ToolCallNarrative():
    tool_name: str
    timestamp: datetime
    narrative: str
    arguments: dict[str, Any] = field(default_factory=dict)
    decision: Decision | None = None
    risk_level: RiskLevel | None = None
    intent_compliant: bool = True
@dataclass
class StatusNarrative():
    timestamp: datetime
    current_objective: str | None = None
    current_step: str | None = None
    steps_completed: int = 0
    tool_calls_made: int = 0
    decisions_blocked: int = 0
    decisions_paused: int = 0
    intent_violations: int = 0
    max_risk_seen: RiskLevel | None = None
    current_budget_remaining: float | None = None
    current_tokens_remaining: int | None = None
    last_tool_narrative: ToolCallNarrative | None = None
    is_paused: bool = False
    pause_reason: str | None = None
class StatusNarrator():
    def __init__(self) -> None: ...
    def set_objective(self, objective: str) -> None: ...
    def record_tool_call(self, tool_name: str, arguments: dict[str, Any], decision: Decision | None=None, risk_level: RiskLevel | None=None, intent_compliant: bool=True) -> ToolCallNarrative: ...
    def pause(self, reason: str) -> None: ...
    def resume(self) -> None: ...
    def get_status(self, current_objective: str | None=None, current_budget_remaining: float | None=None, current_tokens_remaining: int | None=None) -> StatusNarrative: ...
    def get_narrative(self) -> str: ...
```

---

## Data contract: schemas/v1/audit.schema.json

Source: [schemas/v1/audit.schema.json](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/schemas/v1/audit.schema.json)

```json
{
  "$defs": {
    "AuditRecord": {
      "description": "Durable audit record of a consequential decision.\n\nCreated when a decision reaches a Decision Gate outcome that's worth\nrecording (PAUSE, ESCALATE, CHALLENGE, REPLAN, BLOCK, or WARN). Exported\nto governance/graph backends (v0.6+) and used by AgenticLens for\nprovenance tracking.\n\nAttributes:\n    decision_id: Unique identifier for this decision.\n    timestamp: When the decision was made.\n    outcome: The Decision.status (ALLOW, WARN, BLOCK, ...).\n    trigger: DecisionTrigger describing the action that prompted it.\n    rationale: DecisionRationale explaining the outcome.\n    causal_link: CausalLink to parent decision or plan step.\n    execution_context: Snapshot of agent state at decision time.",
      "properties": {
        "decision_id": {
          "title": "Decision Id",
          "type": "string"
        },
        "timestamp": {
          "format": "date-time",
          "title": "Timestamp",
          "type": "string"
        },
        "outcome": {
          "enum": [
            "ALLOW",
            "WARN",
            "BLOCK",
            "CHALLENGE",
            "REPLAN",
            "PAUSE",
            "ESCALATE"
          ],
          "title": "Outcome",
          "type": "string"
        },
        "trigger": {
          "$ref": "#/$defs/DecisionTrigger"
        },
        "rationale": {
          "$ref": "#/$defs/DecisionRationale"
        },
        "causal_link": {
          "anyOf": [
            {
              "$ref": "#/$defs/CausalLink"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "execution_context": {
          "additionalProperties": true,
          "title": "Execution Context",
          "type": "object"
        }
      },
      "required": [
        "decision_id",
        "timestamp",
        "outcome",
        "trigger",
        "rationale"
      ],
      "title": "AuditRecord",
      "type": "object"
    },
    "CausalLink": {
      "description": "Links a decision to the prior decision or plan step that caused it.\n\nAttributes:\n    parent_decision_id: ID of the decision that prompted this one (e.g. a\n        CHALLENGE decision prompts a REPLAN).\n    parent_plan_step: Step in the agent's plan that this decision evaluates.\n    correlation_id: Unique identifier tying this decision to execution trace.",
      "properties": {
        "parent_decision_id": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Parent Decision Id"
        },
        "parent_plan_step": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Parent Plan Step"
        },
        "correlation_id": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Correlation Id"
        }
      },
      "title": "CausalLink",
      "type": "object"
    },
    "DecisionRationale": {
      "description": "Explains why the gate reached a particular outcome.\n\nAttributes:\n    policy_findings: Any Policy Advisor matches (permit/deny rules).\n    risk_findings: Risk Evaluator classification and threshold violations.\n    intent_findings: Intent Guardian constraint violations or drift.\n    budget_findings: Budget Guardian violations (cost/token exceeded).\n    reason: Composite human-readable explanation.",
      "properties": {
        "policy_findings": {
          "items": {
            "type": "string"
          },
          "title": "Policy Findings",
          "type": "array"
        },
        "risk_findings": {
          "items": {
            "type": "string"
          },
          "title": "Risk Findings",
          "type": "array"
        },
        "intent_findings": {
          "items": {
            "type": "string"
          },
          "title": "Intent Findings",
          "type": "array"
        },
        "budget_findings": {
          "items": {
            "type": "string"
          },
          "title": "Budget Findings",
          "type": "array"
        },
        "reason": {
          "default": "",
          "title": "Reason",
          "type": "string"
        }
      },
      "title": "DecisionRationale",
      "type": "object"
    },
    "DecisionTrigger": {
      "description": "Details of the action that triggered the decision boundary.\n\nAttributes:\n    boundary_type: 'tool_call' or other decision boundary.\n    tool_name: Name of the tool/MCP server being called.\n    arguments: Arguments passed to the tool.",
      "properties": {
        "boundary_type": {
          "title": "Boundary Type",
          "type": "string"
        },
        "tool_name": {
          "title": "Tool Name",
          "type": "string"
        },
        "arguments": {
          "additionalProperties": true,
          "title": "Arguments",
          "type": "object"
        }
      },
      "required": [
        "boundary_type",
        "tool_name"
      ],
      "title": "DecisionTrigger",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "const": "sidecar.audit/1",
      "title": "Schema Version",
      "type": "string"
    },
    "audit": {
      "$ref": "#/$defs/AuditRecord"
    }
  },
  "required": [
    "schema_version",
    "audit"
  ],
  "title": "AuditContract",
  "type": "object"
}
```

---

## Data contract: schemas/v1/decision.schema.json

Source: [schemas/v1/decision.schema.json](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/schemas/v1/decision.schema.json)

```json
{
  "$defs": {
    "Decision": {
      "description": "The outcome of a single Decision Gate evaluation for one proposed\naction (tool call).\n\n`risk` is `None` only on the `on_sidecar_failure` path (core/sidecar.py)\n-- when the Sidecar itself errored before Policy/Risk ever ran, there is\nno risk classification to report, and reporting one would misrepresent\nwhat actually happened.\n\nv0.4 adds provenance fields for audit trail: `decision_point` (which\nboundary fired), `trigger_details` (tool/action + arguments), and\n`causal_link` (correlation to prior decisions). Escalation outcomes\n(PAUSE, ESCALATE) may populate `escalation_required`.\n\nFrozen: a `Decision` is a record of what was decided, not a value meant\nto be mutated after the fact.",
      "properties": {
        "decision_id": {
          "title": "Decision Id",
          "type": "string"
        },
        "status": {
          "enum": [
            "ALLOW",
            "WARN",
            "BLOCK",
            "CHALLENGE",
            "REPLAN",
            "PAUSE",
            "ESCALATE"
          ],
          "title": "Status",
          "type": "string"
        },
        "risk": {
          "anyOf": [
            {
              "enum": [
                "LOW",
                "MEDIUM",
                "HIGH"
              ],
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "title": "Risk"
        },
        "reason": {
          "title": "Reason",
          "type": "string"
        },
        "decision_point": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Decision Point"
        },
        "trigger_details": {
          "anyOf": [
            {
              "additionalProperties": true,
              "type": "object"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Trigger Details"
        },
        "escalation_required": {
          "default": false,
          "title": "Escalation Required",
          "type": "boolean"
        },
        "causal_link": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Causal Link"
        }
      },
      "required": [
        "status",
        "risk",
        "reason"
      ],
      "title": "Decision",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "const": "sidecar.decision/1",
      "title": "Schema Version",
      "type": "string"
    },
    "decision": {
      "$ref": "#/$defs/Decision"
    }
  },
  "required": [
    "schema_version",
    "decision"
  ],
  "title": "DecisionContract",
  "type": "object"
}
```

---

## Data contract: schemas/v1/intent.schema.json

Source: [schemas/v1/intent.schema.json](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/schemas/v1/intent.schema.json)

```json
{
  "$defs": {
    "IntentEnvelope": {
      "description": "See concept.md §6 for the worked YAML example this mirrors.\n\nConstraints use explicit ConstraintBindings. Optional AuthorityBindings on\nIntentGuardian enforce boolean task grants with expiry and revocation.\nThe envelope alone does not enforce actions. See the v0.9 guide for the\nnative delegation contract and the distinction from policy rules.",
      "properties": {
        "id": {
          "title": "Id",
          "type": "string"
        },
        "goal": {
          "title": "Goal",
          "type": "string"
        },
        "requested_by": {
          "$ref": "#/$defs/Requester"
        },
        "constraints": {
          "additionalProperties": true,
          "title": "Constraints",
          "type": "object"
        },
        "authority": {
          "additionalProperties": {
            "type": "boolean"
          },
          "title": "Authority",
          "type": "object"
        },
        "expires": {
          "anyOf": [
            {
              "format": "date-time",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Expires"
        },
        "metadata": {
          "additionalProperties": true,
          "title": "Metadata",
          "type": "object"
        }
      },
      "required": [
        "goal",
        "requested_by"
      ],
      "title": "IntentEnvelope",
      "type": "object"
    },
    "Requester": {
      "description": "Who asked for this -- concept.md §6's `requested_by: {type, id}`.",
      "properties": {
        "type": {
          "default": "human",
          "enum": [
            "human",
            "agent",
            "system"
          ],
          "title": "Type",
          "type": "string"
        },
        "id": {
          "title": "Id",
          "type": "string"
        }
      },
      "required": [
        "id"
      ],
      "title": "Requester",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "const": "sidecar.intent/1",
      "title": "Schema Version",
      "type": "string"
    },
    "intent": {
      "$ref": "#/$defs/IntentEnvelope"
    }
  },
  "required": [
    "schema_version",
    "intent"
  ],
  "title": "IntentContract",
  "type": "object"
}
```

---

## Data contract: schemas/v1/scope.schema.json

Source: [schemas/v1/scope.schema.json](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/schemas/v1/scope.schema.json)

```json
{
  "$defs": {
    "ConstraintBinding": {
      "description": "Binds one `IntentEnvelope.constraints` entry to a specific tool\nargument so it can be checked deterministically -- a constraint alone\n(e.g. `maximum_refund: 500`) doesn't say which tool call it applies to.\n\nA binding produces a finding when the tool argument does *not* satisfy\n`actual <op> constraint_value`. E.g. `ConstraintBinding(\nconstraint=\"maximum_refund\", tool=\"issue_refund\", arg_name=\"amount\",\nop=\"lte\")` flags any `issue_refund` call whose `amount` exceeds the\nenvelope's `maximum_refund`. A binding for a constraint the active\nenvelope doesn't declare, or a tool call missing the bound argument,\nsimply doesn't match -- same \"no rule matched\" philosophy as\n`gate/policy.py` and `gate/risk.py`.",
      "properties": {
        "constraint": {
          "title": "Constraint",
          "type": "string"
        },
        "tool": {
          "title": "Tool",
          "type": "string"
        },
        "arg_name": {
          "title": "Arg Name",
          "type": "string"
        },
        "op": {
          "default": "lte",
          "enum": [
            "eq",
            "ne",
            "gt",
            "gte",
            "lt",
            "lte",
            "in",
            "contains"
          ],
          "title": "Op",
          "type": "string"
        },
        "severity": {
          "default": "BLOCK",
          "enum": [
            "WARN",
            "BLOCK"
          ],
          "title": "Severity",
          "type": "string"
        },
        "reason": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Reason"
        }
      },
      "required": [
        "constraint",
        "tool",
        "arg_name"
      ],
      "title": "ConstraintBinding",
      "type": "object"
    },
    "ContextSpec": {
      "additionalProperties": false,
      "description": "Agent-visible instructions and structured context, without enforcement.",
      "properties": {
        "goal": {
          "default": "",
          "title": "Goal",
          "type": "string"
        },
        "values": {
          "additionalProperties": true,
          "title": "Values",
          "type": "object"
        },
        "readers": {
          "items": {
            "type": "string"
          },
          "title": "Readers",
          "type": "array",
          "uniqueItems": true
        },
        "expires": {
          "anyOf": [
            {
              "format": "date-time",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Expires"
        }
      },
      "title": "ContextSpec",
      "type": "object"
    },
    "GuardrailSpec": {
      "additionalProperties": false,
      "description": "A deterministic policy and bound constraints, independent of context.",
      "properties": {
        "rules": {
          "items": {
            "$ref": "#/$defs/PolicyRule"
          },
          "title": "Rules",
          "type": "array"
        },
        "default_effect": {
          "default": "allow",
          "enum": [
            "allow",
            "deny"
          ],
          "title": "Default Effect",
          "type": "string"
        },
        "constraints": {
          "additionalProperties": true,
          "title": "Constraints",
          "type": "object"
        },
        "bindings": {
          "items": {
            "$ref": "#/$defs/ConstraintBinding"
          },
          "title": "Bindings",
          "type": "array"
        }
      },
      "title": "GuardrailSpec",
      "type": "object"
    },
    "PolicyRule": {
      "description": "One allow/deny rule. `tool` is an `fnmatch` glob matched against\n`DecisionContext.tool_name` (e.g. `\"delete_*\"`, `\"*\"`). Rules are\nevaluated in order; the first match wins.",
      "properties": {
        "tool": {
          "title": "Tool",
          "type": "string"
        },
        "effect": {
          "enum": [
            "allow",
            "deny"
          ],
          "title": "Effect",
          "type": "string"
        },
        "reason": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Reason"
        }
      },
      "required": [
        "tool",
        "effect"
      ],
      "title": "PolicyRule",
      "type": "object"
    },
    "ScopeLayer": {
      "additionalProperties": false,
      "description": "Context only, guardrails only, or both at a shared/exclusive scope.",
      "properties": {
        "context": {
          "anyOf": [
            {
              "$ref": "#/$defs/ContextSpec"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "guardrails": {
          "anyOf": [
            {
              "$ref": "#/$defs/GuardrailSpec"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "title": "ScopeLayer",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "const": "sidecar.scope/1",
      "title": "Schema Version",
      "type": "string"
    },
    "system_id": {
      "minLength": 1,
      "title": "System Id",
      "type": "string"
    },
    "task_id": {
      "minLength": 1,
      "title": "Task Id",
      "type": "string"
    },
    "agents": {
      "items": {
        "type": "string"
      },
      "minItems": 1,
      "title": "Agents",
      "type": "array"
    },
    "shared": {
      "$ref": "#/$defs/ScopeLayer"
    },
    "exclusive": {
      "additionalProperties": {
        "$ref": "#/$defs/ScopeLayer"
      },
      "title": "Exclusive",
      "type": "object"
    }
  },
  "required": [
    "schema_version",
    "system_id",
    "task_id",
    "agents"
  ],
  "title": "ScopeContract",
  "type": "object"
}
```

---

## Data contract: schemas/v1/transfer.schema.json

Source: [schemas/v1/transfer.schema.json](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/schemas/v1/transfer.schema.json)

```json
{
  "$defs": {
    "IntentEnvelope": {
      "description": "See concept.md §6 for the worked YAML example this mirrors.\n\nConstraints use explicit ConstraintBindings. Optional AuthorityBindings on\nIntentGuardian enforce boolean task grants with expiry and revocation.\nThe envelope alone does not enforce actions. See the v0.9 guide for the\nnative delegation contract and the distinction from policy rules.",
      "properties": {
        "id": {
          "title": "Id",
          "type": "string"
        },
        "goal": {
          "title": "Goal",
          "type": "string"
        },
        "requested_by": {
          "$ref": "#/$defs/Requester"
        },
        "constraints": {
          "additionalProperties": true,
          "title": "Constraints",
          "type": "object"
        },
        "authority": {
          "additionalProperties": {
            "type": "boolean"
          },
          "title": "Authority",
          "type": "object"
        },
        "expires": {
          "anyOf": [
            {
              "format": "date-time",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Expires"
        },
        "metadata": {
          "additionalProperties": true,
          "title": "Metadata",
          "type": "object"
        }
      },
      "required": [
        "goal",
        "requested_by"
      ],
      "title": "IntentEnvelope",
      "type": "object"
    },
    "Requester": {
      "description": "Who asked for this -- concept.md §6's `requested_by: {type, id}`.",
      "properties": {
        "type": {
          "default": "human",
          "enum": [
            "human",
            "agent",
            "system"
          ],
          "title": "Type",
          "type": "string"
        },
        "id": {
          "title": "Id",
          "type": "string"
        }
      },
      "required": [
        "id"
      ],
      "title": "Requester",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "description": "Untrusted proposal until a receiving host checks its live parent grant.\n\nBindings come exclusively from the host's parent guardian. The shared\nregistry is required: disconnected replicas cannot prove revocation state.",
  "properties": {
    "schema_version": {
      "const": "sidecar.transfer/1",
      "title": "Schema Version",
      "type": "string"
    },
    "parent_intent_id": {
      "minLength": 1,
      "title": "Parent Intent Id",
      "type": "string"
    },
    "parent_grant_id": {
      "minLength": 1,
      "title": "Parent Grant Id",
      "type": "string"
    },
    "task_id": {
      "minLength": 1,
      "title": "Task Id",
      "type": "string"
    },
    "agent_id": {
      "minLength": 1,
      "title": "Agent Id",
      "type": "string"
    },
    "intent": {
      "$ref": "#/$defs/IntentEnvelope"
    }
  },
  "required": [
    "schema_version",
    "parent_intent_id",
    "parent_grant_id",
    "task_id",
    "agent_id",
    "intent"
  ],
  "title": "IntentTransfer",
  "type": "object"
}
```
