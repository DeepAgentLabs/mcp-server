# DeepAgentLabs MCP Server

## Unified MCP interface for agentic workflows

**Version:** 0.2.0  
**Maturity:** Alpha

`deep-agentic-core-mcp` is the shared MCP server layer for the DeepAgentLabs ecosystem. It provides one MCP interface for workflow analysis, resilience testing, server diagnostics, and supervision-readiness discovery.

## What it does

The MCP server brings multiple agentic capabilities together behind a single MCP interface:

- **AgenticLens** — workflow inspection, profiling, analysis, and reporting
- **Agentic Chaos** — controlled fault-injection and resilience experiments
- **Agentic Sidecar** — supervision-readiness and module discovery
- **Core diagnostics** — health, version, verification, and session information

## Key capabilities

### Workflow analysis

Analyze agentic workflow artifacts and inspect metrics such as:

- workflow steps
- token usage
- latency
- cost
- chaos events
- recommendations

### Workflow reports

Generate Markdown summaries of workflow execution, including step-level metrics and overall usage.

### Chaos experiments

Run controlled experiments against a target script using supported fault types such as:

- tool failure
- token timeout
- rate-limit storm
- infinite loop
- memory corruption
- silent degradation
- handoff corruption

### Server diagnostics

Inspect the MCP server's health, version, integration availability, and readiness.

### Sidecar discovery

Inspect the available Agentic Sidecar package, its status, modules, and framework adapters.

## Architecture

```text
                    MCP Client / Host
                           |
                           v
              +--------------------------+
              |  DeepAgentLabs MCP Server |
              +--------------------------+
                    /      |       \
                   /       |        \
                  v        v         v
           AgenticLens  Agentic   Agentic
                       Chaos      Sidecar
                  |
                  v
        AI Operations Workflow
             Specification