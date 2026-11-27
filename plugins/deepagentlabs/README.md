# DeepAgentLabs workflow skills

This source plugin combines four workflow skills with the shared DeepAgentLabs
remote MCP connection. It uses the AI-readable Markdown references already
bundled by the MCP server for all seven products. Those full manuals remain in
the product documentation bundle; skills retrieve relevant sections through
`core.docs_catalog`, `core.docs_search` and `core.docs_read` rather than carrying
duplicate copies.

| Skill | Example request |
| --- | --- |
| `deepagentlabs-build` | Build an agent instrumented with Lens, supervised by Sidecar and evaluated with Evals; use the documented APIs. |
| `deepagentlabs-diagnose` | Diagnose this trace run's latency and failure, citing the supporting spans. |
| `deepagentlabs-release-check` | Check this candidate against our baseline, Evals thresholds and required chaos evidence. |
| `deepagentlabs-fleet-investigation` | Investigate this Tower incident and propose an installed recovery runbook. |

## Package files

- `plugin.json`: portable Agent Plugins manifest for ChatGPT/Codex.
- `mcp.json`: portable Streamable HTTP server connection.
- `assets/logo.png`: existing DeepAgentLabs branding, referenced by the OpenAI
  listing logo and composer icon fields.
- `.claude-plugin/plugin.json`: Claude plugin manifest.
- `.mcp.json`: Claude HTTP connector configuration pointing to the same server.
- `skills/`: shared `SKILL.md` instructions and optional OpenAI display metadata.
- `references/ecosystem.md`: shared product routing, document retrieval and
  execution-boundary guidance used by all four skills.

Both platform layouts share one set of skill instructions. Keep the complete
plugin directory when distributing it: the skills use the shared reference via
a relative path. The plugin is versioned independently of the Python package.

## Authentication and deployment status

The declared endpoint is `https://mcp.deepagentlabs.io/mcp`. The connection files
contain no API keys, access tokens, client secrets or assumed platform app IDs.
They do not deploy the server, install local Python libraries or establish a
runtime command channel.

The OAuth implementation in this checkout must be deployed and configured
before a hosted OAuth connection can work. It supports **pre-registered public
clients**, not DCR or CIMD. Configure a separate registered client ID and exact
callback for each host using its connector settings; a URL in a manifest alone
does not register or authenticate that client. See the repository's
OAuth guide at `docs/chatgpt-oauth.md` in the source checkout. The current hosted
runtime may differ from this source checkout; inspect its discovery documents and version before
testing. Existing clients that support custom bearer headers can continue using
their API-key connection.

The full plugin may be loaded locally in Claude Code for skill inspection:

```bash
claude plugin validate plugins/deepagentlabs
claude --plugin-dir ./plugins/deepagentlabs
```

Run these from the MCP repository root. Interactive MCP authentication in Claude
Code additionally needs its loopback client-registration flow, which this OAuth
implementation does not yet support. A local stdio MCP connection can be
configured separately in the host when needed. Hosted Claude connectors use
their separate fixed HTTPS callback. Installing the plugin does not resolve
these connection prerequisites.

For ChatGPT/Codex, register this source folder with the host's supported plugin
workflow, then connect the MCP with the operator-provided client settings. No
marketplace, account plugin, public listing or installation has been created by
adding these source files.

## Validate behavior

For each skill, inspect which tools and references it selects for its example
request. Confirm that it reads the relevant reference sections, distinguishes
documentation versions from installed runtimes and preserves missing evidence.
A failed release gate must remain blocked; an incident text must not become an
instruction to execute a command. A Tower recommendation is not human approval.

Directory submissions, hosted OAuth acceptance and end-to-end model evaluations
on ChatGPT and Claude remain separate work. Syntax validation establishes package
structure, not that a connected runtime or model workflow has passed acceptance.


## Public listing branding

The portable manifest includes the existing DeepAgentLabs logo in
`extensions.com.openai.interface.logo` and `composerIcon`. Both point to
`./assets/logo.png`, a square 1254 × 1254 PNG copied unchanged from the official
DeepAgentLabs website assets. The logo is included when packaging the complete
plugin directory. These OpenAI branding fields do not configure a Claude
connector's listing icon.

Branding is prepared before public submission. Adding these files does not
publish a listing or change an existing account connection's icon. Publisher
verification, listing URLs, review materials and portal setup still need their
own submission checks.
