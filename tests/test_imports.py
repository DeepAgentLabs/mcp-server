from deep_agentic_core_mcp.tools.chaos import capabilities as chaos_capabilities
from deep_agentic_core_mcp.tools.core import health, version
from deep_agentic_core_mcp.tools.lens import capabilities as lens_capabilities
from deep_agentic_core_mcp.tools.sidecar import capabilities as sidecar_capabilities
from deep_agentic_core_mcp.tools.spec import capabilities as spec_capabilities


def test_health_payload() -> None:
    payload = health()
    expected_adapters = {
        "agenticlens",
        "agentic_chaos",
        "agentic_sidecar",
        "ai_operations_spec",
    }
    assert set(payload["adapters"]) == expected_adapters
    if all(info["available"] for info in payload["adapters"].values()):
        assert payload["status"] == "ok"
    else:
        assert payload["status"] == "degraded"


def test_version_payload() -> None:
    payload = version()
    assert "version" in payload


def test_capability_placeholders() -> None:
    assert "chaos" in chaos_capabilities()
    assert "lens" in lens_capabilities()
    assert "sidecar" in sidecar_capabilities()
    assert "spec" in spec_capabilities()
