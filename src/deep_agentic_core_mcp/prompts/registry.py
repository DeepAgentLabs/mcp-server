"""Reusable prompt catalog placeholders."""


def list_prompts() -> list[dict[str, str]]:
    """Return the initial prompt registry."""
    return [
        {
            "name": "lens.workflow_summary",
            "description": "Summarize an analyzed workflow for a human operator.",
        },
        {
            "name": "chaos.experiment_brief",
            "description": "Explain the intent and expected impact of a chaos run.",
        },
    ]
