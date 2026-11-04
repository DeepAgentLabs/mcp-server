# Phase 6: operational intelligence and containment

MCP 0.6.0 pairs with Chaos 0.10.0. Its new public assertion API requires a minor
Chaos release. Sidecar 0.9.2 widens optional Chaos ranges to `<0.11`; Lens 0.12.0,
Evals 0.10.0, Tower 0.9.0 and AIOS 0.6.1 remain compatible without runtime changes.
Evals v0.11 reusable containment scoring is still the following milestone.

## Hosted Tower credentials

Set the host secret `DEEP_AGENTIC_CORE_MCP_TOWER_BINDINGS` to a JSON object:

```json
{"user-id":{"origin":"https://tower.example","read_token":"SERVER_SECRET","write_token":"OPTIONAL_SEPARATE_SECRET"}}
```

Bindings are selected by the reauthenticated caller's user ID at dispatch and
reloaded on each call. Missing or invalid bindings fail closed without using
local/global Tower credentials. Hosted origins require HTTPS; redirects are
rejected. Each user's Tower tokens must themselves have the correct Tower scope;
never share an administrative Tower token between tenants. MCP allow/deny policy
still applies. Write operations require the separate write credential. Approval
remains human-only in Tower. No URL or credential is accepted as a tool argument.

## Authenticated Sidecar stop/revoke bridge

The embedding host creates a live `TaskRuntime`, binds its Sidecar, installs
`TaskKeyRevoker(owner, task_id, keys, sessions)` at `runtime.revokers['mcp']`, and
passes `SidecarBridge({task_id: TaskBinding(owner, runtime)})` and an independent
`operator_store` to `transport_http.create_app`. See
[the host example](https://github.com/DeepAgentLabs/mcp-server/blob/main/examples/phase6_host.py).

Operator keys have `allow: ['sidecar.stop']` and an exact `task_id`. POST
`/control/tasks/{task_id}/stop` with an operator bearer key; agent keys are refused.
The operator identity must match the host-configured task owner. No model tool
can issue control, choose its owner or approve an operation. Stop continues to
work after the agent key has been revoked, and repeated stop retries revokers.

Sidecar owns the stop latch and pre-action reservation lock. Its native receipt
retains running invocation IDs, cancellation outcomes, epoch, revocations and
audit errors. The bridge returns `acknowledged` only when the native receipt
acknowledges access revocation, the MCP revoker succeeded and audit did not fail.
`acknowledged_at` is recorded after successful MCP revocation; Sidecar's native
`effective_at` remains its earlier latch/control timestamp. A failed revoker or
evidence sink returns `failed`; the emergency latch still
holds. Unknown bindings return `unsupported`. A requested stop is not an ack.

MCP's task-dedicated key must retain that task policy. The revoker checks it under
the same session transaction used by dispatch, waits for in-flight MCP handlers
to leave it, then revokes the user credential. Queued/retried/existing-connection
calls reauthenticate after the transaction lock. External key/policy writes must
use the same `services.remote_sessions.dispatch_transaction` guard. A credential serves one task; a mismatch fails without
revoking a different task. Already-reserved Sidecar calls may complete and cause
side effects after stop; cancellation and unrelated downstream credentials are
harness-owned. This is a host binding, not automatic remote runtime discovery.
Route controls to the actual runtime process. No distributed/fleet atomicity,
rollback, bounded completion time or cancellation guarantee is implied.

## Evidence and native assertions

`mcp.access-decision.v1` remains readable. Its new `io.deepagentlabs.access`
extension follows the spec-owned [exploratory access profile](https://github.com/DeepAgentLabs/ai-operations-spec/tree/main/drafts/access-evidence-v1).
It is not a new normative artifact or AIOS version. Dispatch means reservation
of in-flight work; completion is separate. A per-call native
`revocation_acknowledged` is a rejected dispatch, not global revocation proof.
No key, digest or tool arguments are logged.

`agentic_chaos.containment.assert_contained` verifies the exact ordered snapshot
with Lens before asserting an effective acknowledgement, scope, required denied
attempts and zero subsequent dispatch reservations. It separately reports work
in flight at acknowledgement and later completions. Missing observations,
failed/unknown/incomplete verification, wrong streams, duplicates and bypassed
enforcement fail. Completeness remains producer-declared, and snapshot integrity
does not prove exhaustive runtime capture or make uninstrumented boundaries safe.
The scenario host normalizes native observations into task-scoped envelopes and
preserves the native receipt. A safe answer or BLOCK alone cannot pass.

## Reproduce the acceptance matrix

Seed `601`; synthetic credentials and `policy_bypass` instruction payloads only.
Required tests import actual adapters without `importorskip`. Candidate CI builds
MCP, Chaos and Sidecar wheels, installs Lens and Evals, then runs:

```bash
uv run --no-sync pytest -o pythonpath= tests/test_phase6_containment.py \
  tests/test_access_dispatch.py tests/test_hosted_tower_credentials.py \
  tests/test_intelligence.py
```

The current tested matrix is MCP 0.7.0 / Chaos 0.11.0 / Sidecar 0.10.1 /
Lens 0.13.0 / Evals 0.12.0; native Evals schema 1.0 and AIOS Run 0.4-draft
stay unchanged. See [release readiness](release-readiness.md) for pins and limits. Tests exercise
queued calls and stop concurrency, retries and existing credentials, denied tools,
expiry, delegated authority, cross-user/task controls, evidence/revoker failures
and actual dispatched/completed observations. A deliberately bypassed authorizer
runs a real handler after acknowledgement: the authenticated snapshot must fail.
Remote arbitrary `chaos.run_experiment` remains disabled even with Tower bindings.

## Onboarding, saved artifacts and recall

`core.onboard {}` returns sibling readiness and ordered setup steps without
writing configuration. `core.report_recall {}` lists current saved sessions;
`{"session_id":"example"}` recalls their evidence, recent history and a
deterministic investigation narrative citing stored gate/finding paths. Unknown
inputs stay unknown; this generates no new scoring or containment verdict.
Saved sessions are also listed/read at `resource://sessions/{encoded-session-id}`.
Hosted reads pass through the authorized recall tool and tenant transaction;
a guessed URI cannot read another user's session. Stdio state is process-local;
hosted state uses the configured shared store and existing quotas/history limits.

AIOS 0.6.1 denotes the existing Run/schema compatibility baseline. The new
exploratory access profile is in the coordinated spec repository revision,
not the historical v0.6.1 tag. It is not promoted to a normative schema family.

## Shared Redis dispatch guard

Redis session snapshots use optimistic writes. MCP dispatch and task revocation
therefore also acquire a per-user shared Redis guard. It has no expiry, preventing
a lease from expiring underneath an active handler; acquisition waits at most five
seconds and fails closed if busy or unavailable. A stop may latch but report failed
revocation under contention: retry it after reconciling the in-flight work.
After a worker crash, an operator must reconcile its running invocations before
clearing the orphaned `deep-agentic-core-mcp:dispatch:{owner-sha256}` guard.
Never clear it while an original handler may still run. Memory and PostgreSQL
retain their existing mutex/row-lock transaction boundaries. Custom session
backends must provide equivalent serialization before enabling the live bridge.
