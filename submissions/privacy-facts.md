# Hosted service privacy facts for the publisher

This is preparation guidance, not a published privacy policy or terms document.
The publisher must confirm operational practices and legal commitments before
publishing policy text. Public contact: deepagentlabs@gmail.com.

## Observed implementation

- Signup accepts a display name and issues an account ID and API key. This
  signup does not require an email address, password, or payment.
- The key store persists a SHA-256 key digest, not the plaintext account key.
  OAuth consent receives the existing API key on our service; it is not sent
  to the requesting AI host as that host's OAuth access token.
- Account status, display name, key digest and operator-configured policies
  can be stored in PostgreSQL. The hosted service uses Render and Supabase.
- OAuth records contain account identity/key-digest bindings, scopes, callback,
  grant metadata and token hashes. Raw access/refresh tokens are returned to
  the OAuth client; hashed record lookups are used by the store.
- Default access tokens last one hour. Refresh tokens rotate, with a 30-day
  inactivity window and 90-day maximum connection duration. These defaults
  are configurable; verify actual production settings before promising them.
- OAuth pending consent state lasts 10 minutes and authorization codes two
  minutes. Expiry controls validity; it is not a promise that every expired
  database row or backup is immediately physically erased.
- Workflow/session data supplied to tools can be stored in user-scoped session
  state. The default store TTL is one hour; verify the production setting.
  Submitted artifacts can themselves contain personal or sensitive information.
- Signup/OAuth rate limiting uses request network identity (hashed peer values
  in the distributed store). Infrastructure logs can include request metadata.
- Account DELETE currently sets status to revoked. It does not erase the user
  row, all related stored data, provider logs or backups. Revocation prevents
  subsequent access; do not describe it as complete erasure.
- Some tools can contact separately configured first-party Tower/Sidecar
  runtimes. Disclose actual configured destinations and operators rather than
  claiming all data remains on one host.
- The server returns results to the AI platform chosen by the user. Connecting
  through ChatGPT or Claude also involves that platform's own data practices.

## Facts/decisions still needed

- Actual production data retention and backup retention, including Render and
  Supabase logs; a TTL is not a universal deletion guarantee.
- How users request deletion, what gets deleted, and the response procedure.
- Whether data is used for analytics, marketing, model training or any other
  purpose beyond delivering the service; confirm rather than assume.
- Any additional subprocessors, enabled external runtimes, and storage regions.
- Intended age audience and whether the service is directed at children.
- Applicable service terms, acceptable use, availability, support, and liability
  commitments chosen by the publisher. The repository MIT license does not
  replace hosted-service terms.

Publish an accessible HTTPS privacy-policy page and terms page on a controlled
site. Both must identify the service and publisher. Send the actual URLs so they
can be checked and included in the package; current /privacy and /terms routes
on deepagentlabs.io returned 404 during preparation.
