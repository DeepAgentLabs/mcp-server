"""Read-only documentation tools for hosts that do not retrieve MCP resources."""

from __future__ import annotations

from typing import Any

from jsonschema import ValidationError, validate

from deep_agentic_core_mcp.services import documentation

PRODUCTS = [
    "agenticlens",
    "agentic-evals",
    "agentic-chaos",
    "agentic-sidecar",
    "agenticops-control-tower",
    "ai-operations-spec",
    "mcp-server",
]
_PRODUCT = {"type": "string", "enum": PRODUCTS}
_LIMIT = {"type": "integer", "minimum": 1, "maximum": 20, "default": 10}
_INPUTS: dict[str, dict[str, Any]] = {
    "catalog": {"properties": {"product": _PRODUCT}},
    "read": {
        "properties": {
            "product": _PRODUCT,
            "section": {"type": "string", "minLength": 1, "maxLength": 256},
            "offset": {"type": "integer", "minimum": 0, "default": 0},
            "limit": {"type": "integer", "minimum": 1, "maximum": 32000, "default": 12000},
        },
        "required": ["product"],
    },
    "search": {
        "properties": {
            "query": {"type": "string", "minLength": 1, "maxLength": 300},
            "product": _PRODUCT,
            "limit": _LIMIT,
        },
        "required": ["query"],
    },
}


def _call(operation: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
    args = {} if arguments is None else arguments
    try:
        validate(args, {"type": "object", "additionalProperties": False, **_INPUTS[operation]})
        if operation == "catalog":
            return documentation.catalog(**args)
        if operation == "read":
            return documentation.read(**args)
        return documentation.search(**args)
    except (ValidationError, ValueError, OSError) as exc:
        return {"ok": False, "error": exc.message if isinstance(exc, ValidationError) else str(exc)}


def docs_catalog(arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    return _call("catalog", arguments)


def docs_read(arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    return _call("read", arguments)


def docs_search(arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    return _call("search", arguments)


def tool_definitions() -> list[dict[str, Any]]:
    descriptions = {
        "catalog": "Discover all seven DeepAgentLabs products, bundled documentation versions, "
        "commit-pinned sources and resource URIs. Supply product to list its sections before "
        "writing integration code. Works without sibling packages or network access.",
        "read": "Read the robust AI reference for a product or cited section: APIs, CLI, "
        "configuration, schemas and complete examples. Bounded Unicode character pages; "
        "continue with next_offset. Cite the source_commit and citation; documentation "
        "versions may differ from installed packages.",
        "search": "Search robust AI references across all seven products, optionally filtered "
        "by product. Literal case-insensitive AND-term search returns ranked section snippets, "
        "commit-pinned citations and offsets. Read matched sections with core.docs_read "
        "before generating code.",
    }
    return [
        {
            "name": "core.docs_" + operation,
            "title": "Ecosystem documentation " + operation,
            "description": description,
            "input_schema": {"type": "object", "additionalProperties": False, **_INPUTS[operation]},
            "category": "core",
            "prerequisites": [],
            "expected_duration": "fast",
            "mutates_session": False,
        }
        for operation, description in descriptions.items()
    ]
