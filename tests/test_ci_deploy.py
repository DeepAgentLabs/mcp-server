"""CI preserves infrastructure parameters and refuses unrelated changes."""

import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "aws_ci_deploy", Path(__file__).resolve().parents[1] / "scripts/aws_ci_deploy.py"
)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_image_update_preserves_all_other_parameters():
    image = "123456789012.dkr.ecr.us-east-2.amazonaws.com/mcp@sha256:" + "a" * 64
    parameters = [
        {"ParameterKey": "ImageUri", "ParameterValue": "old"},
        {"ParameterKey": "CachePassword", "ParameterValue": "****"},
        {"ParameterKey": "CustomDomain", "ParameterValue": "mcp.example.com"},
    ]
    assert module.image_parameters(parameters, image) == [
        {"ParameterKey": "ImageUri", "ParameterValue": image},
        {"ParameterKey": "CachePassword", "UsePreviousValue": True},
        {"ParameterKey": "CustomDomain", "UsePreviousValue": True},
    ]
    with pytest.raises(ValueError):
        module.image_parameters(parameters, "mcp:latest")


@pytest.mark.parametrize(
    "resource,action,replacement",
    [("Users", "Modify", "False"), ("Service", "Modify", "True"), ("Service", "Remove", "False")],
)
def test_rejects_infrastructure_changes(resource, action, replacement):
    with pytest.raises(RuntimeError):
        module.review_changes(
            [
                {
                    "ResourceChange": {
                        "LogicalResourceId": resource,
                        "Action": action,
                        "Replacement": replacement,
                    }
                }
            ]
        )


def test_accepts_image_revision_and_service_update():
    module.review_changes(
        [
            {
                "ResourceChange": {
                    "LogicalResourceId": "TaskDefinition",
                    "Action": "Modify",
                    "Replacement": "True",
                }
            },
            {
                "ResourceChange": {
                    "LogicalResourceId": "Service",
                    "Action": "Modify",
                    "Replacement": "False",
                }
            },
        ]
    )
