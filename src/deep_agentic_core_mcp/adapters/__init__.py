"""Integration adapters for sibling DeepAgentLabs projects."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_repo_on_path(repo_name: str, *, src: bool = True) -> Path:
    """Make a sibling repository importable from this workspace.

    The MCP server is developed alongside the reference projects in the same
    parent directory, so we can resolve them directly during local use and in
    tests without requiring wheel installation first.
    """
    workspace_root = Path(__file__).resolve().parents[4]
    repo_root = workspace_root / repo_name
    import_root = repo_root / "src" if src else repo_root
    import_root_str = str(import_root)
    if import_root_str not in sys.path:
        sys.path.insert(0, import_root_str)
    for site_packages in sorted((repo_root / ".venv" / "lib").glob("python*/site-packages")):
        site_packages_str = str(site_packages)
        if site_packages_str not in sys.path:
            sys.path.insert(0, site_packages_str)
    return repo_root
