# Working Outline

The working outline lets the writer judge the argument before prose makes structural change expensive. It is not a high-level draft.

## Build the outline

Use `PREMISE.md`, the resolved article map, its claim-to-evidence plan, any approved practical framework in the map, the confirmed objection response, approved Personal Authority, project context, existing evidence or proof artifacts, and any existing article prose. Read [narrative-tension.md](narrative-tension.md). Save the outline beside the article as `<article-stem>.outline.md`.

Before outlining, revalidate the map's article question, answer, reveal point, and framework role against the resolved feedback and current proof plan. Update the design when a claim was narrowed, removed, contradicted, or newly supported. If the question is no longer genuine or the answer is no longer supported, use a direct structure instead of preserving stale narrative machinery.

Read [visual-placeholders.md](visual-placeholders.md). Start the visual subagent after the headline and major section jobs are stable, then continue building the outline while it works.

Begin the artifact with `Status: working`. Change it to `Status: approved` only after the user explicitly chooses **Draft this structure**. Any material revision resets it to `Status: working`; file existence alone never means approval.

For a normal long-form article, use 300–700 words and a small number of major sections. Include:

- a working headline;
- a generated header-image placeholder immediately after the headline;
- the governing premise, reader, and desired movement;
- the consequential question the article will make the reader want answered, where it emerges, the specific answer, and where that answer becomes clear, when a genuine question belongs;
- major section headings;
- one italic sentence explaining each section's rhetorical job;
- bullets for claims, examples, transitions, objection handling, and intended movement;
- an approved practical framework when one exists, preserving its governing logic, demonstration, and limit;
- proof placeholders attached to the claims they must support;
- explicit requests for missing author information; and
- a closing or CTA plan, omitting a CTA when none belongs.

Carry forward the map's proof and comprehension or story positions when their jobs remain useful. Attach each to the section where it performs that job. Include a relative Markdown image path, concise concept alt text, and one italic production note. Remove a position whose job disappeared, and do not add decorative placeholders merely to reach three images.

Classify unresolved needs:

- **Blocking:** drafting cannot proceed truthfully without an answer.
- **Helpful:** an answer improves specificity, but drafting may proceed.
- **Researchable:** Remarkable can investigate it through `prove`.

Do not turn the outline into a questionnaire, write polished paragraphs, perform sentence-level editing, or generate alternative outlines unless asked.

## Shape the question-and-resolution progression

Use the headings, rhetorical-job notes, and bullets to make the article move rather than merely sort its subject matter. When a genuine consequential question belongs:

1. Establish the situation the reader needs to understand.
2. Make the contrast, contradiction, surprising outcome, or failed expectation visible.
3. Deepen the stakes or test an incomplete explanation without repeating the same problem.
4. Reveal the specific answer at the planned point.
5. Explain, prove, qualify, demonstrate, or apply that answer.
6. Return to the opening situation and show what the resolution now changes.

Before the answer, every section must deepen the question, raise its stakes, eliminate an incomplete explanation, or narrow what the answer must explain. After the answer, every section must help the reader understand, believe, test, remember, or use it. Remove passages that only postpone the answer.

Choose whether the question emerges in the first sentence, after the approved story, or after the problem and stakes. Do not default to a literal question. Prefer headings that perform the progression—situation, mistaken explanation, discovery, mechanism, demonstration, application—over generic headings such as “Background,” “Problem,” or “Solution.”

If no honest consequential question emerges, use a direct argument structure and omit question-and-reveal fields. Never force a Personal Authority story, mystery, or framework into the outline.

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
