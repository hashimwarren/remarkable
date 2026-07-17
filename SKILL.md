---
name: remarkable
description: Build persuasive long-form articles through premise discovery, opening design, claim-proof-consequence development, evidence validation, endings, critique, Slopless hygiene, and Roughdraft review. Use only when a human explicitly invokes Remarkable to create, develop, prove, finish, or critique an article while preserving existing voice and style guidance. Do not use for voice imitation, style-guide generation, general proofreading, or non-article copy formats.
---

# Remarkable

Give AI agents the architecture of persuasion. Style governs how writing sounds; Remarkable governs what the writing helps a reader believe, feel, and do.

Use this positioning: **Bring your own style. Remarkable strengthens the persuasion.** When comparing it with Impeccable, use: **Impeccable gives agents visual rhetoric. Remarkable gives agents verbal rhetoric.** Treat this release as `0.9-beta`.

## Preserve the product boundary

- Put persuasion before style. Do not invent a house voice, imitate a person, or create `VOICE.md` or `STYLE.md`.
- Treat truth as a constraint. Never invent evidence or preserve a strong claim beyond what its proof supports.
- Let the user choose the premise and remain the final editor.
- Keep `PREMISE.md` as the required durable rhetorical artifact.
- Never write rhetoric to `DESIGN.md`. Propose durable `PRODUCT.md` changes and obtain approval before writing them.
- Let Slopless own deterministic prose hygiene and Roughdraft own local review UX.
- Do not make the user learn commands or rhetorical terminology before receiving value.

## Route the invocation

Interpret the user's explicit invocation and route to the smallest useful mode:

- `start` or no mode: run the guided article workflow.
- `premise`: generate or refine premise directions.
- `outline`: create or revise the working outline from the selected premise, article map, and available answers. Read [references/outline.md](references/outline.md).
- `draft`: draft the article from an explicitly approved working outline. Read [references/outline.md](references/outline.md) and [references/article.md](references/article.md).
- `opening`: build or diagnose the reader contract. Read [references/opening.md](references/opening.md).
- `develop`: develop the argument through claim, proof, and consequence. Read [references/develop.md](references/develop.md).
- `prove`: map, research, validate, and design evidence. Read [references/prove.md](references/prove.md) and [references/evidence-design.md](references/evidence-design.md).
- `ending`: complete the premise and, when appropriate, evaluate the CTA. Read [references/ending.md](references/ending.md).
- `critique`: diagnose a complete article before rewriting. Read [references/critique.md](references/critique.md).

Natural phrasing is sufficient; do not require exact command syntax. A focused mode acts only on that stage unless the user asks to continue.

## Discover context progressively

Run the bounded scanner before premise generation, drafting, or critique:

```bash
python3 <skill-directory>/scripts/discover_context.py --root "$PWD"
```

Read returned files in priority order and stop when constraints are clear. Look for `PRODUCT.md`, `DESIGN.md`, `AUDIENCE.md`, `EVIDENCE.md`, `POSITIONING.md`, `VOICE.md`, `STYLE.md`, `COPY.md`, `BRAND.md`, `README.md`, `AGENTS.md`, `CLAUDE.md`, relevant marketing documents, and published writing.

Treat `PRODUCT.md` as enduring product and audience context, `DESIGN.md` as visual context, and `PREMISE.md` as the active article's rhetorical strategy. Track important contextual claims internally as `explicit`, `inferred`, or `uncertain`. Do not ask the user to restate known context or define tone and cadence unless a consequential ambiguity remains.

Read [references/context-artifacts.md](references/context-artifacts.md) before creating or changing any context artifact beyond `PREMISE.md`.

## Run the guided workflow

### 1. Establish intent

If the user has not answered it in substance, ask exactly:

> What do you want the reader to realize, and why should that matter to them right now?

Infer the likely audience, stakes, urgency, and persuasive directions. Ask at most one follow-up and only when the missing information materially changes the premise options.

### 2. Offer three compact premises

Read [references/premise.md](references/premise.md) and [references/premise-transformation.md](references/premise-transformation.md). When the runtime supports subagents, run the five-scout premise council defined in `premise-transformation.md`: give every scout the same bounded brief, assign each a different pair of appeals, wait for all scouts, and pool their strongest candidates. Do not let scouts choose the finalists. The main agent discards the obvious cluster, fingerprints the survivors, scores the complete pool, and runs pairwise distinctness checks before presenting exactly three materially different directions.

Before delegation, tell the user:

> I’m sending the same brief to five independent premise scouts. Each will explore a different persuasive territory. I’ll compare their strongest ideas and show you only the three most promising and genuinely different directions.

