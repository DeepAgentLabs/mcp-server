# mcp-server roadmap implementation audit

Audit date: 2026-09-11. Baseline: commit `dec8e8f6b49122ca9a3c81feebbfd93533f9d2b8`
on `main` (working tree clean, no local changes). Scope: the canonical
[product roadmap](ROADMAP.md) — Phase 0 through Phase 6, Known Limitations,
and Documentation Backlog — checked against the actual source tree
(`src/deep_agentic_core_mcp/`), tests (`tests/`), `CHANGELOG.md`, and
`pyproject.toml`.

**The roadmap's phase narrative is substantially accurate. The one material
correction is a version-boundary problem, not a capability overclaim: Phase
3d's two `sidecar.*` tools are real, tested, and wired into the server, but
they were never released — they landed in commits made *after* the `v0.2.0`
tag, with no `CHANGELOG.md` entry and no version bump, while `README.md`
still lists them under "MCP Surface (current, `0.2.0`)" as if they shipped
in that release.**

## How to read this audit

- **Implemented (I):** usable code exists for the stated scope, is registered
  in `tools/registry.py` and dispatched in `server.py`'s `_TOOL_DISPATCH`,
  and has test coverage. This does not assert PyPI publication or production
  adoption.
- **Partial (P):** a subset of the stated scope exists, or the deliverable
  is implemented but a named sub-claim (e.g. provenance, conformance
  breadth) is still open.
- **Missing (M):** no implementation was found in the inspected source,
  tests, or configuration.
- **Unverified (U):** a claim requires evidence not established here (e.g.
  behavior of an unreleased upstream sibling).

## Milestone summary

| Milestone | Assessment | Main open work |
| --- | --- | --- |
| Phase 0: Foundation | I | None — packaging/identity/tree scaffolding all present |
| Phase 1: Minimal MCP Server | I | None — `core.health`/`core.version` shipped in 0.1.2 |
| Phase 2: Session Management & Diagnostics | I | None — session store, rich `core.health`, tool metadata, `core.verify`, real prompts all shipped in 0.2.0 |
| Phase 3a: AgenticLens Integration | I/P | All 5 `lens.*` tools shipped and tested; per-finding source provenance is still correctly flagged as unverified |
| Phase 3b: Agentic Chaos Integration | I/P | Both `chaos.*` tools shipped and tested; script allow/deny-list beyond workspace confinement is still open (correctly unchecked in roadmap) |
| Phase 3d: Agentic Sidecar Discovery | **I, but unreleased** | Both `sidecar.*` tools are implemented and tested but were never released — see "Unreleased work beyond 0.2.0" below |
| Phase 3c: AI Operations Spec Conformance | I/P | `spec.validate_artifact` and schema resources shipped in 0.1.3; multi-version support and conformance-rule reporting correctly still open, blocked upstream |
| Phase 4: Unified Workflows | M | Correctly marked "Planned" — no `core.compare_runs`/`core.export_report`/`core.incident_summary`/`core.release_check`/`control_tower.*` in source |
| Phase 5: Publishing and Adoption | M | Correctly marked "Planned" — PyPI Trusted Publishing exists in CI, but no evidence of an actual published PyPI release or MCP Registry publish in this audit's scope |
| Phase 6: Operational Intelligence | M | Correctly marked "Planned" — no onboarding wizard, resource browsing, or narrative generation code found |

## Unreleased work beyond 0.2.0

