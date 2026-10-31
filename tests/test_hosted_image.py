"""Hosted images must ship the sibling versions and spec assets Phase 3 depends on.

v0.3.3 shipped server code for provenance, AIOS export and rule-cited
conformance, but the hosted images still pinned agenticlens 0.5.0, omitted
agentic-chaos and fetched only the v0.4 schemas. These checks keep the image
definitions in step with what the adapters need.
"""

import hashlib
import importlib.util
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
DOCKER = REPO / "deploy" / "docker"
STANDALONE_IMAGES = ["Dockerfile.aws", "Dockerfile.render"]

# Minimum sibling versions whose behavior the hosted tools rely on
# (agenticlens 0.7.0 adds lens.diagnose_run and lens.score_analysis; 0.8.0 adds
# lens.suite_from_traces and lens.suite_check; 0.9.0 adds lens.modelfit_recommend;
# 0.10.0 adds lens.routing_decide; 0.11.0 adds lens.optimization_analyze).
REQUIRED_PINS = {"agenticlens": (0, 11, 0), "agentic-chaos": (0, 5, 1)}

# Spec-root-relative paths the ai_operations_spec adapter reads.
SPEC_ASSETS = {
    "specification/v0.4/schemas/common.schema.json",
    "specification/v0.4/schemas/workflow.schema.json",
    "specification/v0.4/schemas/run.schema.json",
    "specification/v0.4/conformance-rules.json",
    "specification/v0.5/compatibility.json",
}


def _version(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in text.split("."))


@pytest.mark.parametrize("dockerfile", STANDALONE_IMAGES)
def test_standalone_images_pin_phase3_sibling_versions(dockerfile: str) -> None:
    content = (DOCKER / dockerfile).read_text(encoding="utf-8")
    for package, minimum in REQUIRED_PINS.items():
        match = re.search(rf'"{package}==([0-9.]+)"', content)
        assert match, f"{dockerfile} does not pin {package}"
        assert _version(match.group(1)) >= minimum, f"{dockerfile} pins {package} too old"


# Exact sibling releases the current hosted images ship (0.4.3: Lens 0.11.0, Chaos 0.8.0,
# Evals 0.10.0, whose native schemas are the 0.9.0 documents bundled here).
HOSTED_PINS = {
    "agenticlens": "0.11.0",
    "agentic-chaos": "0.8.0",
    "agentic-evals": "0.10.0",
    "agentic-sidecar": "0.9.0",
}


@pytest.mark.parametrize("dockerfile", STANDALONE_IMAGES)
def test_standalone_images_pin_the_released_sibling_versions(dockerfile: str) -> None:
    content = (DOCKER / dockerfile).read_text(encoding="utf-8")
    pins = dict(re.findall(r'"([a-z-]+)==([0-9.]+)"', content))
    assert {package: pins.get(package) for package in HOSTED_PINS} == HOSTED_PINS


@pytest.mark.parametrize("dockerfile", STANDALONE_IMAGES)
def test_standalone_images_fetch_assets_into_the_spec_root(dockerfile: str) -> None:
    content = (DOCKER / dockerfile).read_text(encoding="utf-8")
    assert "fetch_schema_assets.py /opt/workspace/ai-operations-spec\n" in content


def test_fetch_script_pins_every_asset_the_spec_adapter_reads() -> None:
    spec = importlib.util.spec_from_file_location(
        "fetch_schema_assets", REPO / "scripts" / "fetch_schema_assets.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert set(module.CHECKSUMS) == SPEC_ASSETS
    assert re.fullmatch(r"[0-9a-f]{40}", module.COMMIT)
    assert all(re.fullmatch(r"[0-9a-f]{64}", digest) for digest in module.CHECKSUMS.values())


def test_pinned_checksums_match_the_pinned_spec_commit() -> None:
    """Read each asset at the pinned commit (not the sibling's current branch).

    Skips when the sibling checkout lacks that commit, e.g. CI's shallow clone;
    later spec changes on its default branch must not break this check.
    """
    spec_root = REPO.parent / "ai-operations-spec"
    if not (spec_root / ".git").exists():
        pytest.skip("ai-operations-spec git checkout unavailable")
    spec = importlib.util.spec_from_file_location(
        "fetch_schema_assets", REPO / "scripts" / "fetch_schema_assets.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    present = subprocess.run(
        ["git", "-C", str(spec_root), "cat-file", "-e", f"{module.COMMIT}^{{commit}}"],
        capture_output=True,
        check=False,
    )
    if present.returncode != 0:
        pytest.skip("pinned ai-operations-spec commit not present in this checkout")
    for relative, expected in module.CHECKSUMS.items():
        content = subprocess.run(
            ["git", "-C", str(spec_root), "show", f"{module.COMMIT}:{relative}"],
            capture_output=True,
            check=True,
        ).stdout
        assert hashlib.sha256(content).hexdigest() == expected, relative


def test_workspace_image_copies_chaos_and_spec_catalogs() -> None:
    dockerfile = (DOCKER / "Dockerfile").read_text(encoding="utf-8")
    ignore = (DOCKER / "Dockerfile.dockerignore").read_text(encoding="utf-8")
    for path in (
        "agentic-chaos/src",
        "ai-operations-spec/specification/v0.4/conformance-rules.json",
        "ai-operations-spec/specification/v0.5/compatibility.json",
    ):
        assert f"COPY {path}" in dockerfile
        assert f"!{path}" in ignore


def test_release_does_not_automatically_deploy_aws():
    workflow = (REPO / ".github/workflows/release-pypi.yml").read_text()
    assert "  deploy:" not in workflow
    assert "aws-actions/configure-aws-credentials" not in workflow
    assert "scripts/aws_ci_deploy.py" not in workflow
