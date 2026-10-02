# Integrations

The MCP Server provides a unified interface over multiple DeepAgentLabs packages.

## AgenticLens

**Status:** Available

AgenticLens provides workflow inspection, analysis, comparison, reporting, and SLO-related capabilities.

The MCP Server exposes these capabilities through:

- `lens.analyze_workflow`
- `lens.report_summary`
- `lens.compare_runs`
- `lens.slo_summary`
- `lens.audit_report`

The verified local environment reports AgenticLens version `0.5.0`.

## Agentic Chaos

**Status:** Available

Agentic Chaos provides controlled fault-injection and resilience testing.

The MCP Server exposes:

- `chaos.list_faults`
- `chaos.run_experiment`

The verified local environment reports Agentic Chaos version `0.4.0`.

## Agentic Sidecar

**Status:** Experimental / scaffold

The Sidecar package is importable, but its decision runtime is not yet implemented.

The MCP Server exposes:

- `sidecar.status`
- `sidecar.module_inventory`

The verified local environment reports:

- Version: `0.6.0`
- Package status: `scaffold`
- Release stage: `pre-alpha`
- Runtime ready: `false`

## AI Operations Specification

**Status:** Unavailable in the current local environment**

The MCP Server provides:

- `spec.validate_artifact`

However, the required AI Operations Specification v0.4 schema documents were not found in the local development environment.

Therefore, this integration could not be successfully validated locally.

## Integration overview

```text
DeepAgentLabs MCP Server
        |
        +-- AgenticLens
        |
        +-- Agentic Chaos
        |
        +-- Agentic Sidecar
        |
        +-- AI Operations Specification