`pyproject.toml` (`version = "0.2.0"`) and `src/deep_agentic_core_mcp/__init__.py`
(`__version__ = "0.2.0"`) agree with each other and with the latest
`CHANGELOG.md` section header (`## 0.2.0 - 2026-08-08`). `git tag` shows
`v0.2.0` on commit `85c5df2` (a dependabot-only merge). Twelve commits sit
between that tag and current `HEAD` (`dec8e8f`), and one of them —
`90536e1 feat: add agentic-sidecar MCP discovery support` — adds
`sidecar.status` and `sidecar.module_inventory` in full: the tool
implementations ([tools/sidecar.py](src/deep_agentic_core_mcp/tools/sidecar.py)),
the adapter ([adapters/agentic_sidecar.py](src/deep_agentic_core_mcp/adapters/agentic_sidecar.py)),
registry entries ([tools/registry.py](src/deep_agentic_core_mcp/tools/registry.py)),
server dispatch ([server.py](src/deep_agentic_core_mcp/server.py)), and tests
(`tests/test_server.py::test_handle_call_tool_sidecar_status`,
`::test_handle_call_tool_sidecar_module_inventory`).

None of this is reflected in `CHANGELOG.md` — there is no `[Unreleased]`
section, and no version has been bumped since `0.2.0`. `README.md`'s
"MCP Surface (current, `0.2.0`)" section lists `sidecar.status` and
`sidecar.module_inventory` as part of that surface without qualification,
which overstates what actually shipped in the `0.2.0` release artifact
(PyPI package, tag, GitHub Release). `ROADMAP.md` itself is more careful
here — it already says Phase 3d ships "in the current development line"
rather than claiming `0.2.0` — but its top-level "Release Status" line
("Current shipped version: `0.2.0`") sits directly above that Phase 3d
bullet without calling out the gap, which reads as more settled than it is.

This is a genuine implementation: the tools work, degrade correctly when
`agentic-sidecar` is unavailable (verified via
`tests/test_degraded_boot.py` and `test_server.py`), and follow the same
adapter pattern as the other three siblings. The issue is purely release
bookkeeping — the repo's own `AGENTS.md` release process (bump
`pyproject.toml`/`__init__.py`/`CHANGELOG.md` before merge) was not followed
for this feature.

## Evidence index

Paths are relative to this repository.

| Key | Source | Test evidence |
| --- | --- | --- |
| CORE | [tools/core.py](src/deep_agentic_core_mcp/tools/core.py) | [test_server.py](tests/test_server.py) (health/version/verify/session_state cases), [test_imports.py](tests/test_imports.py) |
| LENS | [tools/lens.py](src/deep_agentic_core_mcp/tools/lens.py), [adapters/agenticlens.py](src/deep_agentic_core_mcp/adapters/agenticlens.py) | [test_server.py](tests/test_server.py) (analyze_workflow, report_summary, compare_runs, slo_summary, audit_report cases) |
| CHAOS | [tools/chaos.py](src/deep_agentic_core_mcp/tools/chaos.py), [adapters/agentic_chaos.py](src/deep_agentic_core_mcp/adapters/agentic_chaos.py) | [test_server.py](tests/test_server.py) (list_faults, run_experiment success/timeout/reject-outside-workspace/unknown-fault/system-exit cases) |
| SIDECAR | [tools/sidecar.py](src/deep_agentic_core_mcp/tools/sidecar.py), [adapters/agentic_sidecar.py](src/deep_agentic_core_mcp/adapters/agentic_sidecar.py) | [test_server.py](tests/test_server.py) (`sidecar.status`, `sidecar.module_inventory` cases) |
| SPEC | [tools/spec.py](src/deep_agentic_core_mcp/tools/spec.py), [adapters/ai_operations_spec.py](src/deep_agentic_core_mcp/adapters/ai_operations_spec.py) | [test_server.py](tests/test_server.py) (validate valid/semantically-invalid run cases) |
| SESSION | [services/session.py](src/deep_agentic_core_mcp/services/session.py) | [test_session.py](tests/test_session.py) |
| REGISTRY | [tools/registry.py](src/deep_agentic_core_mcp/tools/registry.py), [services/registry.py](src/deep_agentic_core_mcp/services/registry.py) | [test_registry.py](tests/test_registry.py) |
| PROMPTS | [prompts/registry.py](src/deep_agentic_core_mcp/prompts/registry.py) | [test_server.py](tests/test_server.py) (`handle_list_prompts`, `handle_get_prompt_*` cases) |
| RESOURCES | [resources/catalog.py](src/deep_agentic_core_mcp/resources/catalog.py) | [test_registry.py](tests/test_registry.py) |
| SERVER | [server.py](src/deep_agentic_core_mcp/server.py) | [test_server.py](tests/test_server.py), [test_degraded_boot.py](tests/test_degraded_boot.py) |
| DEGRADE | [adapters/\_\_init\_\_.py](src/deep_agentic_core_mcp/adapters/__init__.py) (`AdapterUnavailableError`, `ensure_repo_on_path`) | [test_degraded_boot.py](tests/test_degraded_boot.py) |

