"""Integration adapters for sibling DeepAgentLabs projects."""

from __future__ import annotations

import sys
from pathlib import Path


class AdapterUnavailableError(RuntimeError):
    """Raised when a sibling repo (agenticlens, agentic-chaos, ...) can't be reached.

    Carries the adapter name so callers (tool wrappers, `core.verify`) can
    report which integration is down without parsing the message text.
    """

    def __init__(self, adapter_name: str, cause: BaseException) -> None:
        self.adapter_name = adapter_name
        self.cause = cause
        super().__init__(f"{adapter_name} adapter is unavailable: {cause}")


def workspace_root() -> Path:
    """Return the workspace directory containing this repo and its siblings.

    The MCP server is developed alongside the reference projects in the same
    parent directory, so tools that need to resolve a sibling repo or a
    sandboxed script path share this single definition of "the workspace".
    """
    return Path(__file__).resolve().parents[4]


def ensure_repo_on_path(repo_name: str, *, src: bool = True) -> Path:
    """Make a sibling repository importable from this workspace.

    The MCP server is developed alongside the reference projects in the same
    parent directory, so we can resolve them directly during local use and in
    tests without requiring wheel installation first.
    """
    repo_root = workspace_root() / repo_name
    import_root = repo_root / "src" if src else repo_root
    import_root_str = str(import_root)
    if import_root_str not in sys.path:
        sys.path.insert(0, import_root_str)
    for site_packages in sorted((repo_root / ".venv" / "lib").glob("python*/site-packages")):
        site_packages_str = str(site_packages)
        if site_packages_str not in sys.path:
            sys.path.insert(0, site_packages_str)
    return repo_root
