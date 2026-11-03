"""Read-only evidence verification delegated to Lens with host-owned trust."""

import json
import os
from pathlib import Path
from typing import Any

from deep_agentic_core_mcp.adapters import ensure_repo_on_path


def execution_verify(arguments: dict[str, Any] | None) -> dict[str, Any]:
    """Never accept keys, trust-store paths, or precomputed verdicts from callers."""
    arguments = arguments or {}
    if set(arguments) - {"bundle", "run_id"}:
        return {"ok": False, "error": "Unexpected verification arguments"}
    try:
        ensure_repo_on_path("agenticlens")
        from agenticlens.integrity.execution import ExecutionBundle, execution_summary
    except ImportError:
        return {"ok": False, "error": "Lens execution verification is unavailable"}
    try:
        path = os.environ.get("DEEP_AGENTIC_CORE_MCP_LENS_TRUST_STORE")
        raw_keys = json.loads(Path(path).read_text()) if path else {}
        keys = {name: bytes.fromhex(value) for name, value in raw_keys.items()}
        run_id = arguments["run_id"]
        if not isinstance(run_id, str) or not run_id:
            raise ValueError("Missing expected run identity")
        summary = execution_summary(
            ExecutionBundle.model_validate(arguments["bundle"]),
            trusted_keys=keys,
            expected_run_id=run_id,
        )
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        return {"ok": False, "error": "Invalid evidence or host trust configuration"}
    return {"ok": summary["verification"]["status"] == "verified", **summary}
