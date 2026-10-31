# Evals 0.10.0 evaluation evidence (MCP 0.4.2)

[Agentic Evals 0.10.0](https://github.com/DeepAgentLabs/agentic-evals/releases/tag/v0.10.0)
exports native evaluation reports as AI Operations Specification `0.4-draft`
`evaluation` evidence (`to_aios_evidence`) and merges it into an existing Run
(`attach_aios_evidence`, or `agentic-evals aios export`). This is the Evals
roadmap item that names `spec.validate_artifact` as its validator.

## Validating an export

Pass the merged Run to `spec.validate_artifact` unchanged:

```json
{"name": "spec.validate_artifact", "arguments": {"artifact": {"spec_version": "0.4-draft", "artifact_type": "run", "...": "..."}}}
```

A Run with Evals evidence attached reports `conformance.aligned = true`, with
`AIOS-0.4-P08` (every evaluation has an `evaluates` target) passing. This
holds for the Evals example and for a Chaos 0.8.0 `to_aios_run` Run with
Evals evidence attached. `tests/test_evals_aios_evidence.py` checks it
against the installed Evals, and the orphaned-evaluation negative control
is cited as `P08`.

Alignment is structural. A failed evaluation or a failed `release_gate`
evaluation stays failed in an aligned Run. Use `core.release_check` or
`evals.validate_artifact` on the native gate decision for readiness.

## What changes in MCP

- Hosted images and the development dependency pin `agentic-evals==0.10.0`.
- `evals.validate_artifact` is unchanged. Evals 0.10.0 ships the same native
  report and gate schema documents (`$id` at `v0.9.0`) that MCP bundles, so no
  schema sync is needed.
- No new MCP tool. Exporting stays in the Evals package and CLI, and MCP only
  validates.

See the [Evals guide](https://github.com/DeepAgentLabs/agentic-evals/blob/v0.10.0/docs/aios-evidence.md).
