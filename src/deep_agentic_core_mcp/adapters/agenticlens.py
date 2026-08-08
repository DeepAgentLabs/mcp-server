"""Adapter boundary for agenticlens integration."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from deep_agentic_core_mcp.adapters import AdapterUnavailableError, ensure_repo_on_path

_IMPORT_ERROR: Exception | None = None
_version: str | None = None

try:
    ensure_repo_on_path("agenticlens")

    import agenticlens as _agenticlens_pkg
    from agenticlens.comparison.runner import compare_runs as _compare_runs
    from agenticlens.evaluation.gate import GateConfig, evaluate_gate
    from agenticlens.evaluation.html_report import render_html_report
    from agenticlens.evaluation.models import EvaluationReport
    from agenticlens.exporters.markdown_exporter import MarkdownExporter
    from agenticlens.models.trace import Run
    from agenticlens.models.workflow import Workflow
    from agenticlens.recommenders.engine import RecommendationEngine

    _version = _agenticlens_pkg.__version__
except Exception as exc:  # noqa: BLE001 - captured for core.verify/core.health reporting
    _IMPORT_ERROR = exc


def _require_available() -> None:
    if _IMPORT_ERROR is not None:
        raise AdapterUnavailableError("agenticlens", _IMPORT_ERROR)


def probe() -> dict[str, Any]:
    """Report whether the agenticlens integration is reachable."""
    return {
        "available": _IMPORT_ERROR is None,
        "version": _version,
        "error": None if _IMPORT_ERROR is None else str(_IMPORT_ERROR),
    }


def describe_capabilities() -> list[str]:
    """Return the supported AgenticLens-backed capabilities."""
    return [
        "analyze_workflow",
        "profile_workflow",
        "report_summary",
        "compare_runs",
        "slo_summary",
        "audit_report",
    ]


def _workflow_summary(workflow: Workflow) -> dict[str, Any]:
    return {
        "id": workflow.id,
        "name": workflow.name,
        "step_count": len(workflow.steps),
        "total_tokens": workflow.total_tokens,
        "total_cost": workflow.total_cost,
        "latency_seconds": workflow.latency,
        "chaos_event_count": len(workflow.chaos_events),
    }


def analyze_workflow(artifact: dict[str, Any]) -> dict[str, Any]:
    """Run AgenticLens recommendations against a workflow-shaped artifact."""
    _require_available()
    workflow = Workflow.model_validate(artifact)
    engine = RecommendationEngine()
    recommendations = engine.run(workflow)
    return {
        "workflow": _workflow_summary(workflow),
        "recommendation_count": len(recommendations),
        "estimated_savings_pct": RecommendationEngine.estimated_savings_pct(
            workflow, recommendations
        ),
        "estimated_cost_savings": RecommendationEngine.estimated_cost_savings(recommendations),
        "recommendations": [
            recommendation.model_dump(mode="json") for recommendation in recommendations
        ],
    }


def report_summary(artifact: dict[str, Any]) -> dict[str, Any]:
    """Analyze a workflow and render it through AgenticLens's own Markdown exporter.

    Reuses `MarkdownExporter` rather than reimplementing report formatting -
    the exporter only writes to a path, so a temp file bridges the gap.
    """
    _require_available()
    workflow = Workflow.model_validate(artifact)
    engine = RecommendationEngine()
    recommendations = engine.run(workflow)

    with tempfile.TemporaryDirectory() as tmp_dir:
        report_path = Path(tmp_dir) / "report.md"
        MarkdownExporter().export(workflow, report_path, recommendations)
        markdown_report = report_path.read_text(encoding="utf-8")

    return {
        "workflow": _workflow_summary(workflow),
        "recommendation_count": len(recommendations),
        "estimated_savings_pct": RecommendationEngine.estimated_savings_pct(
            workflow, recommendations
        ),
        "estimated_cost_savings": RecommendationEngine.estimated_cost_savings(recommendations),
        "markdown_report": markdown_report,
    }


def compare_runs(
    baseline: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    *,
    regression_threshold: float = 0.05,
) -> dict[str, Any]:
    """Compare repeated baseline and candidate trace runs for regressions."""
    _require_available()
    baseline_runs = [Run.model_validate(item) for item in baseline]
    candidate_runs = [Run.model_validate(item) for item in candidate]
    report = _compare_runs(
        baseline_runs,
        candidate_runs,
        regression_threshold=regression_threshold,
    )
    dumped: dict[str, Any] = report.model_dump(mode="json")
    return dumped


def slo_summary(
    report: dict[str, Any],
    thresholds: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply release-gate style SLO thresholds to an evaluation report."""
    _require_available()
    evaluation_report = EvaluationReport.model_validate(report)
    gate_config = GateConfig.model_validate(thresholds or {})
    decision = evaluate_gate(evaluation_report, gate_config)
    return {
        "suite_name": evaluation_report.suite_name,
        "suite_version": evaluation_report.suite_version,
        "summary": evaluation_report.summary.model_dump(mode="json"),
        "thresholds": gate_config.model_dump(mode="json"),
        "decision": decision.model_dump(mode="json"),
    }


def audit_report(
    report: dict[str, Any],
    *,
    include_html: bool = False,
) -> dict[str, Any]:
    """Return the full case-by-case evaluation detail, for audit trails."""
    _require_available()
    evaluation_report = EvaluationReport.model_validate(report)
    result: dict[str, Any] = {
        "suite_name": evaluation_report.suite_name,
        "suite_version": evaluation_report.suite_version,
        "summary": evaluation_report.summary.model_dump(mode="json"),
        "cases": [case.model_dump(mode="json") for case in evaluation_report.cases],
    }
    if include_html:
        result["html_report"] = render_html_report(evaluation_report)
    return result
