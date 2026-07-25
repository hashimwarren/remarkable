# Headline Design

## Purpose

Create a specific, defensible headline that earns attention by framing the article's real value. A headline is part of the argument: it should help the right reader recognize why the premise matters without promising more than the article proves.

## Required inputs

- The selected premise, reader, desired movement, and present stakes.
- At outline time: the chosen route, approved Personal Authority and framework when present, plus verified evidence already available.
- At critique time: the complete article and its final evidence boundary.
- In focused mode: enough article context to judge what the piece can honestly promise.

## Process

Generate candidates privately from the five sources below, discard unsupported or interchangeable options, and choose the strongest fit. Treat question, command, list, how-to, and contrarian constructions as formats rather than additional sources.

## User checkpoint

The automatic outline pass has no headline checkpoint. During critique, preserve a strong current headline and optionally offer **Explore alternative headlines**; when it is weak, present supported alternatives, recommend one, and wait for approval. A focused `headline` invocation presents alternatives and waits for a choice before changing the article.

## Artifact or state effects

Write the outline-stage selection as its working headline. A critique or focused-mode selection may replace the canonical article headline only with explicit approval. Create no headline artifact and do not retain the private candidate set.

## Degraded and failure behavior

Never invent a statistic, result, quotation, personal credential, or mechanism for a headline. When evidence cannot carry a candidate, narrow or discard it. Prefer an accurate concrete promise to empty cleverness, generic urgency, or clickbait.

## Completion criterion

The outline contains one defensible working headline, or the writer explicitly approves a critique/focused-mode replacement. The headline accurately frames the article's premise, useful consequence, and proof boundary.

## Next-stage handoff

At outline time, pass the selected working headline and its framing job to [outline.md](outline.md). At critique time, return the approved headline to [critique.md](critique.md). Focused mode ends after the approved article change unless the writer asks to continue.

## Use five sources

Privately create at least one viable candidate from every source the available material genuinely supports:

1. **Premise and tension:** foreground the problem, contradiction, or changed reality the article resolves.
2. **Personal discovery:** lead with the writer's relevant experience, change of mind, or earned lesson.
3. **Method or outcome:** foreground the practical framework, answer, or useful result.
4. **Proof or finding:** lead with a verified statistic, finding, comparison, or observable result and its consequence.
5. **Reader recognition:** name the reader's situation so precisely that the right person recognizes the article is for them.

Do not force all five when a source is absent. Proof-led candidates require verified evidence, and personal-discovery candidates require approved writer-owned material. Varying punctuation or format does not make two candidates meaningfully different.

## Run exactly two automatic passes

### Outline pass

During [outline.md](outline.md), generate the supported candidates privately and select one working headline. Explain none of this taxonomy to the writer and add no decision checkpoint. Let the headline and header-image concept divide the framing work: the image should deepen, concretize, or reframe the promise rather than restating the title.

### Critique pass

During [critique.md](critique.md), judge the current headline against the completed article, verified proof, and final reader movement.

- When it is already strong, preserve it. The critique may offer **Explore alternative headlines** as an optional continuation without manufacturing a problem.
- When it is weak, show up to five concise alternatives drawn from the supported sources, label the source in plain language, recommend one, explain why it better advances the premise, and wait for approval.

Do not run a separate automatic headline pass after proof. Evidence discovered there becomes available to the critique pass, where a genuinely strong statistic or finding may justify a proof-led replacement.

## Focused `headline` mode

Read the current article, `PREMISE.md`, outline, and verified evidence when available. Diagnose the existing headline first. If the writer asks for alternatives, present the strongest supported candidates across materially different sources, not five cosmetic rewrites. Recommend one, allow combination or revision, and change the article only after explicit approval.
