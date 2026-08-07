"""Resource catalog for MCP-exposed reference assets."""

from deep_agentic_core_mcp.adapters.ai_operations_spec import list_schema_resources


def list_resources() -> list[dict[str, str]]:
    """Return the current resource inventory."""
    resources = [
        {
            "uri": "resource://examples/sample_workflow",
            "name": "Sample workflow artifact",
            "kind": "workflow-json",
        },
        {
            "uri": "resource://catalogs/chaos_faults",
            "name": "Chaos fault catalog",
            "kind": "reference",
        },
    ]
    resources.extend(list_schema_resources())
    return resources
