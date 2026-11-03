# Lens execution evidence

The `lens.execution_verify` tool accepts:

```json
{"bundle": {"artifact": {}, "manifest": {}}, "run_id": "expected-run"}
```

Replace the placeholders with a Lens `ExecutionBundle`. It delegates authenticated
snapshot, AIOS `0.4-draft` conformance and lossless-mapping verification to Lens.
It returns `verification` (including coverage) and `causal_links` containing
producer/action/decision/actor/policy/approval identities for verified evidence.
Raw execution payloads are omitted. `ok` is true only for `verified`; failed,
unknown and incomplete remain distinct and expose no causal links.

Set `DEEP_AGENTIC_CORE_MCP_LENS_TRUST_STORE` on the server to a protected JSON
file mapping key IDs to hex HMAC keys of at least 32 bytes. Without a configured
trusted key, verification is unknown. The request cannot provide keys, a trust
file path, or a precomputed verification result. Trust-store changes are read
on each call. Keep historical keys for the retention period; remove compromised
keys. Never put this file in workflow/session data or a source repository.

The host's configured trust applies to its evidence producers; the authenticated
caller remains responsible for selecting the intended run ID. A valid snapshot
is not proof of every real-world dispatch or producer honesty. Expected manifest
freshness remains the operator's responsibility. Existing hosted key permissions,
revocation checks and session isolation apply to this tool, as to other tools.
No execution, signing, stop/revoke operation or Tower credential path is added.

Requires the Lens execution-verification implementation in Lens 0.12.0. Older Lens installations return unavailable; existing tools keep working.
See [Lens's guide](https://github.com/DeepAgentLabs/agenticlens/blob/main/docs/evidence-verification.md)
for export, replay, canonicalization and the symmetric-key trust model.
