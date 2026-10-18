# Tower 0.7.0 integration compatibility

## Control Tower 0.7.0 fleet operations

Tower 0.7.0 adds frozen environment/capability targeting, bulk desired settings,
separate approval, durable per-target results and bounded stop/MCP-revocation
acknowledgement through Python, HTTP and CLI. No fleet atomicity or automatic
rollback/resume is claimed. Timed-out/requested commands need host reconciliation.

Local MCP 0.3.6 investigation tools remain compatible. Tower 0.7 bulk endpoints are Python/HTTP/CLI-only: MCP exposes no new fleet write or approval tools, and hosted Tower restrictions remain in force.

Existing optional dependency ranges remain sufficient. No sibling runtime or
native evidence schema changes are required; this documentation alignment needs
no patch release. See the [operator guide](https://github.com/DeepAgentLabs/agenticops-control-tower/blob/v0.7.0/docs/fleet-operations.md).

Example operator workflow (against a configured Tower server):

```bash
agenticops-control-tower --token "$WRITER_TOKEN" bulk preview fleet.json
agenticops-control-tower --token "$APPROVER_TOKEN" bulk approve BULK_ID
agenticops-control-tower --token "$WRITER_TOKEN" bulk execute BULK_ID
agenticops-control-tower --token "$READER_TOKEN" bulk get BULK_ID
```

Use the exact request and ownership setup in the operator guide. A successful
desired-setting write does not assert runtime application or incident recovery.
