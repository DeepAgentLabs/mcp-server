# Quickstart

**Connect: How can an MCP client access supported DeepAgentLabs capabilities?**

**Input:** MCP requests, supplied artifacts, configured producers, and server settings.  
**Output:** Tool results, diagnostics, session context, and supported combined evidence workflows.

## Install the local server

```
python -m pip install deep-agentic-core-mcp
```

## Connect an MCP client

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

[Download mcp-client.json](examples/mcp-client.json)

## Restart and verify

Restart the client or reconnect the server, then request these tool calls in the client:

```
core.version {}
core.compatibility {}
core.verify {}
```

**Expected:** server diagnostics plus explicit adapter availability. Missing optional producers are not the same as a failed base-server connection. These are MCP tool calls, not shell commands.

## Add a producer

```
python -m pip install agenticlens
```

Restart the server. Read `resource://examples/sample_workflow`, pass its JSON object as `artifact` to `lens.analyze_workflow` with a chosen `session_id`, then call `lens.report_summary` with that session. Inspect compatibility before combining independently installed packages.

[Connection details ↗](../getting-started.md)[Hosted access ↗](../access-control.md)
