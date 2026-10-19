# Features

The DeepAgentLabs MCP Server provides a unified MCP interface over several existing DeepAgentLabs capabilities.

## Capability status

| Capability | Status |
|---|---|
| Core diagnostics | Implemented |
| AgenticLens workflow analysis | Implemented |
| AgenticLens reporting | Implemented |
| Agentic Chaos fault injection | Implemented |
| Agentic Sidecar discovery | Experimental |
| AI Operations Spec validation | Experimental / unavailable locally |

---

## Core Diagnostics

## Unified Phase 4 Workflows

The Phase 4 tools compose existing package capabilities without reimplementing
their engines:

- `core.compare_runs` compares baseline and candidate evidence.
- `core.release_check` combines regressions, evaluation thresholds, and chaos
  outcomes into a deterministic readiness result.
- `core.incident_summary` groups comparison, chaos, and evaluation signals for
  investigation.
- `core.export_report` exports the session's accumulated evidence.

These tools treat missing evidence as unresolved rather than silently passing
an incomplete release check.

The core tools provide information about the MCP server itself.

### `core.health`

Returns detailed server health and integration information.

It reports:

- MCP server version
- available integrations
- integration versions
- package readiness
- number of loaded tools
- number of resources
- number of prompts

Example:

```text
core.health
