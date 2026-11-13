# MCP Server developer guide

Use this guide to set up MCP Server, run a local example, and apply it to your application. Optional provider and integration fragments identify the objects or services you must supply.

[Quickstart](#quickstart) · [Usage](#usage) · [Configuration](#settings) · [Troubleshooting](#troubleshooting) · [Reference](#reference)

## Quickstart

Requires Python 3.10 or newer. Run commands in an activated virtual environment. Download referenced files into the same working directory before running them.

### Install the local server

```
python -m pip install deep-agentic-core-mcp
```

### Connect an MCP client

Merge this entry into your client's MCP configuration; preserve its existing servers. Use the full executable path if the client cannot see your active environment.

mcp-client.json · complete file

```json
{
  "mcpServers": {
    "deep-agentic-core": {
      "command": "deep-agentic-core-mcp",
      "args": []
    }
  }
}
```

[Download mcp-client.json](guide/examples/mcp-client.json)

### Restart and verify

Restart the client or reconnect the server, then request these tool calls in the client:

```
core.version {}
core.compatibility {}
core.verify {}
```

**Expected:** server diagnostics plus explicit adapter availability. Missing optional producers are not the same as a failed base-server connection. These are MCP tool calls, not shell commands.

### Add a producer

```
python -m pip install agenticlens
```

Restart the server. Read `resource://examples/sample_workflow`, pass its JSON object as `artifact` to `lens.analyze_workflow` with a chosen `session_id`, then call `lens.report_summary` with that session. Inspect compatibility before combining independently installed packages.

[Connection details ↗](getting-started.md) · [Hosted access ↗](access-control.md)

## Usage

<span id="release-checks"></span>

### Combine release evidence

#### Tools

| Tool | What it does | Session |
| --- | --- | --- |
| `core.compare_runs` | Lens baseline/candidate comparison; same behavior as `lens.compare_runs` | Stores runs and the comparison |
| `core.release_check` | Gates comparison, evaluation and chaos evidence; fails closed | Stores the result |
| `core.incident_summary` | Collects regressions, chaos crashes/timeouts, failed cases and blocked gates | Stores the result |
| `core.export_report` | Exports everything the session holds as `mcp.unified-report.v1` | Evidence unchanged; the call is recorded in history |

The workflow steps are also served as `resource://workflows/release-check`,

and the `core.release_check` prompt asks a host to explain every gate.

#### Release check

```
{
  "evaluation_report": { "...": "a native Agentic Evals report" },
  "thresholds": { "min_pass_rate": 0.95, "max_average_latency_ms": 2000 },
  "required_evidence": ["comparison", "evaluation", "chaos"],
  "session_id": "release-42"
}
```

`comparison` and `chaos_report` may be passed explicitly; otherwise the

session's last `core.compare_runs`/`lens.compare_runs` and

`chaos.run_experiment` results are used. `evaluation_report` is always passed

explicitly.

Each gate reports a `status`:

| Status | Meaning | Blocks release |
| --- | --- | --- |
| `passed` | Valid evidence that met every check | No |
| `failed` | Valid evidence with regressions, failed Evals thresholds, a crash or a timeout | Yes |
| `invalid` | Evidence that is not an object, does not match its producer's contract (a chaos report needs every `chaos.run_experiment` field with the right type), or came from a failed call | Yes |
| `missing` | A kind listed in `required_evidence` with nothing supplied or stored | Yes |

`ready` is true only when every gate passed. By default all three kinds are

required; narrow `required_evidence` (for example `["evaluation"]`) when a

release only needs some of them. Evidence that is supplied but not required is

still gated.

`thresholds` takes Evals `GateConfig` fields such as `min_pass_rate`,

`max_failed_cases`, `min_average_score`, `max_average_latency_ms`,

`max_total_cost_usd`, the per-tag/per-metric floors and the judge/live-target

limits. Unknown keys are rejected, because the Evals gate would otherwise

ignore a typo. With no thresholds, the Evals default applies: every case must

pass.

A passing comparison may still carry Lens `sample_size_guidance` (for example

when fewer than five runs per cohort were compared). It appears in the gate's

`observed` values and does not block the release on its own.

#### Incident summary

`core.incident_summary` reads the same evidence and the session's last release

check. It reports only failure signals:

- `comparison` / `regression` — regressions in the Lens comparison
- `chaos` / `resilience_failure` — the target crashed or timed out (injected

fault events alone are not an incident)

- `evaluation` / `failed_cases` — the Evals report has failed cases
- `release_check` / `blocked_release` — the gates that did not pass

`status` is `investigate` with findings or `no_signals` without. With no

evidence at all the call returns `ok: false`.

#### Local and hosted use

All four tools are available locally and on the hosted server, where state is

scoped to the authenticated user. Hosted HTTP still rejects

`chaos.run_experiment`, so hosted callers pass a locally produced chaos report

as `chaos_report` or leave `chaos` out of `required_evidence`. Lens-backed

gates need `agenticlens` (installed in the hosted image). Without it, the

comparison and evaluation gates report `invalid` instead of passing, and a call

that sets `thresholds` returns `ok: false` because they cannot be checked.

<span id="settings"></span>

## Configuration

The local MCP server uses the client configuration shown in the quickstart. Optional producers must be installed in the server environment. For hosted authentication and permissions, follow the [access-control guide](access-control.md).

## Troubleshooting

Check the failing boundary before changing application behavior.

- Executable not found: point the client to the environment's executable.
- Producer still missing: restart the server after installation and check which environment it uses.
- Workspace sources override packages: inspect `DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT`.
- Hosted access failure: follow the access-control guide for that deployment rather than changing the local stdio example.

### Verify your environment

Run commands from the environment where you installed the package. Confirm the input file exists and matches the expected artifact contract. Keep the original evidence when diagnosing a failure.

## Reference

Use the current product reference for exact method signatures, command options, and supported artifacts. The code fragments in configuration and how-to articles build on the quickstart; they are not all standalone scripts.

- [Open API / CLI reference ↗](tools.md)


[Complete generated MCP tool reference](tools.md). Optional producer tools require the corresponding configured integration.
