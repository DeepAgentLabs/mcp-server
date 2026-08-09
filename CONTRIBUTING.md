# Contributing

Thanks for helping improve the DeepAgentLabs MCP server.

## Local setup

```bash
git clone https://github.com/DeepAgentLabs/mcp-server.git
cd mcp-server
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

Or with `uv`:

```bash
uv sync --extra dev
```

## Development workflow

1. Create a focused branch from `main`.
2. Add or update tests with every behavior change.
3. Add or update user-facing examples when the tool behavior, CLI contract, or
   MCP output changes.
4. If a roadmap item is completed or its status changes, update `README.md`
   and the roadmap document in the same pull request.
5. If the work is release-ready, update `pyproject.toml`,
   `src/deep_agentic_core_mcp/__init__.py`, and `CHANGELOG.md` as part of the
   release.
6. Run:

```bash
ruff check .
ruff format --check .
mypy
pytest
```

7. Keep PRs focused — one concern per pull request.
8. Write clear commit messages describing *why*, not just *what*.

## Adding a tool

1. Create handler in `src/deep_agentic_core_mcp/tools/`
2. Register in `tools/registry.py` with name, title, description, and `input_schema`
3. Add entry to `_TOOL_DISPATCH` in `server.py`
4. Add tests in `tests/`
5. Add or update usage examples or generated docs for user-facing behavior

## Releases

Releases are automated via GitHub Actions when a GitHub Release is published.

### Release checklist

1. Update the version string in all locations:
   - `pyproject.toml` → `version = "X.Y.Z"`
   - `src/deep_agentic_core_mcp/__init__.py` → `__version__ = "X.Y.Z"`
   - `CHANGELOG.md` → add a `## X.Y.Z - YYYY-MM-DD` section
2. Commit: `git commit -am "release: vX.Y.Z"`
3. Tag: `git tag vX.Y.Z`
4. Push: `git push origin main --tags`
5. Create a GitHub Release — the workflow publishes to PyPI and the MCP Registry.

The `release-pypi.yml` workflow uses Trusted Publishing (OIDC) — no API token needed.
