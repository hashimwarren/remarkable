#!/usr/bin/env python3
"""Create a collision-safe Roughdraft article map from PREMISE.md."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from reserve_draft import reserve


def section(markdown: str, name: str) -> str:
    match = re.search(
        rf"^## {re.escape(name)}\s*$\n(.*?)(?=^## |\Z)",
        markdown,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def build_map(premise_markdown: str) -> str:
    premise = section(premise_markdown, "Premise") or "[Selected premise]"
    audience = section(premise_markdown, "Audience") or "[Intended reader]"
    desired = section(premise_markdown, "Desired Movement") or "[Desired reader movement]"
    why_now = section(premise_markdown, "Why Now") or "[Why this matters now]"
    objection = section(premise_markdown, "Likely Objection") or "[Confirmed likely objection]"
    return f"""# [Working title]

> **Governing premise:** {premise}
>
> **Reader:** {audience}
>
> **Desired movement:** {desired}

## Opening

[Establish the reader's situation, the article's promise, what makes this argument different, and why it matters now: {why_now}]

{{>>What does the reader need to recognize immediately for this premise to feel important now?<<}}

## Argument

[Develop the premise through a small number of necessary claims. Support each claim and show what changes because it is true.]

> **Likely objection:** {objection}
>
> **Author's response direction:** [Add the confirmed response direction before review.]

{{>>What must the reader believe before they can accept the premise? What are the two or three essential steps that will get them there?<<}}

### Claim 1

[State the first necessary claim.]

#### Proof

[Show why the reader should believe this claim.]

#### Consequence

[Explain what changes if the claim is true.]

### Claim 2

[State the next necessary claim. Remove this section if the argument does not need it.]

#### Proof

[Show why the reader should believe this claim.]

#### Consequence

[Explain what changes if the claim is true.]

## Visible evidence

[Place screenshots, demonstrations, charts, quotations, or other assets where they let the reader see an important claim for themselves. Remove this section when no visual proof is useful.]

{{>>Which claim would become more credible if the reader could see it rather than merely being told it?<<}}

<!-- Suggested asset: screenshot, chart, demonstration, quotation, or comparison -->

## Ending

[Complete the movement of the premise through consequence, resolution, transfer, or action.]

{{>>How should the reader's belief, decision, or behavior be different when the article ends?<<}}

## Call to action

[Offer the natural next step only when the argument has earned one. Remove this section when no call to action belongs.]

{{>>What is the most useful next step for this reader, and does the underlying offer make that action valuable and credible?<<}}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", help="Descriptive article topic used for the filename")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--premise", default="PREMISE.md", help="Premise file relative to root")
    parser.add_argument("--directory", default="drafts", help="Draft directory within root")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    premise_path = (root / args.premise).resolve()
    try:
        premise_path.relative_to(root)
    except ValueError:
        parser.error("premise file must stay inside the project root")
    if not premise_path.is_file():
        parser.error(f"not a file: {premise_path}")

    try:
        draft = reserve(root, args.directory, args.topic)
        draft.write_text(build_map(premise_path.read_text(encoding="utf-8")), encoding="utf-8")
    except (OSError, RuntimeError, ValueError) as error:
        parser.error(str(error))

    print(
        json.dumps(
            {
                "status": "created",
                "path": str(draft),
                "relative_path": draft.relative_to(root).as_posix(),
                "premise_path": str(premise_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