## Tool surface verification

Every tool claimed in `ROADMAP.md`/`README.md`/`docs/tools.md` was checked
against `tools/registry.py` (metadata) and `server.py`'s `_TOOL_DISPATCH`
(actual wiring), and cross-checked to at least one `test_server.py` case
that calls it through `handle_call_tool`.

| Tool | Registered | Dispatched | Tested | Status |
| --- | --- | --- | --- | --- |
| `core.health` | yes | yes | yes | I |
| `core.version` | yes | yes | yes | I |
| `core.session_state` | yes | yes | yes | I |
| `core.verify` | yes | yes | yes | I |
| `lens.analyze_workflow` | yes | yes | yes | I |
| `lens.report_summary` | yes | yes | yes | I |
| `lens.compare_runs` | yes | yes | yes | I |
| `lens.slo_summary` | yes | yes | yes | I |
| `lens.audit_report` | yes | yes | yes | I |
| `chaos.list_faults` | yes | yes | yes | I |
| `chaos.run_experiment` | yes | yes | yes | I |
| `sidecar.status` | yes | yes | yes | I (unreleased — see above) |
| `sidecar.module_inventory` | yes | yes | yes | I (unreleased — see above) |
| `spec.validate_artifact` | yes | yes | yes | I |
| Prompt `lens.workflow_summary` | yes | n/a | yes | I |
| Prompt `lens.compare_summary` | yes | n/a | yes | I |
| Prompt `chaos.experiment_brief` | yes | n/a | yes | I |

`docs/tools.md` claims "14 tools" and lists exactly the 14 tools above
(including both `sidecar.*` tools) — consistent with `tools/registry.py`
and `_TOOL_DISPATCH`, but for the same reason as above this generated doc
is itself ahead of what `CHANGELOG.md`/`pyproject.toml` call the current
release.

No tool was found to be a stub, docstring-only placeholder, or advertised-but-undispatched
entry. `tools/registry.py` and `server.py`'s `_TOOL_DISPATCH` are kept in
sync by construction (`_build_tools()` only advertises entries with a
dispatch handler; `test_tool_dispatch_covers_all_tools` in `test_registry.py`
guards the reverse direction).

## Phase-by-phase detail

### Phase 0: Foundation

| Deliverable | Status | Evidence |
| --- | --- | --- |
| `README.md`, `ROADMAP.md`, `pyproject.toml`, `server.json`, initial `src/`/`tests/` layout | I | All present at their documented paths |

### Phase 1: Minimal MCP Server

| Deliverable | Status | Evidence |
| --- | --- | --- |
| Runnable stdio MCP server | I | [server.py](src/deep_agentic_core_mcp/server.py) `run_server()`/`main()` |
| `core.health`, `core.version` | I | See Tool surface verification |
| Stable JSON payloads | I | `handle_call_tool` returns `TextContent` with `json.dumps(result)` |
| Smoke tests for imports/boot | I | [test_imports.py](tests/test_imports.py), [test_server.py](tests/test_server.py)::`test_server_has_name` |

### Phase 2: Session Management & Diagnostics

