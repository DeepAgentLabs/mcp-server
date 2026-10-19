# Unified workflows (MCP 0.4.0)

MCP 0.4.0 adds four `core.*` tools that combine Lens, Evals and Chaos evidence
into a release decision, an incident view and one exportable report. They judge
nothing themselves:

- comparisons are produced and validated by AgenticLens (`ComparisonReport`)
- evaluation reports are judged by the Agentic Evals release gate, the same
  path as `lens.slo_summary`
- chaos evidence must be a `chaos.run_experiment` result from Agentic Chaos

These tools complete Phase 4. Authenticated stop/revoke, tool-level
authorization and correlated denial evidence are Phase 5 hosted access-control
work; see
[ROADMAP.md](https://github.com/DeepAgentLabs/mcp-server/blob/main/ROADMAP.md).

## Tools

| Tool | What it does | Session |
| --- | --- | --- |
| `core.compare_runs` | Lens baseline/candidate comparison; same behavior as `lens.compare_runs` | Stores runs and the comparison |
| `core.release_check` | Gates comparison, evaluation and chaos evidence; fails closed | Stores the result |
| `core.incident_summary` | Collects regressions, chaos crashes/timeouts, failed cases and blocked gates | Stores the result |
| `core.export_report` | Exports everything the session holds as `mcp.unified-report.v1` | Evidence unchanged; the call is recorded in history |

The workflow steps are also served as `resource://workflows/release-check`,
and the `core.release_check` prompt asks a host to explain every gate.

## Release check

```json
{
  "evaluation_report": { "...": "a native Agentic Evals report" },
  "thresholds": { "min_pass_rate": 0.95, "max_average_latency_ms": 2000 },
  "required_evidence": ["comparison", "evaluation", "chaos"],
  "session_id": "release-42"
}
```

`comparison` and `chaos_report` may be passed explicitly; otherwise the
session's last `core.compare_runs`/`lens.compare_runs` and
`chaos.run_experiment` results are used. `evaluation_report` is always passed
explicitly.

Each gate reports a `status`:

| Status | Meaning | Blocks release |
| --- | --- | --- |
| `passed` | Valid evidence that met every check | No |
| `failed` | Valid evidence with regressions, failed Evals thresholds, a crash or a timeout | Yes |
| `invalid` | Evidence that is not an object, does not match its producer's contract (a chaos report needs every `chaos.run_experiment` field with the right type), or came from a failed call | Yes |
| `missing` | A kind listed in `required_evidence` with nothing supplied or stored | Yes |

`ready` is true only when every gate passed. By default all three kinds are
required; narrow `required_evidence` (for example `["evaluation"]`) when a
release only needs some of them. Evidence that is supplied but not required is
still gated.

`thresholds` takes Evals `GateConfig` fields such as `min_pass_rate`,
`max_failed_cases`, `min_average_score`, `max_average_latency_ms`,
`max_total_cost_usd`, the per-tag/per-metric floors and the judge/live-target
limits. Unknown keys are rejected, because the Evals gate would otherwise
ignore a typo. With no thresholds, the Evals default applies: every case must
pass.

A passing comparison may still carry Lens `sample_size_guidance` (for example
when fewer than five runs per cohort were compared). It appears in the gate's
`observed` values and does not block the release on its own.

## Incident summary

`core.incident_summary` reads the same evidence and the session's last release
check. It reports only failure signals:

- `comparison` / `regression` — regressions in the Lens comparison
- `chaos` / `resilience_failure` — the target crashed or timed out (injected
  fault events alone are not an incident)
- `evaluation` / `failed_cases` — the Evals report has failed cases
- `release_check` / `blocked_release` — the gates that did not pass

`status` is `investigate` with findings or `no_signals` without. With no
evidence at all the call returns `ok: false`.

## Exported report

`core.export_report` returns an MCP-local JSON envelope:

```json
{
  "schema_version": "mcp.unified-report.v1",
  "generator": { "name": "io.github.DeepAgentLabs/deep-agentic-core-mcp", "version": "0.4.0" },
  "session_id": "release-42",
  "workflow": null,
  "analysis": null,
  "comparison": { "...": "..." },
  "chaos": { "...": "..." },
  "release_check": { "...": "..." },
  "incident_summary": { "...": "..." },
  "history": []
}
```

It is not an AI Operations Specification artifact, and its embedded sections
keep their producers' shapes. A shared, spec-owned release evidence artifact
would be defined in `ai-operations-spec` first.

## Local and hosted use

All four tools are available locally and on the hosted server, where state is
scoped to the authenticated user. Hosted HTTP still rejects
`chaos.run_experiment`, so hosted callers pass a locally produced chaos report
as `chaos_report` or leave `chaos` out of `required_evidence`. Lens-backed
gates need `agenticlens` (installed in the hosted image). Without it, the
comparison and evaluation gates report `invalid` instead of passing, and a call
that sets `thresholds` returns `ok: false` because they cannot be checked.

## Example

[`examples/unified_release_check.py`](https://github.com/DeepAgentLabs/mcp-server/blob/main/examples/unified_release_check.py)
runs the whole flow on a local workspace checkout: a missing-evidence check, a
ready check, a latency budget that blocks the release, the incident summary and
the export.
