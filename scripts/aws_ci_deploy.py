"""Deploy an immutable image using the existing CloudFormation template.

CI changes only ImageUri, checks the change set, and waits for completion.
Infrastructure changes use the separately reviewed operator deployment flow.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any


def image_parameters(parameters: list[dict[str, Any]], image: str) -> list[dict[str, Any]]:
    if not re.fullmatch(
        r"[0-9]{12}\.dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com/.+@sha256:[a-f0-9]{64}", image
    ):
        raise ValueError("Use an immutable ECR image digest")
    if not any(item["ParameterKey"] == "ImageUri" for item in parameters):
        raise ValueError("Stack has no ImageUri parameter")
    return [
        {"ParameterKey": item["ParameterKey"], "ParameterValue": image}
        if item["ParameterKey"] == "ImageUri"
        else {"ParameterKey": item["ParameterKey"], "UsePreviousValue": True}
        for item in parameters
    ]


def review_changes(changes: list[dict[str, Any]]) -> None:
    allowed = {"TaskDefinition", "Service"}
    for item in changes:
        change = item["ResourceChange"]
        if change["LogicalResourceId"] not in allowed or change["Action"] != "Modify":
            raise RuntimeError(
                "CI refused an infrastructure change: " + change["LogicalResourceId"]
            )
        if change["LogicalResourceId"] == "Service" and change.get("Replacement") != "False":
            raise RuntimeError("CI refused service replacement")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--change-set", required=True)
    parser.add_argument("--stack", default="deep-agentic-core-mcp")
    parser.add_argument("--region", default="us-east-2")
    args = parser.parse_args()

    def aws(*parts: str) -> Any:
        process = subprocess.run(
            ["aws", "--region", args.region, *parts, "--output", "json"],
            capture_output=True,
            text=True,
        )
        if process.returncode:
            raise RuntimeError(process.stderr.strip())
        return json.loads(process.stdout) if process.stdout.strip() else {}

    def stack() -> dict[str, Any]:
        return dict(
            aws("cloudformation", "describe-stacks", "--stack-name", args.stack)["Stacks"][0]
        )

    current = stack()
    if current["StackStatus"] not in {
        "CREATE_COMPLETE",
        "UPDATE_COMPLETE",
        "UPDATE_ROLLBACK_COMPLETE",
    }:
        raise RuntimeError("Stack is busy or needs operator attention: " + current["StackStatus"])
    parameters = image_parameters(current["Parameters"], args.image)
    if (
        next(
            item["ParameterValue"]
            for item in current["Parameters"]
            if item["ParameterKey"] == "ImageUri"
        )
        == args.image
    ):
        print("Image already deployed")
        return
    with tempfile.TemporaryDirectory(prefix="mcp-ci-") as directory:
        parameter_file = Path(directory) / "parameters.json"
        parameter_file.write_text(json.dumps(parameters))
        change = aws(
            "cloudformation",
            "create-change-set",
            "--stack-name",
            args.stack,
            "--change-set-name",
            args.change_set,
            "--change-set-type",
            "UPDATE",
            "--use-previous-template",
            "--parameters",
            "file://" + str(parameter_file),
            "--capabilities",
            "CAPABILITY_IAM",
        )["Id"]
    deadline = time.monotonic() + 600
    while time.monotonic() < deadline:
        description = aws("cloudformation", "describe-change-set", "--change-set-name", change)
        if description["Status"] == "CREATE_COMPLETE":
            break
        if description["Status"] == "FAILED":
            raise RuntimeError("Change set failed: " + description.get("StatusReason", "unknown"))
        time.sleep(15)
    else:
        raise TimeoutError("Change set did not finish preparing")
    review_changes(description.get("Changes", []))
    print("Reviewed image-only change set:", args.change_set)
    aws("cloudformation", "execute-change-set", "--change-set-name", change)
    deadline = time.monotonic() + 1800
    last_status = ""
    while time.monotonic() < deadline:
        status = stack()["StackStatus"]
        if status != last_status:
            print("Stack:", status, flush=True)
            last_status = status
        if status == "UPDATE_COMPLETE":
            print("Image deployment completed:", args.image)
            return
        if status.endswith("FAILED") or status in {"UPDATE_ROLLBACK_COMPLETE", "ROLLBACK_COMPLETE"}:
            events = aws("cloudformation", "describe-events", "--stack-name", args.stack)
            print(json.dumps(events, indent=2))
            raise RuntimeError("Deployment failed; check rollback status: " + status)
        time.sleep(15)
    raise TimeoutError("Deployment timed out; inspect CloudFormation before retrying")


if __name__ == "__main__":
    main()
