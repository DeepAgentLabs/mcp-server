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