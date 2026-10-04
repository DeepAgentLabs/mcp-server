"""Authentication backends. Hosted keys are stored only as SHA-256 digests."""

from __future__ import annotations

import hashlib
import secrets
import time
import uuid
from collections.abc import Mapping
from typing import Any, Protocol


def key_digest(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class KeyStore(Protocol):
    def authenticate(self, token: str) -> str | None: ...

    def ping(self) -> bool: ...


class StaticKeyStore:
    """Explicit local/development configuration, compatible with existing installs."""

    def __init__(self, api_keys: Mapping[str, str]) -> None:
        if not isinstance(api_keys, Mapping) or not api_keys:
            raise ValueError(
                "Configure a nonempty DEEP_AGENTIC_CORE_MCP_API_KEYS user-to-key mapping"
            )
        self.credentials: dict[str, str] = {}
        for user, secret in api_keys.items():
            if not isinstance(user, str) or not user or len(user) > 128:
                raise ValueError("User IDs must be nonempty strings of at most 128 characters")
            if not isinstance(secret, str) or len(secret) < 32 or any(c.isspace() for c in secret):
                raise ValueError("Each user needs a unique bearer key of at least 32 characters")
            digest = key_digest(secret)
            if digest in self.credentials:
                raise ValueError("Bearer keys must be unique per user")
            self.credentials[digest] = user

    def authenticate(self, token: str) -> str | None:
        return self.credentials.get(key_digest(token))

    def ping(self) -> bool:
        return True


class DynamoKeyStore:
    """One active key per user; consistent reads make revocation immediate.

    Only the underlying boto3 client is shared between worker threads. Its resource
    serialization hooks allow native Python values in transaction requests.
    """

    def __init__(self, table_name: str, *, client: Any = None) -> None:
        if client is None:
            import boto3
            from botocore.config import Config

            resource = boto3.resource(
                "dynamodb",
                config=Config(
                    connect_timeout=3,
                    read_timeout=5,
                    retries={"total_max_attempts": 2, "mode": "standard"},
                    max_pool_connections=32,
                ),
            )
            client = resource.meta.client
        self.client = client
        self.table_name = table_name

    def _get(self, pk: str) -> dict[str, Any]:
        result = self.client.get_item(
            TableName=self.table_name, Key={"pk": pk}, ConsistentRead=True
        )
        return dict(result.get("Item", {}))

    def ping(self) -> bool:
        self._get("HEALTH")
        return True

    def authenticate(self, token: str) -> str | None:
        if len(token) < 32 or len(token) > 256 or any(c.isspace() for c in token):
            return None
        digest = key_digest(token)
        key = self._get("KEY#" + digest)
        user = key.get("user_id")
        if not isinstance(user, str):
            return None
        account = self._get("USER#" + user)
        if account.get("status") == "active" and account.get("key_hash") == digest:
            return user
        return None

    def issue(self, display_name: str) -> dict[str, str]:
        user = str(uuid.uuid4())
        token = "dal_" + secrets.token_urlsafe(36)
        self.import_key(user, token, display_name)
        return {"user_id": user, "display_name": display_name, "api_key": token}

    def import_key(self, user: str, token: str, display_name: str) -> None:
        digest = key_digest(token)
        now = int(time.time())
        # Both records are created together; migration never overwrites an account.
        self.client.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": self.table_name,
                        "Item": {
                            "pk": "USER#" + user,
                            "user_id": user,
                            "display_name": display_name,
                            "status": "active",
                            "key_hash": digest,
                            "created_at": now,
                        },
                        "ConditionExpression": "attribute_not_exists(pk)",
                    }
                },
                {
                    "Put": {
                        "TableName": self.table_name,
                        "Item": {"pk": "KEY#" + digest, "user_id": user, "created_at": now},
                        "ConditionExpression": "attribute_not_exists(pk)",
                    }
                },
            ]
        )

    def profile(self, user: str) -> dict[str, str]:
        account = self._get("USER#" + user)
        return {
            "user_id": user,
            "display_name": str(account.get("display_name", "")),
            "status": str(account.get("status", "unknown")),
        }

    def rotate(self, user: str, old_token: str) -> dict[str, str]:
        token = "dal_" + secrets.token_urlsafe(36)
        old_hash, new_hash = key_digest(old_token), key_digest(token)
        # Conditional transaction prevents concurrent rotations/revocations from
        # leaving a second usable key or resurrecting a revoked account.
        self.client.transact_write_items(
            TransactItems=[
                {
                    "Update": {
                        "TableName": self.table_name,
                        "Key": {"pk": "USER#" + user},
                        "UpdateExpression": "SET key_hash = :new",
                        "ConditionExpression": "key_hash = :old AND #s = :active",
                        "ExpressionAttributeNames": {"#s": "status"},
                        "ExpressionAttributeValues": {
                            ":new": new_hash,
                            ":old": old_hash,
                            ":active": "active",
                        },
                    }
                },
                {"Delete": {"TableName": self.table_name, "Key": {"pk": "KEY#" + old_hash}}},
                {
                    "Put": {
                        "TableName": self.table_name,
                        "Item": {"pk": "KEY#" + new_hash, "user_id": user},
                        "ConditionExpression": "attribute_not_exists(pk)",
                    }
                },
            ]
        )
        return {"user_id": user, "api_key": token}

    def revoke(self, user: str, token: str) -> None:
        self.client.update_item(
            TableName=self.table_name,
            Key={"pk": "USER#" + user},
            UpdateExpression="SET #s = :revoked",
            ConditionExpression="key_hash = :hash AND #s = :active",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":revoked": "revoked",
                ":hash": key_digest(token),
                ":active": "active",
            },
        )
