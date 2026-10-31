# Chaos 0.9 compatibility

## Chaos 0.9.0 interoperability

Chaos 0.9.0 adds:

- resilience probes: `HttpProbe`, `ResponseQualityProbe`, `LatencyProbe` and
  `FunctionProbe` check steady state before chaos, while faults are active and
  after recovery. No fault is injected when a pre-chaos probe fails
- a 0-100 resilience score built from recovery, probe, latency,
  retry-efficiency and cost evidence, with per-fault verdicts. The score is
  inconclusive (`null`) when the evidence is missing
- a local run-history store for score trends, with `max_runs` and
  `max_age_days` retention, and a `--min-score` CI gate
- probes and scoring on chaos workflows, experiment files and the pytest marker

Native event IDs and fault types are unchanged. `ChaosReport.probes`,
`ChaosReport.resilience` and the matching `WorkflowReport` fields are optional
and additive. AIOS exports add a derived `resilience_score` measurement. Probe
results and the score breakdown stay in the `io.deepagentlabs.agentic-chaos`
producer extension.

See the [v0.9 guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.9.0/docs/v0.9.md)
and the [offline demo](https://github.com/DeepAgentLabs/agentic-chaos/blob/v0.9.0/examples/chaos_resilience_demo.py).
The resilience score summarizes the evidence of one chaos run. It is not an
Evals score, a release-gate decision, a deployment health signal or proof of
containment. No new shared schema, automatic adapter or hosted execution
capability is introduced.

MCP 0.4.4 pins the published images to Chaos 0.9.0. `chaos.export_aios_run` passes the `resilience_score` measurement and the producer extension through unchanged, and the existing registry discovers faults. Probes, scoring and history are Python/CLI capabilities, not new MCP tools. Hosted HTTP continues to reject `chaos.run_experiment`, so the hosted service neither executes experiment targets nor calls probe endpoints.
