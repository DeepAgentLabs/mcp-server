# Getting started

Use Python 3.10–3.13 and an MCP-compatible client. The base package supports
local stdio without installing optional ecosystem producers.

```bash
python -m pip install deep-agentic-core-mcp==0.8.0
```

Add this server to your client's MCP configuration (merge it with any existing
`mcpServers` entries):

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

Restart the client, then call `core.version {}`, `core.compatibility {}` and
`core.verify {}`. Missing optional adapters are reported explicitly; the base
server remains usable. The compatibility report records distribution versions,
not runtime health. Use the full executable
path if the client does not inherit your Python environment's `PATH`.

For a first analysis, install the tested Lens producer in the same environment:

```bash
python -m pip install agenticlens==0.14.0
```

Restart the server, read `resource://examples/sample_workflow`, then call
`lens.analyze_workflow` with that JSON object as `artifact` and
`"first-analysis"` as `session_id`. Call `lens.report_summary` with the same
`session_id` to reuse the artifact, and `core.session_state` to inspect saved
context. See the [session workflow and prompt examples](examples.md).

For a local workspace checkout, set
`DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT` on the server process to the directory
containing the sibling repositories. Explicit workspace source imports take
precedence over installed copies. For hosted clients, follow the
[user guide](user-guide.md) and [access policy guide](access-control.md).
See [release readiness](release-readiness.md) for the full tested matrix.
