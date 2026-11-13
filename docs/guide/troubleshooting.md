# Troubleshooting

Check the failing boundary before changing application behavior.

- Executable not found: point the client to the environment's executable.
- Producer still missing: restart the server after installation and check which environment it uses.
- Workspace sources override packages: inspect `DEEP_AGENTIC_CORE_MCP_WORKSPACE_ROOT`.
- Hosted access failure: follow the access-control guide for that deployment rather than changing the local stdio example.

## Verify your environment

Run commands from the environment where you installed the package. Confirm the input file exists and matches the expected artifact contract. Keep the original evidence when diagnosing a failure.
