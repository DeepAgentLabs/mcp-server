# Entry points and administrator CLI

The package installs three console entry points. MCP tools and reusable prompts are protocol calls, not additional shell subcommands.

| Executable | Purpose | Requirements |
| --- | --- | --- |
| `deep-agentic-core-mcp` | Local stdio MCP server | Base package and any selected optional producers |
| `deep-agentic-core-mcp-http` | Authenticated Streamable HTTP server | `[http]`, authentication/shared storage and host/origin configuration |
| `deep-agentic-core-mcp-admin` | Operator key-policy and revocation interface | `[http]` dependencies and configured database/DynamoDB store credentials |

The server entry points read their [environment configuration](configuration.md). MCP clients use the [56-tool catalog](tools.md) and [resource/prompt interfaces](resources-and-prompts.md). The administrative CLI has four subcommands:

| Subcommand | Purpose |
| --- | --- |
| `show USER_ID` | Read the user's state and effective/stored access policy |
| `set-permissions USER_ID` | Replace the stored policy |
| `clear-permissions USER_ID` | Restore the default hosted surface |
| `revoke USER_ID` | Revoke that user's key without possessing the agent key |

```bash
deep-agentic-core-mcp-admin show USER_ID
deep-agentic-core-mcp-admin set-permissions USER_ID \
  --allow 'lens.*' --allow core.version --deny 'lens.suite_*' --task-id TASK_ID
deep-agentic-core-mcp-admin clear-permissions USER_ID
deep-agentic-core-mcp-admin revoke USER_ID
```

Replace USER_ID/TASK_ID with the exact intended identities before a mutation. `--allow`/`--deny` are repeatable tool-name globs; deny wins. `--expires-at` accepts an aware ISO 8601 timestamp; `--task-id` binds the policy's task scope. `set-permissions` replaces rather than merges policy configuration. Use its `--help` for syntax.

The CLI selects `DEEP_AGENTIC_CORE_MCP_DATABASE_URL` first, otherwise `DEEP_AGENTIC_CORE_MCP_USERS_TABLE`; it cannot edit a static environment-key map. Successful commands print profile/policy JSON. Unknown users exit 1, invalid policies exit 2, and missing store configuration stops startup. Stored changes take effect on subsequent dispatch/rechecks, not as cancellation of already-running work.

These commands are independent of the model's tool surface. Human Tower approval and POST `/control/tasks/{task_id}/stop` are separate operator boundaries; the admin CLI does not grant Tower approval or automatically find a Sidecar runtime. See [access policy semantics](access-control.md) and [Sidecar stop/revoke setup](phase6-containment.md).