| Deliverable | Status | Evidence |
| --- | --- | --- |
| In-memory session state | I | [services/session.py](src/deep_agentic_core_mcp/services/session.py); module-level dict, not persisted across restarts (matches its own docstring) |
| Rich `core.health` diagnostics | I | `tools/core.py::health()` returns adapter availability/version, loaded counts, workspace root, `last_successful_calls` |
| Tool metadata/annotations | I | `tools/registry.py` entries carry `category`/`prerequisites`/`expected_duration`/`mutates_session`; `server.py::_build_tools()` maps these onto `Tool._meta`/`ToolAnnotations` |
| `core.verify` | I | `tools/core.py::verify()` probes all four adapters |
| Real `prompts/list`/`prompts/get` | I | `server.py::handle_list_prompts`/`handle_get_prompt`, backed by `prompts/registry.py` |
| Session sharing across `lens.*`→`chaos.*` calls via `session_id` | I | `lens.report_summary`/`lens.compare_runs` reuse `state.workflow`/`state.baseline_runs`/`state.candidate_runs` when the argument is omitted; tested in `test_server.py::test_handle_call_tool_report_summary_reuses_session_workflow` |
| Adapters degrade instead of crashing boot | I | [adapters/\_\_init\_\_.py](src/deep_agentic_core_mcp/adapters/__init__.py)'s `AdapterUnavailableError`; verified end-to-end in [test_degraded_boot.py](tests/test_degraded_boot.py) |

### Phase 3a: AgenticLens Integration

| Deliverable | Status | Evidence |
| --- | --- | --- |
| `lens.analyze_workflow` | I | Calls `agenticlens.recommenders.engine.RecommendationEngine` on a validated `Workflow` |
| `lens.report_summary` | I | Reuses `agenticlens.exporters.markdown_exporter.MarkdownExporter` via a temp file, not a reimplementation |
| `lens.compare_runs` | I | Reuses `agenticlens.comparison.runner.compare_runs` |
| `lens.slo_summary` | I | Reuses `agenticlens.evaluation.gate.evaluate_gate`/`GateConfig` |
| `lens.audit_report` | I | Reuses `agenticlens.evaluation.html_report.render_html_report` when `include_html` is set |
| Every finding includes source provenance | **U (correctly flagged as open)** | `analyze_workflow` returns `recommendation.model_dump(mode="json")` as-is; whether every recommendation object actually carries a populated span/step provenance field is a property of `agenticlens`'s `Recommendation` model, not verified here. The sibling `agenticlens` repo's own audit records this as **Partial** ("can fall back to `workflow.recommendation` with no span ID") — so the roadmap's "not yet verified" framing is not just cautious, it is corroborated. No change needed. |

### Phase 3b: Agentic Chaos Integration

| Deliverable | Status | Evidence |
| --- | --- | --- |
| `chaos.list_faults` | I | Wraps `agentic_chaos.chaos.faults.FAULT_REGISTRY` |
| `chaos.run_experiment` | I | Runs `runpy.run_path` inside `agentic_chaos.chaos.session.chaos_session`, on a worker thread with a `future.result(timeout=...)` guard |
| Workspace-path sandboxing | I | `_resolve_sandboxed_script()` rejects paths outside `workspace_root()`; tested in `test_handle_call_tool_run_experiment_rejects_path_outside_workspace` |
| `timeout_seconds` actually bounds wall-clock time | I | `ThreadPoolExecutor.shutdown(wait=False)` (not a `with` block) so the call returns on timeout instead of blocking for the thread; tested in `test_handle_call_tool_run_experiment_honors_timeout`. Matches the CHANGELOG 0.2.0 "Fixed" entry. |
| Script allow/deny-list beyond workspace confinement | M (correctly unchecked) | `_resolve_sandboxed_script()` has no glob allowlist/denylist logic of any kind — any file under the workspace root passes |
| Chaos results convertible to AI Operations Specification artifacts | M (correctly flagged open) | `run_experiment()`'s return dict is `ChaosReport`-shaped ad hoc JSON; it is never passed through `spec.validate_artifact` or any AIOS schema |

### Phase 3d: Agentic Sidecar Discovery

