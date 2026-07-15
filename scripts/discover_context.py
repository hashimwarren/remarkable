#!/usr/bin/env python3
"""Return a bounded, ranked manifest of likely writing-context files."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


PRIORITY_NAMES = [
    "PREMISE.md",
    "REMARKABLE.md",
    ".remarkable.md",
    "PRODUCT.md",
    "DESIGN.md",
    "AUDIENCE.md",
    "EVIDENCE.md",
    "POSITIONING.md",
    "VOICE.md",
    "STYLE.md",
    "COPY.md",
    "BRAND.md",
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
]
PRIORITY = {name.casefold(): index for index, name in enumerate(PRIORITY_NAMES)}
RELEVANT_TERMS = (
    "audience",
    "brand",
    "content",
    "copy",
    "customer",
    "design",
    "editorial",
    "marketing",
    "message",
    "messaging",
    "persona",
    "position",
    "product",
    "remarkable",
    "style",
    "voice",
)
ALLOWED_SUFFIXES = {".md", ".mdx", ".txt"}
EXCLUDED_DIRS = {
    ".cache",
    ".git",
    ".next",
    ".slopless",
    ".turbo",
    "build",
    "coverage",
    "dist",
    "drafts",
    "generated",
    "node_modules",
    "out",
    "output",
    "outputs",
    "target",
    "tmp",
    "vendor",
}
SECRET_NAMES = {
    "credentials.json",
    "secrets.json",
    "service-account.json",
    "id_rsa",
    "id_ed25519",
}
SECRET_SUFFIXES = {".key", ".p12", ".pem"}


def is_secret_like(path: Path) -> bool:
    name = path.name.casefold()
    return (
        name.startswith(".env")
        or name in SECRET_NAMES
        or path.suffix.casefold() in SECRET_SUFFIXES
        or "credential" in name
        or "secret" in name
    )


def classify(path: Path) -> tuple[int, str] | None:
    folded = path.name.casefold()
    if folded in PRIORITY:
        label = PRIORITY_NAMES[PRIORITY[folded]]
        return PRIORITY[folded], f"priority context file: {label}"
    if path.suffix.casefold() not in ALLOWED_SUFFIXES:
        return None
    stem = path.stem.casefold()
    matching = [term for term in RELEVANT_TERMS if term in stem]
    if not matching:
        return None
    return len(PRIORITY_NAMES) + 1, f"relevant filename term: {matching[0]}"


def scan(root: Path, max_depth: int, max_bytes: int, limit: int) -> dict[str, object]:
    candidates: list[dict[str, object]] = []
    skipped_large = 0
    skipped_secret_like = 0

    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        relative_dir = current_path.relative_to(root)
        depth = len(relative_dir.parts)
        dirs[:] = sorted(
            directory
            for directory in dirs
            if directory not in EXCLUDED_DIRS
            and not directory.startswith(".")
            and depth < max_depth
        )

        for filename in sorted(files):
            path = current_path / filename
            if path.is_symlink() or is_secret_like(path):
                skipped_secret_like += 1
                continue
            result = classify(path)
            if result is None:
                continue
            try:
                size = path.stat().st_size
            except OSError:
                continue
            if size > max_bytes:
                skipped_large += 1
                continue
            priority, reason = result
            relative = path.relative_to(root)
            candidates.append(
                {
                    "path": relative.as_posix(),
                    "priority": priority,
                    "reason": reason,
                    "size_bytes": size,
                    "depth": len(relative.parts) - 1,
                }
            )

    candidates.sort(key=lambda item: (item["priority"], item["depth"], item["path"]))
    selected = candidates[:limit]
    return {
        "root": str(root),
        "files": selected,
        "truncated": len(candidates) > limit,
        "candidate_count": len(candidates),
        "skipped_large": skipped_large,
        "skipped_secret_like": skipped_secret_like,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Project root to inspect")
    parser.add_argument("--max-depth", type=int, default=4, choices=range(1, 9))
    parser.add_argument("--max-bytes", type=int, default=65_536)
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    if args.max_bytes < 1 or not 1 <= args.limit <= 30:
        parser.error("--max-bytes must be positive and --limit must be between 1 and 30")

    print(json.dumps(scan(root, args.max_depth, args.max_bytes, args.limit), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
