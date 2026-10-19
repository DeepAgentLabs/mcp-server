# Evals 0.9.0 judge reliability and live resilience (MCP 0.3.14)

Agentic Evals 0.9.0 records judge cost, retries, unavailable judgments and
sampling agreement, and reports live-target timeouts and errors per case. The new
fields are optional additions to native report schema `1.0`:

- `summary.judge`: judge scores, unavailable scores and the cases they belong
  to, retries, cost/token/latency totals and agreement
- `summary.live`: answered, retried, timed-out and errored cases
- `cases[].target_status`, `target_attempts` and `target_error`

MCP 0.3.14 bundles the exact Evals 0.9.0 report and gate schemas, so
`evals.validate_artifact` checks these fields too. For example, it rejects a
`target_status` other than `ok`, `timed_out` or `error`, or a negative count.
Validation stays offline and never fetches or accepts caller schemas. Reports
written by Evals 0.7.2 to 0.8.0 still validate, because every new field is optional.

Call it with the saved report, unchanged:
`{"artifact_type": "evaluation_report", "artifact": <report JSON>}`. Gate decisions use
`"artifact_type": "gate_decision"`.


MCP validates structure only. It does not recompute scores or gates, and it does
not turn an unavailable judgment or a timed-out case into a pass. In Evals, the
default gate fails on any unavailable judge score, and `gate.passed` remains the
producer's decision. Lens report tools (`lens.slo_summary`, `lens.audit_report`,
`lens.score_analysis`) accept 0.9.0 reports unchanged. Lens 0.10.0 already reads
the same `judge_*` score metadata keys.

Hosted images now pin `agentic-evals==0.9.0` next to Lens 0.10.0 and Chaos
0.8.0, so the runtime producer matches the bundled schemas. No MCP tool is added
or changed. See the [Evals guide](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.9.0/docs/judge-reliability.md).
