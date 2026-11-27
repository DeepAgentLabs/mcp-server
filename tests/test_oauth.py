"""OAuth protocol, tenant identity, revocation and multi-worker storage boundaries."""

import base64
import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import parse_qs, urlsplit

import fakeredis
import httpx
import pytest

from deep_agentic_core_mcp.oauth import COOKIE, OAuthConfig, OAuthServer
from deep_agentic_core_mcp.services.access_policy import AccessPolicy
from deep_agentic_core_mcp.services.api_keys import StaticKeyStore, key_digest
from deep_agentic_core_mcp.services.oauth_store import MemoryOAuthStore, RedisOAuthStore
from deep_agentic_core_mcp.services.remote_sessions import MemorySessionStore
from deep_agentic_core_mcp.transport_http import create_app

ORIGIN = "https://mcp.example.com"
CALLBACK = "https://chatgpt.com/connector/oauth/test-callback"
CLIENTS = {"chatgpt-test": {"name": "ChatGPT", "redirect_uris": [CALLBACK]}}
KEY = "a" * 40
VERIFIER = "v" * 64
CHALLENGE = (
    base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).rstrip(b"=").decode()
)


@pytest.fixture
def setup(monkeypatch):
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_DATABASE_URL", raising=False)
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_OAUTH_CLIENTS", raising=False)
    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_REMOTE", "0")
    keys = StaticKeyStore({"alice": KEY, "bob": "b" * 40})
    records = MemoryOAuthStore()
    config = OAuthConfig(ORIGIN, json.loads(json.dumps(CLIENTS)))
    app = create_app(
        key_store=keys,
        store=MemorySessionStore(),
        oauth_config=config,
        oauth_store=records,
        allowed_hosts=["mcp.example.com"],
    )
    return app, keys, records, config


def params(**overrides):
    return {
        "client_id": "chatgpt-test",
        "redirect_uri": CALLBACK,
        "response_type": "code",
        "resource": ORIGIN + "/mcp",
        "scope": "mcp:tools",
        "state": "state-from-chatgpt",
        "code_challenge": CHALLENGE,
        "code_challenge_method": "S256",
        **overrides,
    }


async def consent(client, key=KEY, decision="allow", **overrides):
    page = await client.get("/oauth/authorize", params=params(**overrides))
    assert page.status_code == 200, page.text
    pending = re.search(r'name="pending" value="([^"]+)"', page.text)[1]
    response = await client.post(
        "/oauth/authorize",
        headers={"Origin": ORIGIN},
        data={"pending": pending, "api_key": key, "decision": decision},
    )
    return response


async def code_for(client, **kwargs):
    response = await consent(client, **kwargs)
    assert response.status_code == 303, response.text
    query = parse_qs(urlsplit(response.headers["location"]).query)
    assert query["state"] == ["state-from-chatgpt"]
    assert query["iss"] == [ORIGIN]
    assert KEY not in response.headers["location"]
    return query["code"][0]


def exchange(code, **overrides):
    return {
        "grant_type": "authorization_code",
        "client_id": "chatgpt-test",
        "redirect_uri": CALLBACK,
        "resource": ORIGIN + "/mcp",
        "code_verifier": VERIFIER,
        "code": code,
        **overrides,
    }


async def rpc(client, token, method="tools/call", arguments=None):
    return await client.post(
        "/mcp",
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2025-11-25",
        },
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": arguments or {"name": "core.access_status", "arguments": {}},
        },
    )


