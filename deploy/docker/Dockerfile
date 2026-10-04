# Build from the parent workspace:
# python3 mcp-server/scripts/build_container.py --tag deep-agentic-core-mcp:latest
FROM python:3.12-slim
WORKDIR /app
COPY mcp-server/pyproject.toml mcp-server/README.md ./
COPY mcp-server/src ./src
COPY agenticlens/pyproject.toml agenticlens/README.md agenticlens/LICENSE /opt/workspace/agenticlens/
COPY agenticlens/src /opt/workspace/agenticlens/src
COPY agenticlens/schemas /opt/workspace/agenticlens/schemas
COPY ai-operations-spec/specification/v0.4/schemas /opt/workspace/ai-operations-spec/specification/v0.4/schemas
RUN pip install --no-cache-dir ".[http]" /opt/workspace/agenticlens
RUN useradd --create-home --uid 10001 mcp
USER mcp
ENV DEEP_AGENTIC_CORE_MCP_HTTP_HOST=0.0.0.0 \
    DEEP_AGENTIC_CORE_MCP_HTTP_PORT=8000 \
    DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT=/opt/workspace
EXPOSE 8000
CMD ["deep-agentic-core-mcp-http"]
