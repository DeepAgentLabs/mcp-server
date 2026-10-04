"""Migrate existing keys without printing or storing plaintext in DynamoDB."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import boto3

from deep_agentic_core_mcp.services.api_keys import DynamoKeyStore, StaticKeyStore


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default="deepagentlabs")
    parser.add_argument("--region", default="us-east-2")
    args = parser.parse_args()
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    cf = session.client("cloudformation")

    def outputs(stack: str) -> dict[str, str]:
        return {
            item["OutputKey"]: item["OutputValue"]
            for item in cf.describe_stacks(StackName=stack)["Stacks"][0]["Outputs"]
        }

    current = outputs("deep-agentic-core-mcp")
    table = outputs("deep-agentic-core-mcp-users")["UsersTableName"]
    secret = session.client("secretsmanager").get_secret_value(SecretId=current["ApiKeysSecretArn"])
    credentials = json.loads(secret["SecretString"])
    StaticKeyStore(credentials)  # Validate before writing anything.
    store = DynamoKeyStore(table, client=session.resource("dynamodb").meta.client)
    for user, key in credentials.items():
        if store.authenticate(key) == user:
            continue
        store.import_key(user, key, user)
        if store.authenticate(key) != user:
            raise RuntimeError("Migrated key verification failed")
    state_path = Path(__file__).resolve().parents[1] / "deploy/aws/deployment-state.json"
    state = json.loads(state_path.read_text())
    state["legacy_keys_secret_arn"] = current["ApiKeysSecretArn"]
    state["UsersTableName"] = table
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"Migrated and verified {len(credentials)} existing user(s); no plaintext keys stored")


if __name__ == "__main__":
    main()
