"""Validate installed-wheel resources without runtime producer dependencies."""

import sys
from pathlib import Path

import deep_agentic_core_mcp
from deep_agentic_core_mcp.services.evals_contract import validate_evals_artifact

assert (
    Path(deep_agentic_core_mcp.__file__).parent
    != Path(__file__).resolve().parents[1] / "src/deep_agentic_core_mcp"
)
report = {
    "suite_name": "wheel-smoke",
    "suite_version": "1",
    "cases": [],
    "summary": {
        "total_cases": 0,
        "passed_cases": 0,
        "failed_cases": 0,
        "pass_rate": 0,
        "average_score": 0,
        "average_latency_ms": 0,
    },
}
validate_evals_artifact(report, "evaluation_report")
validate_evals_artifact({"passed": False, "reasons": ["blocked"], "observed": {}}, "gate_decision")
assert "agentic_evals" not in sys.modules
assert "agenticlens" not in sys.modules
print("Installed native Evals contract resources validated without siblings")
