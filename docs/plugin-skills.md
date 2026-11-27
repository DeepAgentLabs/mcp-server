# DeepAgentLabs plugin skills

The source package in `plugins/deepagentlabs/` combines the shared remote MCP
connection with four workflow skills. A portable Agent Plugins manifest supports
ChatGPT/Codex authoring, and a Claude manifest and connector configuration support
Claude authoring. Both use the same skill files; neither publishes a listing or
creates an authenticated connection merely by existing in the repository.

## Included workflows

| Skill | When it applies | Product references |
| --- | --- | --- |
| `deepagentlabs-build` | Build or integrate an agent application with the requested ecosystem products | Relevant subset of all seven products |
| `deepagentlabs-diagnose` | Explain a workflow/run failure, latency, cost or regression from recorded evidence | Lens, MCP and the owning artifact producer |
| `deepagentlabs-release-check` | Assess a candidate against required comparison, native Evals and chaos evidence | MCP unified workflows, Lens, Evals, Chaos and AIOS as needed |
| `deepagentlabs-fleet-investigation` | Investigate Tower incidents and recommend installed recovery runbooks | Tower and relevant Lens/Evals/Sidecar producers |

Example requests:

- “Build a support agent with Lens instrumentation, Sidecar supervision and an
  Evals suite. Read the product APIs before implementing it.”
- “Diagnose this trace run's timeout and cite the spans supporting the cause.”
- “Check this release against our baseline, Evals thresholds and required chaos
  evidence. Explain missing evidence without dropping its gate.”
- “Investigate this Tower incident, build an evidence timeline and propose an
  installed runbook. Do not execute recovery.”

## Existing AI-readable Markdown is the source

Skills explain the workflow and which product owns each decision. They do not
replace or copy `docs/llms-full.md`, capability indexes or checksum manifests.
The server already bundles these references for all seven products and exposes
them through `core.docs_catalog`, `core.docs_search` and `core.docs_read`. See
[the product-reference guide](ecosystem-ai-reference.md).

The skills retrieve the actual section IDs, page through `next_offset`, and cite
the returned source commit and line link. They compare documentation versions
with installed dependencies before generating APIs. An empty literal search,
an absent optional adapter or a denied tool is not evidence that an agent failed.

A shared `references/ecosystem.md` inside the plugin keeps product routing,
document discovery and host/runtime boundaries in one place. In a local product
checkout without MCP, the skills can use the existing AI-readable files directly.
Source paths are environment-dependent; the plugin does not ship another copy
of the manuals or assume that the user's machine has a sibling checkout.

## Source layout and authentication

```text
plugins/deepagentlabs/
  plugin.json
  mcp.json
  .claude-plugin/plugin.json
  .mcp.json
  skills/<skill-name>/SKILL.md
  skills/<skill-name>/agents/openai.yaml
  references/ecosystem.md
  README.md
  LICENSE
```

The portable `mcp.json` uses Streamable HTTP; Claude's `.mcp.json` uses its `http`
transport name. Both declare `https://mcp.deepagentlabs.io/mcp`, contain no secrets
or assumed account app IDs, and rely on a separately configured authenticated
connection. No account upload, local installation or marketplace change is part
of adding these files.

The OAuth source in this checkout must be deployed and given the correct
registered client/callback settings before hosted OAuth can work. It currently
supports pre-registered public clients, not automatic DCR/CIMD. Use host connector
settings to supply the appropriate client ID. See [OAuth setup](chatgpt-oauth.md).
Claude Code's loopback OAuth callback needs additional server support; loading
skills locally does not prove that remote authentication is supported there.

Skills do not broaden the account's tool policy, install local PyPI packages,
create a local runtime command channel or replace Tower's human approval path.
Hosted chaos execution remains excluded. Draft/candidate schema maturity and
producer judgments are preserved.

## Validation and acceptance

Validate each skill with the Skill Creator `quick_validate.py`, and parse the
JSON/YAML manifests as data. When Claude Code is installed, run from the MCP root:

```bash
claude plugin validate plugins/deepagentlabs
```

These checks validate structure, not model behavior. After installing a source
package in the intended host, check skill discovery and authentication, then run
the example requests with representative evidence. In particular, missing gates
must remain blocked, a documentation snapshot must not be treated as an installed
runtime, and an incident artifact must not authorize recovery execution. Live
ChatGPT/Claude acceptance and public directory submission remain outstanding.

Maintain the workflows in `SKILL.md`, shared reference guidance in
`references/ecosystem.md`, and detailed APIs in their owning product docs. Refresh
the existing MCP documentation bundle through its normal committed-source sync;
adding a skill does not require recursively copying manuals into the plugin.
