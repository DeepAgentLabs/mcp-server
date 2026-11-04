# Chaos 0.11 ChaosHub compatibility

MCP 0.6.6 pins Chaos 0.11.0 and Sidecar 0.10.1 in the AWS/Render image recipes. No new hub tool, remote target execution or automatic plugin loading is exposed; hosted chaos.run_experiment remains disabled. Local trusted orchestration retains existing behavior. Publishing does not deploy a running service.

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

See the [ChaosHub guide](https://github.com/DeepAgentLabs/agentic-chaos/blob/main/docs/v0.11.md)
and [offline app](https://github.com/DeepAgentLabs/agentic-chaos/blob/main/examples/chaoshub_app.py).
Coordinated ecosystem v1.0 acceptance remains open.
