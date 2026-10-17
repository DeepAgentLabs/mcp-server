# Sidecar 0.8 integration boundary

## Sidecar 0.8 interoperability

MCP server 0.3.5 retains connectivity, discovery and transport ownership.
Sidecar 0.8 adds a client adapter and a separate-process MCP 2.3.0 gateway example
with server-side enforcement. This does not enable remote operator bridging
in this server or expose shared/exclusive configuration through public tools.

Sidecar 0.8 provides Shared/Exclusive context-only, guardrails-only or combined
configuration, explicit host context delivery and mandatory guardrail composition.
Exclusive rules cannot weaken shared restrictions. Cross-framework privacy,
revocation and delegated authority remain v0.9 validation; stable schemas remain
v1.0. Native correlated Lens readback requires Lens 0.7.1. All sibling packages
stay optional; no dependency floor is increased without a runtime requirement.
See the [Sidecar integration contract](https://github.com/DeepAgentLabs/agentic-sidecar/blob/main/docs/integrations.md).
