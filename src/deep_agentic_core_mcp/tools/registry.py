"""Central tool metadata registry."""


def list_tools() -> list[dict[str, str]]:
    """Return the initial tool inventory for the server."""
    return [
        {
            "name": "core.health",
            "title": "Health Check",
            "description": "Return the basic health status of the MCP server.",
        },
        {
            "name": "core.version",
            "title": "Server Version",
            "description": "Return the current server package version.",
        },
        {
            "name": "lens.analyze_workflow",
            "title": "Analyze Workflow",
            "description": "Analyze an AgenticLens-compatible workflow artifact.",
        },
        {
            "name": "chaos.list_faults",
            "title": "List Chaos Faults",
            "description": "List the supported fault types for chaos experiments.",
        },
    ]
