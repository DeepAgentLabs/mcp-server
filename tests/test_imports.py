from deep_agentic_core_mcp.tools.chaos import capabilities as chaos_capabilities
from deep_agentic_core_mcp.tools.core import health, version
from deep_agentic_core_mcp.tools.lens import capabilities as lens_capabilities
from deep_agentic_core_mcp.tools.spec import capabilities as spec_capabilities


def test_health_payload() -> None:
    payload = health()
    assert payload["status"] == "ok"
    assert set(payload["adapters"]) == {"agenticlens", "agentic_chaos", "ai_operations_spec"}
    assert all(info["available"] for info in payload["adapters"].values())


def test_version_payload() -> None:
    payload = version()
    assert "version" in payload


def test_capability_placeholders() -> None:
    assert "chaos" in chaos_capabilities()
    assert "lens" in lens_capabilities()
    assert "spec" in spec_capabilities()
