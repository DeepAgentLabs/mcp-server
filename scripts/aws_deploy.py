"""Publish, deploy, inspect, and verify the AWS MCP service using AWS CLI.

Hosted key hashes stay in DynamoDB. Verification uses an ignored local key file.
This script never prints bearer keys, Redis passwords, or registry login tokens.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "deploy/aws/deployment-state.json"
ASSETS = "deep-agentic-core-mcp-assets"
SERVICE = "deep-agentic-core-mcp"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action", choices=["publish", "prepare", "execute", "status", "verify", "save-key"]
    )
    parser.add_argument("--profile", default="deepagentlabs")
    parser.add_argument("--region", default="us-east-2")
    parser.add_argument("--tag", default="aws-launch-20261004")
    parser.add_argument("--change-set-type", choices=["CREATE", "UPDATE"], default="CREATE")
    parser.add_argument("--domain", help="Optional CloudFront custom domain")
    parser.add_argument("--certificate-arn", help="Issued ACM certificate ARN in us-east-1")
    args = parser.parse_args()

    def aws(*parts: str) -> Any:
        result = subprocess.run(
            ["aws", "--profile", args.profile, "--region", args.region, *parts, "--output", "json"],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout) if result.stdout.strip() else {}

    def outputs(stack: str) -> dict[str, str]:
        data = aws("cloudformation", "describe-stacks", "--stack-name", stack)
        return {
            item["OutputKey"]: item["OutputValue"] for item in data["Stacks"][0].get("Outputs", [])
        }

    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    if args.action == "publish":
        assets = outputs(ASSETS)
        uri = assets["RepositoryUri"]
        registry, repository = uri.split("/", 1)
        token = subprocess.run(
            [
                "aws",
                "--profile",
                args.profile,
                "--region",
                args.region,
                "ecr",
                "get-login-password",
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        # Docker stores the registry token only in a task-specific /tmp directory.
        config = Path("/tmp/mcp-aws-docker-auth")
        config.mkdir(mode=0o700, exist_ok=True)
        os.chmod(config, 0o700)
        subprocess.run(
            [
                "docker",
                "--config",
                str(config),
                "login",
                "--username",
                "AWS",
                "--password-stdin",
                registry,
            ],
            input=token,
            text=True,
            check=True,
        )
        remote = uri + ":" + args.tag
        subprocess.run(["docker", "tag", "deep-agentic-core-mcp:" + args.tag, remote], check=True)
        subprocess.run(["docker", "--config", str(config), "push", remote], check=True)
        digest = aws(
            "ecr",
            "describe-images",
            "--repository-name",
            repository,
            "--image-ids",
            "imageTag=" + args.tag,
        )["imageDetails"][0]["imageDigest"]
        state.update(
            {
                "image_uri": uri + "@" + digest,
                "repository_arn": assets["RepositoryArn"],
                "profile": args.profile,
                "region": args.region,
            }
        )
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        subprocess.run(["docker", "--config", str(config), "logout", registry], check=True)
        print("Published immutable image:", state["image_uri"])
    elif args.action == "prepare":
        domain = args.domain if args.domain is not None else state.get("custom_domain", "")
        certificate = (
            args.certificate_arn
            if args.certificate_arn is not None
            else state.get("certificate_arn", "")
        )
        if bool(domain) != bool(certificate):
            raise ValueError("Supply both --domain and --certificate-arn")
        prefix = aws(
            "ec2",
            "describe-managed-prefix-lists",
            "--filters",
            "Name=prefix-list-name,Values=com.amazonaws.global.cloudfront.origin-facing",
        )["PrefixLists"][0]["PrefixListId"]
        parameters = [
            {"ParameterKey": "ImageUri", "ParameterValue": state["image_uri"]},
            {"ParameterKey": "RepositoryArn", "ParameterValue": state["repository_arn"]},
            {"ParameterKey": "CloudFrontPrefixList", "ParameterValue": prefix},
            {
                "ParameterKey": "UsersTableName",
                "ParameterValue": outputs(SERVICE + "-users")["UsersTableName"],
            },
            {"ParameterKey": "CustomDomain", "ParameterValue": domain},
            {"ParameterKey": "CertificateArn", "ParameterValue": certificate},
        ]
        parameter_path = ROOT / "deploy/aws/parameters.json"
        parameter_path.write_text(json.dumps(parameters, indent=2) + "\n")
        change = aws(
            "cloudformation",
            "create-change-set",
            "--stack-name",
            SERVICE,
            "--change-set-name",
            args.tag,
            "--change-set-type",
            args.change_set_type,
            "--template-body",
            "file://" + str(ROOT / "deploy/aws/service.json"),
            "--parameters",
            "file://" + str(parameter_path),
            "--capabilities",
            "CAPABILITY_IAM",
            "--tags",
            "Key=Project,Value=deep-agentic-core-mcp",
        )
        state["change_set"] = change["Id"]
        state.update({"custom_domain": domain, "certificate_arn": certificate})
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        print("Prepared change set:", change["Id"])
    elif args.action == "execute":
        change = aws(
            "cloudformation", "describe-change-set", "--change-set-name", state["change_set"]
        )
        if change["Status"] != "CREATE_COMPLETE" or change["ExecutionStatus"] != "AVAILABLE":
            raise RuntimeError("Change set is not ready: " + change["Status"])
        print("Executing reviewed change set with", len(change.get("Changes", [])), "resources")
        aws("cloudformation", "execute-change-set", "--change-set-name", state["change_set"])
    elif args.action == "status":
        data = aws("cloudformation", "describe-stacks", "--stack-name", SERVICE)["Stacks"][0]
        print("Stack status:", data["StackStatus"])
        events = aws("cloudformation", "describe-events", "--stack-name", SERVICE)
        failures = [
            item
            for item in events.get("OperationEvents", [])
            if item.get("EventType", "").endswith("FAILED")
            or item.get("ResourceStatus", "").endswith("FAILED")
        ]
        if failures:
            print(json.dumps(failures, indent=2))
        if data["StackStatus"] in {"CREATE_COMPLETE", "UPDATE_COMPLETE"}:
            current = outputs(SERVICE)
            state.update(current)
            STATE.write_text(json.dumps(state, indent=2) + "\n")
            print(json.dumps(current, indent=2))
    elif args.action in {"verify", "save-key"}:
        current = outputs(SERVICE)
        key_path = ROOT / ".secrets/aws-admin.json"
        if "ApiKeysSecretArn" in current:
            keys = json.loads(
                aws(
                    "secretsmanager", "get-secret-value", "--secret-id", current["ApiKeysSecretArn"]
                )["SecretString"]
            )
        elif key_path.exists():
            keys = {"admin": json.loads(key_path.read_text())["bearer_key"]}
        else:
            raise RuntimeError(
                "DynamoDB stores hashes only. Supply .secrets/aws-admin.json to verify."
            )
        if args.action == "save-key":
            directory = ROOT / ".secrets"
            directory.mkdir(mode=0o700, exist_ok=True)
            os.chmod(directory, 0o700)
            path = key_path
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(descriptor, "w") as file:
                json.dump(
                    {"mcp_url": current["McpUrl"], "user": "admin", "bearer_key": keys["admin"]},
                    file,
                    indent=2,
                )
                file.write("\n")
            os.chmod(path, 0o600)
            print("Credentials saved privately:", path)
        else:
            with urllib.request.urlopen(current["HealthUrl"], timeout=30) as response:
                assert response.status == 200
            try:
                urllib.request.urlopen(
                    urllib.request.Request(
                        current["McpUrl"], data=b"{}", headers={"Content-Type": "application/json"}
                    ),
                    timeout=30,
                )
            except urllib.error.HTTPError as error:
                assert error.code == 401, error.code
            else:
                raise RuntimeError("Unauthenticated request was not rejected")
            request = urllib.request.Request(
                current["McpUrl"],
                data=json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {"name": "core.health", "arguments": {}},
                    }
                ).encode(),
                headers={
                    "Authorization": "Bearer " + keys["admin"],
                    "Accept": "application/json, text/event-stream",
                    "Content-Type": "application/json",
                    "MCP-Protocol-Version": "2025-11-25",
                },
            )
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.loads(response.read())
            payload = json.loads(result["result"]["content"][0]["text"])
            for name in ("agenticlens", "ai_operations_spec"):
                assert payload["adapters"][name]["available"], name + " integration unavailable"
            print("Verified HTTPS health, authentication, and MCP integration readiness")
            print("MCP URL:", current["McpUrl"])


if __name__ == "__main__":
    main()
