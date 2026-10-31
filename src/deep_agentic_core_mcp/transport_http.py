"""Authenticated, stateless HTTP access to the shared MCP tool surface.

TLS terminates at the hosting layer. Keys are provisioned per user; this is
bearer-key authentication, not an OAuth authorization server.
"""

from __future__ import annotations

import asyncio
import contextlib
import functools
import json
import os
import time
from collections.abc import AsyncIterator, Mapping
from typing import Any
from urllib.parse import urlsplit

from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.types import Receive, Scope, Send

from deep_agentic_core_mcp import config
from deep_agentic_core_mcp.server import server
from deep_agentic_core_mcp.services.access_policy import authorize
from deep_agentic_core_mcp.services.api_keys import DynamoKeyStore, KeyStore, StaticKeyStore
from deep_agentic_core_mcp.services.postgres_store import (
    PostgresKeyStore,
    PostgresSessionStore,
    PostgresSignupLimiter,
    connect,
)
from deep_agentic_core_mcp.services.remote_sessions import RedisSessionStore, SessionStore


def create_app(
    *,
    api_keys: Mapping[str, Any] | None = None,
    key_store: KeyStore | None = None,
    store: SessionStore | None = None,
    allowed_hosts: list[str] | None = None,
    allowed_origins: list[str] | None = None,
    requests_per_minute: int = 60,
    max_concurrent_per_user: int = 2,
    max_concurrent_total: int = 16,
) -> Starlette:
    """Create a fail-closed app; authentication and shared session storage are required.

    api_keys maps stable user IDs to unique secrets of at least 32 characters, or
    to {"key": ..., "permissions": {...}} entries carrying a per-key access policy.
    Tests/development may explicitly supply MemorySessionStore. Stateless MCP
    transport avoids task affinity; workflow state lives in the supplied store.
    Rate/concurrency limits apply per process, storage quotas apply per user.
    DEEP_AGENTIC_CORE_MCP_DATABASE_URL selects PostgreSQL (e.g. Supabase) for
    keys and, unless Redis is configured, sessions and signup limits.
    """
    if key_store is not None and api_keys is not None:
        raise ValueError("Supply only one authentication backend")
    if min(requests_per_minute, max_concurrent_per_user, max_concurrent_total) < 1:
        raise ValueError("Request and concurrency limits must be positive")
    database_url = os.environ.get("DEEP_AGENTIC_CORE_MCP_DATABASE_URL")
    pool: Any = None
    if database_url and (store is None or (key_store is None and api_keys is None)):
        # A session transaction holds a connection for a whole tool call, so every
        # admitted request needs one, plus headroom for auth and signup queries.
        pool = connect(database_url, max_size=max_concurrent_total + 4)
    try:
        return _build_app(
            pool=pool,
            api_keys=api_keys,
            key_store=key_store,
            store=store,
            allowed_hosts=allowed_hosts,
            allowed_origins=allowed_origins,
            requests_per_minute=requests_per_minute,
            max_concurrent_per_user=max_concurrent_per_user,
            max_concurrent_total=max_concurrent_total,
        )
    except BaseException:
        if pool is not None:
            pool.close()
        raise


