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
| AI Operations Spec validation | Implemented when schema assets are available |
| Agentic Evals artifact validation | Implemented |
| Control Tower local connector | Implemented with authentication |
| Remote Streamable HTTP MCP | Implemented with bearer authentication |

---

## Agentic Evals

`evals.validate_artifact` validates native Agentic Evals reports and gate
decisions against the published schemas. It is a validation tool, not an Evals
runner: suites, targets, and judges still run through `agentic-evals`.

## Control Tower

The local `tower.*` tools connect to an authenticated Control Tower service for
readiness, evidence, investigation, incident, posture, preview, and approved
recovery operations. Tower approval remains a human-controlled HTTP/CLI flow.

## Local and remote modes

The stdio server is intended for trusted local development and can run local
chaos experiments. The authenticated Streamable HTTP server shares the
analysis surface but disables arbitrary script execution and restricts Tower
operations until per-user credentials are configured.

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
