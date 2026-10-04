"""Build with a minimal context, including on Docker's legacy builder."""

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", default="deep-agentic-core-mcp:latest")
    parser.add_argument("--target", choices=["workspace", "aws", "render"], default="workspace")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    workspace = repo.parent
    paths = [
        "mcp-server/deploy/docker/Dockerfile",
        "mcp-server/pyproject.toml",
        "mcp-server/README.md",
        "mcp-server/src",
        "agenticlens/pyproject.toml",
        "agenticlens/README.md",
        "agenticlens/LICENSE",
        "agenticlens/src",
        "agenticlens/schemas",
        "ai-operations-spec/specification/v0.4/schemas",
    ]
    dockerfile = "mcp-server/deploy/docker/Dockerfile"
    if args.target != "workspace":
        workspace = repo
        dockerfile = f"deploy/docker/Dockerfile.{args.target}"
        paths = [
            dockerfile,
            "pyproject.toml",
            "README.md",
            "src",
            "scripts/fetch_schema_assets.py",
        ]
    with tempfile.TemporaryDirectory(prefix="mcp-image-") as temp:
        root = Path(temp)
        shutil.copy2(repo / "deploy/docker/.dockerignore", root / ".dockerignore")
        for relative in paths:
            source, target = workspace / relative, root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(
                    source,
                    target,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".env*", ".git", ".venv"),
                )
            else:
                shutil.copy2(source, target)
        subprocess.run(
            ["docker", "build", "-f", str(root / dockerfile), "-t", args.tag, temp],
            check=True,
        )


if __name__ == "__main__":
    main()
