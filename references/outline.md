# Working Outline

## Purpose

Let the writer judge an evidence-strengthened argument before prose makes structural change expensive. The working outline is not a high-level draft or questionnaire.

## Required inputs

- `PREMISE.md` and the confirmed private route brief.
- Confirmed objection response, approved Personal Authority, and approved framework when present.
- Project context, existing evidence, and any existing article prose or legacy map material.

## Process

Reserve or reuse the canonical paths, build the scan-friendly structure, incorporate the claim-to-evidence plan from [prove.md](prove.md), then review the evidence-strengthened outline. The detailed rules below own structure and approval.

## User checkpoint

After review, offer exactly **Draft this structure**, **Revise the outline**, or **Help me answer the missing questions**. Require an explicit choice. Only the first choice may approve the outline, and only when no Blocking item remains.

## Artifact or state effects

Save one `<article-stem>.outline.md` beside the canonical article. Begin with `Status: working`; set `Status: approved` only after explicit approval. Material revision resets it to working. Do not create route, story, framework, proof, or alternate outline artifacts.

## Degraded and failure behavior

Use the chat/Markdown path from [roughdraft-handoff.md](roughdraft-handoff.md) when Roughdraft is missing, unsupported, incomplete, or fails. Preserve specific `[AUTHOR INPUT NEEDED: ...]` and accepted non-central `[EVIDENCE NEEDED: ...]` gaps. Stop when a central claim or Blocking item remains unresolved.

## Completion criterion

The writer explicitly chooses **Draft this structure**, the outline says `Status: approved`, and no Blocking item or unsupported central claim remains.

## Next-stage handoff

Pass the approved canonical outline to [article.md](article.md). Never infer approval from file existence or review completion.

## Build from the selected route

Use `PREMISE.md`, the confirmed article-route brief, confirmed objection response, approved Personal Authority, approved practical framework when present, project context, existing evidence, and any existing article prose. A legacy map may supply confirmed writer-owned context, but its old scaffold and questions do not govern the new outline. Read [narrative-tension.md](narrative-tension.md) and [visual-placeholders.md](visual-placeholders.md). Save the outline beside the reserved article as `<article-stem>.outline.md`.

Reuse the valid article path already named in `PREMISE.md`. Reserve a collision-safe path only when it is `pending`, absent, or invalid:

```bash
python3 <skill-directory>/scripts/reserve_draft.py "<descriptive topic>" --root "$PWD"
python3 <skill-directory>/scripts/reserve_outline.py <absolute-article-path> --root "$PWD"
```

Update `PREMISE.md` with a newly reserved relative article path. If outline reservation reports `existing`, update that outline rather than creating a parallel version.

Begin with `Status: working`. Change it to `Status: approved` only after the user explicitly chooses **Draft this structure**. Any material revision resets it to `Status: working`; file existence alone never means approval.

For a normal long-form article, use 300–700 words and a small number of major sections. Include:

- a working headline;
- a header-image concept immediately after the headline;
- the governing premise, reader, and desired movement;
- the chosen route expressed as the article's movement, without naming its internal architecture;
- the consequential question, where it emerges, the specific answer, and where that answer becomes clear when a genuine question belongs;
- major section headings;
- one italic sentence explaining each section's rhetorical job;
- bullets for claims, examples, transitions, objection handling, and intended movement;
- approved Personal Authority and a practical framework only where the route gives them real jobs;
- proof placeholders attached to the claims they must support;
- explicit requests for missing author information; and
- a closing or CTA plan, omitting a CTA when none belongs.

Classify unresolved needs:

- **Blocking:** drafting cannot proceed truthfully without an answer.
- **Helpful:** an answer improves specificity, but drafting may proceed.
- **Researchable:** Remarkable can investigate it through `prove`.

Do not write polished paragraphs, perform sentence-level editing, or expose awareness labels and copywriting-framework names. The invisible architecture should create momentum without turning the outline into a fill-in-the-blanks formula.

## Shape the question-and-resolution progression

Use headings, rhetorical-job notes, and bullets to make the article move rather than merely sort its subject matter. When a genuine consequential question belongs:

1. Establish the situation the reader needs to understand.
2. Make the contrast, contradiction, surprising outcome, or failed expectation visible.
3. Deepen the stakes or test an incomplete explanation without repeating the same problem.
4. Reveal the specific answer at the planned point.
5. Explain, prove, qualify, demonstrate, or apply that answer.
6. Return to the opening situation and show what the resolution now changes.

Before the answer, every section must deepen the question, raise its stakes, eliminate an incomplete explanation, or narrow what the answer must explain. After the answer, every section must help the reader understand, believe, test, remember, or use it. Remove passages that only postpone the answer.

Choose whether the question emerges in the first sentence, after the approved story, or after the problem and stakes. Do not default to a literal question. Prefer headings that perform the selected route—situation, mistaken explanation, discovery, mechanism, demonstration, application—over generic headings such as “Background,” “Problem,” or “Solution.”

If no honest consequential question emerges, use a direct argument structure. Never force a Personal Authority story, mystery, or framework into the outline.

## Strengthen proof before review

After the initial outline exists, read [prove.md](prove.md). Add its compact claim-to-evidence plan to the same outline. Resolve central gaps, then revise headings, claims, route execution, proof assignments, and visual positions when evidence changes what the article can responsibly say.

Keep `Status: working` throughout proof development. A central unsupported claim cannot pass to approval as a placeholder. Preserve explicitly accepted non-central gaps as `[EVIDENCE NEEDED: ...]`.

## Review the evidence-strengthened structure

Read [roughdraft-handoff.md](roughdraft-handoff.md), then open the outline through its watched lifecycle. Add only consequential inline questions about the opening situation, necessary claim order, missing proof or experience, fair treatment of the objection, and ending movement.

After the handoff returns completed review or the writer chooses its chat fallback, incorporate explicit feedback and offer exactly three choices:

- **Draft this structure**
- **Revise the outline**
- **Help me answer the missing questions**

Use the runtime's structured user-input control when available and the same three choices as a plain-text fallback. Require an explicit choice:

- **Draft this structure:** require no Blocking items, set `Status: approved`, and continue to prose.
- **Revise the outline:** ask what should change, update it, set `Status: working`, reopen watched Roughdraft, and repeat this checkpoint.
- **Help me answer the missing questions:** work through unresolved needs, update or reclassify them, set `Status: working`, reopen watched Roughdraft, and repeat the checkpoint. Do not fall through to prose.

## Draft from it

Draft only when the outline says `Status: approved` and no Blocking item remains. If approval is absent or may no longer apply, show a compact structural summary and ask the same three-choice question again; never infer approval from file existence. Preserve the selected route, claim order, proof assignments, objection response, reader movement, and deliberate gaps. Keep `[AUTHOR INPUT NEEDED: ...]` markers for missing personal material. Patch the reserved article Markdown rather than making a parallel full draft.

Do not copy outline-only material into the article: status, rhetorical-purpose notes, planning labels, claim-to-evidence plan, unresolved CriticMarkup, or unused asset and CTA concepts.