@pytest.mark.asyncio
async def test_oauth_end_to_end_same_identity_and_key_still_works(setup):
    app, keys, records, config = setup
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client,
    ):
        denied = await client.get("/mcp")
        assert denied.status_code == 401
        assert 'resource_metadata="' in denied.headers["WWW-Authenticate"]
        metadata = await client.get("/.well-known/oauth-protected-resource/mcp")
        assert metadata.json()["resource"] == config.resource
        metadata = await client.get("/.well-known/oauth-authorization-server")
        assert metadata.json()["code_challenge_methods_supported"] == ["S256"]
        assert "refresh_token" in metadata.json()["grant_types_supported"]
        assert "registration_endpoint" not in metadata.json()
        code = await code_for(client)
        response = await client.post("/oauth/token", data=exchange(code))
        assert response.status_code == 200, response.text
        assert response.headers["Cache-Control"] == "no-store"
        token = response.json()["access_token"]
        assert token != KEY and response.json()["expires_in"] == 3600
        for credential in (token, KEY):
            result = await rpc(client, credential)
            assert result.status_code == 200, result.text
            payload = json.loads(result.json()["result"]["content"][0]["text"])
            assert payload["subject"] == "alice"
        assert OAuthServer(config, records, keys).authorize_token(token).user == "alice"
        # Stored records contain neither the original key, code nor access token.
        serialized = repr(records.records)
        assert KEY not in serialized and code not in serialized and token not in serialized
        assert (await client.post("/oauth/token", data=exchange(code))).status_code == 400
        revoked = await client.post(
            "/oauth/revoke", data={"client_id": "chatgpt-test", "token": token}
        )
        assert revoked.status_code == 200
        assert (await rpc(client, token)).status_code == 401
        assert (await rpc(client, KEY)).status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "change",
    [
        {"redirect_uri": "https://evil.example/callback"},
        {"redirect_uri": CALLBACK + "/extra"},
        {"client_id": "unknown"},
        {"code_challenge_method": "plain"},
        {"code_challenge": "bad"},
        {"resource": "https://other.example/mcp"},
        {"scope": "admin"},
        {"state": ""},
        {"response_type": "token"},
    ],
)
async def test_reject_invalid_authorization_without_redirect(setup, change):
    app, *_ = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        response = await client.get("/oauth/authorize", params=params(**change))
        assert response.status_code == 400
        assert "location" not in response.headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "change",
    [
        {"code_verifier": "w" * 64},
        {"code_verifier": "short"},
        {"redirect_uri": CALLBACK + "/other"},
        {"client_id": "unknown"},
        {"resource": "https://other.example/mcp"},
        {"grant_type": "client_credentials"},
    ],
)
async def test_exchange_binding(setup, change):
    app, *_ = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        code = await code_for(client)
        response = await client.post("/oauth/token", data=exchange(code, **change))
        assert response.status_code in (400, 401)
        assert "access_token" not in response.json()


@pytest.mark.asyncio
async def test_browser_binding_origin_and_consent_denial(setup):
    app, *_ = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        page = await client.get("/oauth/authorize", params=params())
        cookie = page.headers["set-cookie"]
        assert "Secure" in cookie and "HttpOnly" in cookie and "SameSite=lax" in cookie
        pending = re.search(r'name="pending" value="([^"]+)"', page.text)[1]
        form = {"pending": pending, "api_key": KEY, "decision": "allow"}
        assert (await client.post("/oauth/authorize", data=form)).status_code == 403
        assert (
            await client.post(
                "/oauth/authorize", data=form, headers={"Origin": "https://evil.example"}
            )
        ).status_code == 403
        assert (
            await client.post("/oauth/authorize", data=form, headers={"Origin": "null"})
        ).status_code == 403
        client.cookies.clear()
        assert (
            await client.post("/oauth/authorize", data=form, headers={"Origin": ORIGIN})
        ).status_code == 403
        denied = await consent(client, decision="deny")
        assert parse_qs(urlsplit(denied.headers["location"]).query)["error"] == ["access_denied"]
        assert (await consent(client, key="wrong" * 10)).status_code == 401


