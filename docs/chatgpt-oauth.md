# ChatGPT OAuth account linking

The HTTP server optionally supports OAuth authorization code with PKCE (`S256`)
for pre-registered public clients. ChatGPT receives a separate, one-hour access
token plus a rotating refresh token for automatic renewal. Local applications
keep using their existing API key. Both credentials
resolve to the same user and hosted workflow sessions.

This is account linking to the hosted MCP. It does not install Python packages
on a user's computer or establish a local runtime command channel. Tower and
Sidecar control still require their documented host/runtime bindings.

## Enable on the server

1. For PostgreSQL/Supabase, apply the updated `deploy/supabase/schema.sql` before
   enabling OAuth. It adds the private, RLS-protected `mcp.oauth_records` table.
   Redis-backed deployments use separate expiring OAuth keys without a migration.
2. Keep `DEEP_AGENTIC_CORE_MCP_PUBLIC_URL=https://mcp.deepagentlabs.io` configured.
3. Register a public OAuth client with a stable ID you choose, for example
   `deepagentlabs-chatgpt`. In the ChatGPT connection/submission configuration,
   use that client ID and token endpoint authentication method **none** (no
   client secret). Copy the exact HTTPS redirect URI shown by the OpenAI portal.
4. Set `DEEP_AGENTIC_CORE_MCP_OAUTH_CLIENTS` to JSON with that ID and redirect URI:

   ```json
   {
     "deepagentlabs-chatgpt": {
       "name": "ChatGPT",
       "redirect_uris": ["https://REPLACE-WITH-EXACT-OPENAI-CALLBACK"]
     }
   }
   ```

   The callback above is a placeholder, not a working OpenAI callback. Only
   explicitly configured, exact HTTPS callback URLs are accepted. Register
   multiple exact callbacks if testing and directory connections use different
   URLs. No wildcard redirects, dynamic client registration or CIMD are enabled.
5. Deploy the server with `[http]` installed. The existing key backend and shared
   workflow store remain required. OAuth uses PostgreSQL when the app opens a
   database pool, otherwise the configured Redis session client. There is no
   automatic in-memory fallback. Startup and `/healthz` check OAuth storage too.
6. Select OAuth in ChatGPT and connect to `https://mcp.deepagentlabs.io/mcp`.
   Discovery advertises the authorization and token endpoints automatically.
   Request resource `https://mcp.deepagentlabs.io/mcp` and scope `mcp:tools`.

OAuth is disabled when `DEEP_AGENTIC_CORE_MCP_OAUTH_CLIENTS` is absent. Invalid
client configuration fails startup. Remove that variable and restart to disable
OAuth without disabling existing API keys. Short-lived OAuth tokens stored
before disabling are no longer accepted while OAuth is disabled.

## User flow

ChatGPT opens the DeepAgentLabs consent page. The user enters their existing
API key **on that page**, and selects Allow access. The service verifies that
key, binds a single-use authorization code to the account, callback, client,
resource and PKCE challenge, and redirects back to ChatGPT with the code and
original `state`. ChatGPT exchanges it with its PKCE verifier and receives an
access token. The original API key is never returned to ChatGPT or stored in
an OAuth record.

Use the key already configured in the local application to link the same
account. Creating a new key through signup creates a separate account, even
when the display name matches. There are no email/password accounts, recovery
or social-login providers in this implementation.

The scope `mcp:tools` delegates the current key's existing hosted tool permissions,
including permitted writes. It cannot expand an allowlist, cross tenant
boundaries, enable remote chaos execution or grant operator-only Sidecar access.

## Routes and lifecycle

| Route | Method | Purpose |
| --- | --- | --- |
| `/.well-known/oauth-protected-resource` | GET | MCP resource and issuer discovery |
| `/.well-known/oauth-protected-resource/mcp` | GET | Path-specific resource discovery |
| `/.well-known/oauth-authorization-server` | GET | Authorization server metadata |
| `/oauth/authorize` | GET | Validate client, callback, scope, state, resource and PKCE; show consent |
| `/oauth/authorize` | POST | Browser-bound, same-origin approval or cancellation |
| `/oauth/token` | POST | Exchange a single-use code or rotate a refresh token for a fresh token pair |
| `/oauth/revoke` | POST | Revoke a connection using its access or refresh token |

Authorization codes expire after two minutes; pending consent after ten minutes.
Access tokens expire after one hour. ChatGPT can renew them automatically using
`grant_type=refresh_token`. Each successful renewal returns a new access token
and a **new refresh token**; the client must replace its saved refresh token.
The default connection expires after **30 days without renewal** or **90 days
from consent**, whichever happens first. Renewal resets the inactivity window
but never extends the maximum lifetime. Reconnect when either limit is reached.

