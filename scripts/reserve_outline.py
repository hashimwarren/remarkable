#!/usr/bin/env python3
"""Reserve or locate the predictable working outline beside an article."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def outline_path(article: Path) -> Path:
    return article.with_name(f"{article.stem}.outline.md")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", help="Markdown article path")
    parser.add_argument("--root", default=".", help="Project root")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    article = Path(args.article).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    try:
        article.relative_to(root)
    except ValueError:
        parser.error("article must stay inside the project root")
    if not article.is_file():
        parser.error(f"not a file: {article}")
    if article.suffix.casefold() not in {".md", ".mdx"} or article.stem.endswith(".outline"):
        parser.error("article must be Markdown and cannot already be an outline")

    outline = outline_path(article)
    if outline.is_symlink():
        parser.error(f"outline path must not be a symbolic link: {outline}")
    if outline.exists():
        if not outline.is_file():
            parser.error(f"outline path is not a file: {outline}")
        status = "existing"
    else:
        try:
            descriptor = os.open(outline, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            status = "existing"
        except OSError as error:
            parser.error(str(error))
        else:
            os.close(descriptor)
            status = "reserved"

    print(
        json.dumps(
            {
                "status": status,
                "path": str(outline),
                "relative_path": outline.relative_to(root).as_posix(),
                "article_path": str(article),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
