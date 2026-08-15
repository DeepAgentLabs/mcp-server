# deep-agentic-core-mcp

`deep-agentic-core-mcp` is the shared MCP server layer for the DeepAgentLabs
ecosystem. It is designed to expose a single MCP interface that combines:

- `agenticlens` style workflow inspection, profiling, and analysis
- `agentic-chaos` style resilience testing and fault-injection workflows
- `agentic-sidecar` style supervision-readiness and module-surface discovery
- future `agenticops-control-tower` style operator-facing control-plane access

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
- `agentic-sidecar` remains the core decision-supervision and governance engine
- `agenticops-control-tower` remains the future operator-facing control plane
- the `AI Operations Workflow Specification` remains the shared data contract
- `deep-agentic-core-mcp` becomes the MCP-native interface that hosts can call

That means MCP clients can connect once and access observability, chaos,
sidecar discovery, and later Control Tower-aligned operations surfaces through
one server.

## What This Server Should Eventually Do

Planned capability areas:

- profile an agentic workflow and return structured telemetry summaries
- analyze workflow artifacts and surface optimization recommendations
- run controlled chaos experiments against target workflows
- expose sidecar readiness and scaffold inventory while the upstream runtime
  is still under construction
- eventually expose Control Tower inventory and operator-facing control
  surfaces once that sibling package ships them
- compare normal versus chaos runs
- expose shared resources such as workflow schemas, run metadata, and saved
  reports

## Design Principles

- One MCP identity: publish a single server to the MCP Registry
- Python-first: package and publish through PyPI
- Thin orchestration layer: reuse `agenticlens`, `agentic-chaos`, and
  `agentic-sidecar` instead of re-implementing their logic
- Local-first: work well as a stdio MCP server for developer workflows —
  this matters because `chaos.run_experiment` executes real code (see
  [SECURITY.md](SECURITY.md)), so this server is meant for trusted,
  local/stdio use, not exposure to untrusted clients
- Expandable: leave room for a later remote deployment mode if needed

## MCP Surface (current, `0.2.0`)

- `core.health` — rich diagnostics: adapter availability/version, loaded
  tool/resource/prompt counts, workspace root, recent successful calls
- `core.version` — server package version
- `core.verify` — checks agenticlens/agentic-chaos/agentic-sidecar/ai-operations-spec
  connectivity and reports readiness
- `core.session_state` — inspect what the active session has accumulated
- `lens.analyze_workflow` — run AgenticLens recommendations against a
  workflow artifact
- `lens.report_summary` — render a Markdown workflow report
- `lens.compare_runs` — compare baseline/candidate trace runs for
  regressions
- `lens.slo_summary` — apply release-gate style SLO thresholds to an
  evaluation report
- `lens.audit_report` — case-by-case evaluation detail, optionally with HTML
- `chaos.list_faults` — list the supported fault types
- `chaos.run_experiment` — run a workspace-sandboxed target script under
  selected faults ([executes real code — see `SECURITY.md`](SECURITY.md))
- `sidecar.status` — report whether `agentic-sidecar` is connected and
  whether its runtime is implemented yet
- `sidecar.module_inventory` — inspect the current scaffolded sidecar
  modules, framework adapters, and integration placeholders
- `spec.validate_artifact` — validate a workflow/run artifact against the AI
  Operations v0.4 draft

Sequential tool calls can share context via an optional `session_id`
argument, backed by an in-memory session store — see `ROADMAP.md` Phase 2.

See [ROADMAP.md](ROADMAP.md) for what's shipped per phase and what's still
open, and [docs/tools.md](docs/tools.md) for full input schemas and
per-tool metadata (generated from `tools/registry.py`, run `make docs` to
refresh it after changing that file).

## Repository Layout

```text
mcp-server/
├── README.md
├── ROADMAP.md
├── pyproject.toml
├── server.json
├── .gitignore
├── docs/
│   ├── architecture.md
│   └── tools.md          # generated - see scripts/generate_tools_doc.py
├── examples/
│   ├── sample_workflow.json
│   └── chaos_target.py
├── scripts/
│   └── generate_tools_doc.py
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
│       │   ├── registry.py
│       │   └── session.py
│       ├── adapters/
│       │   ├── __init__.py
│       │   ├── agentic_chaos.py
│       │   ├── agenticlens.py
│       │   ├── agentic_sidecar.py
│       │   └── ai_operations_spec.py
│       └── tools/
│           ├── __init__.py
│           ├── registry.py
│           ├── chaos.py
│           ├── core.py
│           ├── lens.py
│           ├── sidecar.py
│           └── spec.py
└── tests/
    ├── test_degraded_boot.py
    ├── test_imports.py
    ├── test_registry.py
    ├── test_server.py
    └── test_session.py
```

## MCP-Oriented Structure

This repository should have all of the standard layers we expect for a useful
MCP server:

- `tools/` for callable MCP tools and their registration metadata
- `resources/` for readable assets such as fault catalogs, templates, and
  workflow examples
- `prompts/` for reusable prompt templates exposed through the server
- `schemas/` for typed request and response contracts
- `services/` for shared orchestration logic that keeps tool modules thin,
  including the in-memory session store (`services/session.py`)
- `adapters/` for integration boundaries to `agenticlens`, `agentic-chaos`,
  `agentic-sidecar`, and `ai-operations-spec` — each degrades to
  `"available": false` rather than crashing server boot if its sibling repo is
  missing

## Packaging and Publishing Model

`deep-agentic-core-mcp` should publish in two layers:

1. Publish the Python package to PyPI.
2. Publish the MCP metadata in `server.json` to the official MCP Registry.

For PyPI-based verification, the `mcp-name` marker above must match the
`name` field in `server.json`.

## What's Next

Phase 2 (session management, rich diagnostics, tool annotations, prompt
registry, `core.verify`) and Phase 3b (Agentic Chaos) are complete as of
`0.2.0`. What's still open (see [ROADMAP.md](ROADMAP.md) for full detail):

- **Phase 3a (AgenticLens)** — provenance verification on
  `lens.analyze_workflow`'s response shape
- **Phase 3d (Agentic Sidecar Discovery)** — now implemented in the current
  development line; richer sidecar control surfaces still depend on upstream
  runtime milestones landing first
- **Phase 3c (AI Operations Specification)** — multi-version schema support
  and conformance-style reporting, both blocked on upstream `ai-operations-spec`
  work landing first
- **Phase 4 (Unified Workflows)** — joined observability + chaos workflows,
  incident/readiness reporting, a higher-level control surface
- **Future Control Tower coordination** — once `agenticops-control-tower`
  ships real control-plane APIs, MCP should expose those operator-facing
  surfaces without reimplementing them here
- **Phase 5/6** — PyPI + MCP Registry publishing, operational intelligence
  features

## Development

A `Makefile` provides shorthand for common tasks:

```bash
make install     # install dev dependencies
make check       # run all quality gates (lint + format + typecheck + test)
make test-cov    # tests with coverage report
make docs        # regenerate docs/tools.md from tools/registry.py
make docs-check  # fail if docs/tools.md is out of date
make help        # list all available targets
```

## Notes

This scaffold assumes the intended GitHub namespace is
`io.github.deepagentlabs/deep-agentic-core-mcp`. If the final publishing
account or org changes, update:

- the `mcp-name` marker in this README
- `server.json`
- any repository URLs in `pyproject.toml`
