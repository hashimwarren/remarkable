# Working Outline

The working outline lets the writer judge the argument before prose makes structural change expensive. It is not a high-level draft.

## Build the outline

Use `PREMISE.md`, the article map and its answers, any approved practical framework in the map, the confirmed objection response, approved Personal Authority, project context, existing evidence or proof artifacts, and any existing article prose. Save it beside the article as `<article-stem>.outline.md`.

Read [visual-placeholders.md](visual-placeholders.md). Start the visual subagent after the headline and major section jobs are stable, then continue building the outline while it works.

Begin the artifact with `Status: working`. Change it to `Status: approved` only after the user explicitly chooses **Draft this structure**. Any material revision resets it to `Status: working`; file existence alone never means approval.

For a normal long-form article, use 300–700 words and a small number of major sections. Include:

- a working headline;
- a generated header-image placeholder immediately after the headline;
- the governing premise, reader, and desired movement;
- major section headings;
- one italic sentence explaining each section's rhetorical job;
- bullets for claims, examples, transitions, objection handling, and intended movement;
- an approved practical framework when one exists, preserving its governing logic, demonstration, and limit;
- proof placeholders attached to the claims they must support;
- explicit requests for missing author information; and
- a closing or CTA plan, omitting a CTA when none belongs.

Evaluate the claims and narrative for up to two additional useful visual placeholders. Attach each to the section where it would perform its proof, comprehension, or story job. Include a relative Markdown image path, concise concept alt text, and one italic production note. Do not add decorative placeholders merely to reach three images.

Classify unresolved needs:

- **Blocking:** drafting cannot proceed truthfully without an answer.
- **Helpful:** an answer improves specificity, but drafting may proceed.
- **Researchable:** Remarkable can investigate it through `prove`.

Do not turn the outline into a questionnaire, write polished paragraphs, perform sentence-level editing, or generate alternative outlines unless asked.

## Review the structure

Open the outline in watched Roughdraft mode. Add only consequential inline questions about the opening situation, necessary claim order, missing proof or experience, fair treatment of the objection, and ending movement.

After `review_completed`, incorporate explicit feedback and offer exactly three choices:

- **Draft this structure**
- **Revise the outline**
- **Help me answer the missing questions**

Use the runtime's structured user-input control when available and the same three choices as a plain-text fallback. Require an explicit choice:

- **Draft this structure:** require no Blocking items, set `Status: approved`, and continue to prose.
- **Revise the outline:** ask what should change, update the artifact, set `Status: working`, reopen watched Roughdraft, and repeat this checkpoint.
- **Help me answer the missing questions:** work through the unresolved needs, update or reclassify them, set `Status: working`, reopen watched Roughdraft, and repeat this checkpoint. Do not fall through to prose.

## Draft from it

Draft only when the outline says `Status: approved` and no Blocking item remains. If approval is absent or may no longer apply, show a compact structural summary and ask the same three-choice question again; never infer approval from file existence. Preserve the claim order, proof assignments, objection response, reader movement, and deliberate gaps. Keep `[AUTHOR INPUT NEEDED: ...]` markers for missing personal material. Patch the existing article Markdown rather than making a parallel full draft.

As the map becomes prose, remove resolved CriticMarkup questions, temporary bracketed scaffold guidance, unused generic claim blocks, and unused asset or CTA placeholders. Preserve deliberate, specific gaps such as `[AUTHOR INPUT NEEDED: ...]` and `[EVIDENCE NEEDED: ...]`.
