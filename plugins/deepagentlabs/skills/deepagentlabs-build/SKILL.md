---
name: deepagentlabs-build
description: >-
  Build or integrate applications with DeepAgentLabs products using their
  AI-readable documentation: AgenticLens, Agentic Evals, Agentic Chaos,
  Agentic Sidecar, AgenticOps Control Tower, AI Operations Specification,
  and the shared MCP server. Use for product API examples, package selection,
  instrumentation, evaluation, supervision and ecosystem integration code.
---

# Build with DeepAgentLabs

Read [the shared product-reference guide](../../references/ecosystem.md) to
select product IDs, retrieve documentation and establish the execution boundary.

## Find the supported path

Map the user's requested behavior to the products that own it. Select only
needed products; a request to use one library does not require the whole stack.
Use `core.docs_catalog` and `core.docs_search` to locate relevant public APIs,
configuration and examples. Read the complete sections with `core.docs_read`
before choosing signatures, extras, environment variables or artifact shapes.
Use returned section IDs and follow `next_offset` until the selection is complete.

Compare documentation snapshot versions with the user's installed versions or
project dependency constraints. `core.compatibility` reports the server's
installed distributions, not the user's laptop. A declared internal helper in
an AI-readable reference is not automatically a supported public API.

## Implement the requested integration

Adapt documented examples to the actual repository, framework and runtime.
Preserve existing dependency management and product boundaries:

- Lens owns workflow/run analysis and instrumentation.
- Evals owns evaluation execution and release-gate judgments.
- Chaos owns controlled fault experiments and their reports.
- Sidecar owns supervision and live task enforcement.
- Tower owns fleet incidents and approved recovery workflows.
- AIOS owns shared operational artifacts and their schema maturity.
- MCP exposes these capabilities and their documentation to clients.

If the user asks for implementation, make the authorized code/configuration
changes and run the relevant validation. If they ask for an explanation or
example, provide that without changing their project. State the version and
source used, required setup and any unsupported boundary that affects the task.

A hosted MCP credential does not install packages on the user's computer or
connect a live local task. Wire local instrumentation, credentials and an actual
runtime connection when the requested integration needs them. Sidecar discovery
alone is not enforcement; a serialized decision or AIOS artifact grants no authority.

## Deliver

Provide working changes or the requested example, installation/configuration
steps that the evidence supports, and the observed validation result. Cite the
product reference for non-obvious API choices. Do not describe a successful
synthetic example, package installation or schema validation as production acceptance.