def _build_app(
    *,
    pool: Any,
    api_keys: Mapping[str, Any] | None,
    key_store: KeyStore | None,
    store: SessionStore | None,
    allowed_hosts: list[str] | None,
    allowed_origins: list[str] | None,
    requests_per_minute: int,
    max_concurrent_per_user: int,
    max_concurrent_total: int,
) -> Starlette:
    if key_store is None:
        table = os.environ.get("DEEP_AGENTIC_CORE_MCP_USERS_TABLE")
        if pool is not None and api_keys is None:
            key_store = PostgresKeyStore(pool)
        elif table and api_keys is None:
            key_store = DynamoKeyStore(table)
        else:
            if api_keys is None:
                api_keys = json.loads(os.environ.get("DEEP_AGENTIC_CORE_MCP_API_KEYS", "{}"))
            key_store = StaticKeyStore(api_keys)
    auth_store = key_store
    if store is None:
        url = os.environ.get("DEEP_AGENTIC_CORE_MCP_REDIS_URL")
        if url:
            store = RedisSessionStore(url)
        elif pool is not None:
            store = PostgresSessionStore(pool)
        else:
            raise ValueError(
                "Configure DEEP_AGENTIC_CORE_MCP_REDIS_URL or DEEP_AGENTIC_CORE_MCP_DATABASE_URL"
                " for shared session storage"
            )
    session_store = store
    config.enable_remote_transport()
    session_manager = StreamableHTTPSessionManager(
        app=server,
        json_response=True,
        stateless=True,
        max_request_body_size=1024 * 1024,
        security_settings=TransportSecuritySettings(
            allowed_hosts=[host.lower() for host in allowed_hosts]
            if allowed_hosts is not None
            else ["localhost", "localhost:*", "127.0.0.1", "127.0.0.1:*"],
            allowed_origins=allowed_origins if allowed_origins is not None else [],
        ),
    )
    active: dict[str, int] = {}
    windows: dict[str, tuple[float, int]] = {}
    total = 0

    class MCPEndpoint:
        async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
            nonlocal total
            request = Request(scope)
            authorization = request.headers.get("authorization", "")
            scheme, _, token = authorization.partition(" ")
            try:
                principal = (
                    await asyncio.to_thread(authorize, auth_store, token)
                    if scheme.lower() == "bearer"
                    else None
                )
            except Exception:
                await PlainTextResponse("Authentication unavailable", status_code=503)(
                    scope, receive, send
                )
                return
            if scheme.lower() != "bearer" or principal is None:
                await PlainTextResponse(
                    "Authentication required",
                    status_code=401,
                    headers={"WWW-Authenticate": 'Bearer realm="mcp"'},
                )(scope, receive, send)
                return
            user = principal.user
            now = time.monotonic()
            start, count = windows.get(user, (now, 0))
            if now - start >= 60:
                start, count = now, 0
            if (
                count >= requests_per_minute
                or active.get(user, 0) >= max_concurrent_per_user
                or total >= max_concurrent_total
            ):
                await PlainTextResponse(
                    "Request limit reached", status_code=429, headers={"Retry-After": "60"}
                )(scope, receive, send)
                return
            windows[user] = (start, count + 1)
            active[user] = active.get(user, 0) + 1
            total += 1
            # These values survive SDK task boundaries through ctx.request.scope.
            scope["deep_agentic_identity"] = user
            scope["deep_agentic_store"] = session_store
            scope["deep_agentic_principal"] = principal
            # Tool dispatch calls this again, after any wait, to re-check the key.
            scope["deep_agentic_authorizer"] = functools.partial(authorize, auth_store, token)
            try:
                await session_manager.handle_request(scope, receive, send)
            finally:
                active[user] -= 1
                total -= 1

    async def healthz(request: Request) -> PlainTextResponse:
        del request
        try:
            ready = await asyncio.to_thread(session_store.ping)
            ready = ready and await asyncio.to_thread(auth_store.ping)
        except Exception:
            ready = False
        return PlainTextResponse(
            "ok" if ready else "unavailable", status_code=200 if ready else 503
        )

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        del app
        try:
            if not await asyncio.to_thread(session_store.ping):
                raise RuntimeError("Session storage is unavailable")
            if not await asyncio.to_thread(auth_store.ping):
                raise RuntimeError("Authentication storage is unavailable")
            async with session_manager.run():
                yield
        finally:
            if pool is not None:
                await asyncio.to_thread(pool.close)

    endpoint = MCPEndpoint()
    routes = [Route("/healthz", healthz), Route("/mcp", endpoint), Route("/mcp/", endpoint)]
    if isinstance(auth_store, (DynamoKeyStore, PostgresKeyStore)):
        from deep_agentic_core_mcp.signup import RedisSignupLimiter, SignupLimiter, signup_routes

        public_url = os.environ.get("DEEP_AGENTIC_CORE_MCP_PUBLIC_URL", "")
        limiter: SignupLimiter | None = None
        if isinstance(session_store, RedisSessionStore):
            limiter = RedisSignupLimiter(session_store.client)
        elif isinstance(auth_store, PostgresKeyStore):
            limiter = PostgresSignupLimiter(auth_store.pool)
        if not public_url.startswith("https://") or limiter is None:
            raise ValueError(
                "Signup requires an HTTPS public URL and Redis or PostgreSQL for shared"
                " signup limits"
            )
        routes += signup_routes(
            auth_store,
            limiter,
            public_url,
            trusted_proxy_hops=int(os.environ.get("DEEP_AGENTIC_CORE_MCP_TRUSTED_PROXY_HOPS", "0")),
            allowed_origins=allowed_origins,
        )
    app = Starlette(
        routes=routes,
        lifespan=lifespan,
    )
    app.state.db_pool = pool
    return app


def main() -> None:
    """Run the authenticated service; use HTTPS at the load balancer."""
    import uvicorn

    default_hosts = "localhost,localhost:*,127.0.0.1,127.0.0.1:*"
    render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if render_hostname:
        default_hosts += "," + render_hostname
    public_host = urlsplit(os.environ.get("DEEP_AGENTIC_CORE_MCP_PUBLIC_URL", "")).hostname
    if public_host:
        default_hosts += "," + public_host
    hosts = os.environ.get("DEEP_AGENTIC_CORE_MCP_ALLOWED_HOSTS", default_hosts)
    origins = os.environ.get("DEEP_AGENTIC_CORE_MCP_ALLOWED_ORIGINS", "")
    app = create_app(
        allowed_hosts=[value.strip() for value in hosts.split(",") if value.strip()],
        allowed_origins=[value.strip() for value in origins.split(",") if value.strip()],
    )
    uvicorn.run(
        app,
        host=os.environ.get("DEEP_AGENTIC_CORE_MCP_HTTP_HOST", "127.0.0.1"),
        port=int(os.environ.get("DEEP_AGENTIC_CORE_MCP_HTTP_PORT", os.environ.get("PORT", "8000"))),
    )


if __name__ == "__main__":
    main()