Operators can set `DEEP_AGENTIC_CORE_MCP_OAUTH_REFRESH_IDLE` (seconds; default
`2592000`) and `DEEP_AGENTIC_CORE_MCP_OAUTH_REFRESH_MAX` (seconds; default
`7776000`). The inactivity lifetime must cover the access token lifetime and
cannot exceed the maximum, which is capped at one year. Lowering a setting does
not rewrite existing records: new connections use the new maximum; subsequent
renewals use the configured inactivity limit without extending their original
maximum. Revoke existing connections when immediate removal is needed.

Token exchange and revocation accept URL-encoded forms. Only authorization code
with `S256` PKCE and the refresh-token grant are supported. A refresh request is:

```text
grant_type=refresh_token&client_id=deepagentlabs-chatgpt&refresh_token=<saved-refresh-token>
```

The resource and scope may be omitted on refresh; when provided, they must match
the original grant. A refresh cannot change client, account, resource or scope.
Only access tokens are accepted at `/mcp`; refresh tokens are used exclusively
at `/oauth/token` and `/oauth/revoke`. Existing access tokens issued before
refresh support do not acquire refresh tokens automatically: reconnect once.

Every renewal uses an atomic compare-and-swap in PostgreSQL or Redis. Reuse of
any previous refresh token revokes that entire connection, including its access
tokens and latest refresh token. Token ancestry hashes remain until the original
maximum expiry so reuse of older ancestors can still be detected. This follows
[RFC 9700 refresh-token rotation](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.14).
Clients must serialize renewals: concurrent refreshes or retrying a spent token
after losing its response require reconnecting. Separate connections for the
same account are independent.

Codes and tokens are indexed only by SHA-256 digests. OAuth records refer to the
account's current key digest, never the original key. Every MCP request and tool
dispatch rechecks token expiry, account status and current key policy. Rotating
or revoking that API key invalidates all OAuth tokens linked through it; reconnect
with the replacement key. Revoking either an access token or a refresh token
ends that connection and its renewal chain, while leaving the API key and other
independent connections usable. Revocation does not cancel work already running.

Browser consent uses a Secure, HttpOnly, SameSite cookie and a server-side nonce;
POST requires the canonical origin. OAuth responses are not cached or framed.
The service accepts OAuth routes only on the canonical public hostname. Codes
are consumed atomically across workers. OAuth endpoints share a 60 requests per
minute limit per peer (PostgreSQL or Redis); configure trusted proxy hops only
when ingress is restricted to that trusted proxy chain. Add ingress-level global
limits for public traffic. Secrets must not be logged by proxies or request-body
capture middleware.

## Validation before public submission

Run the protocol tests and shared-store tests. PostgreSQL integration tests use
`DEEP_AGENTIC_CORE_MCP_TEST_DATABASE_URL`, a disposable superuser database: they
drop and recreate the `mcp` schema. Never point that variable at a hosted service.

Complete a real ChatGPT account-linking test after deployment with the exact
registered client/callback. Check same-account workflow recall, denied tools,
key rotation, automatic renewal, replay detection, token revocation and expiry. Public directory metadata, domain
verification, review materials and OpenAI approval are separate from enabling
OAuth. This repository change does not deploy or submit the service.


### Browser consent checks

The consent page keeps API key errors inline so users can retry. Its account
creation link opens in a new tab, preserving the pending connection form.
`/oauth.css` serves its script-free, responsive styles. The consent response uses
`Referrer-Policy: same-origin` to preserve browser form Origins while withholding
off-site referrers. Its CSP allows the registered client's callback origins so
Chromium can follow the authorization redirect; the server still validates exact
registered callback URLs and rejects missing, null or foreign form Origins.

Run the isolated browser regression (no live accounts or credentials):

```sh
uv sync --extra dev --extra http --extra browser
uv run --no-sync playwright install chromium
uv run --no-sync python scripts/smoke_oauth_browser.py
```


The consent header and connection diagram display the existing DeepAgentLabs
logo. Registered clients with a `chatgpt.com` callback display OpenAI's official
Blossom beside a dotted two-way arrow. Other clients keep their initial badge.
Brand assets are served from a fixed allowlist under `/oauth-assets/`; no
third-party image requests are made. A CSS content hash in the stylesheet URL
ensures branding updates load when the consent form is reopened.
