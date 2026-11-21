# Build with the seven-product AI reference

Connect your copilot to `deep-agentic-core-mcp`, then ask it to build with any
DeepAgentLabs product. The base server bundles each product's **AI Reference
(robust)**: complete documentation, declared APIs, CLI usage, configuration,
schemas and examples. No optional producer package, sibling checkout, network
fetch or API credential is needed to retrieve these public references locally.

## Copilot workflow

For example, ask your connected copilot:

> Build a support agent instrumented with AgenticLens, supervised by Sidecar,
> evaluated with Evals and tested under Chaos faults. Read the product references
> before choosing APIs, show required configuration, and include runnable tests.

The copilot can discover documentation through tools even when its host does
not support attaching MCP resources:

```text
core.docs_catalog {}
core.docs_search {"query":"evaluate_suite","product":"agentic-evals"}
core.docs_catalog {"product":"agentic-evals"}
core.docs_read {"product":"agentic-evals","section":"api-reference"}
```

The last call uses an example section ID. Use the actual `section` returned by
the search or product catalog. Read all required pages before copying a partial
signature or example: pass the returned `next_offset` back as `offset`, keeping
the same product and section. A null `next_offset` means the selection is complete.

`core.docs_read` returns at most 12,000 Unicode characters by default; `limit`
accepts 1–32,000. Omitting `section` pages through the complete reference.
`offset` counts characters within that selection, not bytes or line numbers.
Results include a source commit, snapshot version, checksum and line citation.

Search uses literal, case-insensitive AND terms with deterministic ranking by
phrase, heading and term matches. It returns at most ten section snippets by
default (`limit`: 1–20), each at most 1,000 characters, plus section IDs and
offsets for retrieving the surrounding source. It does not call an embedding
service or execute product code. An empty result is not proof a feature is absent;
try its documented API name or inspect the capability index.

The optional `core.build_with_ecosystem` prompt takes a required `task` and
optional `products` hint. It guides discovery, complete reads, version checking
and source citations. Retrieve it through `prompts/get`; it does not execute
the task or grant additional permissions.

## Products and resources

`resource://docs/catalog` lists all seven products, versions, source commits
and asset URIs. Canonical tool product IDs are:

| Product | Product ID |
| --- | --- |
| AgenticLens | `agenticlens` |
| Agentic Evals | `agentic-evals` |
| Agentic Chaos | `agentic-chaos` |
| Agentic Sidecar | `agentic-sidecar` |
| AgenticOps Control Tower | `agenticops-control-tower` |
| AI Operations Specification | `ai-operations-spec` |
| Deep Agentic Core MCP | `mcp-server` |

Each product exposes four resources:

| URI suffix | MIME type | Contents |
| --- | --- | --- |
| `resource://docs/{product}/reference` | `text/markdown` | Complete robust reference, preserved verbatim |
| `resource://docs/{product}/index` | `text/markdown` | Capability index and detailed source links |
| `resource://docs/{product}/manifest` | `application/json` | Upstream source selection and checksum manifest |
| `resource://docs/{product}/license` | `text/plain` | Product's license notice |

Full reference resources can be large. Prefer section reads/search for an
interactive copilot session. References are public static material; hosted
HTTP still requires bearer authentication, and documentation tools follow the
same per-key allow/deny and dispatch authorization as other tools. Public
documentation resources share the existing public-schema resource boundary;
they contain no tenant sessions, credentials or private reports.

## Versions and maintenance

The catalog reports **documentation snapshot versions**. These can differ from
installed optional producer versions and from a hosted service's deployed MCP
version. Compare them before using a documented interface. Base MCP installs
can explain a product without installing or configuring that product. Draft
schemas, optional adapters and deployment limitations retain their documented
status; source declarations do not make internal helpers public APIs.

Maintain snapshots from committed sibling sources:

```bash
python scripts/sync_ai_references.py --sources ..
python scripts/sync_ai_references.py --check
```

The sync command verifies the robust-reference checksum and every declared
source hash against each repository's selected HEAD Git objects, then copies
the reference, capability index, manifest and license. It records exact commits,
package versions and checksums. Uncommitted changes are not ingested. Update
product-owned sources and regenerate their references before syncing.

For the MCP server's own snapshot, commit its completed code, metadata and
generated reference first, then sync and commit the bundle. This deliberately
pins the self-reference to that preparation commit, avoiding a circular hash of
the package containing itself. Vendored documents are never recursively included
in the MCP reference; only code declarations and selected documentation are.

CI verifies the packaged checksums and exercises all seven references over an
installed-wheel stdio connection without sibling packages. Runtime retrieval
uses bundled assets only; it never follows source URLs or caller-supplied paths.
