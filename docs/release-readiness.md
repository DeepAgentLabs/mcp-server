# MCP 0.8 integration and release readiness

MCP 0.8.0 completes the local integration-readiness milestone over Phase 6.
Contracts remain candidates. Coordinated ecosystem v1.0 still requires each
project's acceptance gates, independent AIOS review and operator deployment acceptance.

## Candidate acceptance matrix

| Component | Acceptance baseline | Boundary |
| --- | --- | --- |
| MCP server | 0.8.0 | Python 3.10–3.13, stdio and authenticated HTTP |
| MCP Python SDK | 2.0.0 | Locked development/protocol acceptance; package range remains >=2,<3 |
| AgenticLens | 0.14.0 | Native analysis and authenticated snapshot verification |
| Agentic Chaos | 0.11.0 | Fault catalog, AIOS export and containment assertions; execution local only |
| Agentic Evals | 0.12.0 | Native report/gate schema 1.0 and containment scoring |
| Agentic Sidecar | 0.11.0 | Explicit host-bound task controls; independent operator authority |
| Control Tower | 0.11.0 | Authenticated HTTP candidate discovery; optional remote service |
| AIOS repository | 0.8.1 | Run/Workflow 0.4-draft, provenance 0.6-draft, operational companions 0.8-draft |

The installed package includes `resources/compatibility.json`. Call
`core.compatibility {}` to read this baseline and local distribution observations:
`baseline_match`, `different_version`, or `not_installed`. A different version
is untested by this exact baseline, not automatically incompatible. Optional
packages may be absent. Distribution metadata does not prove which source tree
was imported: explicit workspace adapters can select sibling checkouts. No
network calls, package installs or credential inspection occur in this tool.
Use `core.verify` for adapter probes and `tower.capability_contract` for remote
contract discovery. Hosted policy controls this diagnostic like every other tool.

The CI AIOS checkout is pinned to `78f1fb682125afc30a3c12003e9beb3c577f793f`.
Standalone images retain the checksum-verified v0.8.1 licensed schema/catalog assets at
`78f1fb682125afc30a3c12003e9beb3c577f793f`; all checked schema families are also bundled in the wheel for offline use.

## Reproduce acceptance

```bash
make install
uv pip install agenticlens==0.14.0 agentic-chaos==0.11.0 agentic-sidecar==0.11.0
make check
make docs-check
uv run python examples/compatibility_check.py
uv build --wheel
uv run --isolated --no-project --with ./dist/deep_agentic_core_mcp-0.8.0-py3-none-any.whl python -I scripts/smoke_protocol.py
```

`make check` uses local sibling checkouts when present. CI separately installs
candidate wheels and runs real MCP/Sidecar/Lens/Chaos containment with Evals
scoring. The standalone protocol smoke starts the built wheel in an empty
workspace with no optional siblings: initialize, tool discovery/calls, packaged
baseline, degraded verification, prompt discovery and resource reading must work.
CI also tests the advertised Chaos 0.5 minimum and the published Tower API.
PostgreSQL acceptance runs against a real PostgreSQL 16 service in CI; local
runs require `DEEP_AGENTIC_CORE_MCP_TEST_DATABASE_URL`. No silent adapter skips
are allowed in the paired containment job.

## Upgrade and rollback

1. Record the current package version, `core.compatibility`, effective access
   policies and configured runtime bindings. Keep credentials out of reports.
2. For stdio, pin `deep-agentic-core-mcp==0.8.0` in a fresh environment, retain
   the selected sibling pins, and restart the client/server. Validate with
   `core.version`, `core.verify` and your saved workflow fixtures.
3. For hosted operation, build and record an immutable image digest. Deploy
   through the manual operator process in the AWS guide. Verify `/healthz`,
   unauthenticated rejection, an authorized `core.version` and `core.verify`,
   and policy denial using a dedicated restricted key. A package tag never
   deploys AWS. Do not infer the running version from PyPI or image recipes.
4. If acceptance fails, stop admitting new work, reconcile in-flight effects
   and dispatch guards, then restore the previous environment or image digest.
   Recheck keys/policies from the authoritative store; never restore revoked
   credentials or blindly clear a Redis guard. Existing in-flight work may
   finish. Database backups and operator reconciliation remain deployment-owned.

This release adds a read-only tool and packaged metadata. It changes no session
storage schema, native producer schema, AIOS marker, key format or public
credential handling. Existing explicit allowlists must opt in to
`core.compatibility`; broad policies continue to apply normally.

## Support and remaining gates

Python 3.10–3.13 is the tested server range. Other versions are unverified by
this milestone. Optional integration versions above record the tested matrix,
not new mandatory dependencies. Older integrations degrade according to their
adapter capability checks; only Chaos 0.5 has an explicit minimum-version CI lane.

Independent security/deployment acceptance, distributed runtime discovery,
remote sandboxed chaos, verified-email recovery/OAuth/billing and stable API
freezing remain separate work. AIOS and producer-native schemas retain their
own maturity and versioning. This release makes no production certification,
exhaustive evidence coverage or guaranteed cancellation claim.
