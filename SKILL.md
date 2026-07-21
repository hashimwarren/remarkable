---
name: remarkable
description: Build persuasive long-form articles through premise discovery, objection handling, Personal Authority, practical frameworks, article routes, evidence-strengthened outlines, drafting, Slopless hygiene, and rhetorical critique. Use only when a human explicitly invokes Remarkable to create, develop, prove, finish, or critique an article while preserving existing voice and style guidance. Do not use for voice imitation, style-guide generation, general proofreading, or non-article copy formats.
---

# Remarkable

Give AI agents the architecture of persuasion. Style governs how writing sounds; Remarkable governs what the writing helps a reader believe, feel, and do.

Use this positioning: **Bring your own style. Remarkable strengthens the persuasion.** When comparing it with Impeccable, use: **Impeccable gives agents visual rhetoric. Remarkable gives agents verbal rhetoric.** Treat this release as `1.2.1`.

## Preserve the product boundary

- Put persuasion before style. Do not invent a house voice, imitate a person, or create `VOICE.md` or `STYLE.md`.
- Treat truth as a constraint. Never invent evidence or preserve a strong claim beyond what its proof supports.
- Let the writer choose the governing premise and remain the final editor.
- Keep `PREMISE.md`, the working outline, and the article Markdown as the only durable stores of article decisions.
- Never write rhetoric to `DESIGN.md`. Propose durable `PRODUCT.md` changes and obtain approval before writing them.
- Let Slopless own deterministic prose hygiene and Roughdraft own local review UX.
- Do not make the writer learn commands or hidden rhetorical terminology before receiving value.

## Route the explicit invocation

Interpret natural phrasing and route to the smallest useful mode. A focused mode acts only on that stage unless the writer asks to continue.

- `start` or no mode: run the guided lifecycle below.
- `premise`: run premise generation or refinement through [references/premise.md](references/premise.md) and its private transformation stage.
- `outline`: select an article route when needed, build the working outline, strengthen proof, and obtain structural approval.
- `draft`: require an approved outline, draft the article, and run Slopless.
- `opening`: build or diagnose the reader contract with [references/opening.md](references/opening.md).
- `develop`: develop claims through proof and consequence with [references/develop.md](references/develop.md).
- `framework`: evaluate or develop an operational framework with [references/framework-design.md](references/framework-design.md).
- `prove`: map, research, validate, or design evidence with [references/prove.md](references/prove.md) and [references/evidence-design.md](references/evidence-design.md).
- `ending`: complete the premise and evaluate the CTA with [references/ending.md](references/ending.md).
- `critique`: diagnose a complete article and obtain revision authority with [references/critique.md](references/critique.md).

## Discover context progressively

Before premise generation, drafting, or critique, run:

```bash
python3 <skill-directory>/scripts/discover_context.py --root "$PWD"
```

Read returned files in priority order and stop when constraints are clear. Treat `PRODUCT.md` as enduring product and audience context, `DESIGN.md` as visual context, and `PREMISE.md` as the active rhetorical strategy. Track consequential context internally as `explicit`, `inferred`, or `uncertain`; do not ask the writer to restate known facts.

Read [references/context-artifacts.md](references/context-artifacts.md) before creating or changing any context artifact beyond `PREMISE.md`. Read [references/wayfinding.md](references/wayfinding.md) at the start of a guided workflow and apply it only at meaningful transitions.

## Run the guided lifecycle

Load only the current stage owner and any shared adapter it explicitly requires. Do not preload later stages. STOP at every owner-defined user checkpoint and never treat silence, file existence, a closed review window, or an ambiguous reply as approval.

