# Public directory submissions

Status: the publisher confirmed the Claude MCP connector is Published. The Claude
plugin bundle is being validated separately; OpenAI submission remains in preparation.

The publisher selected individual identity **PRAMOD BEGUR NAGARAJ**, public
contact **deepagentlabs@gmail.com**, no payments/purchases, and all countries each
platform supports. The product name remains **DeepAgentLabs**. Identity and
domain verification must still be checked in the actual portals.

The canonical source is `plugins/deepagentlabs`, version 0.1.4. An OpenAI upload
is a separate ZIP copy of that directory; the original stays in the repository.
Claude reads the plugin folder from GitHub and accepts the hosted MCP server as
a separate connector submission. `claude-listing.json` is a human worksheet,
not an API payload and not an uploaded plugin manifest.

## Prepared

- Existing logo, four SKILL.md files, shared references, and both host layouts.
- Listing copy, actual public website and GitHub issue support URLs.
- Five positive and three negative cases in the OpenAI manifest, mirrored in
  `review-cases.json`; these are drafts, not claims of model-level acceptance.
- Explicit OpenAI public-client configuration for the tested custom flow.
- Support for a separate confidential Claude directory OAuth client; verify
  its hash-only runtime registration and live checks on the deployed version.

## Remaining preparation

1. Policy pages are published and verified at https://deepagentlabs.io/privacy/
   and https://deepagentlabs.io/terms/. Both identify the publisher/contact and
   cover the hosted service. Their URLs are included in the package and Claude
   worksheet. Keep the policies consistent with future operational changes.
2. Record and host the real demo described in `demo-walkthrough.md`. Enter its
   verified playable URL as `extensions.com.openai.review.demo_recording_url`.
3. Rehearse every review case in the intended host. Track actual results in
   `review-evidence.md`. Direct tool probes are not model-level review cases.
4. Provide a dedicated reviewer account through OpenAI's secure portal fields.
   Do not add reviewer keys, OAuth client secrets or personal credentials to
   source, the ZIP, or this worksheet. Keep access valid for later reviews.
5. Verify the publisher identity/domain and complete required portal checks.
   The publisher must read and complete legal/policy attestations personally.

## Build the candidate

```sh
uv run python scripts/prepare_submission.py --output /tmp/deepagentlabs-submission
```

This creates a separate source copy, ZIP, SHA-256, and a readiness report. A ZIP
can be structurally valid while still missing required submission material.
Use `--require-ready` to fail when mandatory materials remain absent. Do not
label an incomplete candidate ready for review.

## Final portal configuration (after preparation)

OpenAI: https://platform.openai.com/plugins. Select the intended organization,
project and verified individual publisher. Upload the ZIP, connect its MCP entry,
register the exact callback shown by that connection flow if it differs from the
existing ChatGPT callback, run the prepared cases against the saved version, and
resolve scans and missing fields before submitting. An upload is only a draft.

Claude: https://claude.ai/directory/manage. Submit the universal endpoint
`https://mcp.deepagentlabs.io/mcp` as **MCP connector**. Enter the separate
`deepagentlabs-claude-directory` confidential client in the secure OAuth fields
once deployed and tested; never paste the secret into this worksheet. Submit a
**Plugin bundle** from `DeepAgentLabs/mcp-server`, path `plugins/deepagentlabs`,
branch `main`, so the four skills are included too. Validate the exact final
commit. Do not attest that every tool has been tested until that is true.

Neither submission is publication. Verify review status and publish only an
approved version with the intended country availability.

## Authoritative references

- https://developers.openai.com/plugins/deploy/submission
- https://claude.com/docs/plugins/submit
- https://claude.com/docs/connectors/building/submission
- https://claude.com/docs/connectors/building/authentication
