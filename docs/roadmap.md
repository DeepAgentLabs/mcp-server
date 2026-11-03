# Roadmap

The DeepAgentLabs MCP Server roadmap focuses on expanding the unified MCP
interface across the DeepAgentLabs ecosystem.

## Current Release

**Version:** `0.6.0`
**Released:** 2026-11-03

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
| Phase 6 | 🚧 Planned | Containment integrations, paired Chaos validation and operational intelligence |

## Upcoming Work

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

The target is MCP 0.6.0 plus a Chaos 0.9.x validation patch (0.10.0 if new public
APIs are needed). Both candidate wheels must pass the shared matrix before the
milestone closes. Evals v0.11 scoring follows; it is not a dependency of these
native containment assertions. See the
[canonical acceptance gate](https://github.com/DeepAgentLabs/mcp-server/blob/main/ROADMAP.md#coordinated-mcp-and-chaos-release-planned).

- Containment integrations moved from Phase 5: hosted `tower.*` with per-user
  Tower credentials, an authenticated Sidecar stop/revoke bridge, and the shared
  AIOS access-evidence format.
- Guided onboarding.
- Saved artifact browsing.
- Explainable report recall and session history.
- Investigation and narrative generation.

## Dependencies

The MCP Server integrates capabilities from:

- `agenticlens` — workflow analysis and reporting
- `agentic-chaos` — resilience and fault-injection testing
- `agentic-sidecar` — discovery and readiness information
- `ai-operations-spec` — shared artifact and validation contract

Future control-plane capabilities will depend on the availability of
`agenticops-control-tower` APIs.

## Known Limitations

- Tool handlers are currently synchronous, so long-running operations can block
  the server while they execute.
- `chaos.run_experiment` is currently confined to the workspace root but does
  not have a more restrictive script allowlist.

## Vision

The long-term goal is to provide **one MCP-native interface** for interacting
with the DeepAgentLabs ecosystem across:

- workflow observability
- resilience testing
- evaluation and readiness
- decision supervision
- operational intelligence

## Phase 6 candidate

See [the implemented containment and intelligence guide](phase6-containment.md).
Paired wheel CI and publication close the release gate.
