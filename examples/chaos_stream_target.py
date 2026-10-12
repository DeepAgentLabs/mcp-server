"""Offline stream target for agentic-chaos >=0.5.0 via local stdio MCP.

Call chaos.run_experiment with:
{"script": "mcp-server/examples/chaos_stream_target.py", "faults": ["stream_cut"]}
The existing runner owns the chaos session; the target wraps stream delivery.
"""

from agentic_chaos import chaos_stream

if __name__ == "__main__":
    chunks = list(chaos_stream(iter(["Hello", " world", "!"]), step_name="answer"))
    print("".join(chunks))
