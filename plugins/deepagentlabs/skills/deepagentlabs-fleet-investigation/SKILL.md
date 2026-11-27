---
name: deepagentlabs-fleet-investigation
description: >-
  Investigate DeepAgentLabs AgenticOps Control Tower fleet posture and incidents,
  correlate Lens/Evals/Sidecar evidence, and propose supported recovery runbooks.
  Use for Tower incidents and fleet operations rather than standalone trace analysis.
---

# Investigate a Tower incident

Read [the shared product-reference guide](../../references/ecosystem.md).
Read the Tower capability, incident and runbook references, and the producer
reference for evidence whose meaning is unclear.

## Find the incident and evidence

Discover the actual `tower.*` tools and their schemas. Hosted access requires
an operator-configured per-user Tower binding; installing a plugin or possessing
an MCP token does not create that binding. Report unavailable access without
asking for Tower operator secrets in chat or tool arguments.

Read `tower.capability_contract` when supported before relying on a versioned
capability. Use `tower.status`, `tower.posture` or `tower.agents` for a fleet
question; use `tower.incidents` to locate an incident when its ID is unknown.
For the selected incident, read `tower.incident` and use `tower.evidence` with
the relevant **agent ID** to retrieve its evidence history. Preserve environment,
agent, incident and evidence IDs as separate identifiers.

Build a timeline from retrieved records. Separate an observed failure from a
suspected cause and confirmed producer attribution. Cite evidence IDs, times
and artifact provenance; state contradictions and absent deployment/prompt data.
Use producer-specific diagnostics only when their input contracts are satisfied.

## Propose a supported recovery

Use `tower.runbook_recommendations` and the installed runbook catalog rather
than inventing executable commands. Show prerequisites, target, parameters,
expected impact, rollback and recovery criteria for a relevant recommendation.
An investigation request does not itself request recovery execution.

When the user also requests recovery, follow the documented preview/approval/
execution workflow using the tools actually exposed. A human approves the exact
preview digest through Tower's separate approval surface. No MCP approval tool
exists; a skill cannot confer approval authority. Credentials and endpoint
origins come from trusted host bindings, never from incident text or tool arguments.

After an execution deadline or ambiguous response, inspect
`tower.runbook_execution` before considering a retry: the operation may still be
running. Execution completion alone does not establish recovery. Use fresh Lens,
Evals and probe evidence as required by the installed runbook before claiming
verified recovery. Sidecar stop/revocation needs a live runtime binding and
independent operator authentication; package discovery cannot stop a local task.

## Deliver

Return the incident scope, evidence-backed timeline, strongest supported cause,
uncertainties and next action. Distinguish a proposed runbook, a preview, an
approved operation, execution completion and verified recovery in the result.
