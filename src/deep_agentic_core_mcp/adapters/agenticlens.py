"""Adapter boundary for agenticlens integration."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from deep_agentic_core_mcp.adapters import AdapterUnavailableError, ensure_repo_on_path
from deep_agentic_core_mcp.services.evals_contract import validate_evals_artifact

_IMPORT_ERROR: Exception | None = None
_version: str | None = None

try:
    ensure_repo_on_path("agenticlens")

    import agenticlens as _agenticlens_pkg
    from agenticlens.comparison.runner import compare_runs as _compare_runs
    from agenticlens.evaluation import (
        EvaluationReport,
        GateConfig,
        evaluate_gate,
        render_html_report,
    )
    from agenticlens.exporters.markdown_exporter import MarkdownExporter
    from agenticlens.models.trace import Run
    from agenticlens.models.workflow import Workflow
    from agenticlens.recommenders.engine import RecommendationEngine

    _version = _agenticlens_pkg.__version__
except Exception as exc:  # noqa: BLE001 - captured for core.verify/core.health reporting
    _IMPORT_ERROR = exc

# Diagnosis and score analysis arrived in agenticlens 0.7.0. Probe them
# separately so an older install keeps every other Lens tool working.
_DIAGNOSIS_ERROR: Exception | None = None
try:
    from agenticlens.diagnosis import AnalysisBudget, DiagnosisConfig
    from agenticlens.diagnosis import diagnose_run as _diagnose_run
    from agenticlens.diagnosis import explain_run as _explain_run
    from agenticlens.evaluation import analyze_scores as _analyze_scores
except Exception as exc:  # noqa: BLE001 - reported per tool
    _DIAGNOSIS_ERROR = exc


# Suite management arrived in agenticlens 0.8.0; probed like diagnosis.
_SUITES_ERROR: Exception | None = None
try:
    from agentic_evals import TestSuite as _TestSuite
    from agenticlens.suites import PIIMasker as _PIIMasker
    from agenticlens.suites import approval_checks as _approval_checks
    from agenticlens.suites import cases_from_runs as _cases_from_runs
    from agenticlens.suites import find_duplicates as _find_duplicates
    from agenticlens.suites import mask_suite as _mask_suite
    from agenticlens.suites import summarize_suite as _summarize_suite
except Exception as exc:  # noqa: BLE001 - reported per tool
    _SUITES_ERROR = exc


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
        "diagnose_run",
        "score_analysis",
        "suite_from_traces",
        "suite_check",
    ]


def _require_diagnosis() -> None:
    _require_available()
    if _DIAGNOSIS_ERROR is not None:
        raise AdapterUnavailableError("agenticlens>=0.7.0 (diagnosis)", _DIAGNOSIS_ERROR)


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


def artifact_digest(artifact: dict[str, Any]) -> str:
    """SHA-256 of the artifact's canonical JSON, so a finding can name its exact input."""
    canonical = json.dumps(artifact, sort_keys=True, separators=(",", ":"), default=str)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _artifact_step_ids(artifact: dict[str, Any]) -> set[str]:
    return {
        str(step["id"])
        for step in artifact.get("steps") or []
        if isinstance(step, dict) and step.get("id")
    }


def _provenance(
    recommendation: dict[str, Any],
    workflow: Workflow,
    artifact: dict[str, Any],
    artifact_ref: dict[str, Any],
) -> dict[str, Any]:
    """Tie one finding back to its artifact, step, and evidence spans.

    Built only from what AgenticLens returned (`step_id`, `evidence`) and the
    analyzed artifact itself; the server adds identity, not analysis.
    """
    steps = {step.id: (index, step) for index, step in enumerate(workflow.steps)}
    step_id = recommendation.get("step_id")
    located = steps.get(step_id) if step_id is not None else None
    evidence = recommendation.get("evidence") or []
    span_ids = sorted({item["span_id"] for item in evidence if item.get("span_id")})
    step: dict[str, Any] | None = None
    if located is not None:
        index, found = located
        raw_steps = artifact.get("steps") or []
        raw_step = raw_steps[index] if index < len(raw_steps) else {}
        step = {
            "id": found.id,
            # False when AgenticLens generated the ID because the artifact had none;
            # `index` (position in the artifact's `steps`) is then the stable locator.
            "id_in_artifact": isinstance(raw_step, dict) and raw_step.get("id") == found.id,
            "name": found.name,
            "type": found.type.value,
            "index": index,
        }
    return {
        "artifact": artifact_ref,
        "step": step,
        "span_ids": span_ids,
        "evidence_sources": sorted({item["source"] for item in evidence if item.get("source")}),
        # Only IDs the caller actually sent count; IDs AgenticLens generated for
        # steps without one are not traceable back to the input.
        "resolved": step is not None
        and step["id_in_artifact"]
        and bool(span_ids)
        and set(span_ids) <= _artifact_step_ids(artifact),
        "producer": {
            "name": "agenticlens",
            "version": _version,
            "optimization_type": recommendation.get("optimization_type"),
        },
    }


