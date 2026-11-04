"""Candidate acceptance baseline and local distribution observations, without imports."""

import json
from importlib import metadata, resources
from typing import Any


def compatibility_report() -> dict[str, Any]:
    """Read packaged baseline; do not import siblings or contact remote services."""
    baseline = json.loads(
        resources.files("deep_agentic_core_mcp.resources")
        .joinpath("compatibility.json")
        .read_text(encoding="utf-8")
    )
    observations = {}
    for package, expected in baseline["packages"].items():
        try:
            installed = metadata.version(package)
        except metadata.PackageNotFoundError:
            installed = None
        observations[package] = {
            "baseline_version": expected,
            "installed_distribution_version": installed,
            "status": (
                "not_installed"
                if installed is None
                else "baseline_match"
                if installed == expected
                else "different_version"
            ),
        }
    return {"baseline": baseline, "local_distributions": observations}
