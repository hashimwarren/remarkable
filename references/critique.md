# Critique a Complete Article

## Purpose

Diagnose a complete article against its governing premise and rhetorical contract, localize only the highest-value interventions, and leave consequential revision authority with the writer.

## Required inputs

- The canonical article, `PREMISE.md`, and the approved outline with its rhetorical contract when available.
- The actual Slopless outcome and unresolved evidence boundaries.
- The writer's explicit choice to run critique, or a focused `critique` invocation.

## Process

After the first Slopless pass, offer **A. Run Remarkable critique** or **B. Open the draft as-is** and STOP. If critique is chosen, read [rhetorical-contract.md](rhetorical-contract.md), run the adherence and effectiveness passes below, diagnose in the priority order, run the second and final automatic headline pass through [headline.md](headline.md), assess any planned or produced informational images through [informational-images.md](informational-images.md), share one overall diagnosis plus three prioritized revisions and their sequence, and add at most one document-level diagnosis and five localized CriticMarkup interventions. Read [roughdraft-handoff.md](roughdraft-handoff.md) for watched review.

Use this compact offer:

> Would you like me to run **Remarkable critique** before your final review? It will evaluate whether the article preserves and effectively executes its premise, rhetorical choices, argument, evidence, and reader movement. I’ll summarize the priorities here and add up to five focused inline comments in Roughdraft. I won’t rewrite the article until you approve the direction.
>
> **A. Run Remarkable critique**
>
> **B. Open the draft as-is**

Apply the branches exactly:

- **A. Run Remarkable critique:** produce the diagnosis and localized interventions, then launch the annotated canonical article through `roughdraft-handoff.md`. After completed review or its explicit chat fallback, use the revision-authority checkpoint below.
- **B. Open the draft as-is:** add no Remarkable interventions. Launch the unannotated canonical article through `roughdraft-handoff.md`. After completed review or its explicit chat fallback, reread the canonical Markdown, summarize what the writer changed or clarified, and proceed to the ready-state handoff in [wayfinding.md](wayfinding.md). If the review produced a request for substantive rhetorical revision, confirm that request before applying it and rerun [slopless.md](slopless.md) afterward.

Neither branch may end at the A/B choice or treat review completion as approval of unrequested edits.

## User checkpoint

After review, obtain revision authority through **Review revisions one by one**, **Apply recommended revisions**, or **Leave the draft unchanged**. Require one-by-one approval for any premise, rhetorical-direction, proof-burden, major-claim, reader-movement, or CTA change even under blanket approval.

## Artifact or state effects

Patch only the canonical article and, when a different direction is approved, the canonical outline. Do not create a second draft, separate contract, or duplicate Slopless's mechanical findings. CriticMarkup may remain in the canonical article until the writer resolves it.

## Degraded and failure behavior

Use the chat/Markdown fallback in [roughdraft-handoff.md](roughdraft-handoff.md) when Roughdraft cannot complete. Make no rhetorical edits on an ambiguous decision. If no consequential revision exists, say so and proceed instead of manufacturing work.

## Completion criterion

The writer's accepted revisions are applied, rejected and undecided passages remain unchanged, any approved direction change is recorded and reapproved in the outline before prose changes, Slopless is rerun after substantive edits, and the article returns to the available review surface.

## Next-stage handoff

Follow [wayfinding.md](wayfinding.md) for the ready-state handoff and offer another purposeful critique without implying that it is required.

Diagnose in this priority order:

1. Premise
2. Headline and opening frame
3. Question and resolution
4. Argument structure
5. Evidence gaps
6. Reader momentum and visual comprehension
7. Sentence craft

Use five primary principles: reader momentum; concrete before clever; claim, proof, consequence; no orphan claims; lead with the change.

Use supporting principles only after structural issues: frictionless comprehension, one job per sentence, specific beats emphatic, answer the reader's next question, and prefer a sharp noun with a strong verb.

## Compare contract with execution

Run two conceptual passes before recommending revisions:

### Adherence

For each consequential section, compare the draft with the corresponding italic contract sentence in the approved outline. Ask whether the selected move remains recognizable, whether its planned timing and emphasis survived drafting and Slopless, and whether the section still creates the intended effect.

Name drift concretely:

> The outline calls for an investigative opening, but the second paragraph explains the answer. The mystery disappears before it creates momentum.

### Effectiveness

Then judge whether the approved direction actually works. A faithful section may still be weak, confusing, unsupported, or badly placed:

> The closing returns to the opening scene, but currently summarizes the premise instead of transforming the scene's meaning.

