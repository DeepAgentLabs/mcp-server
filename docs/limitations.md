# Limitations

The MCP Server currently has several limitations based on the capabilities and integration status of the current release.

## AI Operations Specification dependency

The `spec.validate_artifact` tool depends on AI Operations Specification v0.4 schema documents.

In the current local development environment, the required schema documents were not available, so artifact validation could not be successfully verified.

## Agentic Sidecar runtime

The Agentic Sidecar integration is currently a scaffold.

The current environment reports:

- Package status: `scaffold`
- Release stage: `pre-alpha`
- Runtime ready: `false`

The available Sidecar tools currently provide status and module discovery rather than the full decision runtime.

## Chaos experiments

`chaos.run_experiment` executes a target script under selected fault configurations.

Because it executes code, experiments should be performed only with trusted and controlled scripts.

A successful experiment does not necessarily mean that a fault was observed. The target may complete without producing a chaos event.

## Local execution

The MCP Server is designed around local, trusted stdio execution.

Remote deployment and broader networked execution are not the primary focus of the current implementation.

## Integration availability

The overall server health can be reported as `degraded` when an optional integration is unavailable.

Use `core.health` and `core.verify` to inspect the availability and readiness of individual integrations.

## Version and maturity

The current MCP Server release documented here is:

```text
0.2.0