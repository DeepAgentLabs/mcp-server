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
attestations. Neither platform has received a submission from this preparation.