If subagents are unavailable, do not block premise discovery: use the single-agent wide-generation fallback in `premise-transformation.md`. Limited concurrency is not unavailability. When fewer than five worker slots are open, run the five scouts in capacity-aware waves, preserve every assignment, and collect all five reports before synthesis. Retry a failed scout once when practical; if it still fails, simulate only that scout’s territory in the main thread and disclose the fallback briefly. Never fabricate scout results.

Before the options, explain:

> I’m going to show you three genuinely different ways this article could move the reader. Each premise combines the central claim with a different persuasive approach. Focus on which realization feels most important and generative—the headline is only an illustration.

State the shared realization and why-now context once at the top. Then label the directions `A`, `B`, and `C`. Each option contains only:

1. **Premise**
2. **Likely objection**
3. **Possible headline**

The premise and persuasive angle are one decision. Integrate the selected appeal and fascination posture into the premise's wording and force, but do not expose appeal, fascination, advantage, pairing, archetype, or attention-strategy labels unless the user explicitly asks how the options were developed. A likely objection is the strongest intelligent reader resistance the article must answer, qualify, or accommodate—not a possible writing mistake. Do not repeat `Reader realization`, `Why it matters now`, `Persuasive angle`, or `Why it works` under each option.

Use the runtime’s structured user-input control when it is available. Keep the full premise explanations in chat and make the control labels compact:

- **A — [short direction name]**
- **B — [short direction name]**
- **C — [short direction name]**

Ask: **Which premise should govern the article: A, B, or C?** Never choose for them. In the preamble, explain that the user can instead type `Make these bolder`, `Go wider`, `[letter], but bolder`, or a natural-language combination in the control's free-form response. Treat **Make these bolder** as a request for a genuinely new, stronger set—not approval of the current options. When structured input is unavailable, offer the same choices in plain text. Accept selection by letter, direction name, or unambiguous natural language. Confirm the chosen premise before writing `PREMISE.md`.

For `Go wider`, discard the explored premise clusters and generate three directions with different core claims, causal explanations, and consequences. For `[letter], but bolder`, preserve the claim, appeal, fascination posture, and truth boundary while intensifying the premise through its fascination trigger. When the user combines options, synthesize one governing premise. Whenever a premise is widened, intensified, or combined, derive a fresh strongest intelligent likely objection rather than carrying one forward from a discarded direction. Confirm the complete revised premise and objection before continuing.

### 3. Pressure-test the objection

After the user confirms the governing premise, read [references/objection-response.md](references/objection-response.md). Show the selected likely objection and ask whether it is the strongest intelligent reader resistance and how the writer would answer it or what the article could show to make a skeptic reconsider.

Use structured input when available with exactly three choices: **Yes — I’ll answer**, **Revise the objection**, and **Help me answer it**. Confirm both the final objection and a compact response direction before continuing. When a premise is widened, intensified, or combined, repeat this checkpoint with a fresh objection and response direction.

Keep only the confirmed objection in `PREMISE.md`. Carry the response direction into the article map; it is argument material, not premise metadata.

### 4. Develop Personal Authority and preserve the premise

After the user confirms the governing premise, read [references/personal-authority.md](references/personal-authority.md). Ask exactly:

> Is there something you discovered, struggled through, or changed your mind about that led you to this premise?

Use the runtime's structured user-input control when available:

- **Yes — I’ll tell you**
- **Help me find it**
- **Not for this piece**

When structured input is unavailable, offer the same choices in plain text. Accept incomplete notes. Select the best-fitting Personal Authority approach internally, ask only necessary factual follow-ups, and read back a compact story architecture—not polished article prose. Then use a structured confirmation question with at most three choices: **Approve**, **Revise it**, and **Skip personal story**. The free-form response can request more questions or less personal detail. Never interpret silence or ambiguity as approval.

Continue revising until the user explicitly approves or skips. Do not fabricate experience, heighten drama beyond the supplied facts, or pressure the user to disclose personal material. After approval or skip, continue automatically to the article map.

Create or update `PREMISE.md` at the project root. Use only this structure:

```markdown
# Premise

Draft: [relative draft path, or pending]
Status: selected
Updated: [YYYY-MM-DD]

## Audience
[Who the reader is and the relevant context they bring.]

## Current Belief
[What the reader currently believes, assumes, or overlooks.]

## Desired Movement
[What the reader should come to believe, feel, or become ready to do.]

## Premise
[The single controlling idea.]

## Likely Objection
[The strongest intelligent resistance the intended reader is likely to have.]

## Why Now
[Why the idea matters now.]
```

When a personal story was approved, append the lean `## Personal Authority` structure defined in `references/personal-authority.md`. Omit that section entirely when the user skips.

Do not expose internal appeal or fascination metadata in `PREMISE.md`. Do not put an argument, proof plan, evidence list, headline, opening, CTA, or polished draft prose in it. If the file belongs to another article, do not overwrite it without permission.

### 5. Create and open the article map

Create a collision-safe scaffold from the selected premise:

