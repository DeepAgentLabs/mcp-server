"""Keep the accepted runtime matrix aligned with image and CI definitions."""

from pathlib import Path

import pytest

from deep_agentic_core_mcp.services import compatibility

REPO = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("image", ["aws", "render"])
def test_candidate_baseline_matches_image_and_ci(image):
    baseline = compatibility.compatibility_report()["baseline"]
    docker = (REPO / f"deploy/docker/Dockerfile.{image}").read_text()
    workflow = (REPO / ".github/workflows/ci.yml").read_text()
    for name, version in baseline["packages"].items():
        if name != "mcp":
            assert f'"{name}=={version}"' in docker
        if name in {"agentic-chaos", "agentic-sidecar", "agenticlens"}:
            assert f"ref: v{version}" in workflow
    assert baseline["aios"]["acceptance_commit"] in workflow
    assert (
        baseline["aios"]["image_asset_commit"]
        in (REPO / "scripts/fetch_schema_assets.py").read_text()
    )
    assert f"agenticops-control-tower[api]=={baseline['tower']['version']}" in workflow
    assert "ref: v0.10.0\n          path: agentic-chaos" not in workflow
    assert "ref: v0.10.0\n          path: agentic-sidecar" not in workflow


def test_baseline_matches_sdk_lock_and_evals_development_pin():
    baseline = compatibility.compatibility_report()["baseline"]
    lock = (REPO / "uv.lock").read_text()
    sdk = baseline["packages"]["mcp"]
    assert f'name = "mcp"\nversion = "{sdk}"' in lock
    evals = baseline["packages"]["agentic-evals"]
    assert f'"agentic-evals=={evals}"' in (REPO / "pyproject.toml").read_text()
    assert f"agentic-evals=={evals}" in (REPO / ".github/workflows/ci.yml").read_text()
