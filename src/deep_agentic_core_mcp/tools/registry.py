"""Central tool metadata registry."""

from typing import Any

_SESSION_ID_PROPERTY = {
    "session_id": {
        "type": "string",
        "description": "Session to read/write shared state under. Defaults to 'default'.",
    }
}


def list_tools() -> list[dict[str, Any]]:
    """Return the current tool inventory for the server.

    Beyond the MCP-standard `name`/`title`/`description`/`input_schema`,
    each entry carries server-specific metadata surfaced to hosts via
    `Tool._meta`/`Tool.annotations` in `server.py`:

    - `category`: rough grouping (`core`, `lens`, `chaos`, `spec`)
    - `prerequisites`: adapter names (see `adapters/`) that must be
      available for the tool to succeed
    - `expected_duration`: `"instant" | "fast" | "slow"`, a rough hint for
      hosts deciding whether to show a spinner
    - `mutates_session`: whether the call writes to the in-memory session
      store (`services/session.py`)
    """
    return [
        {
            "name": "core.health",
            "title": "Health Check",
            "description": "Return rich server diagnostics: adapter availability, loaded "
            "tools/resources/prompts, and recent successful calls.",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
            "category": "core",
            "prerequisites": [],
            "expected_duration": "instant",
            "mutates_session": False,
        },
        {
            "name": "core.version",
            "title": "Server Version",
            "description": "Return the current server package version.",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
            "category": "core",
            "prerequisites": [],
            "expected_duration": "instant",
            "mutates_session": False,
        },
        {
            "name": "core.verify",
            "title": "Verify Integrations",
            "description": "Check connectivity to agenticlens, agentic-chaos, and "
            "ai-operations-spec, and report readiness.",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
            "category": "core",
            "prerequisites": [],
            "expected_duration": "instant",
            "mutates_session": False,
        },
        {
            "name": "core.session_state",
            "title": "Session State",
            "description": "Inspect the artifacts and call history accumulated in a session.",
            "input_schema": {
                "type": "object",
                "properties": {**_SESSION_ID_PROPERTY},
                "additionalProperties": False,
            },
            "category": "core",
            "prerequisites": [],
            "expected_duration": "instant",
            "mutates_session": False,
        },
        {
            "name": "lens.analyze_workflow",
            "title": "Analyze Workflow",
            "description": "Analyze an AgenticLens-compatible workflow artifact.",
            "input_schema": {
                "type": "object",
                "properties": {"artifact": {"type": "object"}, **_SESSION_ID_PROPERTY},
                "required": ["artifact"],
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": True,
        },
        {
            "name": "lens.report_summary",
            "title": "Workflow Report Summary",
            "description": "Render a Markdown workflow report and recommendation summary. "
            "'artifact' may be omitted to reuse the session's stored workflow.",
            "input_schema": {
                "type": "object",
                "properties": {"artifact": {"type": "object"}, **_SESSION_ID_PROPERTY},
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": True,
        },
        {
            "name": "lens.compare_runs",
            "title": "Compare Runs",
            "description": "Compare baseline and candidate trace runs for regressions. "
            "'baseline'/'candidate' may be omitted to reuse the session's stored runs.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "baseline": {"type": "array", "items": {"type": "object"}},
                    "candidate": {"type": "array", "items": {"type": "object"}},
                    "regression_threshold": {"type": "number"},
                    **_SESSION_ID_PROPERTY,
                },
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": True,
        },
        {
            "name": "lens.slo_summary",
            "title": "SLO Summary",
            "description": "Apply release-gate style SLO thresholds to an evaluation report.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "report": {"type": "object"},
                    "thresholds": {"type": "object"},
                    **_SESSION_ID_PROPERTY,
                },
                "required": ["report"],
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": False,
        },
        {
            "name": "lens.audit_report",
            "title": "Audit Report",
            "description": "Return case-by-case evaluation detail for an audit trail.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "report": {"type": "object"},
                    "include_html": {"type": "boolean"},
                    **_SESSION_ID_PROPERTY,
                },
                "required": ["report"],
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": False,
        },
        {
            "name": "chaos.list_faults",
            "title": "List Chaos Faults",
            "description": "List the supported fault types for chaos experiments.",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
            "category": "chaos",
            "prerequisites": ["agentic_chaos"],
            "expected_duration": "instant",
            "mutates_session": False,
        },
        {
            "name": "chaos.run_experiment",
            "title": "Run Chaos Experiment",
            "description": "Run a workspace-sandboxed target script under selected chaos "
            "faults and report the resulting events.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Script path, resolved inside the workspace root.",
                    },
                    "faults": {"type": "array", "items": {"type": "string"}},
                    "timeout_seconds": {"type": "number"},
                    **_SESSION_ID_PROPERTY,
                },
                "required": ["script", "faults"],
                "additionalProperties": False,
            },
            "category": "chaos",
            "prerequisites": ["agentic_chaos"],
            "expected_duration": "slow",
            "mutates_session": True,
        },
        {
            "name": "spec.validate_artifact",
            "title": "Validate AI Operations Artifact",
            "description": (
                "Validate a workflow or run artifact against the AI Operations v0.4 draft."
            ),
            "input_schema": {
                "type": "object",
                "properties": {"artifact": {"type": "object"}},
                "required": ["artifact"],
                "additionalProperties": False,
            },
            "category": "spec",
            "prerequisites": ["ai_operations_spec"],
            "expected_duration": "fast",
            "mutates_session": False,
        },
    ]
