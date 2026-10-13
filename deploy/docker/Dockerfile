# Build from the parent workspace:
# python3 mcp-server/scripts/build_container.py --tag deep-agentic-core-mcp:latest
FROM python:3.12-slim
WORKDIR /app
COPY mcp-server/pyproject.toml mcp-server/README.md ./
COPY mcp-server/src ./src
COPY agenticlens/pyproject.toml agenticlens/README.md agenticlens/LICENSE /opt/workspace/agenticlens/
COPY agenticlens/src /opt/workspace/agenticlens/src
COPY agenticlens/schemas /opt/workspace/agenticlens/schemas
COPY agentic-chaos/pyproject.toml agentic-chaos/README.md agentic-chaos/LICENSE /opt/workspace/agentic-chaos/
COPY agentic-chaos/src /opt/workspace/agentic-chaos/src
COPY ai-operations-spec/specification/v0.4/schemas /opt/workspace/ai-operations-spec/specification/v0.4/schemas
COPY ai-operations-spec/specification/v0.4/conformance-rules.json /opt/workspace/ai-operations-spec/specification/v0.4/
COPY ai-operations-spec/specification/v0.5/compatibility.json /opt/workspace/ai-operations-spec/specification/v0.5/
RUN pip install --no-cache-dir ".[http]" /opt/workspace/agenticlens /opt/workspace/agentic-chaos
RUN useradd --create-home --uid 10001 mcp
USER mcp
ENV DEEP_AGENTIC_CORE_MCP_HTTP_HOST=0.0.0.0 \
    DEEP_AGENTIC_CORE_MCP_HTTP_PORT=8000 \
    DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT=/opt/workspace
EXPOSE 8000
CMD ["deep-agentic-core-mcp-http"]
