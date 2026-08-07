"""Adapter boundary for agenticlens integration."""

from __future__ import annotations

from typing import Any

from deep_agentic_core_mcp.adapters import ensure_repo_on_path

ensure_repo_on_path("agenticlens")

from agenticlens.models.workflow import Workflow  # noqa: E402
from agenticlens.recommenders.engine import RecommendationEngine  # noqa: E402


def describe_capabilities() -> list[str]:
    """Return the supported AgenticLens-backed capabilities."""
    return ["analyze_workflow", "profile_workflow"]


def analyze_workflow(artifact: dict[str, Any]) -> dict[str, Any]:
    """Run AgenticLens recommendations against a workflow-shaped artifact."""
    workflow = Workflow.model_validate(artifact)
    engine = RecommendationEngine()
    recommendations = engine.run(workflow)
    return {
        "workflow": {
            "id": workflow.id,
            "name": workflow.name,
            "step_count": len(workflow.steps),
            "total_tokens": workflow.total_tokens,
            "total_cost": workflow.total_cost,
            "latency_seconds": workflow.latency,
            "chaos_event_count": len(workflow.chaos_events),
        },
        "recommendation_count": len(recommendations),
        "estimated_savings_pct": RecommendationEngine.estimated_savings_pct(
            workflow, recommendations
        ),
        "estimated_cost_savings": RecommendationEngine.estimated_cost_savings(recommendations),
        "recommendations": [
            recommendation.model_dump(mode="json") for recommendation in recommendations
        ],
    }