1. **Premise.** Read [references/premise.md](references/premise.md) to elicit audience and desired perception, present three materially different governing premises, and obtain explicit selection. It loads [references/premise-transformation.md](references/premise-transformation.md) because the private council, audience fit, appeals, Fascinate controls, and distinctness tests belong there. Complete when one premise is explicitly selected and a fresh candidate intelligent objection is ready for pressure-testing.
2. **Objection.** After premise confirmation, read [references/objection-response.md](references/objection-response.md) to confirm the strongest intelligent objection and a compact response direction. Complete when both are confirmed and any resulting premise qualification is reconfirmed.
3. **Personal Authority.** Read [references/personal-authority.md](references/personal-authority.md) to discover, safely structure, and confirm a relevant writer-owned story—or record an explicit skip. Complete when the writer approves the factual story architecture or skips it and `PREMISE.md` reflects only approved material.
4. **Framework.** Read [references/framework-design.md](references/framework-design.md) to test whether the writer's advice benefits from an operational structure before route selection. Complete when a concrete framework is approved, the writer keeps the advice as prose, or no genuine opportunity exists.
5. **Article route.** Read [references/article-routes.md](references/article-routes.md) to infer awareness privately, advocate two distinct invisible architectures, and obtain a route choice. Read [references/narrative-tension.md](references/narrative-tension.md) only when shaping its question and resolution. Complete when one route is explicitly confirmed and a compact private route brief exists.
6. **Working outline.** Read [references/outline.md](references/outline.md) to reserve or reuse the article and outline paths, turn the route into a scan-friendly structure, and classify unresolved needs. Read [references/visual-placeholders.md](references/visual-placeholders.md) only when planning earned visual positions. Complete when the initial outline exists with `Status: working`; this is not approval.
7. **Proof.** Read [references/prove.md](references/prove.md) to build the claim-to-evidence plan inside the outline and resolve every central gap. Complete when every central claim is supported, honestly narrowed, or removed and remaining non-central gaps are explicit.
8. **Outline approval.** Return to [references/outline.md](references/outline.md) for evidence-strengthened structural review. Use [references/roughdraft-handoff.md](references/roughdraft-handoff.md) for the review lifecycle. Complete only when the writer explicitly approves, the outline says `Status: approved`, and no Blocking item remains.
9. **Draft.** Read [references/article.md](references/article.md) and its required [references/slopless.md](references/slopless.md) preflight adapter before prose. Turn the approved outline into the canonical article without leaking planning labels. Complete when the article preserves the governing premise, selected route, proof assignments, deliberate gaps, and truth boundary.
10. **Slopless.** After drafting, return to [references/slopless.md](references/slopless.md) for deterministic hygiene. Complete on a clean result, a transparently reported deliberate exception, or an explained non-English skip.
11. **Critique and review.** Read [references/critique.md](references/critique.md) to offer rhetorical critique, localize high-value interventions, and obtain revision authority. Use [references/roughdraft-handoff.md](references/roughdraft-handoff.md) for every watched review. Complete when accepted edits are applied, Slopless is rerun after substantive revision, and the writer receives the ready-state handoff.

## Resume from durable state

Inspect `PREMISE.md`, the working outline, and the article before choosing a stage. Resume at the earliest unmet observable completion condition. Reuse a valid reserved path and any confirmed writer-owned material from a legacy map, but never restart the retired map workflow. Never create parallel premise, route, story, framework, proof, outline, or prose artifacts merely to represent transient state.

## Report the completed handoff

Use short paragraphs. Include the selected premise; paths to `PREMISE.md`, the outline, and article as applicable; relevant context used; evidence still requiring verification; actual Slopless outcome; and Roughdraft status. Follow [references/slopless.md](references/slopless.md) for transparent lint reporting and [references/wayfinding.md](references/wayfinding.md) for the ready-state continuations.

## Keep release boundaries

- Produce article-oriented long-form writing, not homepage, email, social, or generic copy modes.
- Create evidence specifications, not production media, unless explicitly requested. Low-fidelity outline concepts and placeholders remain permitted.
- Diagnose critique before rewriting and require confirmation before substantial feedback-driven revisions.
- Do not create accounts, telemetry, cloud services, billing, dashboards, custom lint rules, or a proprietary document format.
