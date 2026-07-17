---
name: remarkable
description: Build persuasive long-form articles through premise discovery, opening design, claim-proof-consequence development, evidence validation, endings, critique, Slopless hygiene, and Roughdraft review. Use only when a human explicitly invokes Remarkable to create, develop, prove, finish, or critique an article while preserving existing voice and style guidance. Do not use for voice imitation, style-guide generation, general proofreading, or non-article copy formats.
---

# Remarkable

Give AI agents the architecture of persuasion. Style governs how writing sounds; Remarkable governs what the writing helps a reader believe, feel, and do.

Use this positioning: **Bring your own style. Remarkable strengthens the persuasion.** When comparing it with Impeccable, use: **Impeccable gives agents visual rhetoric. Remarkable gives agents verbal rhetoric.** Treat this release as `0.8-beta`.

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

> I’m sending the same brief to five independent premise scouts. Each will explore two appeals and several fascination triggers. I’ll compare their strongest ideas and show you only the three most promising and genuinely different directions.

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

For `Go wider`, discard the explored premise clusters and generate three directions with different core claims, causal explanations, and consequences. For `[letter], but bolder`, preserve the claim, appeal, fascination posture, and truth boundary while intensifying the premise through its fascination trigger. When the user combines options, synthesize one governing premise and confirm it before continuing.

### 3. Develop Personal Authority and preserve the premise

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

[When a personal story was approved, append the lean `## Personal Authority` structure defined in `references/personal-authority.md`. Omit the section entirely when the user skips.]
```

Do not expose internal appeal or fascination metadata in `PREMISE.md`. Do not put an argument, proof plan, evidence list, headline, opening, CTA, or polished draft prose in it. If the file belongs to another article, do not overwrite it without permission.

### 4. Create and open the article map

Create a collision-safe scaffold from the selected premise:

```bash
python3 <skill-directory>/scripts/create_article_map.py "<descriptive topic>" --root "$PWD"
```

Replace `pending` in `PREMISE.md` with the returned relative draft path. The map contains brief temporary guidance and one CriticMarkup question for each stage: opening, argument, visible evidence, ending, and CTA. Adapt the map to the premise: add or remove claim blocks, omit visible evidence when it adds no proof, and remove the CTA when none belongs.

Before opening it, explain the three interaction modes, then use the runtime's structured user-input control when available:

- **Open Roughdraft** — edit the map or answer inline, then click **Done Reviewing**.
- **Guide me** — answer one section question at a time in chat.
- **Draft it** — let Remarkable proceed from the available context.

When structured input is unavailable, ask for the same choice in plain text. STOP and wait for the user's selection before launching watched mode or drafting.

Only after the user selects **Open Roughdraft**, tell them that Remarkable will resume automatically after **Done Reviewing**, then open the map in watched mode. Do not use `--no-watch` for this handoff:

```bash
python3 <skill-directory>/scripts/open_roughdraft.py <absolute-draft-path> --project-root "$PWD"
```

Wait for the wrapper to report `review_completed`. Read all comments, suggestions, and replies from the same Markdown file. Treat closing or abandoning the review as different from clicking **Done Reviewing**; do not claim completion without the machine-readable completion signal.

If the user switches to **Guide me** or **Draft it** while watched mode is active, stop the watched process before continuing in chat. Do not leave an orphaned review command running.

### 5. Follow the chosen interaction mode

- **Roughdraft:** use the feedback returned by the watched session. Do not ask answered questions again.
- **Guide me:** if the user switches to chat, ask one stage question at a time in this order: opening, develop, prove, ending. Write each answer into the same draft before moving on.
- **Draft it:** if the user asks the agent to proceed, use the premise and available context to complete the map without additional interviewing. Preserve explicit evidence gaps.

The user can change modes at any time. Keep the Markdown draft as the source of truth across all modes. Remove temporary bracketed guidance, resolved scaffold questions, unused claim blocks, unused asset placeholders, and unnecessary CTA sections before linting.

### 6. Develop the article

Read [references/article.md](references/article.md), [references/opening.md](references/opening.md), [references/develop.md](references/develop.md), and [references/ending.md](references/ending.md). Default to 800–1,200 words, aiming for about 1,000, unless the user specifies otherwise.

Keep the premise alive from opening through ending. Build major movements through claim, proof, and consequence. Use evidence supplied by the user or relevant context; mark non-central gaps specifically and stop for central unsupported claims.

When evidence work is requested or necessary, read [references/prove.md](references/prove.md) and [references/evidence-design.md](references/evidence-design.md). Prefer user-owned evidence, then first-party public sources, then credible independent evidence. Ask before materially expanding research into connected private sources. Recommend visible proof only when it performs an evidentiary job.

### 7. Run Slopless

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

### 8. Return to Roughdraft

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
