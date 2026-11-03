"""Guided setup and explainable recall over existing sibling results."""

from __future__ import annotations

from copy import deepcopy
from typing import Any
from urllib.parse import quote

from deep_agentic_core_mcp.services import session


def onboard(_: dict[str, Any] | None = None) -> dict[str, Any]:
    from deep_agentic_core_mcp.tools.core import verify

    readiness = verify()
    return {
        "ok": True,
        "readiness": readiness,
        "steps": [
            {"tool": "core.verify", "purpose": "Check optional sibling availability"},
            {"tool": "core.access_status", "purpose": "Inspect hosted permissions and task scope"},
            {"tool": "lens.analyze_workflow", "purpose": "Supply a workflow and a session_id"},
            {"tool": "core.session_state", "purpose": "Inspect stored evidence and recent history"},
            {
                "tool": "core.report_recall",
                "purpose": "Browse reports and cited investigation notes",
            },
        ],
        "operator_setup": [
            "Configure per-user Tower bindings on the host.",
            "Bind a live Sidecar runtime, task-dedicated revoker and independent operator auth.",
            "Run isolated paired containment acceptance before relying on these boundaries.",
        ],
        "limitations": [
            "Hosted arbitrary chaos execution is disabled",
            "No automatic setup writes",
        ],
    }


def report_recall(arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    args = arguments or {}
    session_id = args.get("session_id")
    if session_id is None:
        return {
            "ok": True,
            "sessions": [
                {
                    "session_id": identifier,
                    "uri": "resource://sessions/" + quote(identifier, safe=""),
                    **state.summary(),
                }
                for identifier, state in sorted(session.all_sessions().items())
            ],
        }
    # Recall never creates an empty report in response to an unknown identifier.
    state = session.all_sessions().get(session_id)
    if state is None:
        return {"ok": False, "error": "No saved session"}
    findings = (state.last_incident_summary or {}).get("findings", [])
    gates = (state.last_release_check or {}).get("gates", [])
    return {
        "ok": True,
        "session_id": session_id,
        "history": deepcopy(list(state.history)),
        "report": deepcopy(
            {
                "analysis": state.last_analysis,
                "comparison": state.last_comparison,
                "chaos": state.last_chaos_report,
                "release_check": state.last_release_check,
                "incident_summary": state.last_incident_summary,
            }
        ),
        "narrative": {
            "basis": "Stored producer results; no fresh scoring, execution or inferred containment",
            "observations": [
                {
                    "text": "Release gate " + str(g.get("name")) + ": " + str(g.get("status")),
                    "source": "release_check.gates[" + str(i) + "]",
                    "evidence": deepcopy(g),
                }
                for i, g in enumerate(gates)
            ]
            + [
                {
                    "text": "Incident signal: " + str(f.get("type")),
                    "source": "incident_summary.findings[" + str(i) + "]",
                    "evidence": deepcopy(f),
                }
                for i, f in enumerate(findings)
            ],
            "unknowns": [
                name
                for name, value in {
                    "analysis": state.last_analysis,
                    "comparison": state.last_comparison,
                    "chaos": state.last_chaos_report,
                    "release_check": state.last_release_check,
                    "incident_summary": state.last_incident_summary,
                }.items()
                if value is None
            ],
        },
    }


def tool_definitions() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "title": title,
            "description": description,
            "input_schema": {
                "type": "object",
                "properties": properties,
                "additionalProperties": False,
            },
            "category": "core",
            "prerequisites": [],
            "expected_duration": "fast",
            "mutates_session": False,
        }
        for name, title, description, properties in [
            ("core.onboard", "Guided setup", "Read-only setup steps with sibling readiness.", {}),
            (
                "core.report_recall",
                "Saved reports",
                "Browse saved artifacts and history with source-cited investigation notes.",
                {"session_id": {"type": "string", "minLength": 1, "maxLength": 128}},
            ),
        ]
    ]
