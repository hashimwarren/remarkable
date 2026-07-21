# Critique a Complete Article

## Purpose

Diagnose a complete article rhetorically, localize only the highest-value interventions, and leave consequential revision authority with the writer.

## Required inputs

- The canonical article, `PREMISE.md` when available, and approved outline when available.
- The actual Slopless outcome and unresolved evidence boundaries.
- The writer's explicit choice to run critique, or a focused `critique` invocation.

## Process

After the first Slopless pass, offer **A. Run Remarkable critique** or **B. Open the draft as-is** and STOP. If critique is chosen, diagnose in the priority order below, share one overall diagnosis plus three prioritized revisions and their sequence, and add at most one document-level diagnosis and five localized CriticMarkup interventions. Read [roughdraft-handoff.md](roughdraft-handoff.md) for watched review.

Use this compact offer:

> Would you like me to run **Remarkable critique** before your final review? It will evaluate the premise, argument, evidence, reader momentum, comprehension, and sentence craft. I’ll summarize the priorities here and add up to five focused inline comments in Roughdraft. I won’t rewrite the article until you approve the direction.
>
> **A. Run Remarkable critique**
>
> **B. Open the draft as-is**

## User checkpoint

After review, obtain revision authority through **Review revisions one by one**, **Apply recommended revisions**, or **Leave the draft unchanged**. Require one-by-one approval for any premise, proof-burden, major-claim, reader-movement, or CTA change even under blanket approval.

## Artifact or state effects

Patch only the canonical article and only within granted authority. Do not create a second draft or duplicate Slopless's mechanical findings. CriticMarkup may remain in the canonical article until the writer resolves it.

## Degraded and failure behavior

Use the chat/Markdown fallback in [roughdraft-handoff.md](roughdraft-handoff.md) when Roughdraft cannot complete. Make no rhetorical edits on an ambiguous decision. If no consequential revision exists, say so and proceed instead of manufacturing work.

## Completion criterion

The writer's accepted revisions are applied, rejected and undecided passages remain unchanged, Slopless is rerun after substantive edits, and the article returns to the available review surface.

## Next-stage handoff

Follow [wayfinding.md](wayfinding.md) for the ready-state handoff and offer another purposeful critique without implying that it is required.

Diagnose in this priority order:

1. Premise
2. Question and resolution
3. Argument structure
4. Evidence gaps
5. Reader momentum
6. Comprehension
7. Sentence craft

Use five primary principles: reader momentum; concrete before clever; claim, proof, consequence; no orphan claims; lead with the change.

Use supporting principles only after structural issues: frictionless comprehension, one job per sentence, specific beats emphatic, answer the reader's next question, and prefer a sharp noun with a strong verb.

When the article uses question-and-resolution architecture, read [narrative-tension.md](narrative-tension.md) and test:

- whether the opening creates a meaningful question from the premise and supported situation rather than generic curiosity;
- whether a heading, summary, transition, or explanatory aside gives away the complete answer before the planned reveal;
- whether the reveal answers the exact question raised instead of switching to a neighboring claim;
- whether the answer is specific, proportionate to the proof, and consequential;
- whether the framework acts as answer, embodiment, or application rather than being appended automatically; and
- whether the sections after the reveal demonstrate, qualify, or apply the answer sufficiently for the resolution to feel earned.

When no genuine question belongs, do not manufacture one as a critique recommendation. Diagnose the direct argument on its own terms.

First return a high-level diagnosis, the three most consequential problems, and a prioritized revision sequence. Do not rewrite the whole article until the writer accepts the direction.

When the writer invokes critique or chooses the post-Slopless critique offer, share the diagnosis in chat and add at most one document-level diagnosis and five high-value inline CriticMarkup interventions by default. The chat prioritizes the editorial work; inline feedback localizes where the writer can act. Do not duplicate the same prose word for word. Comments should ask useful questions or explain stakes; suggestions should show a concrete fix. Do not wallpaper the document with feedback or duplicate Slopless's mechanical checks.

## Obtain revision authority

After the critique and Roughdraft review, use the runtime's structured user-input control when available:

- **Review revisions one by one**
- **Apply recommended revisions**
- **Leave the draft unchanged**

Use the same choices as a short plain-text fallback. Favor **Review revisions one by one** in the ordering and explanation because consequential editorial judgment belongs to the writer. Never interpret an ambiguous response as permission to change the premise, proof burden, major claims, reader movement, or CTA.

- **Review revisions one by one:** use the sequence below. Partial acceptance authorizes only the accepted local edits; leave rejected and undecided passages unchanged.
- **Apply recommended revisions:** apply the presented local recommendations, but review any premise, proof-burden, major-claim, reader-movement, or CTA change one by one because blanket approval does not authorize those changes.
- **Leave the draft unchanged:** make no rhetorical edits. Preserve the current file and proceed to the ready-state handoff.
- **Ambiguous reply:** make no rhetorical edits and ask the same decision again in plain language.

For one-by-one review, present only one consequential recommendation at a time:

1. the issue;
2. why it matters to the governing premise;
3. the proposed direction; and
4. the decision requested.

Allow the writer to accept, modify, discuss, or reject it. Apply only accepted changes and patch the existing article rather than creating a second full draft. If the writer applies all recommendations, still preserve explicit truth boundaries and unresolved evidence gaps. If the article needs no further rhetorical revision, say so instead of manufacturing work.

When the diagnosis finds no consequential revision, skip the approval checkpoint, state that no further rhetorical revision is necessary, and proceed to the ready-state handoff.

Distinguish Slopless's already-applied mechanical cleanup from Remarkable's rhetorical recommendations. After substantive accepted edits, rerun Slopless and return to watched Roughdraft review.
