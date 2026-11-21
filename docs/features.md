# Features

The DeepAgentLabs MCP Server provides a unified MCP interface over several existing DeepAgentLabs capabilities.

See the [complete capability index](developer-guide.md#capability-index), [generated tool catalog](tools.md) and [resource/prompt inventory](resources-and-prompts.md) for the full current surface.

## Capability status

| Capability | Status |
|---|---|
| Core diagnostics | Implemented |
| AgenticLens workflow analysis | Implemented |
| AgenticLens reporting | Implemented |
| Agentic Chaos fault injection | Implemented |
| Agentic Sidecar discovery and explicit operator bridge | Implemented (0.6.0) |
| AI Operations Spec validation | Implemented; bundled offline 0.4/0.6/0.8 draft schema families; workspace catalogs may override |
| Unified release check and incident workflows | Implemented (0.4.0) |

---

## Unified Workflows

The `0.4.0` tools compose existing package capabilities without reimplementing
their engines:

- `core.compare_runs` runs the Lens baseline/candidate comparison and stores it.
- `core.release_check` gates a Lens comparison, an Evals report (judged by the
  Evals release gate) and a chaos report. Missing, malformed or failed-call
  evidence blocks readiness.
- `core.incident_summary` collects only failure signals for investigation.
- `core.export_report` exports the session's evidence as an MCP-local envelope.

See [Unified workflows](unified-workflows.md).

## Candidate compatibility (0.7.0)

`core.compatibility` returns the packaged matrix and installed distribution
observations without importing optional producers or contacting Tower. See
[release readiness](release-readiness.md); matches are not runtime verdicts.

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
