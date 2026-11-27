---
name: deepagentlabs-release-check
description: >-
  Assess an agent application's release readiness from DeepAgentLabs baseline
  comparisons, native Evals reports and Chaos evidence. Use when the user asks
  whether a candidate meets release gates, SLOs or regression thresholds.
  This workflow assesses evidence; it does not publish or deploy a release.
---

# Check agent release readiness

Read [the shared product-reference guide](../../references/ecosystem.md).
Retrieve the MCP unified-workflow documentation and the relevant Lens, Evals
and Chaos contracts before assembling the gate inputs.

## Establish the gate

Identify the candidate, baseline, evaluation report, session ID, required evidence
kinds and thresholds from the user or project configuration. Reuse the session
throughout this check. If thresholds are unspecified, explain the producer's
documented defaults rather than making up an acceptance policy. Missing inputs
can produce a blocked assessment; they do not justify weakening the gate.

`core.release_check` defaults to requiring `comparison`, `evaluation` and `chaos`.
Change `required_evidence` only when the user's intended acceptance policy calls
for a different set. Do not omit a kind merely because the hosted service cannot
generate it. Supplied evidence is gated even when it is not listed as required.

## Assemble producer evidence

Use `core.compare_runs` for supplied baseline and candidate groups, or retrieve
a valid prior Lens comparison from the intended session. Pass a native Evals
report explicitly as `evaluation_report`; a report summary or a model-written
verdict is not a substitute. Use `evals.validate_artifact` for structural checks
when needed, while keeping structural validity distinct from a passing gate.

Use an existing native chaos report, or obtain one through an authorized local
experiment if that is part of the task. Hosted HTTP excludes chaos execution;
pass its report as `chaos_report`. An AIOS export has a different shape from a
native `chaos.run_experiment` result and cannot silently replace it.

Call `core.release_check` using the documented schemas. It composes producer
judgments; do not independently manufacture a passing comparison or Evals decision.

## Report the result

Treat `ok` and `ready` separately. Report readiness only when the tool succeeds
and returns `ready: true`; explain each gate as `passed`, `failed`, `invalid` or
`missing`, using its reasons and observed values. Missing or invalid required
evidence blocks readiness. Preserve sample-size limitations even for a passing gate.

If useful, call `core.incident_summary` for blocked-gate signals and
`core.export_report` for the review artifact. Its `mcp.unified-report.v1` envelope
is MCP-local, not an AIOS conformance certificate. Save an artifact only to a
user-authorized destination. Finish with the candidate, decision, gate evidence
and concrete remaining blockers. A gate result does not authorize deployment.
