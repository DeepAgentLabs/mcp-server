"""Vendor verified, committed AI reference snapshots from the seven product repositories.

Run from the MCP checkout: python scripts/sync_ai_references.py --sources ..
Use --check to verify the packaged pins without requiring sibling checkouts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "src/deep_agentic_core_mcp/resources/documentation"
PRODUCTS = (
    "agenticlens",
    "agentic-evals",
    "agentic-chaos",
    "agentic-sidecar",
    "agenticops-control-tower",
    "ai-operations-spec",
    "mcp-server",
)
ASSETS = {
    "reference": "llms-full.md",
    "index": "ai-reference-index.md",
    "manifest": "ai-docs-manifest.json",
    "license": "LICENSE",
}


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def committed(repo: Path, revision: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=repo)


def sync(sources: Path) -> None:
    products: list[dict[str, Any]] = []
    for product in PRODUCTS:
        repo = sources / product
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo, text=True
        ).strip()
        # Sidecar kept its docs under website/docs before 1.1.0.
        legacy = subprocess.run(
            ["git", "cat-file", "-e", f"{revision}:website/docs/ai-docs-manifest.json"],
            cwd=repo,
            capture_output=True,
        )
        docs = "website/docs" if legacy.returncode == 0 else "docs"
        manifest = json.loads(committed(repo, revision, f"{docs}/ai-docs-manifest.json"))
        # Verify upstream source claims against Git objects, never an uncommitted workspace.
        for source in manifest["sources"]:
            normalized = (
                committed(repo, revision, source["path"])
                .decode("utf-8")
                .replace("\r\n", "\n")
                .encode("utf-8")
            )
            if digest(normalized) != source["sha256"]:
                raise ValueError(f"Stale upstream reference: {product}/{source['path']}")
        reference = committed(repo, revision, f"{docs}/llms-full.md")
        if digest(reference) != manifest["sha256"]:
            raise ValueError(f"Invalid reference checksum: {product}")
        # Parse only this scalar, supporting Python 3.10 without an extra TOML dependency.
        metadata = committed(repo, revision, "pyproject.toml").decode("utf-8")
        version = next(
            line.split('"')[1] for line in metadata.splitlines() if line.startswith("version = ")
        )
        assets = {}
        for kind, filename in ASSETS.items():
            source_path = filename if kind == "license" else f"{docs}/{filename}"
            content = committed(repo, revision, source_path)
            target = DESTINATION / product / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            assets[kind] = {"file": filename, "sha256": digest(content), "bytes": len(content)}
        products.append(
            {
                "product": product,
                "name": manifest["product"],
                "distribution": manifest["distribution"],
                "version": version,
                "source_commit": revision,
                "repository": f"https://github.com/DeepAgentLabs/{product}",
                "source_path": f"{docs}/llms-full.md",
                "source_url": f"https://github.com/DeepAgentLabs/{product}/blob/{revision}/{docs}/llms-full.md",
                "assets": assets,
            }
        )
    (DESTINATION / "catalog.json").write_text(
        json.dumps({"format": "deepagentlabs.documentation.v1", "products": products}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    check()


def check() -> None:
    catalog = json.loads((DESTINATION / "catalog.json").read_text(encoding="utf-8"))
    if [entry["product"] for entry in catalog["products"]] != list(PRODUCTS):
        raise ValueError("Documentation must include exactly the seven products")
    for entry in catalog["products"]:
        for asset in entry["assets"].values():
            content = (DESTINATION / entry["product"] / asset["file"]).read_bytes()
            if digest(content) != asset["sha256"] or len(content) != asset["bytes"]:
                raise ValueError(f"Corrupt documentation: {entry['product']}/{asset['file']}")
        manifest = json.loads(
            (DESTINATION / entry["product"] / ASSETS["manifest"]).read_text(encoding="utf-8")
        )
        if manifest["sha256"] != entry["assets"]["reference"]["sha256"]:
            raise ValueError(f"Manifest mismatch: {entry['product']}")
    print(
        "Verified committed AI references, capability indexes, manifests and licenses: 7 products"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=ROOT.parent)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        sync(args.sources.resolve())