```bash
python3 <skill-directory>/scripts/create_article_map.py "<descriptive topic>" --root "$PWD"
```

Replace `pending` in `PREMISE.md` with the returned relative draft path. The map contains brief temporary guidance and one CriticMarkup question for each stage: opening, argument, visible evidence, ending, and CTA. Adapt the map to the premise: add or remove claim blocks, omit visible evidence when it adds no proof, and remove the CTA when none belongs.

Before opening the map, replace `[Add the confirmed response direction before review.]` with the confirmed response direction. Do not place that response in `PREMISE.md`. If the response names evidence that does not yet exist, preserve it as a specific proof need rather than a fact.

Before opening it, explain the three interaction modes, then use the runtime's structured user-input control when available:

- **Open Roughdraft** — edit the map or answer inline, then click **Done Reviewing**.
- **Guide me** — answer one section question at a time in chat.
- **Build the outline** — let Remarkable resolve the map from available context and propose the argument structure.

When structured input is unavailable, ask for the same choice in plain text. STOP and wait for the user's selection before launching watched mode or building the outline.

Only after the user selects **Open Roughdraft**, tell them that Remarkable will resume automatically after **Done Reviewing**, then open the map in watched mode. Do not use `--no-watch` for this handoff:

```bash
python3 <skill-directory>/scripts/open_roughdraft.py <absolute-draft-path> --project-root "$PWD"
```

Wait for the wrapper to report `review_completed`. Read all comments, suggestions, and replies from the same Markdown file. Treat closing or abandoning the review as different from clicking **Done Reviewing**; do not claim completion without the machine-readable completion signal.

If the user switches to **Guide me** or **Build the outline** while watched mode is active, stop the watched process before continuing in chat. Do not leave an orphaned review command running.

### 6. Follow the chosen interaction mode

- **Roughdraft:** use the feedback returned by the watched session. Do not ask answered questions again.
- **Guide me:** if the user switches to chat, ask one stage question at a time in this order: opening, develop, prove, ending. Write each answer into the same draft before moving on.
- **Build the outline:** use the premise and available context to resolve the map without additional interviewing, classify unanswered needs, and proceed to the working outline. Preserve explicit evidence gaps.

The user can change modes at any time. Keep the Markdown article map as the source of truth across all modes. Do not remove its guidance or unresolved placeholders yet; they are inputs to the working outline.

### 7. Create and approve the working outline

After article-map questions have been answered or classified, read [references/outline.md](references/outline.md). Reserve the predictable outline path beside the article:

```bash
python3 <skill-directory>/scripts/reserve_outline.py <absolute-article-path> --root "$PWD"
```

Use the returned path. If it reports `existing`, update that outline rather than creating a parallel version. Build a 300–700 word, scan-friendly working outline from `PREMISE.md`, the article map, confirmed objection response, Personal Authority when approved, project context, and available evidence. Include major headings, one italic rhetorical-purpose statement per section, bullets, attached proof placeholders, explicit information requests, and a closing or CTA plan. Classify unresolved needs as **Blocking**, **Helpful**, or **Researchable**.

Begin the outline with `Status: working`. Set `Status: approved` only after the user explicitly approves the structure. Any material outline revision resets it to `Status: working`; never infer approval from the file's existence.

Open the outline in watched Roughdraft mode with only a small number of consequential inline questions:

```bash
python3 <skill-directory>/scripts/open_roughdraft.py <absolute-outline-path> --project-root "$PWD"
```

After **Done Reviewing**, incorporate the feedback and use the runtime's structured user-input control when available with exactly three choices: **Draft this structure**, **Revise the outline**, or **Help me answer the missing questions**. Use the same choices as a plain-text fallback. STOP and wait. Do not treat an ambiguous response as approval.

- For **Draft this structure**, require no Blocking items, set `Status: approved`, and continue.
- For **Revise the outline**, ask what should change, update it, set `Status: working`, reopen watched Roughdraft, and repeat the approval checkpoint.
- For **Help me answer the missing questions**, work through unresolved needs, update or reclassify them, set `Status: working`, reopen watched Roughdraft, and repeat the checkpoint. Do not fall through to prose.

### 8. Draft from the approved outline

Require `Status: approved` and no Blocking items in the working outline. If no outline exists, route to `outline`; do not silently jump from the map to prose. If approval is absent or may no longer apply, show a compact structural summary and ask the same three-choice decision again; never infer approval from file existence. Before writing prose, run the Slopless preflight in section 9 and stop if it is not ready. Preserve the selected premise, confirmed objection response, agreed claim order, proof assignments, intended reader movement, and deliberate gaps. Use explicit `[AUTHOR INPUT NEEDED: ...]` markers rather than inventing missing personal information. Patch the existing article Markdown instead of creating a second prose draft.

