from deep_agentic_core_mcp.prompts.registry import list_prompts
from deep_agentic_core_mcp.resources.catalog import list_resources
from deep_agentic_core_mcp.services.registry import (
    prompt_descriptors,
    resource_descriptors,
    tool_descriptors,
)
from deep_agentic_core_mcp.tools.registry import list_tools


def test_tool_registry_has_core_health() -> None:
    names = {tool["name"] for tool in list_tools()}
    assert "core.health" in names
    assert "lens.analyze_workflow" in names
    assert "chaos.list_faults" in names
    assert "spec.validate_artifact" in names


def test_tool_registry_has_phase_2_and_3_additions() -> None:
    names = {tool["name"] for tool in list_tools()}
    assert {
        "core.verify",
        "core.session_state",
        "lens.report_summary",
        "lens.compare_runs",
        "lens.slo_summary",
        "lens.audit_report",
        "chaos.run_experiment",
    } <= names


def test_tool_registry_entries_carry_metadata() -> None:
    for tool in list_tools():
        assert tool["category"] in {"core", "lens", "chaos", "spec"}
        assert isinstance(tool["prerequisites"], list)
        assert tool["expected_duration"] in {"instant", "fast", "slow"}
        assert isinstance(tool["mutates_session"], bool)


def test_run_experiment_is_flagged_slow_and_mutating() -> None:
    entries = {tool["name"]: tool for tool in list_tools()}
    run_experiment = entries["chaos.run_experiment"]
    assert run_experiment["expected_duration"] == "slow"
    assert run_experiment["mutates_session"] is True
    assert "agentic_chaos" in run_experiment["prerequisites"]


def test_resource_registry_not_empty() -> None:
    assert list_resources()
    uris = {resource["uri"] for resource in list_resources()}
    assert "resource://schemas/aiops/v0.4/workflow" in uris


def test_prompt_registry_not_empty() -> None:
    assert list_prompts()


def test_prompt_registry_entries_have_arguments() -> None:
    prompts = {prompt["name"]: prompt for prompt in list_prompts()}
    assert "chaos.experiment_brief" in prompts
    faults_argument = next(
        arg for arg in prompts["chaos.experiment_brief"]["arguments"] if arg["name"] == "faults"
    )
    assert faults_argument["required"] is True


def test_typed_descriptors_build() -> None:
    assert tool_descriptors()
    assert resource_descriptors()
    assert prompt_descriptors()
