"""Fetch canonical AIOS specification assets at a pinned revision, verifying content.

The destination is laid out like an ai-operations-spec checkout (the spec root),
because the server reads `specification/v0.5/compatibility.json` to find each
published schema set and `specification/v0.4/conformance-rules.json` for rule IDs.
"""

import argparse
import hashlib
import urllib.request
from pathlib import Path

# ai-operations-spec v0.6.1 (merge commit the tag points at).
COMMIT = "12897eebe91a5cddeb678d995f1b95e16a2d8030"
CHECKSUMS = {
    "specification/v0.4/schemas/common.schema.json": (
        "d0236f74f78ab1545c4b332b0f8789f88a2638621d94a10d2a8e14f449f99ab0"
    ),
    "specification/v0.4/schemas/workflow.schema.json": (
        "9c69c1282710cab1f0e2f8febd084204fadbcb7cd2089f125e5933508286030b"
    ),
    "specification/v0.4/schemas/run.schema.json": (
        "a282ec1aefd882a24f9cebc3602e1a48c885e0ce4b5dc4c1a19c9432305d2518"
    ),
    "specification/v0.4/conformance-rules.json": (
        "bfdd6f011d15f185548c7ddb3deca7cb214b199fd97034f2ff7da31d949c9faf"
    ),
    "specification/v0.5/compatibility.json": (
        "168d41a97aee1a03994aae4c45ee3f6e4d3d339b7cc626c5ecd0da61d96adfe1"
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="spec root to populate")
    args = parser.parse_args()
    for relative, expected in CHECKSUMS.items():
        url = f"https://raw.githubusercontent.com/DeepAgentLabs/ai-operations-spec/{COMMIT}/{relative}"
        with urllib.request.urlopen(url, timeout=30) as response:
            content = response.read()
        if hashlib.sha256(content).hexdigest() != expected:
            raise ValueError(f"Specification asset checksum mismatch: {relative}")
        target = args.destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    print(f"Verified {len(CHECKSUMS)} AIOS specification assets at {COMMIT}")


if __name__ == "__main__":
    main()
