"""Minimal target script for the `chaos.run_experiment` MCP tool.

Standalone: `python examples/chaos_target.py`
Under chaos (CLI): `agentic-chaos chaos run examples/chaos_target.py --inject silent_degradation`
Under chaos (MCP): call `chaos.run_experiment` with
`{"script": "mcp-server/examples/chaos_target.py", "faults": ["silent_degradation"]}`

Outside a chaos session `chaos_call()` is transparent, so running this script
directly behaves exactly like calling `answer_question()` itself.
"""

from agentic_chaos import chaos_call


def answer_question(prompt: str) -> str:
    """Stand-in for a real LLM call - deterministic so faults are easy to see."""
    return f"answer to: {prompt}"


if __name__ == "__main__":
    result = chaos_call(answer_question, "What is the capital of France?", step_name="answer")
    print(result)
