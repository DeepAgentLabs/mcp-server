# Security Policy

## Supported versions

Security fixes are provided for the latest released version.

| Version | Supported |
| ------- | --------- |
| Latest  | Yes       |
| Older   | Best effort |

## Reporting a vulnerability

Please report security issues privately using GitHub's private vulnerability reporting feature on this repository.

Include:

- Affected version or commit
- Reproduction steps
- Impact assessment
- Any suggested mitigation

Please do not open a public issue for suspected vulnerabilities until the issue has been reviewed.

## Scope

This MCP server orchestrates tool calls across AgenticLens and Agentic Chaos. It does not store API keys or manage cloud credentials directly.

If a vulnerability depends on a specific runtime environment or MCP client, include those environment details in the report.

## `chaos.run_experiment` executes real code

Unlike every other tool in this server, `chaos.run_experiment` is a genuine
code-execution primitive: it runs a target Python script (via `runpy`) inside
an `agentic-chaos` `chaos_session()`. That's intentional — it's what makes
fault injection real instead of simulated — but it means any MCP client that
can call this tool can run arbitrary code that already exists somewhere in
the workspace.

Mitigations currently in place:

- **Sandboxed to the workspace** — `script` is resolved against the
  workspace root (the directory containing `mcp-server` and its sibling
  repos) and rejected if it resolves outside it or doesn't exist. It cannot
  be pointed at arbitrary paths on the host machine.
- **`timeout_seconds` guard** — the script runs on a worker thread with a
  configurable timeout. Note this is *not* a hard kill: Python cannot
  forcibly terminate a thread, so on timeout the script's thread may still
  be running in the background after the tool call returns a `timed_out`
  result.

What this does **not** do: it does not sandbox the script's actual
capabilities (filesystem, network, subprocess access are all whatever the
server process itself has), and it does not authenticate or authorize the
MCP client making the call — that's the host/transport's job.

**Only expose script execution to trusted local MCP clients.** HTTP disables
this tool. A future remote execution feature needs isolated workers and explicit
authorization; workspace-path confinement alone is insufficient.

### Authenticated multi-user HTTP

HTTP requires a unique, high-entropy bearer key per user, configured through
`DEEP_AGENTIC_CORE_MCP_API_KEYS`. Use HTTPS at the hosting layer. The endpoint
validates allowed Host and Origin values, rejects unknown keys with 401, and
puts the authenticated identity in server-controlled request context. Tool
arguments and user-supplied identity headers cannot select another user's
state. Health checks are unauthenticated and expose only readiness status.

HTTP uses stateless MCP transport and a shared Redis session store. Each user
has a separate key containing their workflow sessions. Optimistic transactions
prevent concurrent requests from silently overwriting each other's changes;
conflicting calls fail and may be retried. Successful commits renew a one-hour
TTL. Users are limited to 100 sessions and 4 MiB of serialized state. Configure
Redis eviction/persistence, encryption, access controls, and capacity for the
expected user count. A Redis outage fails tool calls rather than falling back
to unisolated local state.

Defaults per process are 60 authenticated requests/minute/user, two concurrent
requests/user, 16 total concurrent requests, and a 1 MiB request body. These
request counters are not global across replicas; use the hosting layer for
aggregate limits. Cancellation does not forcibly stop synchronous Python work.
Do not treat these controls as an execution sandbox.

The HTTP tool surface excludes `chaos.run_experiment` and its dispatch rejects
calls even when `DEEP_AGENTIC_CORE_MCP_ALLOW_REMOTE_CHAOS` is set. That override
is retained for legacy/local integrations and cannot enable HTTP execution.

This is administrator-provisioned bearer-key access, not an OAuth server.
Do not publish keys, bake them into images, or enable HTTP access without TLS.
See [remote hosting](docs/remote-hosting.md) for configuration and rotation.
