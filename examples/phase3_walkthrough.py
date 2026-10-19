"""Walk through the Phase 3 surface on a local workspace checkout.

Run from the workspace root that holds mcp-server and its sibling repos
(agenticlens, agentic-chaos>=0.5.1, ai-operations-spec):

    uv run --project mcp-server python mcp-server/examples/phase3_walkthrough.py

It calls the same handlers an MCP client reaches over stdio:

1. lens.analyze_workflow - every finding carries artifact/step/span provenance
2. chaos.run_experiment  - the result includes an AIOS v0.4-draft run export
3. spec.validate_artifact - rule-cited conformance and spec_version routing
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from deep_agentic_core_mcp.server import handle_call_tool

EXAMPLES = Path(__file__).resolve().parent


async def call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    result = await handle_call_tool(name, arguments)
    payload: dict[str, Any] = json.loads(result[0].text)
    return payload


async def main() -> None:
    workflow = json.loads((EXAMPLES / "provenance_workflow.json").read_text(encoding="utf-8"))
    analysis = await call("lens.analyze_workflow", {"artifact": workflow, "session_id": "phase3"})
    print("== lens.analyze_workflow provenance")
    for finding in analysis["recommendations"]:
        provenance = finding["provenance"]
        step = provenance["step"] or {}
        print(f"- {finding['title']}: step={step.get('name')} spans={provenance['span_ids']}")
    print("  summary:", analysis["provenance_summary"])

    experiment = await call(
        "chaos.run_experiment",
        {
            "script": "mcp-server/examples/chaos_target.py",
            "faults": ["silent_degradation"],
            "workflow_id": "customer-support",
            "session_id": "phase3",
        },
    )
    print("\n== chaos.run_experiment AIOS export")
    print("  export:", {k: v for k, v in experiment["aios_export"].items() if k != "issues"})
    run = experiment["aios_run"]
    if run is None:
        print("  (install agentic-chaos>=0.5.1 for AIOS run export)")
        return

    report = await call("spec.validate_artifact", {"artifact": run})
    print("\n== spec.validate_artifact on the exported run")
    print(
        "  compatibility:", report["compatibility"]["decision"], report["compatibility"]["rule_id"]
    )
    print("  conformance summary:", report["conformance"]["summary"])

    future = await call(
        "spec.validate_artifact", {"artifact": {**run, "spec_version": "0.5-draft"}}
    )
    print("\n== a run declaring an unpublished marker")
    print("  ", future["compatibility"]["decision"], future["compatibility"]["rule_id"])
    print("  ", future["errors"][0])


if __name__ == "__main__":
    asyncio.run(main())
