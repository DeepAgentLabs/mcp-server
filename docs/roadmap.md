# Roadmap

The DeepAgentLabs MCP Server roadmap focuses on expanding the unified MCP
interface across the DeepAgentLabs ecosystem.

## Current Release

**Version:** `0.3.13`
**Released:** 2026-10-18

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
| Phase 4 | 🏗️ In progress | Unified workflows and local Tower connector |
| Phase 5 | 🚧 Planned | Publishing and adoption |
| Phase 6 | 🚧 Planned | Operational intelligence |

## Upcoming Work

### Phase 3 — Ecosystem Integrations

Phase 3 is complete. The MCP server now exposes Lens, Chaos, Sidecar
discovery, AI Operations Spec validation, native Evals artifact validation,
and the local Control Tower connector.

### Phase 4 — Unified Workflows

- Combine observability and resilience workflows.
- Compare baseline and chaos runs.
- Surface incident and readiness evidence through one MCP interface.

### Phase 5 — Publishing and Adoption

- Verify PyPI packaging.
- Publish the package and MCP Registry metadata.
- Add CI for package and registry publishing.

### Phase 6 — Operational Intelligence

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
- `agentic-evals` — native evaluation report and gate schemas
- `agenticops-control-tower` — authenticated local operator and evidence APIs

Future control-plane capabilities will depend on the availability of
`agenticops-control-tower` APIs.

## Known Limitations

- Hosted HTTP requires bearer authentication and shared Redis-backed sessions.
- `chaos.run_experiment` is local-only; remote HTTP transport rejects arbitrary
  script execution.
- Evals validation checks report and gate structure; it does not run suites or
  judges.
- Control Tower approval remains a human-controlled Tower HTTP/CLI workflow.

## Vision

The long-term goal is to provide **one MCP-native interface** for interacting
with the DeepAgentLabs ecosystem across:

- workflow observability
- resilience testing
- evaluation and readiness
- decision supervision
- operational intelligence
