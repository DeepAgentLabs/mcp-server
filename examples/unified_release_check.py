"""Walk through the unified release-check workflow on a local workspace checkout.

Run from the workspace root that holds mcp-server and its sibling repos
(agenticlens with its pitch_demo artifacts, agentic-chaos, agentic-evals):

    uv run --project mcp-server python mcp-server/examples/unified_release_check.py

It calls the same handlers an MCP client reaches over stdio:

1. core.compare_runs     - Lens baseline/candidate comparison, stored in the session
2. chaos.run_experiment  - local-only; hosted callers pass chaos_report instead
3. core.release_check    - Evals gate + comparison + chaos, failing closed
4. core.incident_summary - failure signals only; no_signals when nothing failed
5. core.export_report    - the session's evidence as one mcp.unified-report.v1 envelope
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from deep_agentic_core_mcp.server import handle_call_tool

ARTIFACTS = (
    Path(__file__).resolve().parents[2] / "agenticlens" / "examples" / "pitch_demo" / "artifacts"
)
SESSION = "release-demo"


async def call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    result = await handle_call_tool(name, {**arguments, "session_id": SESSION})
    payload: dict[str, Any] = json.loads(result[0].text)
    return payload


def load(name: str) -> dict[str, Any]:
    data: dict[str, Any] = json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))
    return data


def show_gates(check: dict[str, Any]) -> None:
    print(f"  ready={check['ready']} missing={check['missing_evidence']}")
    for gate in check["gates"]:
        print(f"  - {gate['name']}: {gate['status']} {gate['reasons']}")


async def main() -> None:
    trace = load("trace.json")
    comparison = await call("core.compare_runs", {"baseline": [trace], "candidate": [trace]})
    print("== core.compare_runs")
    print("  regressions:", comparison["regressions"])
    print("  guidance:", comparison.get("sample_size_guidance"))

    print("\n== core.release_check before any chaos evidence")
    show_gates(await call("core.release_check", {"evaluation_report": load("evaluation.json")}))

    chaos = await call(
        "chaos.run_experiment",
        {"script": "mcp-server/examples/chaos_target.py", "faults": ["silent_degradation"]},
    )
    print("\n== chaos.run_experiment")
    print(f"  crashed={chaos['crashed']} timed_out={chaos['timed_out']}")

    print("\n== core.release_check with all three kinds of evidence")
    show_gates(await call("core.release_check", {"evaluation_report": load("evaluation.json")}))

    print("\n== core.release_check with a latency budget the run misses")
    blocked = await call(
        "core.release_check",
        {
            "evaluation_report": load("evaluation.json"),
            "thresholds": {"max_average_latency_ms": 1},
        },
    )
    show_gates(blocked)

    incidents = await call("core.incident_summary", {})
    print("\n== core.incident_summary")
    print("  status:", incidents["status"])
    for finding in incidents["findings"]:
        print(f"  - {finding['source']}: {finding['type']}")

    exported = await call("core.export_report", {})
    report = exported["report"]
    print("\n== core.export_report")
    print("  schema_version:", report["schema_version"])
    print("  sections:", [key for key, value in report.items() if value])


if __name__ == "__main__":
    asyncio.run(main())
