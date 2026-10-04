"""Fetch canonical AIOS schema assets at a pinned revision, verifying content."""

import argparse
import hashlib
import urllib.request
from pathlib import Path

COMMIT = "31a5ffa7d3baabe41a6d9d85945d722f77ebb9dd"
CHECKSUMS = {
    "common.schema.json": "d0236f74f78ab1545c4b332b0f8789f88a2638621d94a10d2a8e14f449f99ab0",
    "workflow.schema.json": "9c69c1282710cab1f0e2f8febd084204fadbcb7cd2089f125e5933508286030b",
    "run.schema.json": "a282ec1aefd882a24f9cebc3602e1a48c885e0ce4b5dc4c1a19c9432305d2518",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    args.destination.mkdir(parents=True, exist_ok=True)
    for name, expected in CHECKSUMS.items():
        url = (
            "https://raw.githubusercontent.com/DeepAgentLabs/ai-operations-spec/"
            f"{COMMIT}/specification/v0.4/schemas/{name}"
        )
        with urllib.request.urlopen(url, timeout=30) as response:
            content = response.read()
        if hashlib.sha256(content).hexdigest() != expected:
            raise ValueError(f"Schema checksum mismatch: {name}")
        (args.destination / name).write_bytes(content)
    print(f"Verified {len(CHECKSUMS)} AIOS schemas at {COMMIT}")


if __name__ == "__main__":
    main()
