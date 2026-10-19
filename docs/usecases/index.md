# MCP Server Use Cases

Explore practical examples demonstrating how to use the DeepAgentLabs MCP Server and its existing package integrations.

These examples use simulated data where indicated. They demonstrate workflow analysis, reporting, evaluation, and fault-testing capabilities. They do not perform real-world bookings or guarantee that injected faults will occur.

## Use Case 1: AI Travel Planner

**Goal:** Demonstrate a travel-planning workflow using simulated flight, hotel, and weather information.

- **Capabilities:** AgenticLens workflow analysis and reporting.
- **Scenario:** Plan a three-day trip from Bengaluru to Goa.
- **Data:** Simulated travel data; no bookings are made.

[Read the AI Travel Planner walkthrough](use-case-1.md)

## Use Case 2: Workflow Fault Testing

**Goal:** Explore how Agentic Chaos runs a fault experiment against a local workflow.

- **Capabilities:** Fault discovery and chaos experiment execution.
- **Scenario:** Run a simulated workflow with a selected fault configuration.
- **Limitation:** An experiment may complete without recording a chaos event.

[Read the Workflow Fault Testing walkthrough](use-case-2.md)

## Use Case 3: Evaluation and Release Gate

**Goal:** Demonstrate evaluation reports and threshold-based decisions.

- **Capabilities:** AgenticLens SLO summary and audit report.
- **Scenario:** Evaluate a sample report against configured thresholds.
- **Data:** Sample evaluation metrics are illustrative, not measured production results.

[Read the Evaluation and Release Gate walkthrough](use-case-3.md)

## Important Notes

- Examples must be run with a compatible version of the MCP Server and its dependencies.
- Tool availability depends on the installed package versions and local configuration.
- Sample values must not be interpreted as real-world measurements.
