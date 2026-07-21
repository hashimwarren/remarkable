#!/usr/bin/env python3
"""Verify that a Remarkable installation contains one coherent release bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Remarkable skill directory (defaults to the script's parent directory).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    manifest_path = root / "release-manifest.json"

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "invalid", "error": str(error)}))
        return 1

    expected = manifest.get("files")
    release = manifest.get("release")
    if not isinstance(release, str) or not isinstance(expected, dict) or not expected:
        print(json.dumps({"status": "invalid", "error": "manifest requires release and files"}))
        return 1

    failures: list[dict[str, str]] = []
    for relative, expected_hash in sorted(expected.items()):
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            failures.append({"path": relative, "error": "path escapes skill directory"})
            continue
        if not candidate.is_file():
            failures.append({"path": relative, "error": "missing"})
            continue
        data = candidate.read_bytes()
        actual_hash = hashlib.sha1(
            f"blob {len(data)}\0".encode("ascii") + data
        ).hexdigest()
        if actual_hash != expected_hash:
            failures.append(
                {
                    "path": relative,
                    "error": "hash mismatch",
                    "expected": expected_hash,
                    "actual": actual_hash,
                }
            )

    payload = {
        "status": "verified" if not failures else "mismatch",
        "release": release,
        "checked_files": len(expected),
        "failures": failures,
    }
    print(json.dumps(payload, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
