"""Public key signup and bearer-authenticated account management."""

from __future__ import annotations

import asyncio
import hashlib
import json
from importlib.resources import files
from typing import Any, Protocol

from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from deep_agentic_core_mcp.services.api_keys import DynamoKeyStore


class SignupLimiter(Protocol):
    def allow(self, peer: str) -> bool: ...


class RedisSignupLimiter:
    """Shared limits: 10 signups/hour/client and 100/day across the service."""

    def __init__(self, client: Any) -> None:
        self.client = client

    def allow(self, peer: str) -> bool:
        script = """
        if tonumber(redis.call('GET', KEYS[1]) or '0') >= 10 or
           tonumber(redis.call('GET', KEYS[2]) or '0') >= 100 then return 0 end
        if redis.call('INCR', KEYS[1]) == 1 then redis.call('EXPIRE', KEYS[1], 3600) end
        if redis.call('INCR', KEYS[2]) == 1 then redis.call('EXPIRE', KEYS[2], 86400) end
        return 1
        """
        return bool(
            self.client.eval(
                script,
                2,
                "mcp:signup:ip:" + hashlib.sha256(peer.encode()).hexdigest(),
                "mcp:signup:global",
            )
        )


def signup_routes(
    keys: DynamoKeyStore,
    limiter: SignupLimiter,
    public_url: str,
    *,
    trusted_proxy_hops: int = 0,
    allowed_origins: list[str] | None = None,
) -> list[Route]:
    """Expose a small signup portal; there are no cookies, passwords, or login sessions."""
    origin = public_url.rstrip("/")
    browser_origins = {origin, *(allowed_origins or [])}
    headers = {
        "Cache-Control": "no-store",
        "Content-Security-Policy": (
            "default-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
        ),
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "no-referrer",
        "X-Frame-Options": "DENY",
    }

    def reply(payload: dict[str, Any], status: int = 200) -> Response:
        return Response(json.dumps(payload), status, headers=headers, media_type="application/json")

    async def page(request: Request) -> Response:
        del request
        content = files("deep_agentic_core_mcp").joinpath("web/signup.html").read_text()
        return Response(content, headers=headers, media_type="text/html")

    async def script(request: Request) -> Response:
        del request
        content = files("deep_agentic_core_mcp").joinpath("web/signup.js").read_text()
        return Response(content, headers=headers, media_type="application/javascript")

    async def stylesheet(request: Request) -> Response:
        del request
        content = files("deep_agentic_core_mcp").joinpath("web/signup.css").read_text()
        return Response(content, headers=headers, media_type="text/css")

    async def signup(request: Request) -> Response:
        if request.headers.get("origin", origin) not in browser_origins:
            return reply({"error": "Origin not allowed"}, 403)
        if request.headers.get("content-type", "").split(";")[0] != "application/json":
            return reply({"error": "Send application/json"}, 415)
        body = bytearray()
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > 4096:
                return reply({"error": "Signup request too large"}, 413)
        try:
            data = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            return reply({"error": "Invalid JSON"}, 400)
        name = data.get("display_name") if isinstance(data, dict) else None
        if not isinstance(name, str) or not 2 <= len(name.strip()) <= 80:
            return reply({"error": "Enter a display name of 2–80 characters"}, 400)
        peer = request.client.host if request.client else "unknown"
        if trusted_proxy_hops:
            # CloudFront appends the viewer IP; ALB appends the origin IP. Trust
            # this suffix only when ingress is restricted to that proxy chain.
            forwarded = request.headers.get("x-forwarded-for", "").split(",")
            if len(forwarded) < trusted_proxy_hops:
                return reply({"error": "Proxy information unavailable"}, 503)
            peer = forwarded[-trusted_proxy_hops].strip()
        try:
            if not await asyncio.to_thread(limiter.allow, peer):
                response = reply({"error": "Signup limit reached. Please try again later."}, 429)
                response.headers["Retry-After"] = "3600"
                return response
            result = await asyncio.to_thread(keys.issue, name.strip())
        except Exception:
            return reply({"error": "Signup temporarily unavailable"}, 503)
        return reply({**result, "mcp_url": origin + "/mcp"}, 201)

    async def account(request: Request) -> Response:
        if request.headers.get("origin", origin) not in browser_origins:
            return reply({"error": "Origin not allowed"}, 403)
        scheme, _, token = request.headers.get("authorization", "").partition(" ")
        if scheme.lower() != "bearer":
            return reply({"error": "Your MCP key is required"}, 401)
        try:
            user = await asyncio.to_thread(keys.authenticate, token)
            if user is None:
                return reply({"error": "Invalid or revoked MCP key"}, 401)
            if request.method == "POST":
                result = await asyncio.to_thread(keys.rotate, user, token)
            elif request.method == "DELETE":
                await asyncio.to_thread(keys.revoke, user, token)
                result = {"status": "revoked"}
            else:
                result = await asyncio.to_thread(keys.profile, user)
        except keys.client.exceptions.TransactionCanceledException:
            return reply({"error": "Account changed. Retry with your current key."}, 409)
        except keys.client.exceptions.ConditionalCheckFailedException:
            return reply({"error": "Account changed. Retry with your current key."}, 409)
        except Exception:
            return reply({"error": "Account temporarily unavailable"}, 503)
        return reply({**result, "mcp_url": origin + "/mcp"})

    return [
        Route("/", page),
        Route("/signup", page),
        Route("/signup.js", script),
        Route("/signup.css", stylesheet),
        Route("/api/signup", signup, methods=["POST"]),
        Route("/api/account", account, methods=["GET", "POST", "DELETE"]),
    ]
