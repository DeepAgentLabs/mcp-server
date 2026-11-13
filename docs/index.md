# MCP Server

## MCP Server overview

How can an MCP client access supported DeepAgentLabs capabilities?

MCP requests, supplied artifacts, configured producers, and server settings. Tool results, diagnostics, session context, and supported combined evidence workflows.

**When to start here**

Connect locally and inspect core.version, core.compatibility, and core.verify.

## Inputs and outputs

| You provide | You receive |
| --- | --- |
| MCP requests, supplied artifacts, configured producers, and server settings. | Tool results, diagnostics, session context, and supported combined evidence workflows. |

## Execution boundary

Installed versions, adapter readiness, and runtime health are separate checks. Optional producer capabilities depend on the environment.

[Start the MCP Server quickstart →](guide/quickstart.md)

## Capabilities

Use these capabilities to address connect tasks in your application.

| Capability | What it provides |
| --- | --- |
| Client connection | Expose supported capabilities through local stdio or configured hosted access. |
| Diagnostics and discovery | Inspect server health, compatibility, installed producers, and session state. |
| Workflow analysis | Invoke Lens-backed analysis, reports, comparisons, and other supported operations. |
| Release workflows | Combine explicit comparison, evaluation, and chaos evidence under a release policy. |
| Artifact validation | Validate native Evals or shared-spec artifacts with the matching tool. |
| Operational tools | Use supported Tower integrations and inspect available Sidecar or Chaos capabilities. |

## Supported scope

Installed versions, adapter readiness, and runtime health are separate checks. Optional producer capabilities depend on the environment.

## Core concepts

| Concept | Meaning |
| --- | --- |
| Server vs producer | The MCP server provides access; individual capability implementations may require producer packages. |
| Tool vs resource | Tools perform supported operations; resources expose reusable examples or workflow context. |
| Session | A session ID lets related calls reuse explicitly stored artifacts and results. |
| Local vs hosted | Execution permissions and available tools differ; hosted access is not identical to local execution. |
| Required evidence | A release check needs the selected evidence types; missing or invalid data blocks acceptance. |

## Recommended workflow

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

## Next steps

Connect locally and inspect core.version, core.compatibility, and core.verify.

[Open the developer quickstart →](guide/quickstart.md)
