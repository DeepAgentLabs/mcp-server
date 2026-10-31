"""Central tool metadata registry."""

from typing import Any

from deep_agentic_core_mcp.tools.tower import tool_definitions

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

    - `category`: rough grouping (`core`, `lens`, `chaos`, `sidecar`, `spec`)
    - `prerequisites`: adapter names (see `adapters/`) that must be
      available for the tool to succeed
    - `expected_duration`: `"instant" | "fast" | "slow"`, a rough hint for
      hosts deciding whether to show a spinner
    - `mutates_session`: whether the call writes to the in-memory session
      store (`services/session.py`)
    """
    return tool_definitions() + [
        {
            "name": "evals.validate_artifact",
            "title": "Validate Native Evals Artifact",
            "description": "Validate native evaluation reports or gate decisions against the "
            "published Evals 1.0 schemas. Structural validation is not AIOS conformance "
            "and does not compute or pass a release gate.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "artifact": {"type": "object"},
                    "artifact_type": {"enum": ["evaluation_report", "gate_decision"]},
                },
                "required": ["artifact", "artifact_type"],
                "additionalProperties": False,
            },
            "category": "evals",
            "prerequisites": [],
            "expected_duration": "fast",
            "mutates_session": False,
        },
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
            "description": "Check connectivity to agenticlens, agentic-chaos, "
            "agentic-sidecar, and ai-operations-spec, and report readiness.",
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
            "name": "core.access_status",
            "title": "Access Status",
            "description": "Report the calling hosted key's effective access policy: allow and "
            "deny globs, task scope, expiry, and the tools it may call right now. Policies are "
            "enforced at dispatch, outside the model; local stdio reports `enforced: false`.",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
            "category": "core",
            "prerequisites": [],
            "expected_duration": "instant",
            "mutates_session": False,
        },
        {
            "name": "lens.analyze_workflow",
            "title": "Analyze Workflow",
            "description": "Analyze an AgenticLens-compatible workflow artifact. Each "
            "recommendation carries a `provenance` block (artifact digest, workflow step, "
            "evidence span IDs, producer) and the response summarizes how many resolve.",
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
            "name": "lens.diagnose_run",
            "title": "Diagnose Run",
            "description": "Diagnose a trace run: failure taxonomy, faulty step and agent "
            "with confidence and supporting spans, incident timeline, anomalies against "
            "optional baseline runs, and an investigation narrative. Needs agenticlens>=0.7.0.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "run": {"type": "object"},
                    "baseline": {"type": "array", "items": {"type": "object"}},
                    "config": {"type": "object"},
                    "budget": {"type": "object"},
                    "include_narrative": {"type": "boolean"},
                    **_SESSION_ID_PROPERTY,
                },
                "required": ["run"],
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": False,
        },
        {
            "name": "lens.score_analysis",
            "title": "Score Analysis",
            "description": "Report deterministic and model-based scores separately, judge cost "
            "(kept apart from agent cost), and evaluator disagreement for an evaluation "
            "report. Needs agenticlens>=0.7.0.",
            "input_schema": {
                "type": "object",
                "properties": {"report": {"type": "object"}, **_SESSION_ID_PROPERTY},
                "required": ["report"],
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": False,
        },
        {
            "name": "lens.suite_from_traces",
            "title": "Suite From Traces",
            "description": "Convert successful trace runs into a draft regression suite: each case "
            "expects the run's tool trajectory and latency/cost within a margin, is marked "
            "needs_review, and has PII masked unless 'mask' is false. Failed runs are skipped "
            "with a reason. Nothing is stored. Needs agenticlens>=0.8.0.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "runs": {"type": "array", "items": {"type": "object"}, "minItems": 1},
                    "name": {"type": "string", "minLength": 1},
                    "version": {"type": "string", "minLength": 1},
                    "latency_margin": {"type": ["number", "null"], "minimum": 1},
                    "cost_margin": {"type": ["number", "null"], "minimum": 1},
                    "include_output": {"type": "boolean"},
                    "mask": {"type": "boolean"},
                    "strategy": {"type": "string", "enum": ["redact", "hash"]},
                    "salt": {
                        "type": "string",
                        "description": "Salt for 'hash' masking; a random per-call salt is "
                        "used (and not returned) when omitted.",
                    },
                    **_SESSION_ID_PROPERTY,
                },
                "required": ["runs", "name", "version"],
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": False,
        },
        {
            "name": "lens.suite_check",
            "title": "Suite Check",
            "description": "Check a test suite before approval: counts by split, domain, tag, "
            "source and review status; exact, near and conflicting duplicates; unmasked PII "
            "(types and locations only); and the approval checks AgenticLens would run. "
            "Nothing is stored. Needs agenticlens>=0.8.0.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "suite": {"type": "object"},
                    "threshold": {"type": "number", "exclusiveMinimum": 0, "maximum": 1},
                    **_SESSION_ID_PROPERTY,
                },
                "required": ["suite"],
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": False,
        },
        {
            "name": "lens.modelfit_recommend",
            "title": "ModelFit Recommend",
            "description": "Recommend a model per task category from supplied AgenticLens "
            "experiment reports, under hard quality, cost, latency, safety, provider and "
            "deployment constraints that fail closed. Returns per-category recommendations "
            "with confidence, fallbacks, savings against a reference variant and quality "
            "risks, plus the full ModelFit report and task-level model matrix. No model is "
            "called and nothing is stored. Needs agenticlens>=0.9.0.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "reports": {
                        "type": "array",
                        "items": {"type": "object"},
                        "minItems": 1,
                        "description": "Experiment reports (agenticlens experiment run --save).",
                    },
                    "config": {
                        "type": "object",
                        "description": "ModelFit config: categories, defaults, weights, "
                        "candidates, reference_variant_id.",
                    },
                    "variant_metadata": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "object",
                            "additionalProperties": {"type": "string"},
                        },
                        "description": "Variant ID -> manifest metadata (provider, "
                        "deployment, capabilities).",
                    },
                    **_SESSION_ID_PROPERTY,
                },
                "required": ["reports"],
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": False,
        },
        {
            "name": "lens.routing_decide",
            "title": "Routing Decision",
            "description": "Explain a model route from a saved ModelFit report and routing policy. "
            "Returns selected targets, fallback chain, confidence, constraint rejections and "
            "evidence/policy hashes. Read-only in every mode: no model calls, callbacks, "
            "audit-file writes or approval execution. Needs agenticlens>=0.10.0.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "report": {"type": "object", "description": "ModelFit report JSON."},
                    "request": {
                        "type": "object",
                        "properties": {
                            "request_id": {"type": "string", "minLength": 1},
                            "category_id": {"type": "string", "minLength": 1},
                        },
                        "required": ["request_id", "category_id"],
                        "additionalProperties": False,
                    },
                    "policy": {
                        "type": "object",
                        "description": "Lens RoutingPolicy; default advisory.",
                    },
                    **_SESSION_ID_PROPERTY,
                },
                "required": ["report", "request"],
                "additionalProperties": False,
            },
            "category": "lens",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": False,
        },
        {
            "name": "lens.optimization_analyze",
            "title": "Optimization Opportunities",
            "description": "Rank evidence-backed optimizations from AgenticLens Run traces: "
            "prompt caching and compression, retrieval pruning and reranking, memory "
            "summarization, tool caching, retry policy, redundant steps, unnecessary handoffs "
            "and quality-cost trade-offs between variants. Each opportunity keeps projected "
            "benefit, confidence and quality risks separate. Advisory and read-only: no "
            "decision ledger writes and nothing is changed. Needs agenticlens>=0.11.0.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "traces": {
                        "type": "array",
                        "items": {"type": "object"},
                        "minItems": 1,
                        "description": "AgenticLens Run trace JSON objects with unique run_id.",
                    },
                    "config": {
                        "type": "object",
                        "description": "Lens OptimizationConfig thresholds; unknown keys fail.",
                    },
                    "baseline_variant_id": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Variant to compare quality-cost trade-offs against.",
                    },
                    **_SESSION_ID_PROPERTY,
                },
                "required": ["traces"],
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
            "faults and report the resulting events. The script must also pass the "
            "configured allow/deny glob policy. With agentic-chaos>=0.5.1 the result "
            "includes an AI Operations v0.4-draft run artifact and its conformance check.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Script path, resolved inside the workspace root.",
                    },
                    "faults": {"type": "array", "items": {"type": "string"}},
                    "timeout_seconds": {"type": "number"},
                    "export_aios": {
                        "type": "boolean",
                        "description": "Attach an AIOS run export (`aios_run`). Defaults to true.",
                    },
                    "workflow_id": {
                        "type": "string",
                        "description": "External Workflow ID for the export's run-of link.",
                    },
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
            "name": "chaos.export_aios_run",
            "title": "Export Chaos Report as AIOS Run",
            "description": "Convert a chaos report into an AI Operations v0.4-draft run "
            "artifact (via agentic-chaos>=0.5.1) and validate it with rule-cited "
            "conformance. 'report' may be omitted to reuse the session's last experiment.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "report": {"type": "object"},
                    "status": {
                        "type": "string",
                        "enum": ["created", "running", "completed", "failed", "cancelled"],
                        "description": "Observed run status; derived from crashed/timed_out "
                        "when omitted.",
                    },
                    "workflow_id": {"type": "string"},
                    **_SESSION_ID_PROPERTY,
                },
                "additionalProperties": False,
            },
            "category": "chaos",
            "prerequisites": ["agentic_chaos", "ai_operations_spec"],
            "expected_duration": "fast",
            "mutates_session": False,
        },
        {
            "name": "sidecar.status",
            "title": "Sidecar Status",
            "description": "Report whether agentic-sidecar is importable and whether "
            "its decision runtime APIs are installed; no live task connection is implied.",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
            "category": "sidecar",
            "prerequisites": ["agentic_sidecar"],
            "expected_duration": "instant",
            "mutates_session": False,
        },
        {
            "name": "sidecar.module_inventory",
            "title": "Sidecar Module Inventory",
            "description": "List installed modules, framework adapter files, "
            "and integration placeholders present in agentic-sidecar.",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
            "category": "sidecar",
            "prerequisites": ["agentic_sidecar"],
            "expected_duration": "instant",
            "mutates_session": False,
        },
        {
            "name": "spec.validate_artifact",
            "title": "Validate AI Operations Artifact",
            "description": "Validate a workflow or run artifact against the schema set its "
            "`spec_version` names (v0.5 compatibility rules), returning a conformance report "
            "that cites AI Operations rule IDs separately from server presentation.",
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
        {
            "name": "core.compare_runs",
            "title": "Unified Run Comparison",
            "description": "Compare baseline and candidate trace runs for regressions, "
            "storing the comparison for core.release_check. Same behavior as "
            "lens.compare_runs.",
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
            "category": "core",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": True,
        },
        {
            "name": "core.release_check",
            "title": "Unified Release Check",
            "description": "Decide release readiness from a Lens comparison, an Evals "
            "report (judged by the Evals release gate) and a chaos.run_experiment report. "
            "Fails closed: required evidence that is missing, malformed or from a failed "
            "call blocks readiness. Comparison and chaos evidence default to this session.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "comparison": {
                        "type": "object",
                        "description": "A lens/core.compare_runs result. Defaults to the "
                        "session's last comparison.",
                    },
                    "evaluation_report": {
                        "type": "object",
                        "description": "A native Agentic Evals evaluation report.",
                    },
                    "chaos_report": {
                        "type": "object",
                        "description": "A chaos.run_experiment result. Defaults to the "
                        "session's last chaos report.",
                    },
                    "thresholds": {
                        "type": "object",
                        "description": "Evals GateConfig fields (for example min_pass_rate, "
                        "max_failed_cases). Unknown keys are rejected. The Evals default "
                        "requires every case to pass.",
                    },
                    "required_evidence": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["comparison", "evaluation", "chaos"]},
                        "minItems": 1,
                        "uniqueItems": True,
                        "description": "Evidence kinds that must be present. Defaults to "
                        "all three.",
                    },
                    **_SESSION_ID_PROPERTY,
                },
                "additionalProperties": False,
            },
            "category": "core",
            "prerequisites": ["agenticlens"],
            "expected_duration": "fast",
            "mutates_session": True,
        },
        {
            "name": "core.incident_summary",
            "title": "Unified Incident Summary",
            "description": "Collect regressions, chaos crashes or timeouts, failed "
            "evaluation cases and blocked release gates from supplied or session "
            "evidence for investigation. Reports no_signals when nothing failed.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "comparison": {"type": "object"},
                    "evaluation_report": {"type": "object"},
                    "chaos_report": {"type": "object"},
                    **_SESSION_ID_PROPERTY,
                },
                "additionalProperties": False,
            },
            "category": "core",
            "prerequisites": [],
            "expected_duration": "fast",
            "mutates_session": True,
        },
        {
            "name": "core.export_report",
            "title": "Export Unified Report",
            "description": "Export the session's workflow, analysis, comparison, chaos, "
            "release-check and incident evidence as one MCP-local JSON envelope "
            "(mcp.unified-report.v1; not an AIOS artifact).",
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
    ]
