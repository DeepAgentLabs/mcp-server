"""`core.access_status`: what the calling key may do, as enforced at dispatch."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

from deep_agentic_core_mcp.services.access_evidence import SCHEMA
from deep_agentic_core_mcp.services.access_policy import Principal

_PRINCIPAL: ContextVar[Principal | None] = ContextVar("access_principal", default=None)


@contextmanager
def principal_scope(principal: Principal) -> Iterator[None]:
    """Expose the dispatch-time principal to tool handlers on this thread."""
    token = _PRINCIPAL.set(principal)
    try:
        yield
    finally:
        _PRINCIPAL.reset(token)


def access_status(_: dict[str, Any] | None = None) -> dict[str, Any]:
    """Report the caller's effective policy and the tools it can call now."""
    principal = _PRINCIPAL.get()
    if principal is None:
        return {
            "transport": "stdio",
            "enforced": False,
            "note": "Local stdio is trusted; per-key access policies apply to hosted HTTP.",
        }
    # Imported lazily: the server module imports this one to register the handler.
    from deep_agentic_core_mcp.server import _remote_tool_names

    policy = principal.policy
    expires_at = (
        None
        if policy.expires_at is None
        else datetime.fromtimestamp(policy.expires_at, timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )
    return {
        "transport": "http",
        "enforced": True,
        "subject": principal.user,
        "policy_configured": policy.configured,
        "policy_error": policy.error,
        "allow": list(policy.allow),
        "deny": list(policy.deny),
        "task_id": policy.task_id,
        "expires_at": expires_at,
        "expired": policy.expired(),
        "permitted_tools": [name for name in _remote_tool_names() if policy.permits(name)],
        "evidence_schema": SCHEMA,
    }
