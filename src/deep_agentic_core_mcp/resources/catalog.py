"""Placeholder resource catalog."""


def list_resources() -> list[dict[str, str]]:
    """Return the initial resource inventory."""
    return [
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
