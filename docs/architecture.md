# Architecture

## Overview

`deep-agentic-core-mcp` is intended to be a thin MCP server that orchestrates
existing DeepAgentLabs capabilities instead of re-implementing them.

The package is organized around six layers:

1. `server.py`
   The MCP transport entrypoint and registration boundary.
2. `tools/`
   Host-facing callable operations such as health checks, workflow analysis,
   and chaos experiments.
3. `services/`
   Shared application logic used by tools.
4. `schemas/`
   Request and response models for consistent payloads.
5. `resources/`
   Readable static or generated assets that clients may inspect.
6. `adapters/`
   Bridges into sibling libraries like `agenticlens` and `agentic-chaos`.

## Why This Shape

- Keeps host-facing interfaces stable even if underlying integrations change.
- Prevents tool modules from becoming large orchestration files.
- Makes it easier to expose prompts and resources alongside tools.
- Gives us a clean place to add typed contracts before networked or remote use.

## Remote request flow

`transport_http.py` authenticates each HTTP request, validates its transport
headers, and attaches the trusted user identity and session backend to ASGI
request scope. MCP passes that request to `_on_call_tool`; identity is read there
rather than relying on context inherited by SDK background tasks.

Dispatch opens a tenant transaction in a worker thread. `session_scope` binds
session reads and writes to that snapshot; local stdio calls retain their
process-local store. Redis commits use WATCH/EXEC, return conflicts instead of
losing updates, and enforce per-user expiry and storage quotas. HTTP transport
is stateless, so replicas need shared storage but no MCP session affinity.

## Where cross-project logic lives (Phase 3)

The MCP layer composes sibling behavior and adds identity, routing and labels.
It does not own analysis, artifact mapping or normative rules:

| Capability | Owned by | MCP adds |
|---|---|---|
| Which step a recommendation is about | `agenticlens` recommenders (`step_id`, `evidence`) | `provenance` block: artifact digest, step index, `resolved` check |
| ChaosReport → AIOS Run mapping | `agentic-chaos` (`agentic_chaos.export.to_aios_run`) | Run status from the observed crash/timeout, validation of the export |
| Schema sets per `spec_version`, rule IDs, compatibility rows | `ai-operations-spec` (`conformance-rules.json`, `compatibility.json`) | Routing by marker, labeling issues with rule IDs, MCP resources |
| Which scripts may run | Server operator (environment globs) | Enforcement before `runpy` executes anything |

Every sibling dependency is optional at import time. A missing or older sibling
degrades its fields (`resolved=false`, `aios_export.available=false`,
`catalog_available=false`) rather than failing server boot.