@pytest.mark.asyncio
async def test_policy_changes_rotation_and_expiry_apply_to_oauth(setup):
    app, keys, records, config = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        code = await code_for(client)
        issued = await client.post("/oauth/token", data=exchange(code))
        token = issued.json()["access_token"]
        oauth = OAuthServer(config, records, keys)
        keys.policies["alice"] = AccessPolicy(allow=("core.*",))
        assert oauth.authorize_token(token).policy.allow == ("core.*",)
        assert oauth.authorize_token(token).user != "bob"
        expiry, payload = records.records["access", key_digest(token)]
        records.records["access", key_digest(token)] = (0, payload)
        assert oauth.authorize_token(token) is None
        records.records["access", key_digest(token)] = (expiry, payload)
        keys.credentials.pop(key_digest(KEY))
        assert oauth.authorize_token(token) is None


@pytest.mark.asyncio
async def test_duplicate_parameters_body_limits_expired_code_and_unavailable_store(setup):
    app, _, records, _ = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        duplicate = list(params().items()) + [("client_id", "other")]
        assert (await client.get("/oauth/authorize", params=duplicate)).status_code == 400
        assert (await client.post("/oauth/token", json={})).status_code == 400
        assert (
            await client.post(
                "/oauth/token",
                content="x" * 9000,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        ).status_code == 400
        code = await code_for(client)
        _, value = records.records["code", key_digest(code)]
        records.records["code", key_digest(code)] = (0, value)
        assert (await client.post("/oauth/token", data=exchange(code))).status_code == 400

        def unavailable(*args):
            raise RuntimeError("database secret that must not be returned")

        records.allow = unavailable
        response = await client.get("/oauth/authorize", params=params())
        assert response.status_code == 503 and "secret" not in response.text


def test_config_and_no_implicit_memory_fallback(monkeypatch):
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_DATABASE_URL", raising=False)
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_REDIS_URL", raising=False)
    with pytest.raises(ValueError, match="PostgreSQL or Redis"):
        create_app(
            api_keys={"alice": KEY},
            store=MemorySessionStore(),
            oauth_config=OAuthConfig(ORIGIN, CLIENTS),
        )
    for public_url, clients in [
        ("http://insecure.example", CLIENTS),
        (ORIGIN + "/path", CLIENTS),
        (ORIGIN, {}),
        (ORIGIN, {"x": {"name": "X", "redirect_uris": ["http://evil.example"]}}),
        (ORIGIN, {"x": {"name": "X", "redirect_uris": [CALLBACK + "#fragment"]}}),
    ]:
        with pytest.raises(ValueError):
            OAuthConfig(public_url, clients)


@pytest.mark.parametrize("kind", ["memory", "redis"])
def test_store_atomic_single_use_and_shared_workers(kind):
    if kind == "redis":
        client = fakeredis.FakeRedis(decode_responses=True)
        first, second = RedisOAuthStore(client), RedisOAuthStore(client)
    else:
        first = second = MemoryOAuthStore()
    first.put("code", "secret", {"user": "alice"}, 60)
    assert second.get("code", "secret") == {"user": "alice"}
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: second.take("code", "secret"), range(8)))
    assert results.count({"user": "alice"}) == 1
    assert first.get("code", "secret") is None
    assert first.ping()
    assert all(first.allow("peer") for _ in range(60))
    assert not second.allow("peer")


@pytest.mark.asyncio
async def test_oauth_shares_key_sessions_but_not_other_accounts(setup, monkeypatch):
    from deep_agentic_core_mcp.tools import lens

    monkeypatch.setattr(
        lens, "adapter_analyze_workflow", lambda artifact: {"name": artifact["name"]}
    )
    app, keys, *_ = setup
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client,
    ):
        code = await code_for(client)
        token = (await client.post("/oauth/token", data=exchange(code))).json()["access_token"]
        written = await rpc(
            client,
            KEY,
            arguments={
                "name": "lens.analyze_workflow",
                "arguments": {"artifact": {"name": "private-workflow"}, "session_id": "shared"},
            },
        )
        assert not written.json()["result"]["isError"]
        query = {"name": "core.export_report", "arguments": {"session_id": "shared"}}
        for credential in (KEY, token):
            result = await rpc(client, credential, arguments=query)
            assert "private-workflow" in result.text
        bob = await rpc(client, "b" * 40, arguments=query)
        assert "private-workflow" not in bob.text
        keys.policies["alice"] = AccessPolicy(allow=("core.access_status",))
        denied = await rpc(client, token, arguments=query)
        assert denied.json()["result"]["isError"]


