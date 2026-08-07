"""Central tool metadata registry."""


def list_tools() -> list[dict[str, object]]:
    """Return the current tool inventory for the server."""
    return [
        {
            "name": "core.health",
            "title": "Health Check",
            "description": "Return the basic health status of the MCP server.",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
        },
        {
            "name": "core.version",
            "title": "Server Version",
            "description": "Return the current server package version.",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
        },
        {
            "name": "lens.analyze_workflow",
            "title": "Analyze Workflow",
            "description": "Analyze an AgenticLens-compatible workflow artifact.",
            "input_schema": {
                "type": "object",
                "properties": {"artifact": {"type": "object"}},
                "required": ["artifact"],
                "additionalProperties": False,
            },
        },
        {
            "name": "chaos.list_faults",
            "title": "List Chaos Faults",
            "description": "List the supported fault types for chaos experiments.",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
        },
        {
            "name": "spec.validate_artifact",
            "title": "Validate AI Operations Artifact",
            "description": (
                "Validate a workflow or run artifact against the"
                " AI Operations v0.4 draft."
            ),
            "input_schema": {
                "type": "object",
                "properties": {"artifact": {"type": "object"}},
                "required": ["artifact"],
                "additionalProperties": False,
            },
        },
    ]
