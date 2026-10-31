# Hosted access control (0.5.0)

MCP 0.5.0 adds per-key tool permissions to the hosted HTTP service. The server
checks them at dispatch, outside the model: a client that skips `tools/list`, or
a model told to call a hidden tool, still gets a denial. Local stdio is trusted
and does not use policies.

## What a policy holds

A policy is operator configuration attached to one hosted key:

| Field | Meaning |
| --- | --- |
| `allow` | Tool-name globs the key may call. Default `["*"]`, the full hosted surface |
| `deny` | Tool-name globs the key may never call. Deny always wins |
| `expires_at` | ISO 8601 timestamp with a timezone, or epoch seconds. After it, every tool is denied |
| `task_id` | The task this key is delegated to. It appears in every evidence record |

Globs are case-sensitive `fnmatch` patterns (`lens.*`, `core.version`), with at
most 64 per list. Keys without a policy keep the default hosted surface, so
signup keys and existing deployments behave as before.

`core.access_status` stays callable under any valid policy, including an
expired one, so a client can find out why its calls fail. An explicit `deny`
entry can still remove it. A stored policy that fails validation denies every
tool, `core.access_status` included. It never falls back to the default
surface.

Hosted HTTP still rejects `chaos.run_experiment` and `tower.*`. A policy can
narrow the hosted surface but cannot widen it.

## When it is enforced

On every hosted `tools/call`, after the call has waited for the caller's
session lock and immediately before the handler runs, the server:

1. re-authenticates the same bearer key against the key store,
2. reloads that key's policy, and
3. checks the tool against it.

So a revocation, a narrower policy or an expiry takes effect for:

- calls queued behind another call from the same user,
- client retries, and
- requests on connections or MCP sessions opened before the change.

New requests with a revoked key get HTTP 401 at the endpoint. A call that is
already running is not cancelled, and keys or credentials the agent holds for
other systems are not revoked. If the key store cannot be reached at dispatch,
the call is denied.

`tools/list` uses the policy loaded at request time, so a hosted client sees only
the tools it can call.

## Configuring policies

### Environment keys (`DEEP_AGENTIC_CORE_MCP_API_KEYS`)

Map a user to an object instead of a plain key string:

```json
{
  "alice": "<alice's key>",
  "release-bot": {
    "key": "<release-bot's key>",
    "permissions": {
      "allow": ["core.*", "spec.validate_artifact", "evals.validate_artifact"],
      "deny": ["core.session_state"],
      "task_id": "release-2026-11",
      "expires_at": "2026-11-30T00:00:00Z"
    }
  }
}
```

Invalid policies stop the service at startup. Changing environment keys
requires restarting the workers.

### Hosted stores (Supabase/PostgreSQL and DynamoDB)

Stored policies apply from the next dispatch, without a restart or a new key.
PostgreSQL needs the `permissions` column. Re-run `deploy/supabase/schema.sql`,
or apply just this statement:

```sql
ALTER TABLE mcp.users ADD COLUMN IF NOT EXISTS permissions jsonb;
```

DynamoDB stores the policy as a `permissions` map on the `USER#<id>` item and
needs no migration.

Use the operator CLI, which ships with the package. It needs the service's store
credentials (`DEEP_AGENTIC_CORE_MCP_DATABASE_URL` or
`DEEP_AGENTIC_CORE_MCP_USERS_TABLE`), not the agent's key:

```bash
deep-agentic-core-mcp-admin show <user-id>
deep-agentic-core-mcp-admin set-permissions <user-id> \
  --allow 'lens.*' --allow core.version --deny 'lens.suite_*' \
  --task-id incident-118 --expires-at 2026-11-07T00:00:00Z
deep-agentic-core-mcp-admin clear-permissions <user-id>
deep-agentic-core-mcp-admin revoke <user-id>
```

`revoke` is the operator's own revocation path. It works when the agent's key is
lost or compromised, and it does not depend on the agent's cooperation. The
self-service `/signup` revocation still requires the key itself.

## Denials and evidence

A denied call returns a structured tool error:

```json
{
  "ok": false,
  "error": "Access denied: tool not in policy allow list",
  "access_denied": true,
  "revoked": false,
  "access_decision": {
    "schema": "mcp.access-decision.v1",
    "event": "denial",
    "decision": "deny",
    "correlation_id": "6f1c…",
    "recorded_at": "2026-11-01T09:30:00.123456Z",
    "subject": "release-bot",
    "tool": "lens.analyze_workflow",
    "task_id": "release-2026-11",
    "reason": "tool not in policy allow list"
  }
}
```

A call rejected because its key was revoked or replaced while it was queued
returns `"revoked": true` with a `revocation_acknowledged` record.

Every hosted call also writes JSON lines to the `deep_agentic_core_mcp.access`
logger. Allowed calls write a `dispatch` and a `completion` record (`outcome`
is `ok` or `error`). Denied calls write `denial` or `revocation_acknowledged`.
All records of one call share a `correlation_id`. They never include bearer
keys, key digests or tool arguments. `deep-agentic-core-mcp-http` prints them to
stdout, one JSON object per line, unless the host has already configured a
handler for that logger. On Render they appear in the service logs.

`mcp.access-decision.v1` is an MCP-local record, not an AIOS artifact. A shared
authority and evidence format for Tower and containment scoring belongs in
`ai-operations-spec` first. Until that exists, Tower and log pipelines join on
`correlation_id`, `subject` and `task_id`.

## Control Tower and Sidecar

Tower's `MCPAccessRevoker` revokes a task's hosted key through the key store's
`revoke(user, token)` and confirms it with `authenticate`. Its interface is
unchanged. From 0.5.0 that revocation also stops calls that are already queued,
and those calls leave a `revocation_acknowledged` record. Tower still reports
in-flight calls and downstream credentials as outside complete containment, which
matches this server's limits.

Hosted `tower.*` tools with per-user Tower credentials are still roadmap work.
So is an authenticated stop/revoke bridge to Sidecar's runtime controls.

## Example

[`examples/hosted_access_status.py`](https://github.com/DeepAgentLabs/mcp-server/blob/main/examples/hosted_access_status.py)
prints a key's effective policy and then tries one tool, showing either its
result or the denial evidence.
