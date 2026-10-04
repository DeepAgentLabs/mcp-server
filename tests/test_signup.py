"""DynamoDB transactions, public signup, key lifecycle and trusted identity tests."""

import json

import boto3
import fakeredis
import httpx
import pytest
from moto import mock_aws
from starlette.applications import Starlette

from deep_agentic_core_mcp.services.api_keys import DynamoKeyStore
from deep_agentic_core_mcp.services.remote_sessions import RedisSessionStore
from deep_agentic_core_mcp.signup import RedisSignupLimiter, signup_routes
from deep_agentic_core_mcp.transport_http import create_app


@pytest.fixture
def backend():
    with mock_aws():
        resource = boto3.resource("dynamodb", region_name="us-east-2")
        resource.create_table(
            TableName="users",
            KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        yield DynamoKeyStore("users", client=resource.meta.client)


def test_hashes_only_rotation_revocation_and_stable_identity(backend):
    first = backend.issue("Alex")
    second = backend.issue("Alex")
    assert first["user_id"] != second["user_id"]
    assert backend.authenticate(first["api_key"]) == first["user_id"]
    rows = backend.client.scan(TableName="users")["Items"]
    assert first["api_key"] not in json.dumps(rows, default=str)
    rotated = backend.rotate(first["user_id"], first["api_key"])
    assert rotated["user_id"] == first["user_id"]
    assert backend.authenticate(first["api_key"]) is None
    assert backend.authenticate(rotated["api_key"]) == first["user_id"]
    with pytest.raises(backend.client.exceptions.TransactionCanceledException):
        backend.rotate(first["user_id"], first["api_key"])
    backend.revoke(first["user_id"], rotated["api_key"])
    assert backend.authenticate(rotated["api_key"]) is None
    assert backend.authenticate(second["api_key"]) == second["user_id"]
    with pytest.raises(backend.client.exceptions.TransactionCanceledException):
        backend.rotate(first["user_id"], rotated["api_key"])


def test_migration_preserves_existing_user_identity_without_overwrite(backend):
    backend.import_key("admin", "a" * 48, "admin")
    assert backend.authenticate("a" * 48) == "admin"
    with pytest.raises(backend.client.exceptions.TransactionCanceledException):
        backend.import_key("admin", "b" * 48, "admin")
    assert backend.authenticate("b" * 48) is None
    assert backend.authenticate("a" * 48) == "admin"


def test_signup_limits_are_shared_and_do_not_store_client_ips():
    redis = fakeredis.FakeRedis()
    first, second = RedisSignupLimiter(redis), RedisSignupLimiter(redis)
    for _ in range(10):
        assert first.allow("192.0.2.1")
    assert not second.allow("192.0.2.1")
    for ip in range(9):
        for _ in range(10):
            assert second.allow(f"192.0.2.{ip + 2}")
    assert not first.allow("192.0.2.99")
    assert all(b"192.0.2" not in key for key in redis.scan_iter())
    assert all(redis.ttl(key) > 0 for key in redis.scan_iter())


@pytest.mark.asyncio
async def test_signup_and_account_routes(backend):
    app = Starlette(
        routes=signup_routes(
            backend, RedisSignupLimiter(fakeredis.FakeRedis()), "https://mcp.example"
        )
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="https://mcp.example"
    ) as client:
        page = await client.get("/signup")
        assert page.status_code == 200
        assert "frame-ancestors 'none'" in page.headers["content-security-policy"]
        assert (await client.get("/signup.js")).status_code == 200
        assert (await client.get("/signup.css")).status_code == 200
        assert (await client.post("/api/signup", json={"display_name": "x"})).status_code == 400
        assert (await client.post("/api/signup", json=[])).status_code == 400
        assert (
            await client.post(
                "/api/signup",
                json={"display_name": "Alex"},
                headers={"Origin": "https://attacker.example"},
            )
        ).status_code == 403
        assert (
            await client.post(
                "/api/signup", content="x" * 4097, headers={"Content-Type": "application/json"}
            )
        ).status_code == 413
        result = await client.post("/api/signup", json={"display_name": "Alex", "user_id": "admin"})
        assert result.status_code == 201
        assert result.headers["cache-control"] == "no-store"
        key = result.json()["api_key"]
        assert result.json()["user_id"] != "admin"
        auth = {"Authorization": "Bearer " + key}
        assert (await client.get("/api/account")).status_code == 401
        account = await client.get("/api/account", headers=auth)
        assert account.json()["display_name"] == "Alex"
        replacement = await client.post("/api/account", headers=auth)
        assert replacement.status_code == 200
        assert (await client.get("/api/account", headers=auth)).status_code == 401
        auth = {"Authorization": "Bearer " + replacement.json()["api_key"]}
        assert (await client.delete("/api/account", headers=auth)).status_code == 200
        assert (await client.get("/api/account", headers=auth)).status_code == 401


@pytest.mark.asyncio
async def test_domain_migration_keeps_only_explicit_browser_origins(backend):
    app = Starlette(
        routes=signup_routes(
            backend,
            RedisSignupLimiter(fakeredis.FakeRedis()),
            "https://mcp.deepagentlabs.io",
            allowed_origins=["https://previous.cloudfront.net"],
        )
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="https://mcp.deepagentlabs.io"
    ) as client:
        result = await client.post(
            "/api/signup",
            json={"display_name": "Alex"},
            headers={"Origin": "https://previous.cloudfront.net"},
        )
        assert result.status_code == 201
        assert result.json()["mcp_url"] == "https://mcp.deepagentlabs.io/mcp"
        result = await client.post(
            "/api/signup",
            json={"display_name": "Alex"},
            headers={"Origin": "https://untrusted.example"},
        )
        assert result.status_code == 403


@pytest.mark.asyncio
async def test_proxy_suffix_prevents_spoofing_signup_limit(backend):
    app = Starlette(
        routes=signup_routes(
            backend,
            RedisSignupLimiter(fakeredis.FakeRedis()),
            "https://mcp.example",
            trusted_proxy_hops=2,
        )
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="https://mcp.example"
    ) as client:
        for spoof in range(10):
            result = await client.post(
                "/api/signup",
                json={"display_name": "Alex"},
                headers={"X-Forwarded-For": f"spoof{spoof}, 192.0.2.1, 10.0.0.1"},
            )
            assert result.status_code == 201
        result = await client.post(
            "/api/signup",
            json={"display_name": "Alex"},
            headers={"X-Forwarded-For": "new-spoof, 192.0.2.1, 10.0.0.1"},
        )
        assert result.status_code == 429


@pytest.mark.asyncio
async def test_signup_fails_closed_on_storage_outage(backend, monkeypatch):
    class BrokenLimiter:
        def allow(self, peer):
            raise RuntimeError("Redis unavailable")

    app = Starlette(routes=signup_routes(backend, BrokenLimiter(), "https://mcp.example"))
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="https://mcp.example"
    ) as client:
        response = await client.post("/api/signup", json={"display_name": "Alex"})
        assert response.status_code == 503
        assert "Redis" not in response.text
        assert backend.client.scan(TableName="users")["Count"] == 0


