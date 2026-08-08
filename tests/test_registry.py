from deep_agentic_core_mcp.prompts.registry import list_prompts
from deep_agentic_core_mcp.resources.catalog import list_resources
from deep_agentic_core_mcp.services.registry import (
    prompt_descriptors,
    resource_descriptors,
    tool_descriptors,
)
from deep_agentic_core_mcp.tools.registry import list_tools


def test_tool_registry_has_core_health() -> None:
    names = {tool["name"] for tool in list_tools()}
    assert "core.health" in names
    assert "lens.analyze_workflow" in names
    assert "chaos.list_faults" in names
    assert "spec.validate_artifact" in names


def test_resource_registry_not_empty() -> None:
    assert list_resources()
    uris = {resource["uri"] for resource in list_resources()}
    assert "resource://schemas/aiops/v0.4/workflow" in uris


def test_prompt_registry_not_empty() -> None:
    assert list_prompts()


def test_typed_descriptors_build() -> None:
    assert tool_descriptors()
    assert resource_descriptors()
    assert prompt_descriptors()
