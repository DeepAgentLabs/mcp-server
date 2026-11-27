# Configuration

The server supports local stdio and authenticated Streamable HTTP. The same tools have different access/execution boundaries by transport. Configuration belongs to the server process or embedding host, not to model-visible tool arguments.

## Local stdio

```bash
python -m pip install deep-agentic-core-mcp
deep-agentic-core-mcp
```

Usually the MCP client launches the executable using the [quickstart configuration](developer-guide.md#quickstart); it exchanges MCP messages on stdin/stdout. `python -m deep_agentic_core_mcp.server` is the equivalent module entry point. Optional producer packages must be installed in that interpreter's environment. Restart after installing/changing them.

`DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT` selects the parent directory containing sibling repositories and the allowed local script tree. Source development can select sibling `src` checkouts over installed packages; the adapter also considers sibling environments for fallback dependencies. Installed distribution metadata alone cannot identify the imported source. Use `core.verify` plus [compatibility observations](release-readiness.md) to inspect the selected setup.

The spec adapter uses an available workspace catalog as authoritative; otherwise packaged schema/catalog resources support offline validation. A sibling spec checkout is not required for a standalone wheel. Never fetch remote schemas merely because an artifact contains a reference URI.

## Local chaos script policy

| Setting | Behavior |
| --- | --- |
| `DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT` | Resolved local workspace boundary |
| `DEEP_AGENTIC_CORE_MCP_ALLOWED_SCRIPT_GLOBS` | Comma-separated workspace-relative POSIX globs; empty permits scripts within the root subject to denies |
| `DEEP_AGENTIC_CORE_MCP_DENIED_SCRIPT_GLOBS` | Additional denied patterns; deny always wins |

VCS internals, virtual environments and site-packages are always denied. Path confinement and configured script timeout are separate from an OS/container sandbox. `DEEP_AGENTIC_CORE_MCP_REMOTE` marks network transport; the HTTP entry point sets it itself. `DEEP_AGENTIC_CORE_MCP_ALLOW_REMOTE_CHAOS` is a legacy opt-in for custom integrations and does **not** enable script execution through the authenticated HTTP service. See [Chaos integration](integrations.md#agentic-chaos) and [limitations](limitations.md).

## Hosted HTTP

```bash
python -m pip install 'deep-agentic-core-mcp[http]'
# Configure authentication, session storage and external host/origin settings first.
deep-agentic-core-mcp-http
```

The command starts `/mcp` using the environment below and refuses missing authentication/shared storage. PostgreSQL/Supabase can hold keys, signup limits and sessions; DynamoDB can hold signup keys; Redis can hold sessions. Static environment keys are another authentication backend, not a session backend.

| Environment variable | Purpose / precedence |
| --- | --- |
| `DEEP_AGENTIC_CORE_MCP_DATABASE_URL` | PostgreSQL connection for keys/signup and, without Redis, sessions; apply the documented SQL schema first |
| `DEEP_AGENTIC_CORE_MCP_USERS_TABLE` | DynamoDB key/signup table when no database key backend is selected |
| `DEEP_AGENTIC_CORE_MCP_API_KEYS` | JSON stable-user → key or key/policy objects when no database/DynamoDB backend is selected |
| `DEEP_AGENTIC_CORE_MCP_REDIS_URL` | Redis session backend; takes precedence over database sessions |
| `DEEP_AGENTIC_CORE_MCP_HTTP_HOST` | Bind host, default `127.0.0.1` |
| `DEEP_AGENTIC_CORE_MCP_HTTP_PORT` | Port; falls back to `PORT`, then `8000` |
| `DEEP_AGENTIC_CORE_MCP_ALLOWED_HOSTS` | Allowed request hosts; defaults include loopback; the entry point includes configured public/Render hosts |
| `DEEP_AGENTIC_CORE_MCP_ALLOWED_ORIGINS` | Exact permitted browser origins; absent Origin is allowed |
| `DEEP_AGENTIC_CORE_MCP_OAUTH_REFRESH_IDLE` | Refresh connection inactivity lifetime in seconds (default 2592000 / 30 days) |
| `DEEP_AGENTIC_CORE_MCP_OAUTH_REFRESH_MAX` | Maximum refresh connection lifetime in seconds (default 7776000 / 90 days; cap one year) |
| `DEEP_AGENTIC_CORE_MCP_OAUTH_CLIENTS` | Optional JSON mapping of registered client IDs to names and exact HTTPS redirect URIs; enables [OAuth](chatgpt-oauth.md) |
| `DEEP_AGENTIC_CORE_MCP_PUBLIC_URL` | Public HTTPS origin for signup/client details and origin checks |
| `DEEP_AGENTIC_CORE_MCP_TRUSTED_PROXY_HOPS` | Trusted suffix position in forwarded client addressing; configure for the actual proxy boundary |
| `RENDER_EXTERNAL_HOSTNAME` | Hosting-provided hostname used by the HTTP entry point |

Keys must be unique per stable user and at least 32 characters; generate random values with `secrets.token_urlsafe(32)`. An environment policy object has `key` and optional `permissions` (`allow`, `deny`, `expires_at`, `task_id`). Do not put keys in tool arguments, URLs, workflow data or source control. See [key policy configuration](access-control.md) and [complete hosting/storage setup](remote-hosting.md).

### Embedding API and process limits

`transport_http.create_app(...)` accepts explicit `api_keys` or `key_store`, `store`, host/origin rules and process-level request/concurrency limits. Explicit stores support controlled tests and custom hosts. In-memory session storage must be supplied explicitly and is single-process only; it is not the hosted CLI's production fallback.

| Argument | Default / behavior |
| --- | --- |
| `requests_per_minute` | `60`, per worker |
| `max_concurrent_per_user` | `2`, per worker |
| `max_concurrent_total` | `16`, per worker |
| `operator_store`, `sidecar_bridge` | Supply both or neither; operator authentication must be independent of agent authentication |

Workflow state has separate shared per-user quotas: 100 sessions, 4 MiB serialized state and a one-hour idle TTL. Durable behavior depends on the chosen backing store and deployment. `/healthz` reports storage readiness, not sibling/runtime acceptance. For shared-guard failures and crash reconciliation, see [Redis dispatch serialization](phase6-containment.md#shared-redis-dispatch-guard).

This complete local configuration fragment constructs an app without binding a network port or accessing a database:

```python
import secrets
from deep_agentic_core_mcp.services.remote_sessions import MemorySessionStore
from deep_agentic_core_mcp.transport_http import create_app

app = create_app(
    api_keys={"local-demo": secrets.token_urlsafe(32)},
    store=MemorySessionStore(),
    allowed_hosts=["localhost", "127.0.0.1"],
)
```

Install `[http]` before using it. A real host supplies the credential securely to its authorized client and manages the app lifecycle.

## Tower, task controls and evidence trust

| Host setting | Boundary |
| --- | --- |
| `AGENTICOPS_TOWER_URL`, `AGENTICOPS_TOWER_READ_TOKEN`, `AGENTICOPS_TOWER_WRITE_TOKEN` | Trusted local stdio Tower connector configuration |
| `DEEP_AGENTIC_CORE_MCP_TOWER_BINDINGS` | Hosted user-ID → HTTPS origin/read-token/write-token bindings; selected from authenticated identity and reloaded per call |
| `DEEP_AGENTIC_CORE_MCP_LENS_TRUST_STORE` | Protected JSON key-ID → hex HMAC-key map, minimum 32-byte keys, used by execution verification |

Hosted Tower calls never fall back to global/local credentials and never accept origins/tokens as tool arguments. Human approval stays in Tower. The independent Sidecar stop route requires an explicitly host-bound runtime, task-dedicated key revoker and separate operator store; no environment-only switch discovers a live runtime. See [full binding and control setup](phase6-containment.md) and [Lens execution trust/rotation](lens-execution-evidence.md).

## Administration and deployment

The [administrator CLI](cli-reference.md) selects a configured PostgreSQL key store or DynamoDB table; it uses the store's operator credentials, not the agent bearer key. Static environment-key changes require worker restart. Database/Dynamo policy/key changes are rechecked at subsequent dispatch, including queued calls.

Use the [hosting guide](remote-hosting.md), [AWS lifecycle instructions](https://github.com/DeepAgentLabs/mcp-server/blob/main/deploy/aws/CI-CD.md) and [upgrade/rollback policy](release-readiness.md) for actual operator deployment. Console startup, package publication and image recipes do not themselves deploy or certify a running service. All producer-native and AIOS schema versions remain independent of the MCP package version.
