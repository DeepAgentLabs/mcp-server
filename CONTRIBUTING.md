# Contributing

Thanks for helping improve the DeepAgentLabs MCP server.

## Local setup

```bash
git clone https://github.com/DeepAgentLabs/mcp-server.git
cd mcp-server
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev,http]"
```

Or with `uv`:

```bash
uv sync --extra dev --extra http
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

## Local and remote development

The same repository provides `deep-agentic-core-mcp` for local stdio and
`deep-agentic-core-mcp-http` for hosted Streamable HTTP. Local stdio requires no
AWS account. HTTP requires bearer credentials and Redis; AWS signup additionally
uses DynamoDB for user records and hashed API keys. HTTP disables chaos script
execution. Preserve local behavior and verify HTTP authentication and user
isolation when changing shared tool dispatch.

HTTP/signup support is included from `0.3.0`; the earlier PyPI `0.2.0`
release supports local stdio. See [docs/user-guide.md](docs/user-guide.md) for
client examples and [docs/remote-hosting.md](docs/remote-hosting.md) for configuration.
Docker definitions belong in `deploy/docker/`; AWS templates belong in `deploy/aws/`.
Never commit credentials, generated API keys, or local deployment state.

## CI and AWS deployment

Pull requests, pushes to `main`, and manual CI runs perform lint, format, typing,
tests across Python 3.10–3.13, and package build checks without deploying AWS.
A pushed `v*` version tag runs the same validation before package publication.
After PyPI succeeds, the release workflow deploys the tagged source to AWS.
It publishes an immutable ECR image, updates the existing CloudFormation
stack, and verifies MCP authentication and integration readiness. It preserves
infrastructure parameters and rejects unrelated infrastructure changes.

AWS deployment requires repository secrets `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, and `MCP_SMOKE_KEY`. See
[deploy/aws/CI-CD.md](deploy/aws/CI-CD.md) for permissions and operational limits.
Infrastructure changes use the separate reviewed operator deployment flow.
AWS deployment is a downstream release job; it does not publish to PyPI itself.

## Releases

Package releases start when a `v*` version tag is pushed. Creating a GitHub
Release manually is not the trigger. `release-pypi.yml` publishes to PyPI using
Trusted Publishing (OIDC), creates the GitHub Release from the changelog, and
then publishes to the MCP Registry. AWS deployment runs after successful PyPI
publication.

1. On a feature branch, update `pyproject.toml`,
   `src/deep_agentic_core_mcp/__init__.py`, both version fields in `server.json`,
   and `uv.lock` (`uv lock`), plus a dated
   `## X.Y.Z - YYYY-MM-DD` section in `CHANGELOG.md`.
2. Run `make check`, commit the release preparation, and merge through a PR.
3. From the updated `main`, create an annotated `vX.Y.Z` tag on the merge commit.
   Use the matching changelog section as its message with
   `git tag -a vX.Y.Z -F <release-notes-file> --cleanup=verbatim`.
4. Push that tag: `git push origin vX.Y.Z`.
5. Approve the existing `pypi` environment gate when required, then verify PyPI,
   GitHub Release, MCP Registry, and AWS deployment jobs.

AWS updates through CI only as part of a version-tag release after PyPI succeeds.
A `main` push does not publish a package or deploy the hosted service.
