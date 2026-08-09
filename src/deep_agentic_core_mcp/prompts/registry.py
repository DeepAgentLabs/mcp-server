"""Reusable prompt catalog, wired into the server's `prompts/list` and `prompts/get`."""

from typing import Any


def list_prompts() -> list[dict[str, Any]]:
    """Return the current prompt registry, with MCP-shaped `arguments`."""
    return [
        {
            "name": "lens.workflow_summary",
            "description": "Summarize an analyzed workflow for a human operator.",
            "arguments": [
                {
                    "name": "workflow_name",
                    "description": "Name of the analyzed workflow.",
                    "required": True,
                },
                {
                    "name": "recommendation_count",
                    "description": "Number of recommendations produced.",
                    "required": False,
                },
                {
                    "name": "estimated_savings_pct",
                    "description": "Estimated token savings percentage.",
                    "required": False,
                },
            ],
        },
        {
            "name": "lens.compare_summary",
            "description": "Summarize a baseline-vs-candidate run comparison for a release "
            "decision.",
            "arguments": [
                {
                    "name": "baseline_label",
                    "description": "Baseline group label.",
                    "required": False,
                },
                {
                    "name": "candidate_label",
                    "description": "Candidate group label.",
                    "required": False,
                },
            ],
        },
        {
            "name": "chaos.experiment_brief",
            "description": "Explain the intent and expected impact of a chaos run.",
            "arguments": [
                {
                    "name": "faults",
                    "description": "Comma-separated fault names being injected.",
                    "required": True,
                },
                {
                    "name": "script",
                    "description": "Target script being exercised.",
                    "required": False,
                },
            ],
        },
    ]


def render_prompt(name: str, arguments: dict[str, str] | None = None) -> str:
    """Render a prompt template's user-message text for `prompts/get`."""
    arguments = arguments or {}
    if name == "lens.workflow_summary":
        savings = arguments.get("estimated_savings_pct")
        savings_clause = f" with an estimated {savings}% token savings" if savings else ""
        return (
            "Summarize the AgenticLens analysis of workflow "
            f"'{arguments.get('workflow_name', 'the workflow')}' for a human operator. "
            f"It produced {arguments.get('recommendation_count', 'an unknown number of')} "
            f"recommendation(s){savings_clause}. Call out the highest-severity recommendation "
            "first, in plain language."
        )
    if name == "lens.compare_summary":
        return (
            "Summarize the run comparison between "
            f"'{arguments.get('baseline_label', 'baseline')}' and "
            f"'{arguments.get('candidate_label', 'candidate')}' for a human operator, "
            "highlighting any regressions and whether the candidate is safe to ship."
        )
    if name == "chaos.experiment_brief":
        return (
            "Explain the intent and expected impact of injecting the fault(s) "
            f"'{arguments.get('faults', 'the configured faults')}' into "
            f"'{arguments.get('script', 'the target script')}', for someone who has not "
            "read the agentic-chaos documentation."
        )
    raise KeyError(f"Unknown prompt: {name}")