@pytest.mark.asyncio
async def test_canonical_host_rate_limit_and_consent_single_use(setup):
    app, _, records, _ = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        page = await client.get("/oauth/authorize", params=params())
        pending = re.search(r'name="pending" value="([^"]+)"', page.text)[1]
        browser = client.cookies.get(COOKIE)
        form = {"pending": pending, "api_key": KEY, "decision": "allow"}
        assert (
            await client.post("/oauth/authorize", data=form, headers={"Origin": ORIGIN})
        ).status_code == 303
        replay = await client.post(
            "/oauth/authorize",
            data=form,
            headers={
                "Origin": ORIGIN,
                "Cookie": COOKIE + "=" + browser,
            },
        )
        assert replay.status_code == 403
        wrong_host = await client.get(
            "/.well-known/oauth-authorization-server", headers={"Host": "evil.example"}
        )
        assert wrong_host.status_code == 421
        records.allow = lambda _: False
        limited = await client.post("/oauth/token", data=exchange("unknown"))
        assert limited.status_code == 429 and limited.headers["Retry-After"] == "60"


@pytest.mark.asyncio
async def test_registered_client_cannot_exchange_or_revoke_another_clients_grant(setup):
    app, keys, records, config = setup
    # Explicit second public client, independently registered by the operator.
    config.clients["second"] = {"name": "Other client", "redirect_uris": [CALLBACK + "/other"]}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        code = await code_for(client)
        wrong = await client.post("/oauth/token", data=exchange(code, client_id="second"))
        assert wrong.status_code == 400
        code = await code_for(client)
        token = (await client.post("/oauth/token", data=exchange(code))).json()["access_token"]
        await client.post("/oauth/revoke", data={"client_id": "second", "token": token})
        oauth = OAuthServer(config, records, keys)
        assert oauth.authorize_token(token).user == "alice"
        del config.clients["chatgpt-test"]
        assert oauth.authorize_token(token) is None


def renewal(token, **overrides):
    return {
        "grant_type": "refresh_token",
        "client_id": "chatgpt-test",
        "refresh_token": token,
        **overrides,
    }


@pytest.mark.asyncio
async def test_refresh_renews_expired_access_without_consent_and_rotates(setup):
    app, keys, records, config = setup
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client,
    ):
        code = await code_for(client)
        issued = (await client.post("/oauth/token", data=exchange(code))).json()
        old_access, old_refresh = issued["access_token"], issued["refresh_token"]
        _, grant = records.records["access", key_digest(old_access)]
        absolute_expiry = grant["absolute_expiry"]
        family_key = ("family", key_digest(grant["family"]))
        _, family = records.records[family_key]
        records.records[family_key] = (time.time() + 60, family)
        records.records["access", key_digest(old_access)] = (0, grant)
        assert (await rpc(client, old_access)).status_code == 401
        renewed = await client.post("/oauth/token", data=renewal(old_refresh))
        assert renewed.status_code == 200, renewed.text
        pair = renewed.json()
        assert pair["access_token"] != old_access and pair["refresh_token"] != old_refresh
        assert pair["expires_in"] == 3600 and pair["scope"] == "mcp:tools"
        assert renewed.headers["Cache-Control"] == "no-store"
        assert (await rpc(client, pair["access_token"])).status_code == 200
        next_grant = records.get("access", pair["access_token"])
        assert next_grant["absolute_expiry"] == absolute_expiry
        assert records.records[family_key][0] > time.time() + 29 * 86400
        assert (
            OAuthServer(config, records, keys).authorize_token(pair["access_token"]).user == "alice"
        )
        serialized = repr(records.records)
        for secret in (KEY, old_refresh, pair["access_token"], pair["refresh_token"]):
            assert secret not in serialized
        # A fresh server instance can use the rotated token without browser cookies.
        another = OAuthServer(config, records, keys)
        assert (await another.refresh(renewal(pair["refresh_token"]))).status_code == 200