When a consequential section is weak, prefer strengthening the approved direction. When a different direction may work better, explain the tradeoff and offer:

- **Strengthen this direction**
- **Explore a different direction**
- **Keep it as written**

Example:

> We could replace the investigative opening with a result-first opening. It would create faster authority and urgency, but sacrifice some mystery and personal identification.

Do not change direction under general revision approval. If the writer chooses **Explore a different direction**, update the outline's contract sentence first, reset it to `Status: working`, revise affected bullets, and obtain **Draft this structure** approval before materially rewriting the article.

When the article uses question-and-resolution architecture, read [narrative-tension.md](narrative-tension.md) and test:

- whether the opening creates a meaningful question from the premise and supported situation rather than generic curiosity;
- whether a heading, summary, transition, or explanatory aside gives away the complete answer before the planned reveal;
- whether the reveal answers the exact question raised instead of switching to a neighboring claim;
- whether the answer is specific, proportionate to the proof, and consequential;
- whether the framework acts as answer, embodiment, or application rather than being appended automatically; and
- whether the sections after the reveal demonstrate, qualify, or apply the answer sufficiently for the resolution to feel earned.

When no genuine question belongs, do not manufacture one as a critique recommendation. Diagnose the direct argument on its own terms.

Read [headline.md](headline.md) and judge the current headline against the completed article. Preserve it when it already earns attention, frames the premise, and stays inside the evidence boundary; optionally offer **Explore alternative headlines**. When it is weak, include source-diverse alternatives and a recommendation in the critique, then require approval before replacing it.

For every planned or produced article image, read [informational-images.md](informational-images.md). Confirm that it performs a Legitimacy, Explanation, Numbers, or Steps job, sits near the claim it advances, adds information beyond the caption, and remains faithful to the evidence. Recommend removal or redesign when prose works better. Never treat visual polish as a substitute for proof.

First return a high-level diagnosis, distinguish adherence from effectiveness, identify the three most consequential problems, and give a prioritized revision sequence. Do not rewrite the whole article until the writer accepts the direction.

When the writer invokes critique or chooses the post-Slopless critique offer, share the diagnosis in chat and add at most one document-level diagnosis and five high-value inline CriticMarkup interventions by default. The chat prioritizes the editorial work; inline feedback localizes where the writer can act. Do not duplicate the same prose word for word. Comments should ask useful questions or explain stakes; suggestions should show a concrete fix. Do not wallpaper the document with feedback or duplicate Slopless's mechanical checks.

## Obtain revision authority

After the critique and Roughdraft review, use the runtime's structured user-input control when available:

- **Review revisions one by one**
- **Apply recommended revisions**
- **Leave the draft unchanged**

Use the same choices as a short plain-text fallback. Favor **Review revisions one by one** in the ordering and explanation because consequential editorial judgment belongs to the writer. Never interpret an ambiguous response as permission to change the premise, rhetorical direction, proof burden, major claims, reader movement, or CTA.

- **Review revisions one by one:** use the sequence below. Partial acceptance authorizes only the accepted local edits; leave rejected and undecided passages unchanged.
- **Apply recommended revisions:** apply the presented local recommendations, but review any premise, rhetorical-direction, proof-burden, major-claim, reader-movement, or CTA change one by one because blanket approval does not authorize those changes.
- **Leave the draft unchanged:** make no rhetorical edits. Preserve the current file and proceed to the ready-state handoff.
- **Ambiguous reply:** make no rhetorical edits and ask the same decision again in plain language.

For one-by-one review, present only one consequential recommendation at a time:

1. the issue;
2. why it matters to the governing premise;
3. the proposed direction; and
4. the decision requested.

Allow the writer to accept, modify, discuss, or reject it. Apply only accepted changes and patch the existing article rather than creating a second full draft. If the writer applies all recommendations, still preserve explicit truth boundaries and unresolved evidence gaps. If the article needs no further rhetorical revision, say so instead of manufacturing work.

For an approved change of rhetorical direction, follow [rhetorical-contract.md](rhetorical-contract.md): update and reapprove the outline before changing the article. Never silently replace an approved choice with a safer, more conventional one.

When the diagnosis finds no consequential revision, skip the approval checkpoint, state that no further rhetorical revision is necessary, and proceed to the ready-state handoff.

Distinguish Slopless's already-applied mechanical cleanup from Remarkable's rhetorical recommendations. After substantive accepted edits, rerun Slopless, verify the rhetorical contract again, and return to watched Roughdraft review.
