"""Minimal server entrypoint scaffold."""

from deep_agentic_core_mcp.config import SERVER_NAME, VERSION
from deep_agentic_core_mcp.services.registry import (
    prompt_descriptors,
    resource_descriptors,
    tool_descriptors,
)


def main() -> None:
    """Run the MCP server entrypoint.

    This is a placeholder until the concrete MCP SDK wiring is implemented.
    """
    summary = {
        "server": SERVER_NAME,
        "version": VERSION,
        "tools": len(tool_descriptors()),
        "resources": len(resource_descriptors()),
        "prompts": len(prompt_descriptors()),
    }
    print(summary)


if __name__ == "__main__":
    main()
