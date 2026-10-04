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

The HTTP/signup changes are unreleased source work, rather than features of the
existing PyPI `0.2.0` release. See [docs/user-guide.md](docs/user-guide.md) for
client examples and [docs/remote-hosting.md](docs/remote-hosting.md) for configuration.
Docker definitions belong in `deploy/docker/`; AWS templates belong in `deploy/aws/`.
Never commit credentials, generated API keys, or local deployment state.

## CI and AWS deployment

Pull requests run lint, format, typing, tests across Python 3.10–3.13, and package
build checks. Pushes/merges to `main` and manual CI runs on `main` deploy the AWS
service after these checks succeed. CI publishes an immutable ECR image, updates
the existing CloudFormation deployment, and verifies hosted MCP authentication
and integration readiness. It preserves infrastructure parameters and rejects
unrelated infrastructure changes.

AWS deployment requires repository secrets `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, and `MCP_SMOKE_KEY`. See
[deploy/aws/CI-CD.md](deploy/aws/CI-CD.md) for permissions and operational limits.
Infrastructure changes use the separate reviewed operator deployment flow.
An AWS deployment does not publish a package version to PyPI.

## Releases

Package releases start when a `v*` version tag is pushed. Creating a GitHub
Release manually is not the trigger. `release-pypi.yml` publishes to PyPI using
Trusted Publishing (OIDC), creates the GitHub Release from the changelog, and
then publishes to the MCP Registry.

1. On a feature branch, update `pyproject.toml`,
   `src/deep_agentic_core_mcp/__init__.py`, and a dated
   `## X.Y.Z - YYYY-MM-DD` section in `CHANGELOG.md`.
2. Run `make check`, commit the release preparation, and merge through a PR.
3. From the updated `main`, create an annotated `vX.Y.Z` tag on the merge commit.
   Use the matching changelog section as its message with
   `git tag -a vX.Y.Z -F <release-notes-file> --cleanup=verbatim`.
4. Push that tag: `git push origin vX.Y.Z`.
5. Verify the PyPI, GitHub Release, and MCP Registry workflow jobs.

The version-tag workflow does not deploy AWS. AWS runs independently on the
`main` push from the merge, so hosted fixes can ship before the next PyPI release.
