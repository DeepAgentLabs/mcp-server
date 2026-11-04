# Tower 0.10 capability contract compatibility

Updated 2026-11-04.

Tower 0.10 adds authenticated `GET /contracts/capabilities` and the Python
`ControlTowerAPI.get_capability_contract()` facade. The descriptor publishes
`tower.capabilities.v1` as a candidate, with registration/heartbeat/readback JSON
Schemas, status values and existing merge/replacement semantics. CPython and
Node.js HTTP clients are tested against a live server and durable SQLite
readback. Existing routes and payloads remain compatible.

MCP owns tool transport and access checks. Existing tower.* tools keep using existing Tower API routes (inventory, incidents, configuration and runbooks); MCP 0.6.5 adds read-only `tower.capability_contract`; existing host bindings are reused.

## Operator example

Against a running Tower server with a reader token:

```bash
curl --fail -H "Authorization: Bearer $AGENTICOPS_READ_TOKEN" \
  "$AGENTICOPS_API_URL/contracts/capabilities"
```

Expect `contract_version: tower.capabilities.v1` and `maturity: candidate`.
A writer token can also read this route; readers cannot register workers.
Use Tower's [Python and Node examples](https://github.com/DeepAgentLabs/agenticops-control-tower/tree/v0.10.0/examples/runtimes)
for registration through heartbeat/readback. A duplicate registration replaces
the record; heartbeat merges metadata and replaces reported status. Reported
health does not automatically expire or derive from producer outcomes.

## Dependencies and release boundary

MCP 0.6.5 adds read-only `tower.capability_contract` with no arguments. It uses
the configured reader credential and existing hosted per-user authorization.
No runtime dependency, optional range, native schema or export marker changes
are required. Older Tower servers return a safe `Tower HTTP 404` error. Siblings remain optional to Tower.
The candidate is preparation for the coordinated ecosystem v1.0 release;
independent acceptance and stable freezing remain open. See the
[Tower contract and migration policy](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.10.0/docs/capability-contract.md).

## Discover through MCP 0.6.5

Call `tower.capability_contract` with `{}`. The result is `{"ok": true, "data": ...}`
containing Tower's unchanged candidate descriptor and schemas. This requires
Tower 0.10+ and a configured reader credential. Hosted callers also need a
per-user Tower binding and an MCP policy permitting `tower.capability_contract`.
An unbound hosted caller cannot fall back to process credentials. This read does
not register agents, approve actions or declare the contract stable.

With a local configured connector, run:

```bash
uv run python examples/tower_capability_contract.py
```

The hosted equivalent is `python3 examples/hosted_access_status.py --tool tower.capability_contract`
against a server upgraded to MCP 0.6.5. Package publication does not deploy that
hosted server; an older server reports an unknown tool.
