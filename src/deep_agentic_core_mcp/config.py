"""Shared project constants and metadata."""

import os

from deep_agentic_core_mcp import __version__

SERVER_NAME = "io.github.DeepAgentLabs/deep-agentic-core-mcp"
PACKAGE_NAME = "deep-agentic-core-mcp"
VERSION = __version__

# Remote/HTTP entrypoints must call enable_remote_transport() before serving.
# The default stdio entrypoint never does, so trusted local installs keep
# full tool access; network-reachable deployments get the safer default.
REMOTE_TRANSPORT_ENV = "DEEP_AGENTIC_CORE_MCP_REMOTE"
ALLOW_REMOTE_CHAOS_ENV = "DEEP_AGENTIC_CORE_MCP_ALLOW_REMOTE_CHAOS"


def _env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes"}


def is_remote_transport() -> bool:
    """Whether this process is serving MCP over a network-reachable transport."""
    return _env_flag(REMOTE_TRANSPORT_ENV)


def enable_remote_transport() -> None:
    """Mark this process as serving over a network-reachable transport.

    Called by remote/HTTP entrypoints before they start accepting requests.
    """
    os.environ[REMOTE_TRANSPORT_ENV] = "1"


def remote_chaos_allowed() -> bool:
    """Legacy opt-in for custom integrations; authenticated HTTP always rejects chaos.

    Only set this once the deployment actually sandboxes the executed script
    (container, restricted user, hard resource limits) - see SECURITY.md.
    """
    return _env_flag(ALLOW_REMOTE_CHAOS_ENV)