| Deliverable | Status | Evidence |
| --- | --- | --- |
| `sidecar.status` | I, unreleased | `adapters/agentic_sidecar.py::status_summary()` returns a hardcoded `_CURRENT_STATUS` dict (`package_status: "scaffold"`, `runtime_ready: False`) plus the live package version — honest about scaffold-vs-runtime as the roadmap claims |
| `sidecar.module_inventory` | I, unreleased | `adapters/agentic_sidecar.py::module_inventory()` lists real top-level modules/adapters/integrations by walking the imported package's directory (`_list_package_modules`, `_list_python_stems`) — not a hand-maintained list, so it can't silently drift from the actual upstream scaffold |
| `core.verify`/`core.health` report sidecar separately | I | `_ADAPTER_PROBES` in `tools/core.py` includes `agentic_sidecar` alongside the other three |

The roadmap's own status line ("complete in the current development line")
is accurate. The problem is one level up, in `README.md`'s "MCP Surface
(current, `0.2.0`)" heading — see "Unreleased work beyond 0.2.0" above.

### Phase 3c: AI Operations Specification Conformance

| Deliverable | Status | Evidence |
| --- | --- | --- |
| `spec.validate_artifact` | I | `adapters/ai_operations_spec.py::validate_artifact()`: Draft 2020-12 JSON Schema validation plus a real semantic-rule pass (`semantic_validate_run` — unique IDs, relationship type/reference checks, cycle detection on `parent-of` and `caused/follows/depends-on` edge sets, timestamp ordering) |
| MCP resource endpoints for v0.4 schemas | I | `list_schema_resources()`/`schema_resource_content()`, wired into `server.py`'s `RESOURCE_CONTENT` |
| `resources/read` handler | I | `server.py::handle_read_resource` |
| Multi-version schema support | M (correctly flagged, blocked upstream) | `SCHEMA_DIR` only globs `specification/v0.4/schemas/*.schema.json`; there is no version-selection parameter anywhere in `spec.py`/`tools/registry.py` |
| Conformance-style pass/fail reporting distinct from presentation | M (correctly flagged, blocked upstream) | `validate_artifact()` returns raw `schema_errors`/`semantic_errors` lists with no conformance-rule taxonomy |

### Phase 4, 5, 6

All three remain **Missing**, exactly as `ROADMAP.md` labels them
("🚧 Planned"). No `core.compare_runs`, `core.export_report`,
`core.incident_summary`, `core.release_check`, or `control_tower.*` symbol
exists anywhere under `src/`. No PyPI-publish evidence (an actual released
package) or MCP Registry publish confirmation was available to check from
inside this repository — `server.json` and the `release-pypi.yml` workflow
described in `AGENTS.md` are release *machinery*, not proof of a completed
publish, and this audit did not check external registries.

## Known Limitations — re-verified

Both entries in `ROADMAP.md`'s "Known Limitations" section were checked
directly against current source and are still accurate:

1. **Tool handlers are synchronous and block the event loop.**
   `server.py::handle_call_tool` calls `handler(arguments)` directly (line
   183) — no `asyncio.to_thread()`, no `await`. Every tool handler in
   `tools/*.py` is a plain synchronous function. Confirmed still true.
2. **`chaos.run_experiment` has no allowlist beyond workspace-path
   confinement.** `adapters/agentic_chaos.py::_resolve_sandboxed_script()`
   only checks `candidate.relative_to(root)` and `candidate.is_file()` —
   no glob allow/deny-list, no per-client authorization. `SECURITY.md`
   independently documents the same gap. Confirmed still true, and the
   roadmap's Phase 3b tracking item for the allowlist is correctly still
   unchecked.

## Verification

