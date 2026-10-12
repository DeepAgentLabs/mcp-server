# Roadmap

The DeepAgentLabs MCP Server roadmap focuses on expanding the unified MCP
interface across the DeepAgentLabs ecosystem.

## Current Release

**Version:** `0.2.0`  
**Released:** 2026-08-08

## Development Status

| Phase | Status | Focus |
|---|---|---|
| Phase 0 | ✅ Complete | Foundation and project setup |
| Phase 1 | ✅ Complete | Minimal MCP server |
| Phase 2 | ✅ Complete | Session management and diagnostics |
| Phase 3a | 🏗️ In progress | AgenticLens integration |
| Phase 3b | ✅ Complete | Agentic Chaos integration |
| Phase 3d | ✅ Implemented | Agentic Sidecar discovery |
| Phase 3c | 🏗️ In progress | AI Operations Specification conformance |
| Phase 4 | 🚧 Planned | Unified workflows |
| Phase 5 | 🚧 Planned | Publishing and adoption |
| Phase 6 | 🚧 Planned | Operational intelligence |

## Upcoming Work

### Phase 3 — Ecosystem Integrations

- Continue AgenticLens integration and provenance support.
- Expand AI Operations Specification conformance.
- Continue exposing Agentic Sidecar readiness and discovery capabilities.

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