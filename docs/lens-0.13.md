# Lens 0.13 readiness compatibility

Lens 0.13.0 adds an opt-in single-node project artifact service, scoped bearer
roles, atomic local audit, immutable model/prompt metadata registries, mandatory
pattern redaction, trace retention and reproducible Evals release receipts.

MCP 0.6.4 updates its hosted image recipes and integration CI to Lens 0.13.0, alongside Evals 0.12.0, Sidecar 0.10.0 and Chaos 0.10.0. Existing MCP tools and hosted authorization are unchanged. Lens project HTTP routes are not exposed through new MCP tools or automatically deployed.

Native trace, evaluation and integrity contracts retain their existing meanings.
Audit integrity is explicitly not verified; compliance export is not certification.
No new automatic sibling reader or shared conformance claim is introduced.
Independent security/deployment acceptance and the coordinated v1.0 API freeze
remain open. See the [Lens production guide](https://github.com/DeepAgentLabs/agenticlens/blob/v0.13.0/docs/production-readiness.md)
and [tested dependency matrix](https://github.com/DeepAgentLabs/agenticlens/blob/v0.13.0/docs/lens-0.13-compatibility.md).

## Operator example

Keep existing native evidence readers and optional integrations. To explore the
new storage workflow independently, in a Lens 0.13 checkout run:

```bash
uv run python examples/enterprise_demo.py
```

It uses only synthetic local data, stores a redacted trace in an isolated SQLite
database and exports project metadata with `certification: not_assessed`. It does
not execute targets, call providers, start a hosted service or alter sibling state.

