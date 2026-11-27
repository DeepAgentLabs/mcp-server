---
name: deepagentlabs-diagnose
description: >-
  Diagnose agent workflows, trace runs, evaluation failures, latency, cost or
  regressions using DeepAgentLabs MCP evidence and AgenticLens. Use for an
  observed run or supplied workflow artifact; use fleet investigation for
  incidents whose primary evidence lives in AgenticOps Control Tower.
---

# Diagnose an agent workflow

Read [the shared product-reference guide](../../references/ecosystem.md).
Use the Lens reference and the MCP tool schemas to determine which artifact
shape the user supplied; workflow artifacts, trace runs and Evals reports are
different inputs. Read the owning producer's reference if conversion is needed.

## Inspect the evidence

Use the user's session ID when supplied. Otherwise select a task-specific ID
before storing analysis, and reuse it for every call in this investigation.
`core.report_recall` can locate prior saved results; `core.session_state`
reports which artifacts exist without returning their full content. Use
`core.export_report` to retrieve the stored artifacts needed for analysis.

Choose the supported tool for the evidence:

- Workflow artifact: `lens.analyze_workflow`, then `lens.report_summary` with
  the same session.
- Trace run: `lens.diagnose_run`; use `lens.optimization_analyze` if optimization
  is requested and the evidence meets that tool's input contract.
- Baseline and candidate run groups: `core.compare_runs` (or `lens.compare_runs`).
- Native Evals report: `lens.score_analysis`, `lens.slo_summary` or
  `lens.audit_report`, according to the requested diagnosis.
- Existing comparison, Evals and chaos evidence: `core.incident_summary` can
  combine failure signals. It does not discover a remote runtime or create
  evidence for missing producers.

Confirm fields against discovered schemas before calling; do not convert an
arbitrary log into a purported producer-native report by inventing missing fields.
Distinguish optional adapter unavailability, denied access and invalid input from
an observed failure of the user's agent. If essential evidence is missing, identify
what is needed and continue only with conclusions supported by the available data.

## Explain the finding

Lead with observed impact and the strongest supported attribution. Cite run,
trace, span, step or finding IDs and returned provenance where available. Separate
observations from hypotheses; preserve contradictions, sample-size guidance,
uncertainty and missing evidence. Keep estimated savings separate from measured
cost or latency, and deterministic scores separate from model-judge scores.

Recommend the smallest useful next action and a way to measure whether it helps.
Run a new experiment or change application behavior only when that work is in the
user's request. Hosted MCP does not execute `chaos.run_experiment`; local trusted
execution is a separate capability. Do not label a trace diagnosis a release
approval or claim that remediation succeeded without a new measurement.
