"""Service helpers for server-side registries."""

from deep_agentic_core_mcp.prompts.registry import list_prompts
from deep_agentic_core_mcp.resources.catalog import list_resources
from deep_agentic_core_mcp.schemas.tooling import (
    PromptDescriptor,
    ResourceDescriptor,
    ToolDescriptor,
)
from deep_agentic_core_mcp.tools.registry import list_tools


def tool_descriptors() -> list[ToolDescriptor]:
    """Return typed tool metadata."""
    return [ToolDescriptor(**tool) for tool in list_tools()]


def resource_descriptors() -> list[ResourceDescriptor]:
    """Return typed resource metadata."""
    return [ResourceDescriptor(**resource) for resource in list_resources()]


def prompt_descriptors() -> list[PromptDescriptor]:
    """Return typed prompt metadata."""
    return [PromptDescriptor(**prompt) for prompt in list_prompts()]