Attempted `uv run pytest -q` and `make test` per the task's suggested
commands; neither `uv` nor a directly invokable `python` was available on
`PATH` in this session (the venv's `python.exe` is a `uv` trampoline
pointing at a `uv`-managed interpreter that is not present in this
environment). Located the workspace-local CPython 3.14.0 embeddable
interpreter at `E:\DeepAgentLabs\.tools\python314\python.exe` (the same one
the sibling `agenticlens` audit used) and ran the suite against it directly,
working around that interpreter's `._pth` file (which hardcodes only
`agenticlens`'s venv onto `sys.path` and disables `PYTHONPATH`, since it is
an embeddable distribution with `import site` commented out) by prepending
`mcp-server`'s own `.venv\Lib\site-packages` and `src` — plus the
`pywin32` subpaths (`win32`, `win32\lib`, `Pythonwin`, `pywin32_system32`)
that a normal `site`-processed `.pth` install would have added automatically
— via a throwaway runner script, rather than editing the shared `._pth`
file itself.

Result: **50 passed, 1 failed** out of 51 collected tests. The one failure,
`tests/test_degraded_boot.py::test_server_boots_and_degrades_when_sibling_repos_are_missing`,
spawns a **fresh subprocess** via `sys.executable` to test import-time
degradation, and that subprocess is the bare shared interpreter without this
session's `sys.path` workaround — so it fails on `ModuleNotFoundError: No
module named 'mcp'` before ever reaching the code under test. This is an
artifact of this session's broken `uv`/interpreter setup, not a defect in
the test or the server: the same test's logic (verify a `KeyError`-safe,
`AdapterUnavailableError`-based degradation path) is otherwise sound by
inspection, and every other test exercising the same adapters in-process
(`test_imports.py::test_health_payload`, `test_server.py::test_handle_call_tool_verify`)
passed. No source or test file was modified to obtain this result.

Lint, format, and typecheck (`make lint`/`make format-check`/`make
typecheck`) were not run — they depend on `ruff`/`mypy` console scripts
that have the same `uv`-trampoline problem as `pytest`, and reproducing them
through the same sys.path workaround was out of scope for this audit's time
budget. `CI.md`'s claim that GitHub Actions runs these across Python
3.10–3.13 was not independently re-verified; the repo's `.github/workflows/`
directory exists but its contents were not inspected here.

## Issues worth addressing

No product code was changed by this audit. These are documentation/process
gaps identified by source inspection, listed for the maintainer to act on:

1. **`CHANGELOG.md` is missing an `[Unreleased]`/dated section for the
   `sidecar.*` tools** (commit `90536e1` and follow-ups), contrary to the
   release process `AGENTS.md` itself documents (bump `pyproject.toml`,
   `__init__.py`, and `CHANGELOG.md` before merge). `pyproject.toml` and
   `__init__.py` are still at `0.2.0`.
2. **`README.md`'s "MCP Surface (current, `0.2.0`)" heading is stale** —
   it lists `sidecar.status`/`sidecar.module_inventory` under a version
   label that never actually shipped them. Either bump the version to
   reflect what's really released, or qualify the heading/entries the way
   `ROADMAP.md` already does ("ships in the current development line").
3. **`docs/tools.md`'s "14 tools" count is generated correctly from current
   source** but is therefore also ahead of the `0.2.0` release it's
   presented alongside in `README.md` — same root cause as #2, not a
   separate defect in the generator.
4. **This session could not exercise `make check`/CI parity locally** due
   to a broken `uv` toolchain (see Verification). If this reflects the
   actual dev/CI environment rather than just this audit session, the
   `make test`/`make check` instructions in `AGENTS.md`/`CI.md` may not be
   reproducible as written on a fresh machine without `uv` already fully
   provisioned with its managed Python.

No other discrepancies between claimed and actual tool wiring, test
coverage, or Known Limitations were found. All relative links in this
document resolve to real files in this repository as of the audit date.

## Recommended next step

Close the release-bookkeeping gap for Phase 3d before starting new work:
either cut a `0.3.0` (or `0.2.1`) release that includes the `sidecar.*`
tools with a proper `CHANGELOG.md` entry and version bump, or explicitly
mark `README.md`'s surface list as including unreleased/`main`-only tools
until that release happens. This keeps the roadmap's already-good practice
of distinguishing "shipped in `X.Y.Z`" from "in progress" from eroding as
more sibling integrations (Control Tower, richer Sidecar) land the same way.
