# Coordinated v1.0 engineering readiness

MCP 0.8.0 implements all AIOS 0.4/0.6/0.8 draft schema families, with
schema and semantic checks and source-pinned packaged resources. spec.validate_artifact
keeps its existing tool input/output envelope and routes by the declared marker.
No sibling checkout or network is needed for the specification adapter. An explicit
workspace catalog remains authoritative when present. Same-named common schemas
are registered by full $id; companion dependencies resolve offline.

The Python adapter adds resolve_provenance(record, held_subject_bytes). It never
fetches a URI and keeps reference identity, digest and content validity separate.
Process and cross-artifact rules are not marked passed by single-artifact checks.
The full pinned portable suite includes 66 outcomes and 5 resolution cases.

`deep_agentic_core_mcp.services.access_evidence.export_audit_event` projects a
native access observation with a public target and optional public actor id.
Actual dispatch maps to started, denial/revocation acknowledgement to denied,
completion ok/error to succeeded/failed, and missing completion outcome to
unknown. Native event and correlation ids are retained. Private reasons,
subjects/tool names and credentials are withheld. Run the offline
`examples/operational_artifacts.py` example. This adds no automatic remote
export, authorization or cancellation capability.

Candidate baseline: Lens 0.14.0, Chaos 0.11.0, Evals 0.12.0, Sidecar 0.11.0,
Tower 0.11.0, AIOS snapshot 0.8.0. New versions are acceptance pins, not increased
optional minimum requirements. The JSON Schema format extra is required for
consistent RFC3339/URI validation. Publishing a package does not deploy AWS.

Migration/rollback: current tool callers are compatible; spec validation now
accepts explicitly supported companions and bundles their resource families.
Pin 0.7.0 to roll back, disable companion projections and retain native sources.
Consumers limited to 0.4-draft reject new markers rather than relabeling them.

Independent acceptance, live/deployment evidence and the stable freeze remain
separate gates. See the [shared release policy](https://github.com/DeepAgentLabs/.github/blob/main/profile/RELEASE_POLICY.md).
