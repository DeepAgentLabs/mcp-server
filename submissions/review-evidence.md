# Review evidence

Preparation date: 2026-11-26 (publisher's client date).

The user confirmed successful custom connections in both ChatGPT and Claude.
Live server probes also verified OAuth code exchange, MCP initialize/discovery,
version/docs calls, token refresh, replay revocation and test-key cleanup.
Offline Chromium checks verify the actual browser-generated consent Origin,
cookies and outgoing callback for both clients. These are distinct from model
review cases and directory-portal validation.

| Case | Model-level status | Current evidence |
| --- | --- | --- |
| P1 Hosted version/compatibility | Not run | Version endpoint previously probed; full prompt/call/result comparison still needed. |
| P2 Seven-product catalog | Not run | Catalog/search/read successfully probed on the hosted server. |
| P3 Documented instrumentation | Not run | Reference retrieval works; model example and citations not yet reviewed. |
| P4 Fault catalog | Not run | Live server call passed with the real installed catalog; model scenarios still need rehearsal. |
| P5 AIOS draft validation | Not run | Inline workflow returned ok=true, empty schema/semantic errors and conformance.aligned=true; model explanation still needs rehearsal. |
| N1 Local script execution | Not run | Hosted transport omits chaos.run_experiment; actual model refusal still needed. |
| N2 Cross-account disclosure | Not run | Tenant-isolation tests exist; actual model handling still needed. |
| N3 Local installation/control | Not run | Documented boundary; actual model handling still needed. |

All 34 advertised hosted tools have now been exercised with public synthetic
fixtures in the dedicated reviewer account. The direct HTTP/structured-result
smoke returned 33 successful results and one expected fallback:
`lens.execution_verify` reports unknown because the host trust store is not
configured. No execution verification or live containment is claimed. All tools
advertised `openWorldHint: false`; no external agent action ran. See
`live-tool-probes.json` for the per-tool outcomes. This establishes the described
server probes, not exhaustive semantic acceptance or model-level review cases.

The separate confidential directory client passed live Basic code exchange,
POST refresh and authenticated revocation; missing/incorrect client secrets
were rejected. Both existing public clients still passed consent, exchange and
refresh. Tool discovery returned explicit boolean annotations for all 34 tools.
A dedicated reviewer account remains active with credentials stored privately
outside source and ZIPs; enter them only through the secure review fields.

Required later: readable demo recording URL, final saved submission version,
secure reviewer access, domain/developer verification, scans and publisher
attestations. The publisher subsequently confirmed that the Claude MCP connector
is Published; the separate plugin bundle is still in validation.


## Plugin directory validation: 0.1.3

On 2026-11-27, Claude Code 2.1.332 reported Validation passed for the plugin
folder: four skills and one HTTP MCP server, with no directory-check findings.
Its only advice was to add a marketplace install command once a marketplace
exists. This local command does not run the portal's security scan or policy
review. The installed older CLI 2.1.92 rejects the newer directory listing
fields; validation used an isolated current CLI without changing that install.

The logo's C2PA provenance chunk contained printable `curl` and environment-like
references that appeared to cause the portal's image findings. Only that chunk
was removed. The remaining PNG chunks, compressed image data and decoded pixel
stream are byte-identical to the original; the brand image is unchanged. The
README no longer presents the image path as code. The Claude manifest now
provides the icon, documentation, support, privacy and terms fields described in
Anthropic's manifest reference. Revalidate the updated main commit in the portal
to determine whether its findings are resolved.

GitHub reports admin and push access for pramodbn27 on DeepAgentLabs/mcp-server.
The portal's access failure therefore needs a fresh Claude GitHub authorization
or permission check; changing repository collaborators is not indicated.