@pytest.mark.asyncio
async def test_dynamic_key_authentication_and_mcp_identity(backend, monkeypatch):
    monkeypatch.setenv("DEEP_AGENTIC_CORE_MCP_PUBLIC_URL", "https://mcp.example")
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_REMOTE_TRANSPORT", raising=False)
    store = RedisSessionStore("redis://localhost")
    store.client = fakeredis.FakeRedis(decode_responses=True)
    app = create_app(key_store=backend, store=store, allowed_hosts=["mcp.example"])
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="https://mcp.example"
        ) as client,
    ):
        first = (await client.post("/api/signup", json={"display_name": "Alex"})).json()
        second = (await client.post("/api/signup", json={"display_name": "Alex"})).json()

        async def call(key):
            return await client.post(
                "/mcp",
                headers={
                    "Authorization": "Bearer " + key,
                    "Accept": "application/json, text/event-stream",
                    "MCP-Protocol-Version": "2025-11-25",
                },
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": "core.version", "arguments": {}},
                },
            )

        assert (await call(first["api_key"])).status_code == 200
        assert (await call(second["api_key"])).status_code == 200
        assert len(list(store.client.scan_iter("deep-agentic-core-mcp:user:*"))) == 2
        rotated = backend.rotate(first["user_id"], first["api_key"])
        assert (await call(first["api_key"])).status_code == 401
        assert (await call(rotated["api_key"])).status_code == 200
        assert len(list(store.client.scan_iter("deep-agentic-core-mcp:user:*"))) == 2
        backend.revoke(first["user_id"], rotated["api_key"])
        assert (await call(rotated["api_key"])).status_code == 401
        assert (await call(second["api_key"])).status_code == 200

        def unavailable(token):
            raise RuntimeError("Storage unavailable")

        monkeypatch.setattr(backend, "authenticate", unavailable)
        assert (await call(second["api_key"])).status_code == 503
