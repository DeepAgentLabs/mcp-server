# deep-agentic-core-mcp

`deep-agentic-core-mcp` is the shared MCP server layer for the DeepAgentLabs
ecosystem. It is designed to expose a single MCP interface that combines:

- `agenticlens` style workflow inspection, profiling, and analysis
- `agentic-chaos` style resilience testing and fault-injection workflows

It sits above the **AI Operations Workflow Specification**, exposing a unified
MCP-native control surface over the shared operational model used by the
reference implementations.

The goal is one MCP server, one package, and one registry identity rather than
separate MCP servers for each product surface.

<!-- mcp-name: io.github.DeepAgentLabs/deep-agentic-core-mcp -->

## Idea

This project is the control plane between LLM hosts and the existing Python
libraries:

- `agenticlens` remains the core profiling and analysis engine
- `agentic-chaos` remains the core chaos and resilience engine
- the `AI Operations Workflow Specification` remains the shared data contract
- `deep-agentic-core-mcp` becomes the MCP-native interface that hosts can call

That means MCP clients can connect once and access both observability and chaos
testing capabilities through one server.

## What This Server Should Eventually Do

Planned capability areas:

- profile an agentic workflow and return structured telemetry summaries
- analyze workflow artifacts and surface optimization recommendations
- run controlled chaos experiments against target workflows
- compare normal versus chaos runs
- expose shared resources such as workflow schemas, run metadata, and saved
  reports

## Design Principles

- One MCP identity: publish a single server to the MCP Registry
- Python-first: package and publish through PyPI
- Thin orchestration layer: reuse `agenticlens` and `agentic-chaos` instead of
  re-implementing their logic
- Local-first: work well as a stdio MCP server for developer workflows
- Expandable: leave room for a later remote deployment mode if needed

## Initial Scope

The first milestone is foundation only:

- repository structure
- packaging metadata
- MCP registry metadata
- roadmap and product framing
- minimal server entrypoint and tool layout

The first working implementation can stay intentionally small while the shape of
the tool surface stabilizes.

## Proposed MCP Surface

Possible first tool groups:

- `lens.profile_workflow`
- `lens.analyze_workflow`
- `chaos.run_experiment`
- `chaos.list_faults`
- `core.health`
- `core.version`

These names are placeholders, but the structure matters: one server can expose
multiple tools without needing multiple MCP packages or registry entries.

## Repository Layout

```text
mcp-server/
├── README.md
├── ROADMAP.md
├── pyproject.toml
├── server.json
├── .gitignore
├── docs/
│   └── architecture.md
├── examples/
│   └── sample_workflow.json
├── src/
│   └── deep_agentic_core_mcp/
│       ├── __init__.py
│       ├── server.py
│       ├── config.py
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── registry.py
│       ├── resources/
│       │   ├── __init__.py
│       │   └── catalog.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── tooling.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── registry.py
│       ├── adapters/
│       │   ├── __init__.py
│       │   ├── agentic_chaos.py
│       │   └── agenticlens.py
│       └── tools/
│           ├── __init__.py
│           ├── registry.py
│           ├── chaos.py
│           ├── core.py
│           └── lens.py
└── tests/
    ├── test_imports.py
    └── test_registry.py
```

## MCP-Oriented Structure

This repository should have all of the standard layers we expect for a useful
MCP server:

- `tools/` for callable MCP tools and their registration metadata
- `resources/` for readable assets such as fault catalogs, templates, and
  workflow examples
- `prompts/` for reusable prompt templates exposed through the server
- `schemas/` for typed request and response contracts
- `services/` for shared orchestration logic that keeps tool modules thin
- `adapters/` for integration boundaries to `agenticlens` and
  `agentic-chaos`

The implementation is still early, but the file structure now reflects that
shape so we can add functionality without reshuffling the repo later.

## Packaging and Publishing Model

`deep-agentic-core-mcp` should publish in two layers:

1. Publish the Python package to PyPI.
2. Publish the MCP metadata in `server.json` to the official MCP Registry.

For PyPI-based verification, the `mcp-name` marker above must match the
`name` field in `server.json`.

## Near-Term Build Order

1. Lock the canonical namespace and package metadata.
2. Implement the stdio MCP server entrypoint.
3. Add a minimal `core.health` tool.
4. Add the first `agenticlens` and `agentic-chaos` adapter-backed tools.
5. Add examples and publishable packaging checks.

## Notes

This scaffold assumes the intended GitHub namespace is
`io.github.deepagentlabs/deep-agentic-core-mcp`. If the final publishing
account or org changes, update:

- the `mcp-name` marker in this README
- `server.json`
- any repository URLs in `pyproject.toml`
