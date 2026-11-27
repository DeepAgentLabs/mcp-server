# Manual submission handoff

The publisher confirmed the Claude MCP connector is Published. The Claude plugin
bundle is in validation; the OpenAI plugin has not been submitted.
Source plugin version: 0.1.4. Hosted runtime tested: 1.3.0.

## 1. Finish the real demo and review rehearsal

OpenAI requires a real playable walkthrough recording for initial MCP review.
Follow `demo-walkthrough.md` using the already working development connection.
Run the five positive and three negative prompts in `review-cases.json`, inspect
actual calls/results, and record the result rather than claiming automatic
model acceptance from the server probes. Use the dedicated reviewer account.

Host the recording at a reviewer-accessible URL. Add the verified URL to
`extensions.com.openai.review.demo_recording_url` in `plugin.json` and rebuild
the ZIP. If the portal offers an editable demo field because the ZIP omits it,
you can supply the recording there instead. Do not submit without the required
recording and accurate case results.

## 2. OpenAI: combined MCP and skills plugin

Portal: https://platform.openai.com/plugins

- Choose the intended organization/project and verified individual identity
  **PRAMOD BEGUR NAGARAJ**. Complete individual verification if requested.
- Select **Upload new or existing plugin** and upload the candidate ZIP built
  by `scripts/prepare_submission.py`. It contains the hosted MCP and four skills.
- Under **Metadata & Skills**, verify DeepAgentLabs branding, publisher/contact,
  free/no-commerce declaration, all supported countries, and both policy URLs.
- Under **MCPs**, connect `deepagentlabs` and inspect the provided OAuth client:
  `deepagentlabs-chatgpt`, token authentication `none`, scope `mcp:tools`.
  There is no OAuth client secret for this OpenAI public client.
- Complete OAuth using the dedicated reviewer account and run the prepared
  cases against this exact saved draft. Put reviewer access only in the secure
  review fields, never in public listing text, source, or the ZIP.
- If the portal shows a different OAuth callback or a domain challenge, copy
  the exact callback or public challenge URL/token to the maintainer. Register
  that exact callback or publish the exact challenge; do not guess or use a
  wildcard. Wait for verification/scans and resolve reported issues.
- Read and complete the current policy/legal attestations yourself. Confirm
  the final saved version and countries, then submit for review.

An upload is a draft. Review approval and publication are separate states.

## 3. Claude: submit the MCP connector

Portal: https://claude.ai/directory/manage

Select **Submit new → MCP connector**:

| Field | Value |
| --- | --- |
| Server URL | `https://mcp.deepagentlabs.io/mcp` |
| Name | DeepAgentLabs |
| Publisher | PRAMOD BEGUR NAGARAJ |
| Contact/support | deepagentlabs@gmail.com |
| Documentation | `https://deepagentlabs.io/mcp/docs/` |
| Privacy policy | `https://deepagentlabs.io/privacy/` |
| Terms | `https://deepagentlabs.io/terms/` |
| Account requirement | A DeepAgentLabs API key; the hosted service is free. |
| Authentication | OAuth, always required |
| OAuth client mode | Anthropic-held client credentials |
| OAuth client ID | `deepagentlabs-claude-directory` |
| OAuth callback | `https://claude.ai/api/mcp/auth_callback` |
| OAuth client secret | Copy only from the protected credential store into the secure client-secret field. |

Use `claude-listing.json` for the one-liner, description and other prepared copy.
Upload the existing logo from `plugins/deepagentlabs/assets/logo.png`.
The suggested slug `deepagentlabs` is not reserved; inspect its availability.

All 34 advertised tools were exercised directly with synthetic fixtures. One
integrity tool has a documented unknown result without configured host trust;
read `live-tool-probes.json` before making any per-tool confirmation. Do not
claim that execution verification or live containment was demonstrated.
Read the platform acknowledgments, verify every statement, and submit only the
completed connector form. This does not submit the four-skill plugin bundle.

## 4. Claude: submit the plugin bundle too

In the same portal select **Submit new → Plugin bundle**:

- Repository: `https://github.com/DeepAgentLabs/mcp-server`
- Plugin path: `plugins/deepagentlabs`
- Tracked branch: `main`
- Plugin version: `0.1.4`

Connect a GitHub account with push access, validate the current commit, inspect
the imported listing and four skills, and fill in accurate data-handling and
compliance answers. Pair/reference the separately submitted MCP connector where
the portal supports that workflow. The native Claude Code loopback OAuth flow
is not supported by our pre-registered clients; do not claim it is. Existing
web/desktop account connectors and the explicit configured directory client
are the tested OAuth paths.

## Published policies and source references

The publisher approved service-only workflow data use, no sale/advertising/model
training, age 13+ subject to platform rules, and the contact above. Policy pages
were published and inspected before their URLs were added to the manifests.
The publisher must still personally complete current platform attestations.

- https://developers.openai.com/plugins/deploy/submission
- https://claude.com/docs/connectors/building/submission
- https://claude.com/docs/plugins/submit
- https://claude.com/docs/connectors/building/authentication
