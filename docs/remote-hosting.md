# Authenticated multi-user hosting

The stdio package and authenticated HTTP service share tool implementations.
HTTP clients connect to `/mcp` with a unique per-user bearer key. Workflow state
is shared across workers through Redis, while MCP transport is stateless and
requires no load-balancer session affinity. Users cannot inspect other users'
workflows by supplying their session names.

## Configuration

| Environment variable | Required | Purpose |
| --- | --- | --- |
| `DEEP_AGENTIC_CORE_MCP_API_KEYS` | Without DynamoDB | JSON object mapping stable user IDs to unique secrets |
| `DEEP_AGENTIC_CORE_MCP_USERS_TABLE` | AWS signup | DynamoDB user/key table; overrides environment key configuration |
| `DEEP_AGENTIC_CORE_MCP_PUBLIC_URL` | AWS signup | HTTPS origin for connection details and browser origin checks |
| `DEEP_AGENTIC_CORE_MCP_TRUSTED_PROXY_HOPS` | No | Trusted suffix position in X-Forwarded-For; AWS sets 2 for its restricted CloudFront/ALB chain |
| `DEEP_AGENTIC_CORE_MCP_REDIS_URL` | Yes | Shared Redis URL; use `rediss://` for TLS |
| `DEEP_AGENTIC_CORE_MCP_ALLOWED_HOSTS` | For remote hosting | Comma-separated Host values, e.g. `mcp.example.com` |
| `DEEP_AGENTIC_CORE_MCP_ALLOWED_ORIGINS` | For browser clients | Exact permitted origins, e.g. `https://client.example.com`; absent Origin is permitted |
| `DEEP_AGENTIC_CORE_MCP_HTTP_HOST` | No | Bind address; default `127.0.0.1`, container uses `0.0.0.0` |
| `DEEP_AGENTIC_CORE_MCP_HTTP_PORT` | No | Default `8000` |
| `DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT` | Container sets it | Canonical sibling/schema asset directory |

Example secret shape (replace the placeholders with independently generated
random secrets of at least 32 characters; generate with `secrets.token_urlsafe(32)`):

```json
{
  "alice": "<alice's independently generated random secret>",
  "bob": "<bob's independently generated random secret>"
}
```

Keep user IDs stable during key rotation to preserve session ownership. Replace
credentials and restart all workers; during rolling rotation, old and new
workers otherwise accept different keys. Removal revokes future access once all
workers restart. Existing in-flight calls may finish. Redis state expires after
one hour of inactivity, measured from a completed tool call. Sharing a key means
sharing a user identity.

This supports MCP clients that can supply bearer credentials. The AWS deployment
provides `/signup` for immediate key signup, replacement, and revocation using
DynamoDB, without worker restarts. Display names are unverified labels; identities
are generated UUIDs. Keys are shown once and cannot be recovered. OAuth discovery,
verified email login, account recovery, and billing are not implemented.

## Container build

Build from the parent workspace, which contains `mcp-server`, `agenticlens`, and
`ai-operations-spec`:

```bash
python3 mcp-server/scripts/build_container.py --tag deep-agentic-core-mcp:latest
```

The build helper stages only required source, metadata, and schema files, so
unrelated workspace files and credentials never enter the build context.
With BuildKit, a direct workspace build also supports `deploy/docker/Dockerfile.dockerignore`. The image installs AgenticLens and includes the canonical v0.4
schema files. Chaos and Sidecar integrations are optional and are not included
in this analysis/validation image; their diagnostic tools can report unavailable.

Inject credentials and the Redis URL at runtime. Without either setting the
service refuses to start. `/healthz` returns 200 while Redis is available and
503 on storage failure; it checks storage readiness, not every optional adapter.
Use `core.verify` to inspect integration availability.

## AWS deployment requirements

The deployable AWS templates and lifecycle instructions are in
[deploy/aws/README.md](https://github.com/DeepAgentLabs/mcp-server/blob/main/deploy/aws/README.md). They use an ECS service behind
a private ALB and CloudFront HTTPS, with a DynamoDB user/key table and Valkey sessions.
The following also applies to other container hosting configurations.

Run the container as an ECS service behind an HTTPS load balancer.
Keep container ingress restricted to the load balancer, and Redis ingress
restricted to the service. Use `/healthz` as the target-group health path and
container port 8000. All replicas need the same key configuration and Redis URL.
Provide credentials through ECS secret injection rather than image layers or
checked-in task definitions. See [ECS secret injection](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-secrets-manager.html)
and [ECS load balancer setup](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/alb.html). Set allowed hosts to the external MCP hostname.
Configure your Redis persistence/eviction policy and capacity for the expected
users; the application does not provision infrastructure or guarantee durable
storage independently of Redis configuration.

Rate and concurrent-request counters are per worker. An additional hosting-layer
limit is needed for service-wide quotas. Workflow storage limits are shared:
100 sessions and 4 MiB of serialized state per user, with a one-hour idle TTL.
Redis WATCH/EXEC prevents lost updates across workers. Concurrent tool calls for
the same user may return a retryable conflict instead of silently overwriting
state. HTTP never runs chaos scripts, so retrying a rejected commit cannot
repeat externally executed code.

## Client requests

Supply `Authorization: Bearer <your-key>` on every MCP request. The `/mcp`
endpoint responds directly without redirecting. For example:

```bash
curl https://mcp.example.com/mcp \
  -H "Authorization: Bearer $MCP_API_KEY" \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -H 'MCP-Protocol-Version: 2025-11-25' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"core.session_state","arguments":{"session_id":"my-workflow"}}}'
```

The same session name is private to each authenticated user. Omit it to use
that user's private `default` workflow session. Never put credentials in query
parameters or tool arguments.

## Render deployment

The root `render.yaml` provisions a free Docker web service and a free,
internal-only Key Value instance in Oregon. `deploy/docker/Dockerfile.render` builds from this
repository alone: AgenticLens 0.5.0 comes from PyPI and the canonical AIOS schemas
are downloaded at a pinned Git commit with SHA-256 verification.

Render's `PORT` and `RENDER_EXTERNAL_HOSTNAME` are used automatically. The Key
Value connection string is injected through the Blueprint. Supply
`DEEP_AGENTIC_CORE_MCP_API_KEYS` as the user-to-secret JSON mapping when applying
it; never commit actual keys. For a custom domain, explicitly set
`DEEP_AGENTIC_CORE_MCP_ALLOWED_HOSTS` to include both the assigned Render hostname
and your custom hostname. Browser clients also need an allowed Origin.

After these files are pushed to the repository, create the Blueprint at:
https://dashboard.render.com/blueprint/new?repo=https://github.com/DeepAgentLabs/mcp-server

Check `/healthz`, verify an unauthenticated `/mcp` request returns 401, and test
an authenticated tool call before sharing the endpoint with users. The deployed
MCP URL is `https://<assigned-hostname>/mcp`.

Free web services can spin down when idle, and free Key Value loses data on
restart. This is an initial test deployment; upgrade for an always-available
service and persistent session storage. Automatic deploys are disabled to avoid
publishing later repository changes without an explicit deployment action.
See [Render free-service limits](https://render.com/docs/free).
