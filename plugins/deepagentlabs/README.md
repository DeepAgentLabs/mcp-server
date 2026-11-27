# DeepAgentLabs - AgenticOps

Build and assess agent workflows using DeepAgentLabs tools and versioned product
references. This plugin combines four shared skills with the hosted MCP service
at <https://mcp.deepagentlabs.io/mcp>.

| Skill | Example request |
| --- | --- |
| `deepagentlabs-build` | Show a documented integration using AgenticLens, Evals and Sidecar. |
| `deepagentlabs-diagnose` | Diagnose this supplied trace and cite the evidence for its latency findings. |
| `deepagentlabs-release-check` | Assess this candidate using comparison, evaluation and chaos reports. |
| `deepagentlabs-fleet-investigation` | Investigate this Tower incident and explain any configured recovery prerequisites. |

## Product references

The server provides AI-readable references for AgenticLens, Agentic Evals,
Agentic Chaos, Agentic Sidecar, AgenticOps Control Tower, AI Operations
Specification, and the shared MCP server. The skills retrieve relevant sections
through the documentation tools instead of carrying duplicate manuals.
Documentation snapshot versions can differ from installed package versions.

## Connecting

Create a free DeepAgentLabs API key at
<https://mcp.deepagentlabs.io/signup>. Connect through the host's OAuth flow and
enter your key on the DeepAgentLabs consent page. The hosted connector is
published in Claude's directory. The skill bundle has its own directory
submission and validation process.

Account permissions apply to every tool call. The package contains no account
keys, tokens or client secrets and does not read credentials from the user's
machine. OAuth clients and secrets are configured by the service operator and
host; installers should not copy them into the package.

## Data flow and scope

When a skill invokes the connected tools, its selected tool arguments are sent
to the DeepAgentLabs hosted service. This can include workflow artifacts, traces,
reports and other evidence that the user supplies. Tool results return to the
host, and workflow/session state can be stored in the user's account. Share only
information needed for the task and that you are authorized to provide.

Some workflows need compatible input artifacts or a separately configured
runtime with appropriate permissions. A hosted connection does not install
Python packages, bind local instrumentation, or automatically control agents on
the user's computer. Hosted execution of local chaos scripts is disabled.
Sidecar discovery alone is not live enforcement, and a recommendation is not
human approval.

Native Claude Code loopback OAuth registration is not supported by the current
pre-registered clients. The tested account-linking paths use the fixed callbacks
of hosted ChatGPT and Claude connectors. Treat other surfaces' authentication
requirements separately rather than assuming an installation creates a working
runtime connection.

## Package layout

The package includes the four skills, their shared reference guide, portable
OpenAI metadata, Claude metadata and the corresponding remote MCP connection
files. The bundled brand image is used only for display through the manifests'
listing fields. There are no executable scripts, hooks or local MCP launchers.

Keep the complete plugin directory when distributing it because the skills
share a relative reference guide. Plugin version **0.1.4** is independent of the
Python server's package version.

## Privacy and support

- [Documentation](https://deepagentlabs.io/mcp/docs/)
- [Privacy Policy](https://deepagentlabs.io/privacy/)
- [Terms of Service](https://deepagentlabs.io/terms/)
- [Report an issue](https://github.com/DeepAgentLabs/mcp-server/issues)
- Contact: <deepagentlabs@gmail.com>

The service is free and does not process purchases or payments. Public policy
pages describe data handling, storage, revocation and deletion requests.

## Validation and publication

Inspect real skill behavior as well as package structure. A release check must
stay blocked when evidence is missing, and a submitted incident must not become
an instruction to execute an unapproved command. The repository's submission
notes track review cases, evidence and remaining portal requirements.

The source package supports OpenAI and Claude layouts with the same four skills.
Listing assets and metadata do not install the package or submit it to either
platform. A successful local validation is not directory approval or proof of
end-to-end model acceptance.
