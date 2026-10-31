"""Operator access policies and revocation in the DynamoDB store and admin CLI."""

import boto3
import pytest
from moto import mock_aws

from deep_agentic_core_mcp import admin
from deep_agentic_core_mcp.services.access_policy import AccessPolicy
from deep_agentic_core_mcp.services.api_keys import DynamoKeyStore


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


def test_dynamo_policies_round_trip_and_apply_on_next_authorize(backend):
    issued = backend.issue("Ada")
    user, token = issued["user_id"], issued["api_key"]
    principal = backend.authorize(token)
    assert principal is not None and principal.user == user and not principal.policy.configured
    backend.set_access_policy(
        user,
        AccessPolicy.from_config(
            {"allow": ["lens.*"], "expires_at": "2030-01-01T00:00:00Z", "task_id": "t-1"}
        ),
    )
    policy = backend.authorize(token).policy
    assert policy.allow == ("lens.*",) and policy.task_id == "t-1"
    assert backend.stored_access_policy(user)["expires_at"] == "2030-01-01T00:00:00Z"
    assert policy.permits("lens.analyze_workflow") and not policy.permits("core.version")
    backend.set_access_policy(user, None)
    assert not backend.authorize(token).policy.configured
    with pytest.raises(KeyError):
        backend.set_access_policy("missing", None)


def test_dynamo_stored_numeric_and_invalid_policies(backend):
    issued = backend.issue("Ada")
    user, token = issued["user_id"], issued["api_key"]
    backend.client.update_item(
        TableName="users",
        Key={"pk": "USER#" + user},
        UpdateExpression="SET #p = :p",
        ExpressionAttributeNames={"#p": "permissions"},
        ExpressionAttributeValues={":p": {"allow": ["*"], "expires_at": 1000}},
    )
    assert backend.authorize(token).policy.expired()
    backend.client.update_item(
        TableName="users",
        Key={"pk": "USER#" + user},
        UpdateExpression="SET #p = :p",
        ExpressionAttributeNames={"#p": "permissions"},
        ExpressionAttributeValues={":p": {"allow": "*"}},
    )
    assert backend.authorize(token).policy.denial_reason("core.version") == "invalid access policy"


def test_operator_revocation_needs_no_agent_key(backend):
    issued = backend.issue("Ada")
    backend.revoke_user(issued["user_id"])
    assert backend.authorize(issued["api_key"]) is None
    with pytest.raises(KeyError):
        backend.revoke_user("missing")


def test_admin_cli_sets_shows_clears_and_revokes(backend):
    issued = backend.issue("Ada")
    user = issued["user_id"]
    shown = admin.run(
        [
            "set-permissions",
            user,
            "--allow",
            "lens.*",
            "--allow",
            "core.version",
            "--deny",
            "lens.suite_*",
            "--task-id",
            "task-7",
        ],
        backend,
    )
    assert shown["status"] == "active" and shown["policy_error"] is None
    assert shown["permissions"] == {
        "allow": ["lens.*", "core.version"],
        "deny": ["lens.suite_*"],
        "task_id": "task-7",
    }
    assert admin.run(["show", user], backend)["permissions"]["task_id"] == "task-7"
    assert admin.run(["clear-permissions", user], backend)["permissions"] is None
    assert admin.run(["revoke", user], backend)["status"] == "revoked"
    assert backend.authorize(issued["api_key"]) is None
    with pytest.raises(ValueError, match="timezone"):
        admin.run(["set-permissions", user, "--expires-at", "2030-01-01T00:00:00"], backend)


def test_admin_main_reports_unknown_users(backend, monkeypatch, capsys):
    monkeypatch.setattr(admin, "_store", lambda: (backend, None))
    with pytest.raises(SystemExit) as exc:
        admin.main(["show", "missing"])
    assert exc.value.code == 1 and "Unknown user" in capsys.readouterr().err
    monkeypatch.undo()
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_DATABASE_URL", raising=False)
    monkeypatch.delenv("DEEP_AGENTIC_CORE_MCP_USERS_TABLE", raising=False)
    with pytest.raises(SystemExit, match="DATABASE_URL"):
        admin.main(["show", "x"])
