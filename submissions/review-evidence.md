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
| P4 Fault catalog | Not run | Requires case-specific live/host rehearsal. |
| P5 AIOS draft validation | Not run | Requires case-specific live/host rehearsal. |
| N1 Local script execution | Not run | Hosted transport omits chaos.run_experiment; actual model refusal still needed. |
| N2 Cross-account disclosure | Not run | Tenant-isolation tests exist; actual model handling still needed. |
| N3 Local installation/control | Not run | Documented boundary; actual model handling still needed. |

Anthropic's per-tool confirmation remains incomplete: hosted discovery currently
advertises 34 tools, while live case evidence does not cover every tool with
valid inputs and prerequisites. Do not mark the portal confirmation complete on
this evidence alone. Do not turn an unavailable backend into a claimed success.

Required later: readable demo recording URL, final saved submission version,
secure reviewer access, domain/developer verification, scans and publisher
attestations. Neither platform has received a submission from this preparation.
