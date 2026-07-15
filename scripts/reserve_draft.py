#!/usr/bin/env python3
"""Atomically reserve a collision-safe Markdown file under drafts/."""

from __future__ import annotations

import argparse
import json
import os
import re
import unicodedata
from pathlib import Path


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.casefold()).strip("-")
    return slug[:72].rstrip("-") or "article"


def reserve(root: Path, directory: str, topic: str) -> Path:
    drafts = (root / directory).resolve()
    try:
        drafts.relative_to(root)
    except ValueError as error:
        raise ValueError("draft directory must stay inside the project root") from error
    drafts.mkdir(parents=True, exist_ok=True)

    base = slugify(topic)
    for number in range(1, 10_000):
        suffix = "" if number == 1 else f"-{number}"
        candidate = drafts / f"{base}{suffix}.md"
        try:
            descriptor = os.open(candidate, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            continue
        else:
            os.close(descriptor)
            return candidate
    raise RuntimeError("could not reserve a unique draft filename")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", help="Descriptive article topic used for the filename")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--directory", default="drafts", help="Draft directory within the root")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    try:
        path = reserve(root, args.directory, args.topic)
    except (OSError, RuntimeError, ValueError) as error:
        parser.error(str(error))
    print(
        json.dumps(
            {
                "status": "reserved",
                "path": str(path),
                "relative_path": path.relative_to(root).as_posix(),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
