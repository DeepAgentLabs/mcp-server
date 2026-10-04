# Container builds

Dockerfiles and ignore files live here. Build contexts still refer to the
repository root (AWS/Render) or parent workspace (local sibling-package build).
Run the build helper from the repository root; it stages only required files
and applies the common `.dockerignore`, including with Docker's legacy builder:

```bash
python3 scripts/build_container.py --target aws --tag deep-agentic-core-mcp:my-release
python3 scripts/build_container.py --target render --tag deep-agentic-core-mcp:render
python3 scripts/build_container.py --target workspace --tag deep-agentic-core-mcp:local
```

`workspace` is the default and needs sibling `agenticlens` and
`ai-operations-spec` checkouts. AWS and Render builds use this repository's
source, published AgenticLens, and pinned schema downloads.

With BuildKit, direct standalone builds from the repository root also work:

```bash
docker build -f deploy/docker/Dockerfile.aws -t deep-agentic-core-mcp:my-release .
docker build -f deploy/docker/Dockerfile.render -t deep-agentic-core-mcp:render .
```

The adjacent `Dockerfile.*.dockerignore` files filter those direct build
contexts. The helper is the portable option across Docker builders.
