## Deep Agentic Core MCP Development Reference

## Build and Run

- Install: `uv sync --extra dev` or `pip install -e ".[dev]"`
- Test: `pytest`
- Lint: `ruff check .`
- Type check: `mypy`
- Run server: `uv run deep-agentic-core-mcp`

## Code Style

- Strict typing (mypy strict mode, Python 3.10+)
- Line length: 100
- Ruff rules: E, F, I, UP, B, SIM, N

## Repo Map

| Path | Purpose |
|------|---------|
| `src/deep_agentic_core_mcp/server.py` | MCP server entrypoint and handler registration |
| `src/deep_agentic_core_mcp/tools/` | Tool implementations (core, lens, chaos, spec) |
| `src/deep_agentic_core_mcp/adapters/` | Integration adapters for sibling repos |
| `src/deep_agentic_core_mcp/resources/` | MCP resource catalog |
| `src/deep_agentic_core_mcp/schemas/` | Pydantic descriptors |
| `tests/` | Pytest test suite |

## Release

1. Bump version in `pyproject.toml`, `src/deep_agentic_core_mcp/__init__.py`, and `CHANGELOG.md`
2. Commit: `git commit -am "release: vX.Y.Z"`
3. Tag: `git tag vX.Y.Z`
4. Push: `git push origin main --tags`
5. Create a GitHub Release — the workflow publishes to PyPI and the MCP Registry
