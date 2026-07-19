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


def approved_personal_story(markdown: str) -> str:
    personal = section(markdown, "Personal Authority")
    if not personal:
        return ""
    match = re.search(
        r"^\*\*Approved story:\*\*\s*$\n(.*?)(?=^\*\*|\Z)",
        personal,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def quote_context(label: str, value: str) -> str:
    if not value:
        return ""
    lines = value.splitlines()
    quoted = [f"> **{label}:** {lines[0]}"]
    quoted.extend(f"> {line}" for line in lines[1:])
    return "\n".join(quoted) + "\n>\n"


def build_map(premise_markdown: str) -> str:
    premise = section(premise_markdown, "Premise") or "[Selected premise]"
    audience = section(premise_markdown, "Audience") or "[Intended reader]"
    desired = section(premise_markdown, "Desired Movement") or "[Desired reader movement]"
    why_now = section(premise_markdown, "Why Now") or "[Why this matters now]"
    objection = section(premise_markdown, "Likely Objection") or "[Confirmed likely objection]"
    personal_story = approved_personal_story(premise_markdown)
    personal_context = quote_context("Approved Personal Authority", personal_story)
    return f"""# [Working title]

[HEADER IMAGE PLACEHOLDER: Create a concept that expresses the central tension or promise of this premise without pretending to be evidence: {premise}]

*Visual job: Make the article's promise emotionally and conceptually legible before the opening.*

> **Governing premise:** {premise}
>
> **Reader:** {audience}
>
> **Desired movement:** {desired}
>
{personal_context}> **The article should make the reader want to understand:** [State the consequential question this article should make the reader want answered.]
>
> **The answer becomes clear:** [Name the specific answer and the body movement where it should become clear.]
>
> **How the article resolves it:** [Describe how the answer and any approved framework work together without naming an internal classification.]

## Opening

[Establish the reader's situation, the article's promise, what makes this argument different, and why it matters now. When the map contains a genuine article question, preserve its planned answer timing; otherwise state the premise directly: {why_now}]

{{>>Does this capture the situation and stakes accurately, or is an important fact missing?<<}}

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

## Practical framework

[Add the approved framework body here, or remove only this heading and marker when skipped.]

## Comprehension or story visual

[COMPREHENSION OR STORY VISUAL PLACEHOLDER: Show the framework's actual logic, a consequential process or comparison, or a personal scene that would become easier to understand or remember.]

*Visual job: Explain or humanize a consequential part of the argument; remove this position when it would be merely decorative.*

## Proof needs

[After the map is resolved, identify the consequential claims, what proof each requires, what already exists, and what must be researched, supplied, narrowed, or removed.]

[PROOF VISUAL PLACEHOLDER: Attach a chart, screenshot, source excerpt, demonstration, comparison, or other visible evidence to the strongest claim the reader should be able to see for themselves.]

*Visual job: Make one important claim more credible; remove this position when no visual proof is useful.*

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
