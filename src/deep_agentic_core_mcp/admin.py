"""Operator CLI for hosted keys: access policies and revocation by user ID.

This path needs the service's store credentials, not the agent's bearer key, so
an operator can still revoke or narrow a key after the agent's key is lost or
compromised. Changes apply at the key's next dispatch; running calls finish.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence
from typing import Any

from deep_agentic_core_mcp.services.access_policy import AccessPolicy
from deep_agentic_core_mcp.services.api_keys import DynamoKeyStore, PolicyAdminStore


def _store() -> tuple[PolicyAdminStore, Any]:
    database_url = os.environ.get("DEEP_AGENTIC_CORE_MCP_DATABASE_URL")
    if database_url:
        from deep_agentic_core_mcp.services.postgres_store import PostgresKeyStore, connect

        pool = connect(database_url, max_size=1)
        return PostgresKeyStore(pool), pool
    table = os.environ.get("DEEP_AGENTIC_CORE_MCP_USERS_TABLE")
    if table:
        return DynamoKeyStore(table), None
    raise SystemExit("Set DEEP_AGENTIC_CORE_MCP_DATABASE_URL or DEEP_AGENTIC_CORE_MCP_USERS_TABLE")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deep-agentic-core-mcp-admin", description=__doc__.splitlines()[0]
    )
    commands = parser.add_subparsers(dest="command", required=True)
    show = commands.add_parser("show", help="Show a user's status and access policy")
    show.add_argument("user")
    grant = commands.add_parser("set-permissions", help="Replace a user's access policy")
    grant.add_argument("user")
    grant.add_argument("--allow", action="append", help="Tool-name glob (repeatable)")
    grant.add_argument("--deny", action="append", default=[], help="Tool-name glob (repeatable)")
    grant.add_argument("--expires-at", help="ISO 8601 timestamp with a timezone")
    grant.add_argument("--task-id", help="Task this key is delegated to")
    clear = commands.add_parser("clear-permissions", help="Restore the default hosted surface")
    clear.add_argument("user")
    revoke = commands.add_parser("revoke", help="Revoke a user's key without that key")
    revoke.add_argument("user")
    return parser


def run(argv: Sequence[str] | None, store: PolicyAdminStore) -> dict[str, Any]:
    args = _parser().parse_args(argv)
    if args.command == "set-permissions":
        config: dict[str, Any] = {"allow": args.allow or ["*"], "deny": args.deny}
        if args.expires_at:
            config["expires_at"] = args.expires_at
        if args.task_id:
            config["task_id"] = args.task_id
        store.set_access_policy(args.user, AccessPolicy.from_config(config))
    elif args.command == "clear-permissions":
        store.set_access_policy(args.user, None)
    elif args.command == "revoke":
        store.revoke_user(args.user)
    stored = store.stored_access_policy(args.user)
    policy = AccessPolicy.load(stored)
    return {
        **store.profile(args.user),
        "permissions": None if stored is None else policy.to_config(),
        "policy_error": policy.error,
    }


def main(argv: Sequence[str] | None = None) -> None:
    store, pool = _store()
    try:
        print(json.dumps(run(argv, store), indent=2, default=str))
    except KeyError as exc:
        print(f"Unknown user: {exc.args[0]}", file=sys.stderr)
        raise SystemExit(1) from None
    except ValueError as exc:
        print(f"Invalid access policy: {exc}", file=sys.stderr)
        raise SystemExit(2) from None
    finally:
        if pool is not None:
            pool.close()


if __name__ == "__main__":
    main()
