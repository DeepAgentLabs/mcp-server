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

**Only expose this server to trusted MCP clients and keep it stdio/local.**
If a remote deployment mode is ever added (see `ROADMAP.md`), this tool
needs a real sandbox (container, restricted user, etc.) before it can be
exposed to untrusted callers — workspace-path confinement alone is not
sufficient at that point.
