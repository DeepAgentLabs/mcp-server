# AI Reference capability index

Open the generated [AI Readable Documentation](https://deepagentlabs.io/ai-operations-spec/docs/llms-full.md) for the complete reference. The [API Reference (detailed)](api-reference.md) gives the field and rule tables for each artifact family. In that raw Markdown file, **Full reference** links to an included section; **Source** identifies the maintained document. Use the [Developer Guide (simple)](developer-guide.md#capability-index) for short workflows.

## Capability index

| Capability | Included scope | Detailed reference |
| --- | --- | --- |
| Runtime model | Distinguish all fifteen runtime concepts and their boundaries. | <a href="#detailed-reference-core-runtime-concepts">Full reference</a> · [Source](../specification/v0.1/core-concepts.md) |
| Execution graphs | Represent containment, ordering, causality, participation and evidence links. | <a href="#detailed-reference-relationships-and-execution-structure">Full reference</a> · [Source](../specification/v0.2/relationships.md) |
| Retries and recovery evidence | Preserve separate attempts and link observed recovery. | <a href="#detailed-reference-canonical-examples-and-negative-controls">Full reference</a> · [Source](../specification/v0.6/examples.md) |
| Semantic events | Record canonical lifecycle events and producer event names. | <a href="#detailed-reference-semantic-event-conventions">Full reference</a> · [Source](../specification/v0.3/semantic-conventions.md) |
| Measurements | Preserve units, currency and observed/estimated/derived meaning. | <a href="#detailed-reference-semantic-event-conventions">Full reference</a> · [Source](../specification/v0.3/semantic-conventions.md) |
| Run and Workflow artifacts | Exchange execution artifacts and reusable workflow definitions. | <a href="#detailed-reference-json-schema-artifacts">Full reference</a> · [Source](../specification/v0.4/README.md) |
| Offline structural validation | Route to the declared schema and register local dependencies. | <a href="#detailed-reference-json-schema-artifacts">Full reference</a> · [Source](../specification/v0.4/README.md) |
| Semantic conformance | Check identity, references, timestamps and graph invariants. | <a href="#detailed-reference-run-and-workflow-conformance">Full reference</a> · [Source](../specification/v0.4/conformance.md) |
| Version routing and compatibility | Separate repository releases, artifact markers and consumer support. | <a href="#detailed-reference-versioning-and-compatibility">Full reference</a> · [Source](../specification/v0.5/versioning.md) |
| Extensions and preservation | Publish reusable metadata contracts without changing core meaning. | <a href="#detailed-reference-extension-model">Full reference</a> · [Source](../specification/v0.6/extension-model.md) |
| Naming conventions | Apply field, vocabulary, event and rule-ID grammars. | <a href="#detailed-reference-naming-conventions">Full reference</a> · [Source](../specification/v0.6/naming-conventions.md) |
| Provenance and lineage | Link subjects, sources and findings in a separate companion. | <a href="#detailed-reference-provenance-records">Full reference</a> · [Source](../specification/v0.6/provenance.md) |
| Cross-artifact resolution | Resolve subject identity, held bytes, digests and typed object references. | <a href="#detailed-reference-portable-conformance-suite">Full reference</a> · [Source](../specification/v0.6/conformance-suite/README.md) |
| Portable validator suite | Compare schema, semantic, unsupported and resolution outcomes offline. | <a href="#detailed-reference-portable-conformance-suite">Full reference</a> · [Source](../specification/v0.6/conformance-suite/README.md) |
| Verification signals | Represent second opinions, grounding, safety and unavailable assessments. | <a href="#detailed-reference-verification-signals">Full reference</a> · [Source](../specification/v0.8/verification-signals.md) |
| Audit events | Record attributed actions, observation times, targets and native outcomes. | <a href="#detailed-reference-audit-events">Full reference</a> · [Source](../specification/v0.8/audit-events.md) |
| Investigation reports | Summarize incidents, citations, uncertainty, timelines and recovery. | <a href="#detailed-reference-investigation-reports">Full reference</a> · [Source](../specification/v0.8/investigation-reports.md) |
| Operational conformance and privacy | Apply companion semantic rules and separate process obligations. | <a href="#detailed-reference-operational-companion-conformance">Full reference</a> · [Source](../specification/v0.8/conformance.md) |
| OpenTelemetry mapping | Project observed events with explicit timing, identities and losses. | <a href="#detailed-reference-opentelemetry-companion-binding">Full reference</a> · [Source](../specification/v0.6/otel-binding.md) |
| Migration, rollout and rollback | Adopt cumulative layers and companion families without rewriting markers. | <a href="#detailed-reference-migration-and-rollout">Full reference</a> · [Source](../specification/v0.6/migration-guide.md) |
| Access-evidence profile | Embed individual dispatch, completion, denial and revocation observations. | <a href="#detailed-reference-non-normative-access-evidence-profile">Full reference</a> · [Source](../drafts/access-evidence-v1/README.md) |
| Sidecar correlation profile | Preserve native decision identity and explicit host correlation. | <a href="#detailed-reference-non-normative-sidecar-correlation">Full reference</a> · [Source](../drafts/sidecar-correlation-v1/README.md) |
| Sidecar candidate contracts | Inspect native intent, decision, audit, scope and transfer mappings. | <a href="#detailed-reference-non-normative-sidecar-candidate-contracts">Full reference</a> · [Source](../drafts/sidecar-contracts-v1/README.md) |
| Ecosystem adoption and ownership | Map Lens, Evals, Chaos, Sidecar, MCP and Tower evidence explicitly. | <a href="#detailed-reference-coordinated-engineering-readiness">Full reference</a> · [Source](coordinated-v1-readiness.md) |
| Review gates and maturity | Assess draft claims and independent implementation evidence. | <a href="#detailed-reference-specification-reading-order-and-maturity">Full reference</a> · [Source](../SPECIFICATION.md) |
| Documentation and contribution workflow | Build both sites, refresh the reference and keep coverage complete. | <a href="#detailed-reference-documentation-build-and-publication">Full reference</a> · [Source](documentation-site.md) |

## How to use the robust reference

1. Choose a capability above, then read its detailed requirements and examples. The full reference includes every maintained specification layer, interoperability-profile page, review page and release-labelled ecosystem note selected by `docs/ai-docs.json`.
2. Use **Data contract** sections for complete published JSON Schemas and the non-normative profile schema copies. Use **Reference data** sections for catalogs, mappings, suite expectations, positive/negative cases and review artifacts. A negative fixture intentionally violates its named rule; it is not a producer template.
3. Route artifacts by the exact marker/type pair in the compatibility catalog. Run/Workflow use `0.4-draft`, provenance `0.6-draft`, operational companions `0.8-draft`; the repository release is independently versioned. Native Sidecar and access profiles remain non-normative.
4. Read source pages and rule catalogs together. Draft specification prose defines requirements within that draft; catalogs mirror it. Example code performs only its stated checks. Repository reference helpers are tests, not a public runtime API.
5. Check `ai-docs-manifest.json` before ingestion: each selected source has a normalized text hash and the reference has its own checksum. Download original fixture bytes from the source links for provenance digest verification; code blocks and normalized hashes do not preserve byte-level evidence.
6. Retain uncertainty and native outcomes. Fixture validity does not authenticate sources, prove coverage, establish safety, authorize actions or close independent-review gates. Historical notes apply to their named releases; superseded `drafts/v0.4` material is included for migration/history only.

## Maintaining coverage

Both capability indexes must list new user-facing capabilities. `docs/ai-docs.json` explicitly selects maintained Markdown and uses JSON globs for schemas, catalogs, mappings, examples and portable fixtures. Add new prose sources to that config. Generated outputs must never include themselves. From this repository root, with Python 3.11 or newer and the shared website checkout alongside it:

```bash
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project ai-operations-spec
python3 ../deepagentlabs.github.io/scripts/build_ai_docs.py --sources .. --project ai-operations-spec --check
```

The shared website publishes the robust reference verbatim as raw Markdown; it is excluded from rendered page search. The repository's standalone documentation also preserves a raw download. Neither publication changes schema maturity or the acceptance evidence.
