"""Opt-in OAuth authorization-code/PKCE linking to existing bearer-key accounts.

Only operator-registered public clients are accepted. A key is entered on our
consent page, never sent to the OAuth client or persisted in an OAuth record.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import html
import json
import os
import re
import secrets
import time
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from importlib.resources import files
from typing import Any, Protocol, cast
from urllib.parse import parse_qsl, unquote_plus, urlencode, urlsplit

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.routing import Route

from deep_agentic_core_mcp.services.access_policy import Principal, authorize
from deep_agentic_core_mcp.services.api_keys import KeyStore, key_digest
from deep_agentic_core_mcp.services.oauth_store import OAuthStore

SCOPE = "mcp:tools"
TOKEN_PREFIX = "dal_oauth_"
REFRESH_PREFIX = "dal_refresh_"
COOKIE = "__Host-dal-oauth"
_HEADERS = {
    "Cache-Control": "no-store",
    "Pragma": "no-cache",
    "Referrer-Policy": "no-referrer",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Content-Security-Policy": (
        "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
    ),
}


def _https(value: str, *, origin: bool = False) -> bool:
    try:
        parts = urlsplit(value)
        return bool(
            parts.scheme == "https"
            and parts.hostname
            and parts.port in (None, 443)
            and not parts.username
            and not parts.password
            and not parts.fragment
            and not any(c.isspace() or ord(c) < 32 for c in value)
            and (not origin or (parts.path in ("", "/") and not parts.query))
        )
    except ValueError:
        return False


@dataclass(frozen=True)
class OAuthConfig:
    public_url: str
    clients: Mapping[str, Any]
    access_token_seconds: int = 3600
    trusted_proxy_hops: int = 0
    refresh_idle_seconds: int = 30 * 86400
    refresh_max_seconds: int = 90 * 86400

    def __post_init__(self) -> None:
        if self.trusted_proxy_hops < 0:
            raise ValueError("OAuth trusted proxy hops must be nonnegative")
        if not _https(self.public_url, origin=True):
            raise ValueError("OAuth requires an HTTPS public origin")
        if not 60 <= self.access_token_seconds <= 86400:
            raise ValueError("OAuth access token lifetime must be between 60 and 86400 seconds")
        if not self.access_token_seconds <= self.refresh_idle_seconds <= self.refresh_max_seconds:
            raise ValueError("OAuth refresh lifetime must cover access tokens and fit maximum")
        if self.refresh_max_seconds > 365 * 86400:
            raise ValueError("OAuth refresh maximum must not exceed one year")
        if not isinstance(self.clients, Mapping) or not self.clients:
            raise ValueError("OAuth requires explicitly registered clients")
        for client_id, entry in self.clients.items():
            if not isinstance(client_id, str) or not 1 <= len(client_id) <= 256:
                raise ValueError("OAuth client IDs must be strings of 1–256 characters")
            required = {"name", "redirect_uris"}
            if (
                not isinstance(entry, dict)
                or not required <= set(entry)
                or set(entry) - required - {"client_secret_sha256"}
            ):
                raise ValueError("OAuth clients require name and redirect_uris")
            if "client_secret_sha256" in entry and (
                not isinstance(entry["client_secret_sha256"], str)
                or not re.fullmatch(r"[a-f0-9]{64}", entry["client_secret_sha256"])
            ):
                raise ValueError("OAuth client secret must be a lowercase SHA-256 digest")
            if not isinstance(entry["name"], str) or not 1 <= len(entry["name"]) <= 100:
                raise ValueError("OAuth client name must have 1–100 characters")
            uris = entry["redirect_uris"]
            if (
                not isinstance(uris, list)
                or not uris
                or len(uris) > 20
                or any(not isinstance(uri, str) or not _https(uri) for uri in uris)
            ):
                raise ValueError("OAuth redirects must be exact HTTPS URLs without fragments")
            for uri in uris:
                if {key for key, _ in parse_qsl(urlsplit(uri).query)} & {"code", "error", "state"}:
                    raise ValueError("OAuth redirects cannot contain reserved response parameters")

    @property
    def origin(self) -> str:
        return self.public_url.rstrip("/")

    @property
    def resource(self) -> str:
        return self.origin + "/mcp"


class OAuthKeyStore(KeyStore, Protocol):
    def authorize_digest(self, digest: str) -> Principal | None: ...


class OAuthServer:
    def __init__(self, config: OAuthConfig, records: OAuthStore, keys: KeyStore) -> None:
        if not callable(getattr(keys, "authorize_digest", None)):
            raise ValueError("OAuth requires a key store supporting authorize_digest")
        self.config, self.records = config, records
        self.keys = cast(OAuthKeyStore, keys)

    @property
    def challenge(self) -> str:
        return (
            f'Bearer resource_metadata="{self.config.origin}/.well-known/oauth-protected-resource",'
            f' scope="{SCOPE}"'
        )

    def authorize_token(self, token: str) -> Principal | None:
        if not token.startswith(TOKEN_PREFIX):
            return authorize(self.keys, token)
        if len(token) > 256:
            return None
        grant = self.records.get("access", token)
        if (
            not grant
            or grant["resource"] != self.config.resource
            or grant["scope"] != SCOPE
            or grant["client_id"] not in self.config.clients
        ):
            return None
        if grant.get("family"):
            family = self.records.get("family", grant["family"])
            if not family or family["absolute_expiry"] <= time.time():
                return None
        # Re-read the account and current key policy on every request AND dispatch.
        # Key rotation, account revocation and policy edits therefore affect OAuth too.
        lookup: Callable[[str], Principal | None] = self.keys.authorize_digest
        principal = lookup(grant["key_hash"])
        return principal if principal and principal.user == grant["user"] else None

    @staticmethod
    def error(code: str, status: int = 400) -> JSONResponse:
        return JSONResponse({"error": code}, status_code=status, headers=_HEADERS)

    async def _form(self, request: Request) -> dict[str, str] | None:
        if request.headers.get("content-type", "").split(";")[0] != (
            "application/x-www-form-urlencoded"
        ):
            return None
        body = bytearray()
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > 8192:
                return None
        try:
            pairs = parse_qsl(body.decode("utf-8"), keep_blank_values=True, max_num_fields=20)
        except (ValueError, UnicodeDecodeError):
            return None
        if len(dict(pairs)) != len(pairs):
            return None
        return dict(pairs)

    async def protected_metadata(self, request: Request) -> Response:
        del request
        return JSONResponse(
            {
                "resource": self.config.resource,
                "authorization_servers": [self.config.origin],
                "scopes_supported": [SCOPE],
                "bearer_methods_supported": ["header"],
            },
            headers=_HEADERS,
        )

    async def authorization_metadata(self, request: Request) -> Response:
        del request
        return JSONResponse(
            {
                "issuer": self.config.origin,
                "authorization_endpoint": self.config.origin + "/oauth/authorize",
                "token_endpoint": self.config.origin + "/oauth/token",
                "revocation_endpoint": self.config.origin + "/oauth/revoke",
                "response_types_supported": ["code"],
                "grant_types_supported": ["authorization_code", "refresh_token"],
                "token_endpoint_auth_methods_supported": self.client_auth_methods(),
                "revocation_endpoint_auth_methods_supported": self.client_auth_methods(),
                "code_challenge_methods_supported": ["S256"],
                "scopes_supported": [SCOPE],
                "authorization_response_iss_parameter_supported": True,
            },
            headers=_HEADERS,
        )

    async def authorize_page(self, request: Request) -> Response:
        pairs = list(request.query_params.multi_items())
        data = dict(pairs)
        if len(pairs) != len(data) or len(str(request.url.query)) > 8192:
            return self.error("invalid_request")
        client = self.config.clients.get(data.get("client_id", ""))
        if not client or data.get("redirect_uri") not in client["redirect_uris"]:
            # Never redirect until the client and exact callback are trusted.
            return self.error("invalid_client")
        if data.get("response_type") != "code":
            return self.error("unsupported_response_type")
        if data.get("resource") != self.config.resource:
            return self.error("invalid_target")
        if data.get("scope", SCOPE) != SCOPE:
            return self.error("invalid_scope")
        challenge = data.get("code_challenge", "")
        if data.get("code_challenge_method") != "S256" or not re.fullmatch(
            r"[A-Za-z0-9_-]{43}", challenge
        ):
            return self.error("invalid_request")
        if not 1 <= len(data.get("state", "")) <= 1024:
            return self.error("invalid_request")
        pending, browser = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        cookie_name = COOKIE + "-" + key_digest(pending)[:16]
        await asyncio.to_thread(
            self.records.put,
            "pending",
            pending,
            {
                "client_id": data["client_id"],
                "redirect_uri": data["redirect_uri"],
                "resource": self.config.resource,
                "scope": SCOPE,
                "state": data["state"],
                "code_challenge": challenge,
                "browser_hash": key_digest(browser),
                "cookie_name": cookie_name,
            },
            600,
        )
        response = self.consent_response(data["client_id"], pending)
        response.set_cookie(
            cookie_name, browser, max_age=600, secure=True, httponly=True, samesite="lax"
        )
        return response

    def consent_response(
        self, client_id: str, pending: str, *, error: str = "", status: int = 200
    ) -> HTMLResponse:
        """Render a script-free, browser-compatible consent form."""
        client = self.config.clients[client_id]
        content = files("deep_agentic_core_mcp").joinpath("web/oauth.html").read_text()
        client_hosts = {urlsplit(uri).hostname for uri in client["redirect_uris"]}
        if "chatgpt.com" in client_hosts:
            client_icon = '<img src="/oauth-assets/openai.svg" alt="" width="36" height="36">'
        elif "claude.ai" in client_hosts:
            client_icon = (
                '<img class="claude-logo" src="/oauth-assets/claude.svg" '
                'alt="" width="32" height="32">'
            )
        else:
            client_icon = html.escape(client["name"][:1].upper(), quote=True)
        values = {
            "client_name": html.escape(client["name"], quote=True),
            "client_icon": client_icon,
            "asset_version": hashlib.sha256(
                files("deep_agentic_core_mcp").joinpath("web/oauth.css").read_bytes()
            ).hexdigest()[:12],
            "pending": html.escape(pending, quote=True),
            "error": '<p class="form-error" role="alert">' + html.escape(error) + "</p>"
            if error
            else "",
        }
        content = re.sub(
            r"\{\{(client_name|client_icon|asset_version|pending|error)\}\}",
            lambda match: values[match[1]],
            content,
        )
        # A browser form inherits this policy. no-referrer causes Origin: null
        # on POST and fails the same-origin CSRF check. Keep off-site referrers private.
        headers = {**_HEADERS, "Referrer-Policy": "same-origin"}
        # Chromium also checks form redirects against form-action. Permit only
        # the registered client's callback origins; exact redirects are validated separately.
        callbacks = sorted({"https://" + urlsplit(uri).netloc for uri in client["redirect_uris"]})
        headers["Content-Security-Policy"] += (
            " " + " ".join(callbacks) + "; style-src 'self'; img-src 'self'"
        )
        return HTMLResponse(content, status_code=status, headers=headers)

    async def stylesheet(self, request: Request) -> Response:
        del request
        return Response(
            files("deep_agentic_core_mcp").joinpath("web/oauth.css").read_text(),
            media_type="text/css",
            headers={"Cache-Control": "public, max-age=3600", "X-Content-Type-Options": "nosniff"},
        )

    async def branding_asset(self, request: Request) -> Response:
        assets = {
            "deepagentlabs.png": "image/png",
            "openai.svg": "image/svg+xml",
            "claude.svg": "image/svg+xml",
        }
        name = request.path_params["name"]
        if name not in assets:
            return Response(status_code=404)
        return Response(
            files("deep_agentic_core_mcp").joinpath("web/" + name).read_bytes(),
            media_type=assets[name],
            headers={
                "Cache-Control": "public, max-age=3600",
                "X-Content-Type-Options": "nosniff",
                "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
            },
        )

    def _redirect(self, pending: dict[str, Any], **result: str) -> Response:
        query = {**result, "state": pending["state"], "iss": self.config.origin}
        separator = "&" if "?" in pending["redirect_uri"] else "?"
        response = RedirectResponse(
            pending["redirect_uri"] + separator + urlencode(query), 303, headers=_HEADERS
        )
        response.delete_cookie(
            pending.get("cookie_name", COOKIE), secure=True, httponly=True, samesite="lax"
        )
        return response

    async def approve(self, request: Request) -> Response:
        if request.headers.get("origin") != self.config.origin:
            return self.error("invalid_request", 403)
        form = await self._form(request)
        if not form or form.get("decision") not in {"allow", "deny"}:
            return self.error("invalid_request")
        secret = form.get("pending", "")
        pending = await asyncio.to_thread(self.records.get, "pending", secret)
        cookie_name = pending.get("cookie_name", COOKIE) if pending else COOKIE
        browser = request.cookies.get(cookie_name, "")
        if (
            not pending
            or not browser
            or not secrets.compare_digest(pending["browser_hash"], key_digest(browser))
        ):
            return self.error("invalid_request", 403)
        principal = None
        key = form.get("api_key", "")
        if form["decision"] == "allow":
            if not 32 <= len(key) <= 256:
                return self.consent_response(
                    pending["client_id"],
                    secret,
                    error="That API key wasn't accepted. Check your key and try again.",
                    status=401,
                )
            principal = await asyncio.to_thread(authorize, self.keys, key)
            if principal is None or principal.policy.error or principal.policy.expired():
                return self.consent_response(
                    pending["client_id"],
                    secret,
                    error="That API key wasn't accepted. Check your key and try again.",
                    status=401,
                )
        pending = await asyncio.to_thread(self.records.take, "pending", secret)
        if pending is None:
            return self.error("invalid_request")
        if form["decision"] == "deny":
            return self._redirect(pending, error="access_denied")
        assert principal is not None
        code = secrets.token_urlsafe(32)
        grant = {
            k: pending[k]
            for k in ("client_id", "redirect_uri", "resource", "scope", "code_challenge")
        }
        grant.update(user=principal.user, key_hash=key_digest(key))
        await asyncio.to_thread(self.records.put, "code", code, grant, 120)
        return self._redirect(pending, code=code)

    def client_auth_methods(self) -> list[str]:
        methods = []
        if any("client_secret_sha256" not in client for client in self.config.clients.values()):
            methods.append("none")
        if any("client_secret_sha256" in client for client in self.config.clients.values()):
            methods += ["client_secret_basic", "client_secret_post"]
        return methods

    def authenticate_client(self, request: Request, form: dict[str, str]) -> bool:
        """Authenticate before consuming a code, rotating tokens or revoking a family."""
        headers = request.headers.getlist("authorization")
        if len(headers) > 1:
            return False
        secret = form.get("client_secret", "")
        if headers:
            scheme, separator, encoded = headers[0].partition(" ")
            if not separator or scheme.lower() != "basic" or len(encoded) > 2048:
                return False
            if "client_secret" in form:
                return False  # RFC 6749: never combine authentication methods.
            try:
                decoded = base64.b64decode(encoded, validate=True).decode("utf-8")
                client_id, colon, password = decoded.partition(":")
                if not colon:
                    return False
                client_id = unquote_plus(client_id, errors="strict")
                secret = unquote_plus(password, errors="strict")
            except (ValueError, UnicodeError):
                return False
            if "client_id" in form and form["client_id"] != client_id:
                return False
            form["client_id"] = client_id
        client = self.config.clients.get(form.get("client_id", ""))
        if client is None:
            return False
        expected = client.get("client_secret_sha256")
        if expected is None:
            return not headers and not secret
        return bool(
            1 <= len(secret) <= 512
            and secrets.compare_digest(hashlib.sha256(secret.encode()).hexdigest(), expected)
        )

    def client_error(self) -> JSONResponse:
        response = self.error("invalid_client", 401)
        response.headers["WWW-Authenticate"] = 'Basic realm="oauth"'
        return response

    async def token(self, request: Request) -> Response:
        form = await self._form(request)
        if not form:
            return self.error("invalid_request")
        if not self.authenticate_client(request, form):
            return self.client_error()
        if form.get("grant_type") == "refresh_token":
            return await self.refresh(form)
        if form.get("grant_type") != "authorization_code":
            return self.error("unsupported_grant_type")
        if form.get("resource") != self.config.resource:
            return self.error("invalid_target")
        code = form.get("code", "")
        if not 1 <= len(code) <= 256:
            return self.error("invalid_grant")
        grant = await asyncio.to_thread(self.records.take, "code", code)
        verifier = form.get("code_verifier", "")
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        if (
            not grant
            or grant["client_id"] != form["client_id"]
            or grant["redirect_uri"] != form.get("redirect_uri")
            or grant["resource"] != form["resource"]
            or not re.fullmatch(r"[A-Za-z0-9._~-]{43,128}", verifier)
            or not secrets.compare_digest(challenge.rstrip(b"=").decode(), grant["code_challenge"])
        ):
            return self.error("invalid_grant")
        lookup: Callable[[str], Principal | None] = self.keys.authorize_digest
        principal = await asyncio.to_thread(lookup, grant["key_hash"])
        if (
            principal is None
            or principal.user != grant["user"]
            or principal.policy.error
            or principal.policy.expired()
        ):
            return self.error("invalid_grant")
        family_id = secrets.token_urlsafe(32)
        grant["family"] = family_id
        grant["absolute_expiry"] = int(time.time()) + self.config.refresh_max_seconds
        refresh = REFRESH_PREFIX + secrets.token_urlsafe(36)
        family = {**grant, "refresh_hash": key_digest(refresh)}
        await asyncio.to_thread(
            self.records.put, "family", family_id, family, self.config.refresh_idle_seconds
        )
        return await self.issue_pair(grant, refresh)

    async def issue_pair(self, grant: dict[str, Any], refresh: str) -> Response:
        """Persist only token hashes; retain refresh ancestry until the maximum expiry."""
        remaining = int(grant["absolute_expiry"] - time.time())
        if remaining < 1:
            return self.error("invalid_grant")
        await asyncio.to_thread(
            self.records.put,
            "refresh",
            refresh,
            {"family": grant["family"], "client_id": grant["client_id"]},
            remaining,
        )
        access = TOKEN_PREFIX + secrets.token_urlsafe(36)
        access_seconds = min(self.config.access_token_seconds, remaining)
        await asyncio.to_thread(self.records.put, "access", access, grant, access_seconds)
        return JSONResponse(
            {
                "access_token": access,
                "token_type": "Bearer",
                "expires_in": access_seconds,
                "scope": grant["scope"],
                "refresh_token": refresh,
            },
            headers=_HEADERS,
        )

    async def refresh(self, form: dict[str, str]) -> Response:
        token = form.get("refresh_token", "")
        if not token.startswith(REFRESH_PREFIX) or len(token) > 256:
            return self.error("invalid_grant")
        reference = await asyncio.to_thread(self.records.get, "refresh", token)
        if not reference or reference["client_id"] != form["client_id"]:
            return self.error("invalid_grant")
        family_id = reference["family"]
        family = await asyncio.to_thread(self.records.get, "family", family_id)
        if not family or family["client_id"] != form["client_id"]:
            return self.error("invalid_grant")
        if (
            family["resource"] != self.config.resource
            or form.get("resource", family["resource"]) != family["resource"]
        ):
            return self.error("invalid_target")
        if form.get("scope", family["scope"]) != family["scope"]:
            return self.error("invalid_scope")
        if not secrets.compare_digest(family["refresh_hash"], key_digest(token)):
            # Reuse of any ancestor invalidates the entire connection, including
            # access tokens and the latest descendant refresh token (RFC 9700).
            await asyncio.to_thread(self.records.take, "family", family_id)
            return self.error("invalid_grant")
        principal = await asyncio.to_thread(self.keys.authorize_digest, family["key_hash"])
        if (
            principal is None
            or principal.user != family["user"]
            or principal.policy.error
            or principal.policy.expired()
        ):
            await asyncio.to_thread(self.records.take, "family", family_id)
            return self.error("invalid_grant")
        remaining = int(family["absolute_expiry"] - time.time())
        if remaining < 1:
            return self.error("invalid_grant")
        refresh = REFRESH_PREFIX + secrets.token_urlsafe(36)
        updated = {**family, "refresh_hash": key_digest(refresh)}
        rotated = await asyncio.to_thread(
            self.records.compare_swap,
            "family",
            family_id,
            family,
            updated,
            min(self.config.refresh_idle_seconds, remaining),
        )
        if not rotated:
            # A concurrent renewal/revocation won. Never leave a raced token valid.
            await asyncio.to_thread(self.records.take, "family", family_id)
            return self.error("invalid_grant")
        grant = {k: value for k, value in updated.items() if k != "refresh_hash"}
        return await self.issue_pair(grant, refresh)

    async def revoke(self, request: Request) -> Response:
        form = await self._form(request)
        if not form or len(form.get("token", "")) > 256:
            return self.error("invalid_request")
        if not self.authenticate_client(request, form):
            return self.client_error()
        token = form.get("token", "")
        kind = "refresh" if token.startswith(REFRESH_PREFIX) else "access"
        grant = await asyncio.to_thread(self.records.get, kind, token)
        if grant and grant["client_id"] == form["client_id"]:
            if grant.get("family"):
                await asyncio.to_thread(self.records.take, "family", grant["family"])
            else:
                await asyncio.to_thread(self.records.take, "access", token)
        return Response(status_code=200, headers=_HEADERS)

    def routes(self) -> list[Route]:
        def guarded(
            handler: Callable[[Request], Awaitable[Response]],
        ) -> Callable[[Request], Awaitable[Response]]:
            async def endpoint(request: Request) -> Response:
                try:
                    host = request.headers.get("host", "").lower()
                    expected = urlsplit(self.config.origin).netloc.lower()
                    if host not in {expected, expected.removesuffix(":443") + ":443"}:
                        return self.error("invalid_request", 421)
                    if request.url.path.startswith("/oauth/"):
                        peer = request.client.host if request.client else "unknown"
                        if self.config.trusted_proxy_hops:
                            forwarded = request.headers.get("x-forwarded-for", "").split(",")
                            if len(forwarded) < self.config.trusted_proxy_hops:
                                return self.error("temporarily_unavailable", 503)
                            peer = forwarded[-self.config.trusted_proxy_hops].strip()
                        if not await asyncio.to_thread(self.records.allow, peer):
                            response: Response = self.error("temporarily_unavailable", 429)
                            response.headers["Retry-After"] = "60"
                            return response
                    response = await handler(request)
                    return response
                except Exception:
                    # Storage outages fail closed; never expose credentials or internals.
                    return self.error("temporarily_unavailable", 503)

            return endpoint

        return [
            Route("/.well-known/oauth-protected-resource", guarded(self.protected_metadata)),
            Route("/.well-known/oauth-protected-resource/mcp", guarded(self.protected_metadata)),
            Route("/.well-known/oauth-authorization-server", guarded(self.authorization_metadata)),
            Route("/oauth.css", guarded(self.stylesheet)),
            Route("/oauth-assets/{name}", guarded(self.branding_asset)),
            Route("/oauth/authorize", guarded(self.authorize_page), methods=["GET"]),
            Route("/oauth/authorize", guarded(self.approve), methods=["POST"]),
            Route("/oauth/token", guarded(self.token), methods=["POST"]),
            Route("/oauth/revoke", guarded(self.revoke), methods=["POST"]),
        ]


def config_from_environment(public_url: str, raw_clients: str) -> OAuthConfig:
    """Validate opt-in operator settings; no implicit or wildcard callback registration."""
    clients = json.loads(raw_clients)
    directory = json.loads(os.environ.get("DEEP_AGENTIC_CORE_MCP_OAUTH_DIRECTORY_CLIENTS", "{}"))
    if not isinstance(clients, dict) or not isinstance(directory, dict):
        raise ValueError("OAuth client registrations must be objects")
    if clients.keys() & directory.keys():
        raise ValueError("Directory OAuth clients cannot overwrite existing clients")
    if any(
        not isinstance(entry, dict) or "client_secret_sha256" not in entry
        for entry in directory.values()
    ):
        raise ValueError("Directory OAuth clients require a client-secret digest")
    return OAuthConfig(
        public_url,
        {**clients, **directory},
        trusted_proxy_hops=int(os.environ.get("DEEP_AGENTIC_CORE_MCP_TRUSTED_PROXY_HOPS", "0")),
        refresh_idle_seconds=int(
            os.environ.get("DEEP_AGENTIC_CORE_MCP_OAUTH_REFRESH_IDLE", "2592000")
        ),
        refresh_max_seconds=int(
            os.environ.get("DEEP_AGENTIC_CORE_MCP_OAUTH_REFRESH_MAX", "7776000")
        ),
    )
