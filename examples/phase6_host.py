"""Explicit host wiring; supply provisioned stores and secrets outside source control."""

from typing import Any

from agentic_sidecar import Sidecar, TaskRuntime

from deep_agentic_core_mcp.services.containment import SidecarBridge, TaskBinding, TaskKeyRevoker
from deep_agentic_core_mcp.transport_http import create_app


def build_host(keys: Any, sessions: Any, operators: Any, owner: str, task_id: str) -> Any:
    runtime = TaskRuntime(task_id)
    sidecar = Sidecar(runtime=runtime, mode="govern", on_sidecar_failure="fail_closed")
    runtime.revokers["mcp"] = TaskKeyRevoker(owner, task_id, keys, sessions)
    app = create_app(
        key_store=keys,
        store=sessions,
        operator_store=operators,
        sidecar_bridge=SidecarBridge({task_id: TaskBinding(owner, runtime)}),
    )
    # The actual agent host must use this Sidecar's framework adapters for dispatch.
    return app, sidecar
