# Recommended workflow

## Connect and discover

After configuring the client, inspect server diagnostics and optional producers. Tool calls shown here are MCP requests, not shell commands.

```
core.health {}
core.compatibility {}
core.verify {}
```

## Analyze a supplied artifact

Read the sample workflow resource, pass the JSON to `lens.analyze_workflow`, and assign a session ID. Use the same session for report summaries and subsequent supported operations.

## Assemble a release check

Supply a native evaluation report explicitly. Add a valid comparison and chaos result when your release policy requires them. `core.release_check` reports passed, failed, invalid, or missing evidence. A release is ready only when every applicable gate passes.

## Investigate and export

Use `core.incident_summary` to collect observed failure signals and `core.export_report` to retain the session evidence. The exported MCP envelope is not automatically an AIOS artifact.

## Respect hosting boundaries

The documented hosted flow rejects local chaos execution. Supply a locally produced chaos report or choose a policy that does not require that evidence. Permissions and producer availability still apply.
