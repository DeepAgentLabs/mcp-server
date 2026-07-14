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
