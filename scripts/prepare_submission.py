"""Build a separate public plugin candidate and report missing review materials.

This performs local structural checks; it neither submits nor publishes a plugin.
Use a new output directory. Credentials and submission worksheets stay outside ZIPs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import struct
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins/deepagentlabs"


def https(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parts = urlsplit(value)
    return parts.scheme == "https" and bool(parts.hostname) and not parts.username


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(SOURCE.resolve()):
        parser.error("Output must be outside the plugin source directory")
    for item in SOURCE.rglob("*"):
        if item.is_symlink():
            raise ValueError("Submission source must not contain symlinks")
    manifest = json.loads((SOURCE / "plugin.json").read_text())
    compatibility = json.loads((SOURCE / ".claude-plugin/plugin.json").read_text())
    assert manifest["name"] == compatibility["name"] == "deepagentlabs"
    assert manifest["version"] == compatibility["version"]
    assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
    assert not (SOURCE / ".app.json").exists()
    for filename in ("plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
        path = SOURCE / filename
        if path.exists():
            data = json.loads(path.read_text())
            assert data.get("apps") is None
            assert data.get("extensions", {}).get("com.openai", {}).get("apps") is None
    settings = manifest["extensions"]["com.openai"]
    interface = settings["interface"]
    for key, maximum in (("displayName", 30), ("shortDescription", 30), ("developerName", 80)):
        assert 0 < len(interface[key]) <= maximum
    assert interface["category"] == "Developer Tools"
    for key in ("logo", "composerIcon"):
        path = (SOURCE / interface[key]).resolve()
        assert path.is_relative_to(SOURCE.resolve())
        data = path.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) <= 5 * 1024 * 1024
        width, height = struct.unpack(">II", data[16:24])
        assert (256 if key == "logo" else 48) <= width == height <= 4096
    cases = settings["review"]["test_cases"]
    assert len(cases["positive"]) == 5 and len(cases["negative"]) == 3
    for group, entries in cases.items():
        fields = ["description", "prompt"]
        if group == "positive":
            fields += ["tools_triggered", "expected_behavior"]
        for entry in entries:
            assert all(isinstance(entry[k], str) and entry[k].strip() for k in fields)
    assert len(list((SOURCE / "skills").glob("*/SKILL.md"))) == 4
    mcp = json.loads((SOURCE / "mcp.json").read_text())
    endpoint = mcp["mcpServers"]["deepagentlabs"]["url"]
    assert endpoint == "https://mcp.deepagentlabs.io/mcp"
    assert "clientSecret" not in json.dumps(mcp) and "Authorization" not in json.dumps(mcp)
    missing = [
        "interface." + field
        for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL")
        if not https(interface.get(field))
    ]
    if not https(settings["review"].get("demo_recording_url")):
        missing.append("review.demo_recording_url")
    output.mkdir(parents=True, exist_ok=False)
    candidate = output / "deepagentlabs"
    shutil.copytree(SOURCE, candidate)
    archive = output / ("deepagentlabs-" + manifest["version"] + "-candidate.zip")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for item in sorted(candidate.rglob("*")):
            if item.is_file():
                bundle.write(item, item.relative_to(output))
    with zipfile.ZipFile(archive) as bundle:
        names = set(bundle.namelist())
        assert "deepagentlabs/plugin.json" in names
        assert "deepagentlabs/assets/logo.png" in names
        assert len([name for name in names if name.endswith("/SKILL.md")]) == 4
        assert not any(".app.json" in name or "/submissions/" in name for name in names)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / "SHA256SUMS").write_text(digest + "  " + archive.name + "\n")
    report = {
        "status": "Candidate prepared; not uploaded, submitted or published",
        "version": manifest["version"],
        "archive": archive.name,
        "sha256": digest,
        "local_structure_checks": "passed",
        "missing_package_materials": missing,
        "manual_verifications_required": [
            "Fetch and inspect all four actual listing URLs and play back the demo URL",
            "Run review prompts in the intended host and inspect calls/results",
            "Verify dedicated reviewer access through secure portal fields",
            "Select the verified publisher and complete domain checks and scans",
            "Publisher must read and complete current legal/policy attestations",
            "Inspect the exact saved submission and authentication configuration",
        ],
        "ready_for_submission": False,
    }
    (output / "readiness.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if args.require_ready and missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
