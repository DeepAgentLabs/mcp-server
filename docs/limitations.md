# Limitations

The current candidate acceptance matrix and upgrade/rollback steps are in
[release readiness](release-readiness.md). Package publication does not deploy
the hosted service or demonstrate production health.

## Optional integrations and draft contracts

The base package runs without sibling packages. `core.health` and `core.verify`
report unavailable adapters as degraded. AIOS validation requires the configured
schema/catalog assets; schemas remain draft. `core.compatibility` reads installed
distribution metadata, which may differ from explicit workspace source imports.
It does not probe the remote Tower server or make a readiness verdict.

## Local chaos execution

`chaos.run_experiment` executes trusted local Python scripts. Workspace confinement
and allow/deny globs do not sandbox script behavior. HTTP always rejects this
tool, including when the legacy remote override is set. A completed experiment
does not prove a fault was observed or a containment boundary held.

## Hosted authority and task control

Per-key policies are checked again at dispatch, including queued calls and
existing sessions. Revocation does not cancel a running call or revoke unrelated
credentials. Hosted Tower tools require explicit per-user bindings. Sidecar task
controls require explicit live runtime bindings and independent operator auth;
package discovery does not connect a task automatically.

Sidecar actions already reserved may complete with side effects. There is no
automatic distributed runtime discovery, fleet atomicity or guaranteed downstream
cancellation. Redis guards fail closed; a worker crash requires operator
reconciliation before clearing an orphaned guard.

## Evidence

Lens snapshot authentication verifies supplied evidence. Coverage remains
producer-declared; uninstrumented paths are not proven safe. MCP access records
and the spec-owned exploratory extension preserve producer attribution. Native
Evals gates, Chaos assertions, Sidecar receipts and Tower deployment health are
distinct. Missing or invalid evidence cannot pass the unified release check.