@pytest.mark.asyncio
async def test_refresh_replay_revokes_entire_connection_but_not_other_connections(setup):
    app, keys, records, config = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        code = await code_for(client)
        first = (await client.post("/oauth/token", data=exchange(code))).json()
        code = await code_for(client)
        independent = (await client.post("/oauth/token", data=exchange(code))).json()
        second = (await client.post("/oauth/token", data=renewal(first["refresh_token"]))).json()
        replay = await client.post("/oauth/token", data=renewal(first["refresh_token"]))
        assert replay.status_code == 400 and replay.json()["error"] == "invalid_grant"
        oauth = OAuthServer(config, records, keys)
        assert oauth.authorize_token(first["access_token"]) is None
        assert oauth.authorize_token(second["access_token"]) is None
        assert (
            await client.post("/oauth/token", data=renewal(second["refresh_token"]))
        ).status_code == 400
        assert oauth.authorize_token(independent["access_token"]).user == "alice"
        assert keys.authenticate(KEY) == "alice"


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["access_token", "refresh_token"])
async def test_revoking_either_token_ends_automatic_renewal(setup, kind):
    app, keys, records, config = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        pair = (await client.post("/oauth/token", data=exchange(await code_for(client)))).json()
        response = await client.post(
            "/oauth/revoke", data={"client_id": "chatgpt-test", "token": pair[kind]}
        )
        assert response.status_code == 200
        assert OAuthServer(config, records, keys).authorize_token(pair["access_token"]) is None
        assert (
            await client.post("/oauth/token", data=renewal(pair["refresh_token"]))
        ).status_code == 400
        assert keys.authenticate(KEY) == "alice"


@pytest.mark.asyncio
async def test_refresh_cannot_change_client_resource_scope_or_use_api_key(setup):
    app, _, _, config = setup
    config.clients["other"] = {"name": "Other", "redirect_uris": [CALLBACK + "/other"]}
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        pair = (await client.post("/oauth/token", data=exchange(await code_for(client)))).json()
        for overrides, error in [
            ({"client_id": "other"}, "invalid_grant"),
            ({"resource": "https://other.example/mcp"}, "invalid_target"),
            ({"scope": "admin"}, "invalid_scope"),
            ({"refresh_token": KEY}, "invalid_grant"),
            ({"refresh_token": pair["access_token"]}, "invalid_grant"),
        ]:
            response = await client.post(
                "/oauth/token", data=renewal(pair["refresh_token"], **overrides)
            )
            assert response.status_code == 400 and response.json()["error"] == error
        # Invalid binding attempts must not consume the owner's legitimate token.
        response = await client.post(
            "/oauth/token",
            data=renewal(pair["refresh_token"], resource=ORIGIN + "/mcp", scope="mcp:tools"),
        )
        assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("reason", ["idle", "maximum", "key_revoked", "policy_expired"])
async def test_refresh_expiry_and_account_controls(setup, reason):
    app, keys, records, _ = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        pair = (await client.post("/oauth/token", data=exchange(await code_for(client)))).json()
        reference = records.get("refresh", pair["refresh_token"])
        identity = ("family", key_digest(reference["family"]))
        expiry, family = records.records[identity]
        if reason == "idle":
            records.records[identity] = (0, family)
        elif reason == "maximum":
            family["absolute_expiry"] = 0
        elif reason == "key_revoked":
            keys.credentials.pop(key_digest(KEY))
        else:
            keys.policies["alice"] = AccessPolicy(expires_at=1)
        response = await client.post("/oauth/token", data=renewal(pair["refresh_token"]))
        assert response.status_code == 400 and response.json()["error"] == "invalid_grant"


