"""Explicit host bindings to live Sidecar runtimes; no model-owned controls.

A binding is local to the process hosting the actual runtime. Replicated MCP
frontends must route control to that host; no distributed stop is inferred.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol

from deep_agentic_core_mcp.services.remote_sessions import dispatch_transaction


class Runtime(Protocol):
    task_id: str
    revokers: dict[str, Any]

    def control(self, action: str, actor: str) -> dict[str, Any]: ...


@dataclass(frozen=True)
class TaskBinding:
    owner: str
    runtime: Runtime


class SidecarBridge:
    """Only an independently authenticated operator can stop its exact bound task.

    Hosts install the task-specific MCP credential revoker in runtime.revokers.
    No configured revoker, partial failure or audit failure is an access success.
    Sidecar owns the stop latch, reservation lock and in-flight accounting.
    """

    def __init__(self, bindings: dict[str, TaskBinding]) -> None:
        self._bindings = dict(bindings)
        for task_id, binding in self._bindings.items():
            if task_id != binding.runtime.task_id or not binding.owner:
                raise ValueError("Sidecar task binding mismatch")

    def stop(self, owner: str, task_id: str) -> dict[str, Any]:
        binding = self._bindings.get(task_id)
        if binding is None or binding.owner != owner:
            return {"ok": False, "status": "unsupported"}
        receipt = binding.runtime.control("stop", "mcp-operator:" + owner)
        acknowledged = (
            receipt.get("access_revocation") == "acknowledged"
            and receipt.get("revocations", {}).get("mcp") is True
            and not receipt.get("audit_error")
        )
        return {
            "ok": acknowledged,
            "status": "acknowledged" if acknowledged else "failed",
            "task_id": task_id,
            "acknowledged_at": datetime.now(timezone.utc).isoformat() if acknowledged else None,
            "receipt": receipt,
        }


class TaskKeyRevoker:
    """Bound task revocation, serialized with this host's MCP dispatch transactions.

    Waits for in-flight MCP work to leave the user's transaction before acknowledging.
    Use the same shared SessionStore as the HTTP app. Credentials are dedicated to
    one task; external key/policy administration must use the same transaction.
    """

    def __init__(self, owner: str, task_id: str, keys: Any, sessions: Any) -> None:
        self.owner = owner
        self.task_id = task_id
        self.keys = keys
        self.sessions = sessions

    def __call__(self, task_id: str) -> bool:
        from deep_agentic_core_mcp.services.access_policy import AccessPolicy

        if task_id != self.task_id:
            return False
        with dispatch_transaction(self.sessions, self.owner):
            policy = AccessPolicy.load(self.keys.stored_access_policy(self.owner))
            if policy.error is not None or policy.task_id != self.task_id:
                return False
            self.keys.revoke_user(self.owner)
            return True