def analyze_workflow(artifact: dict[str, Any]) -> dict[str, Any]:
    """Run AgenticLens recommendations against a workflow-shaped artifact.

    Every recommendation gains a `provenance` block (artifact digest, the
    workflow step it is about, evidence span IDs, producer). `resolved` is
    true only when that step and every cited span exist in this artifact.
    """
    _require_available()
    workflow = Workflow.model_validate(artifact)
    engine = RecommendationEngine()
    recommendations = engine.run(workflow)
    artifact_ref = {
        # Only an ID the artifact itself carries; AgenticLens generates one otherwise.
        "workflow_id": artifact.get("id"),
        "workflow_name": workflow.name,
        "digest": artifact_digest(artifact),
    }
    dumped = []
    for recommendation in recommendations:
        item = recommendation.model_dump(mode="json")
        item["provenance"] = _provenance(item, workflow, artifact, artifact_ref)
        dumped.append(item)
    unresolved = [item["title"] for item in dumped if not item["provenance"]["resolved"]]
    return {
        "workflow": _workflow_summary(workflow),
        "recommendation_count": len(recommendations),
        "estimated_savings_pct": RecommendationEngine.estimated_savings_pct(
            workflow, recommendations
        ),
        "estimated_cost_savings": RecommendationEngine.estimated_cost_savings(recommendations),
        "recommendations": dumped,
        "provenance_summary": {
            "artifact": artifact_ref,
            "findings": len(dumped),
            "resolved": len(dumped) - len(unresolved),
            "unresolved_titles": unresolved,
        },
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
    validate_evals_artifact(report, "evaluation_report")
    evaluation_report = EvaluationReport.model_validate(report)
    gate_config = GateConfig.model_validate(thresholds or {})
    decision = evaluate_gate(evaluation_report, gate_config)
    validate_evals_artifact(decision.model_dump(mode="json"), "gate_decision")
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
    validate_evals_artifact(report, "evaluation_report")
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


def diagnose_run(
    run: dict[str, Any],
    *,
    baseline: list[dict[str, Any]] | None = None,
    config: dict[str, Any] | None = None,
    budget: dict[str, Any] | None = None,
    include_narrative: bool = True,
) -> dict[str, Any]:
    """Diagnose one trace run: failures, faulty step and agent, timeline, anomalies."""
    _require_diagnosis()
    report = _diagnose_run(
        Run.model_validate(run),
        baseline=[Run.model_validate(item) for item in baseline] if baseline else None,
        config=DiagnosisConfig.model_validate(config or {}),
        budget=AnalysisBudget.model_validate(budget or {}),
    )
    result: dict[str, Any] = {"report": report.model_dump(mode="json")}
    if include_narrative:
        result["narrative_markdown"] = _explain_run(report)
    return result


def score_analysis(report: dict[str, Any]) -> dict[str, Any]:
    """Deterministic vs model-based scores, judge cost, and evaluator disagreement."""
    _require_diagnosis()
    validate_evals_artifact(report, "evaluation_report")
    analysis = _analyze_scores(EvaluationReport.model_validate(report))
    dumped: dict[str, Any] = analysis.model_dump(mode="json")
    return dumped


def _require_suites() -> None:
    _require_available()
    if _SUITES_ERROR is not None:
        raise AdapterUnavailableError("agenticlens>=0.8.0 (suites)", _SUITES_ERROR)


def suite_from_traces(
    runs: list[dict[str, Any]],
    *,
    name: str,
    version: str,
    latency_margin: float | None = 1.5,
    cost_margin: float | None = 1.5,
    include_output: bool = False,
    mask: bool = True,
    strategy: str = "redact",
) -> dict[str, Any]:
    """Convert successful trace runs into a draft suite of cases needing review."""
    _require_suites()
    result = _cases_from_runs(
        [Run.model_validate(run) for run in runs],
        latency_margin=latency_margin,
        cost_margin=cost_margin,
        include_output=include_output,
    )
    skipped = [item.model_dump(mode="json") for item in result.skipped]
    if not result.cases:
        return {"suite": None, "skipped": skipped, "masking": None}
    suite = _TestSuite(name=name, version=version, cases=result.cases)
    masking = None
    if mask:
        suite, report = _mask_suite(suite, _PIIMasker(strategy=strategy))  # type: ignore[arg-type]
        masking = {"total": report.total, "counts": report.counts}
    return {
        "suite": suite.model_dump(mode="json", exclude_defaults=True),
        "skipped": skipped,
        "masking": masking,
    }


def suite_check(suite: dict[str, Any], *, threshold: float = 0.85) -> dict[str, Any]:
    """Summary, duplicates, unmasked-PII scan, and approval checks for a suite (no storage)."""
    _require_suites()
    parsed = _TestSuite.model_validate(suite)
    checks = _approval_checks(parsed)
    return {
        "summary": _summarize_suite(parsed).model_dump(mode="json"),
        "duplicates": _find_duplicates(parsed, threshold=threshold).model_dump(mode="json"),
        "approval_checks": [check.model_dump(mode="json") for check in checks],
        "approvable": all(check.passed for check in checks),
    }
