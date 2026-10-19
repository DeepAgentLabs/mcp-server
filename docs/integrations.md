# Integrations

The MCP Server provides a unified interface over multiple DeepAgentLabs packages.

## Phase 4 unified workflows

The `core.compare_runs`, `core.release_check`, `core.incident_summary`, and
`core.export_report` tools compose the existing integrations into one workflow.
They do not replace AgenticLens, Agentic Chaos, Agentic Evals, AI Operations
Spec, Sidecar, or Control Tower logic.

## AgenticLens

**Status:** Available

AgenticLens provides workflow inspection, analysis, comparison, reporting, and SLO-related capabilities.

The MCP Server exposes these capabilities through:

- `lens.analyze_workflow`
- `lens.report_summary`
- `lens.compare_runs`
- `lens.slo_summary`
- `lens.audit_report`

The current compatibility target is AgenticLens `0.10.0`. Optional imports
degrade cleanly when the package is absent or older than the requested feature.

## Agentic Chaos

**Status:** Available

Agentic Chaos provides controlled fault-injection and resilience testing.

The MCP Server exposes:

- `chaos.list_faults`
- `chaos.run_experiment`

The current compatibility target is Agentic Chaos `0.8.0`. MCP uses its
exporter and fault catalog; arbitrary chaos execution remains local-only.

## Agentic Sidecar

**Status:** Experimental / scaffold

The Sidecar package is importable, but its decision runtime is not yet implemented.

The MCP Server exposes:

- `sidecar.status`
- `sidecar.module_inventory`

The verified local environment reports:

- Version: `0.8.5`
- Package status: `scaffold`
- Release stage: `pre-alpha`
- Runtime ready: `false`

## AI Operations Specification

**Status:** Read-only compatibility surface

The MCP Server provides:

- `spec.validate_artifact`

The current compatibility target is AI Operations Specification `0.5.1`; the
MCP package bundles the canonical schemas and uses the sibling package for
optional catalog and conformance integration.

## Integration overview

```mermaid
graph TD
    A[DeepAgentLabs MCP Server] --> B[AgenticLens]
    A --> C[Agentic Chaos]
    A --> D[Agentic Sidecar]
    A --> E[AI Operations Specification]
```
