"""Per-key access policy validation and decisions."""

import pytest

from deep_agentic_core_mcp.services.access_policy import AccessPolicy, Principal, authorize
from deep_agentic_core_mcp.services.api_keys import StaticKeyStore


def test_default_policy_permits_everything_and_is_unconfigured():
    policy = AccessPolicy.from_config(None)
    assert policy.permits("lens.analyze_workflow")
    assert not policy.configured


def test_allow_globs_deny_wins_and_access_status_is_always_permitted():
    policy = AccessPolicy.from_config(
        {"allow": ["lens.*", "core.version"], "deny": ["lens.suite_*"]}
    )
    assert policy.permits("lens.analyze_workflow")
    assert policy.permits("core.version")
    assert policy.denial_reason("lens.suite_check") == "tool denied by policy"
    assert policy.denial_reason("spec.validate_artifact") == "tool not in policy allow list"
    assert policy.permits("core.access_status")
    # An explicit deny still removes it.
    assert not AccessPolicy.from_config({"deny": ["core.*"]}).permits("core.access_status")


def test_globs_are_case_sensitive():
    assert not AccessPolicy.from_config({"allow": ["LENS.*"]}).permits("lens.analyze_workflow")


@pytest.mark.parametrize(
    "expires_at", [1_000.0, "1970-01-01T00:16:40Z", "1970-01-01T00:16:40+00:00"]
)
def test_expiry_denies_every_tool_except_access_status(expires_at):
    policy = AccessPolicy.from_config({"expires_at": expires_at, "task_id": "task-1"})
    assert policy.expires_at == 1_000.0
    assert policy.permits("core.version", now=999.0)
    assert policy.denial_reason("core.version", now=1_000.0) == "access policy expired"
    assert policy.permits("core.access_status", now=2_000.0)
    assert policy.to_config() == {
        "allow": ["*"],
        "deny": [],
        "expires_at": 1_000.0,
        "task_id": "task-1",
    }


@pytest.mark.parametrize(
    "config",
    [
        {"allow": "lens.*"},
        {"allow": [""]},
        {"allow": ["x" * 129]},
        {"allow": ["*"] * 65},
        {"deny": [1]},
        {"expires_at": "2026-11-01T00:00:00"},
        {"expires_at": "tomorrow"},
        {"expires_at": True},
        {"expires_at": float("nan")},
        {"expires_at": float("inf")},
        {"task_id": ""},
        {"task_id": 7},
        {"tools": ["*"]},
        ["*"],
    ],
)
def test_malformed_configuration_is_rejected(config):
    with pytest.raises(ValueError):
        AccessPolicy.from_config(config)


def test_stored_invalid_policy_fails_closed():
    policy = AccessPolicy.load({"allow": "lens.*"})
    assert policy.error
    assert policy.denial_reason("lens.analyze_workflow") == "invalid access policy"
    assert not policy.permits("core.access_status")


def test_static_store_entries_carry_policies_and_validate_at_startup():
    store = StaticKeyStore(
        {"alice": "a" * 40, "bob": {"key": "b" * 40, "permissions": {"allow": ["core.*"]}}}
    )
    assert store.authorize("a" * 40) == Principal("alice")
    bob = store.authorize("b" * 40)
    assert bob is not None and bob.policy.allow == ("core.*",)
    assert store.authorize("c" * 40) is None
    with pytest.raises(ValueError, match="allow"):
        StaticKeyStore({"bob": {"key": "b" * 40, "permissions": {"allow": "core.*"}}})
    with pytest.raises(ValueError, match="only 'key'"):
        StaticKeyStore({"bob": {"key": "b" * 40, "scope": "x"}})
    with pytest.raises(ValueError, match="32 characters"):
        StaticKeyStore({"bob": {"permissions": {}}})


def test_authorize_falls_back_to_authenticate_for_legacy_stores():
    class LegacyStore:
        def authenticate(self, token):
            return "carol" if token == "ok" else None

    assert authorize(LegacyStore(), "ok") == Principal("carol")
    assert authorize(LegacyStore(), "no") is None