As the article map becomes prose, remove resolved CriticMarkup questions, temporary bracketed scaffold guidance, unused generic claim blocks, and unused asset or CTA placeholders. Preserve deliberate, specific gaps such as `[AUTHOR INPUT NEEDED: ...]` and `[EVIDENCE NEEDED: ...]`.

Read [references/article.md](references/article.md), [references/opening.md](references/opening.md), [references/develop.md](references/develop.md), and [references/ending.md](references/ending.md). Default to 800–1,200 words, aiming for about 1,000, unless the user specifies otherwise.

Keep the premise alive from opening through ending. Build major movements through claim, proof, and consequence. Use evidence supplied by the user or relevant context; mark non-central gaps specifically and stop for central unsupported claims.

When evidence work is requested or necessary, read [references/prove.md](references/prove.md) and [references/evidence-design.md](references/evidence-design.md). Prefer user-owned evidence, then first-party public sources, then credible independent evidence. Ask before materially expanding research into connected private sources. Recommend visible proof only when it performs an evidentiary job.

### 9. Run Slopless

For English articles, preflight before substantive drafting:

```bash
python3 <skill-directory>/scripts/run_slopless.py --preflight --project-root "$PWD"
```

The wrapper prefers an installed Slopless and otherwise acquires pinned `slopless@0.2.23` through `npx --yes` without modifying project dependencies. Continue only when it reports `ready`. If blocked by Node.js, network, or execution permissions, stop before drafting. Never silently produce an unlinted English article.

After drafting, run:

```bash
python3 <skill-directory>/scripts/run_slopless.py <absolute-draft-path> --project-root "$PWD"
```

Record the initial finding count, rule-type count, rule IDs, and total lint runs. Revise findings selectively, preserving the premise, facts, project style, and useful rhetorical force. Rerun until clean or only deliberate exceptions remain. Derive no more than three truthful, plain-language improvement themes; do not recite a rule-by-rule changelog.

Skip Slopless for non-English drafts and explain its language limitation.

### 10. Return to Roughdraft

After the first draft passes Slopless, offer exactly:

> Would you like me to run **Remarkable critique** before your final review? It will evaluate the premise, argument, evidence, reader momentum, comprehension, and sentence craft. I’ll summarize the priorities here and add up to five focused inline comments in Roughdraft. I won’t rewrite the article until you approve the direction.
>
> **A. Run Remarkable critique**
>
> **B. Open the draft as-is**

STOP and wait for the user's choice.

If the user chooses critique, read [references/critique.md](references/critique.md). Share one overall diagnosis, three prioritized revisions, and a recommended revision sequence in chat. Add the same critique at action resolution—not word-for-word duplication—as at most five localized CriticMarkup comments or suggestions in the draft. Then open the annotated file in watched mode.

If the user chooses the draft as-is, open it directly in watched mode:

```bash
python3 <skill-directory>/scripts/open_roughdraft.py <absolute-draft-path> --project-root "$PWD"
```

Before running the watched command, explain:

> Roughdraft is open for your review. You can edit the text directly, leave inline comments, or suggest changes. When you’re finished, click **Done Reviewing**; Remarkable will automatically resume here with your feedback.

Wait for the wrapper to report `review_completed`. Read the reviewed Markdown, summarize what the writer accepted, rejected, or clarified, and obtain confirmation before a substantial rewrite. Preserve the premise, evidence constraints, and the writer's accepted judgment. After substantive revisions, rerun Slopless and reopen watched Roughdraft for final review.

## Critique independently

For `critique`, do not rerun the complete creation workflow. Read the draft, `PREMISE.md` when available, and [references/critique.md](references/critique.md). Return the diagnosis and prioritized sequence first.

When the user approves Roughdraft annotation, add at most one document-level diagnosis and five high-value CriticMarkup comments or suggestions by default. Do not duplicate Slopless findings. Open the annotated draft in Roughdraft and use the same explicit handoff instructions.

## Report the completed handoff

Use short paragraphs, not a long checklist. Include the selected premise, paths to `PREMISE.md` and the draft, relevant context files used, evidence still requiring verification, and Roughdraft status.

Name Slopless transparently. When it found issues, use real numbers:

> **Slopless:** It flagged [initial count] issues across [rule-type count] patterns. I revised the draft, ran Slopless [run count] times in total, and it now passes clean. The main improvements were [up to three grouped outcomes].

If the first run was clean, say so without implying revisions. If deliberate exceptions remain, report their real number and explain why. Never output a long list of individual edits unless asked.

## Keep beta boundaries

- Produce article-oriented long-form writing, not homepage, email, social, or generic copy modes.
- Create evidence specifications, not media, unless explicitly requested.
- Diagnose critique before rewriting.
- Require confirmation before applying substantial feedback-driven revisions.
- Do not create accounts, telemetry, cloud services, billing, dashboards, custom lint rules, or a proprietary document format.