@pytest.mark.asyncio
async def test_racing_refreshes_cannot_leave_a_replayed_connection_active(setup):
    import asyncio

    app, keys, records, config = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        pair = (await client.post("/oauth/token", data=exchange(await code_for(client)))).json()
        results = await asyncio.gather(
            *[client.post("/oauth/token", data=renewal(pair["refresh_token"])) for _ in range(2)]
        )
        assert sorted(response.status_code for response in results) == [200, 400]
        success = next(response.json() for response in results if response.status_code == 200)
        assert OAuthServer(config, records, keys).authorize_token(success["access_token"]) is None


@pytest.mark.parametrize("kind", ["memory", "redis"])
def test_refresh_family_rotation_is_atomic_between_workers(kind):
    if kind == "redis":
        client = fakeredis.FakeRedis(decode_responses=True)
        first, second = RedisOAuthStore(client), RedisOAuthStore(client)
    else:
        first = second = MemoryOAuthStore()
    original = {"refresh_hash": "old"}
    first.put("family", "connection-id", original, 60)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(
            pool.map(
                lambda i: second.compare_swap(
                    "family", "connection-id", original, {"refresh_hash": str(i)}, 60
                ),
                range(8),
            )
        )
    assert results.count(True) == 1
    assert first.get("family", "connection-id") != original
    assert not first.compare_swap("family", "missing", original, {}, 60)
    first.put("family", "expired", original, 60)
    if kind == "memory":
        _, value = first.records["family", key_digest("expired")]
        first.records["family", key_digest("expired")] = (0, value)
    else:
        client.delete(first._key("family", "expired"))
    assert not first.compare_swap("family", "expired", original, {}, 60)


@pytest.mark.parametrize("idle,maximum", [(30, 100), (7200, 3600), (3600, 366 * 86400)])
def test_reject_invalid_refresh_lifetime_configuration(idle, maximum):
    with pytest.raises(ValueError, match="refresh"):
        OAuthConfig(ORIGIN, CLIENTS, refresh_idle_seconds=idle, refresh_max_seconds=maximum)


@pytest.mark.asyncio
async def test_consent_page_headers_styles_and_retry(setup):
    app, *_ = setup
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN) as client:
        page = await client.get("/oauth/authorize", params=params())
        assert page.headers["Referrer-Policy"] == "same-origin"
        csp = page.headers["Content-Security-Policy"]
        assert "form-action 'self' https://chatgpt.com" in csp
        assert "style-src 'self'" in csp and "default-src 'none'" in csp
        assert 'target="_blank" rel="noopener noreferrer"' in page.text
        assert "Create New API Key" in page.text
        assert "(open in new tab)" in page.text
        stylesheet = await client.get("/oauth.css")
        assert stylesheet.status_code == 200
        assert stylesheet.headers["content-type"].startswith("text/css")
        assert ".consent-card" in stylesheet.text
        pending = re.search(r'name="pending" value="([^"]+)"', page.text)[1]
        form = {"pending": pending, "api_key": "wrong" * 10, "decision": "allow"}
        failed = await client.post("/oauth/authorize", data=form, headers={"Origin": ORIGIN})
        assert failed.status_code == 401
        assert 'role="alert"' in failed.text and "try again" in failed.text
        assert form["api_key"] not in failed.text
        assert pending in failed.text
        retried = await client.post(
            "/oauth/authorize", data={**form, "api_key": KEY}, headers={"Origin": ORIGIN}
        )
        assert retried.status_code == 303


def test_consent_escapes_client_name_without_recursive_template_expansion():
    config = OAuthConfig(
        ORIGIN, {"test": {"name": "<script>{{pending}}</script>", "redirect_uris": [CALLBACK]}}
    )
    server = OAuthServer(config, MemoryOAuthStore(), StaticKeyStore({"alice": KEY}))
    rendered = server.consent_response("test", "pending-test").body.decode()
    assert "<script>" not in rendered
    assert "&lt;script&gt;{{pending}}&lt;/script&gt;" in rendered
