# AIOS v0.6.1 compatibility

AI Operations Specification repository v0.6.1 adds the first v0.6.x drafts:
[provenance records](https://github.com/DeepAgentLabs/ai-operations-spec/blob/v0.6.1/specification/v0.6/provenance.md)
(`spec_version: "0.6-draft"`, `artifact_type: "provenance"`), a
[portable conformance suite](https://github.com/DeepAgentLabs/ai-operations-spec/tree/v0.6.1/specification/v0.6/conformance-suite)
and naming conventions. Run and Workflow artifacts stay `0.4-draft`, and the
v0.4 schemas and rule catalog are unchanged.

## What MCP 0.4.5 does

- `spec.validate_artifact` passes every `0.4-draft` case of the suite with the
  expected outcome and rule citations (`tests/test_spec_conformance_suite.py`).
- Two fixes came out of running it: a Step whose `ended_at` precedes its
  `started_at` now fails `AIOS-0.4-P04`, and an artifact type the declared
  marker does not publish (for example a provenance record labeled
  `0.4-draft`) is rejected with an `AIOS-0.5-V03` compatibility decision.
- `0.6-draft` is reported by `core.verify` as a published but unchecked
  marker, and provenance records are rejected under `AIOS-0.5-V03`. MCP does
  not validate, resolve or emit provenance records yet; that is future work.

## Dependencies

No runtime dependency changes. From MCP 0.4.6, hosted images pin AIOS v0.6.1
schema assets, so hosted `core.verify` also lists `0.6-draft` under
`published_unchecked_versions`; `0.4-draft` validation is byte-for-byte the
same schemas and rule catalog as before. A
passing suite run is repository-local evidence, not stable conformance or
independent review.
