# Roadmap

The DeepAgentLabs MCP Server roadmap focuses on expanding the unified MCP
interface across the DeepAgentLabs ecosystem.

## Current Release

**Version:** `0.7.0`
**Released:** 2026-11-04

## Development Status

| Phase | Status | Focus |
|---|---|---|
| Phase 0 | ✅ Complete | Foundation and project setup |
| Phase 1 | ✅ Complete | Minimal MCP server |
| Phase 2 | ✅ Complete | Session management and diagnostics |
| Phase 3a | ✅ Complete | AgenticLens integration |
| Phase 3b | ✅ Complete | Agentic Chaos integration |
| Phase 3d | ✅ Implemented | Agentic Sidecar discovery |
| Phase 3c | ✅ Complete | AI Operations Specification conformance |
| Phase 4 | ✅ Complete | Unified workflows |
| Phase 5 | ✅ Complete | Publishing, adoption and hosted access control (`0.5.0`) |
| Phase 6 | ✅ Complete | Task-scoped containment, paired Chaos validation and operational intelligence (`0.6.0`) |

## v0.7 integration readiness — complete

Packaged candidate compatibility baseline and `core.compatibility`, released
sibling CI alignment, standalone installed-wheel protocol acceptance, support
policy, onboarding/session/prompt examples and upgrade/rollback documentation.
See [the tested matrix and remaining gates](release-readiness.md).

The coordinated v1.0 release remains gated on each project's readiness,
independent AIOS review and operator security/deployment acceptance.

## Delivered Milestones

### Phase 3 — Ecosystem Integrations

Phase 3 is complete. The current MCP surface includes Lens, Chaos, Sidecar
discovery, AI Operations Spec validation, native Evals validation, and local
Control Tower connector tools.

### Phase 4 — Unified Workflows

Complete. Delivered in `0.4.0`:

- `core.compare_runs`, a fail-closed `core.release_check`,
  `core.incident_summary` and `core.export_report`
  ([guide](unified-workflows.md)).
- Local Control Tower connector tools (since `0.3.6`).

Access-containment items moved to Phase 5 on 2026-10-19.

### Phase 5 — Publishing and Adoption

- ~~PyPI packaging, publishing and MCP Registry metadata with release CI~~ ✅
- ~~Hosted access control (moved from Phase 4)~~ ✅ `0.5.0`: tool-level
  permissions per key (allow/deny, expiry, task scope), revocation and policy
  re-checked at dispatch, correlated `mcp.access-decision.v1` evidence,
  `core.access_status` and the `deep-agentic-core-mcp-admin` operator path
  ([guide](access-control.md)).

### Phase 6 — Operational Intelligence

Phase 6 is a coordinated MCP/Chaos delivery: the Sidecar stop/revoke bridge
must ship alongside a Chaos sibling release validating actual enforcement.
Require zero forbidden dispatches after effective acknowledgement, including
queues/retries/existing sessions; report in-flight effects separately. A bypassed
negative control must fail, and missing or unverified evidence cannot pass.
Run real adapters in CI on isolated targets with synthetic credentials.

The release pairing is MCP 0.6.0, Chaos 0.10.0 and Sidecar 0.9.2, with
Lens 0.12.0 snapshot authentication. Required CI validates the candidate wheels
with actual enforcing adapters and publishes seed-601 observations. Evals reusable containment scoring shipped in MCP 0.6.1; the 0.7 matrix tests
Evals 0.12.0 alongside the native Chaos assertions.
See the [operator guide and limits](phase6-containment.md).

Delivered in 0.6.0:

- Hosted `tower.*` with per-user credentials and dispatch authorization.
- Independently authorized task-scoped Sidecar stop/revoke and a spec-owned
  exploratory access extension; no new normative AIOS artifact is claimed.
- `core.onboard` guided setup and `core.report_recall` source-cited recall.
- Tenant-scoped saved-artifact resources, session history and deterministic
  report/investigation narratives from stored producer findings.

## Dependencies

The MCP Server integrates capabilities from:

- `agenticlens` — workflow analysis and reporting
- `agentic-chaos` — resilience and fault-injection testing
- `agentic-sidecar` — discovery and explicit live host-bound stop/revoke
- `ai-operations-spec` — shared artifact and validation contract

`agenticops-control-tower` supplies the authenticated control-plane APIs;
`agentic-evals` owns native evaluation and gate semantics.

## Known Limitations

- Hosted arbitrary chaos execution remains disabled; local scripts are trusted
  and constrained by workspace and script policy, not a sandbox.
- Sidecar reservations already in flight may complete and cause side effects.
  Downstream cancellation and unrelated credentials remain harness-owned.
- Live runtime bindings are explicit; no automatic distributed runtime discovery
  or fleet atomicity is claimed.
- Redis guards fail closed and require operator reconciliation after worker crashes.
- Evidence completeness remains producer-declared; authenticated snapshots do not
  prove exhaustive observation or containment of uninstrumented paths.

## Vision

The long-term goal is to provide **one MCP-native interface** for interacting
with the DeepAgentLabs ecosystem across:

- workflow observability
- resilience testing
- evaluation and readiness
- decision supervision
- operational intelligence

## Phase 6 acceptance

See [the implemented containment and intelligence guide](phase6-containment.md).
Paired wheel CI and publication close the release gate.
