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

## Bundled product documentation

The seven product references are commit-pinned snapshots. Their versions can
differ from the producer packages installed in the server environment, and they
change only when a new MCP release refreshes them. `core.docs_search` is literal,
case-insensitive term matching, not semantic search: an empty result is not proof
that a feature is absent. Documentation tools read text only; they never run
product code or fetch newer documentation over the network.

## Lens analysis and recommendations

Lens tools read the artifacts you supply. `lens.modelfit_recommend`,
`lens.routing_decide` and `lens.optimization_analyze` compose recorded evidence
and do not call provider models or adopt a recommendation. `lens.execution_verify`
needs a host-configured trust store; callers cannot supply keys or verdicts.

## Prompts and resources

Prompt templates return text for the host to use. They do not run tools, fill in
missing analysis or grant approval. Resource URIs are references, not artifacts:
read the resource and pass its content to a tool.

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

## Hosted sessions and keys

Each user is limited to 100 sessions and 4 MiB of serialized state, with a
one-hour idle TTL; save results you need to keep. Rate and concurrency counters
are per worker, so add a hosting-layer limit for fleet-wide caps. Signup keys are
shown once and cannot be recovered, and display names are unverified labels.
`/healthz` checks storage readiness, not every optional adapter.

## Evidence

Lens snapshot authentication verifies supplied evidence. Coverage remains
producer-declared; uninstrumented paths are not proven safe. MCP access records
and the spec-owned exploratory extension preserve producer attribution. Native
Evals gates, Chaos assertions, Sidecar receipts and Tower deployment health are
distinct. Missing or invalid evidence cannot pass the unified release check.
