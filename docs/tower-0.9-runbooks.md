# Control Tower 0.9.0 runbook tools (MCP 0.5.1)

Control Tower 0.9.0 ships versioned runbooks: an immutable catalog, exact-digest
previews, separate human approval, bounded ordered steps, compensation,
cancellation, lease-based reconciliation and evidence-based verification. MCP
0.5.1 exposes eight local tools over Tower's runbook HTTP routes.

| Tool | Credential | Tower route |
| --- | --- | --- |
| `tower.runbooks` | reader | `GET /runbooks` |
| `tower.runbook_recommendations` (`incident_id`) | reader | `GET /incidents/{id}/runbooks` |
| `tower.runbook_executions` (`incident_id`) | reader | `GET /incidents/{id}/runbook-executions` |
| `tower.runbook_execution` (`execution_id`) | reader | `GET /runbook-executions/{id}` |
| `tower.runbook_preview` (`incident_id`, `runbook_id`, `version`, `parameters`, optional `expires_in_seconds`) | writer | `POST /incidents/{id}/runbooks/preview` |
| `tower.runbook_execute` (`execution_id`, `preview_digest`) | writer | `POST /runbook-executions/{id}/execute` |
| `tower.runbook_cancel` (`execution_id`) | writer | `POST /runbook-executions/{id}/cancel` |
| `tower.runbook_verify` (`execution_id`, `lens_evidence_id`, `evals_evidence_id`) | writer | `POST /runbook-executions/{id}/verify` |

`parameters` is the only structured argument: an object of at most 20
string-to-string entries. Tower validates names and values against the runbook's
declared parameters and the installed connector. Tools cannot supply steps,
commands, endpoints or credentials.

There is still no MCP approval or revocation tool. A human approves the exact
preview digest with Tower's separate approver credential through HTTP or the CLI,
so Tower applies the same role, scope and approval checks to MCP as to every
other surface. Recommendations come only from installed runbook versions, which
keeps the model from inventing executable actions.

`tower.runbook_execute` is marked `slow` and waits up to 150 seconds, covering
Tower's 120-second worst-case runbook budget; other Tower tools keep the
ten-second deadline. If execution still reports a deadline, Tower may be running
the steps: read `tower.runbook_execution` before doing anything else, and never
retry blindly. Tower rejects a second execute of a consumed approval anyway.
Required arguments are checked before any request is sent.

Hosted MCP still hides and refuses every `tower.*` tool until per-user Tower
credential binding exists. The `tower.investigation` prompt now points the model
at `tower.runbook_recommendations` when Tower 0.9 is configured.

The existing `deep-agentic-core-mcp>=0.3.6,<1` extra in Tower is unchanged. The
new tools need Tower 0.9.0; against an older Tower they return `Tower HTTP 404`.

Use Tower's [runbook guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.9.0/docs/runbooks.md)
for definitions, step outcomes, request bodies and limits, and its
[standalone walkthrough](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.9.0/examples/runbook_recovery.py).
