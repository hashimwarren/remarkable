# Premise Generation

## Purpose

Establish the governing persuasive idea—not a topic, thesis label, or headline—and let the writer choose among three strategically different directions.

## Required inputs

- The writer's audience, desired change in perception, and present stakes.
- Relevant project context and evidence boundaries.
- The private candidate pool produced by [premise-transformation.md](premise-transformation.md).

## Process

If the writer has not answered in substance, ask exactly:

> Who’s this for? What should they see differently—and why does that matter now?

Extract the reader, desired perception change, and why that change matters now. Use context to sharpen rather than replace the answer. Ask at most one follow-up, only when a conflict or omission would materially change the options.

Read [premise-transformation.md](premise-transformation.md), run its private council or fallback, and receive the complete candidate pool. Generate exactly three finalists that ask the reader to make different realizations, care for different reasons, or respond to different consequences. Reject lexical variants of the same idea.

Use the public presentation and audit below. Keep appeals, Fascinate methodology, audience provenance, scoring, and scout assignments private unless the writer asks how the options were developed.

## User checkpoint

Ask the writer which premise should govern the article. Accept A, B, C, `Go wider`, a bolder request, or a combination. Use structured input when available with compact A/B/C labels and the same plain-text fallback. Never choose for the writer or infer approval.

## Artifact or state effects

This stage owns the canonical schema below but does not write it yet. Hold the selected audience, current belief, desired movement, premise, likely objection, and why-now context as transient state until objection pressure-testing and Personal Authority complete. Then [personal-authority.md](personal-authority.md) performs the single atomic create or update at the project root using only this schema:

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

Append only the approved Personal Authority shape from [personal-authority.md](personal-authority.md). Do not store appeals, Fascinate metadata, response direction, argument, proof plan, evidence list, headline, opening, CTA, or polished prose. Do not overwrite a file belonging to another article without permission.

## Degraded and failure behavior

When subagents cannot run, use the single-context fallback in `premise-transformation.md` and disclose it briefly. Limited concurrency is not unavailability. Never fabricate scout participation, evidence, audience research, or approval.

## Completion criterion

One governing premise is explicitly selected and its newly derived strongest candidate intelligent objection is ready for pressure-testing. A widened, intensified, combined, or materially qualified premise resets this criterion.

## Next-stage handoff

Pass the confirmed premise, likely objection, audience fields, why-now context, and the unwritten canonical schema to [objection-response.md](objection-response.md). Do not skip pressure-testing or write the durable artifact before the objection and optional story decisions are complete.

## Return exactly three options

State the shared understanding once before the options:

```markdown
**Reader:** [Concise audience interpretation]
**What they should see differently:** [Desired belief shift]
**Why now:** [Why that belief shift matters now]

I’m going to show you three genuinely different ways this article could move the reader. Each premise combines the central claim with a different persuasive approach. Focus on which realization feels most important and generative—the headline is only an illustration.
```

Do not repeat the shared reader, belief shift, or why-now context inside every option. Assign the options the letters `A`, `B`, and `C`, keeping the letter attached to the direction name.

Use this compact structure:

```markdown
## [A, B, or C]. [Distinctive direction name]

**Premise**
[One concise governing persuasive idea with the selected appeal and fascination posture already integrated.]

**Likely objection**
[The strongest intelligent resistance this premise must answer, qualify, or accommodate.]

**Possible headline**
[One illustrative headline.]
```

Do not add `Reader realization`, `Why it matters now`, `Persuasive angle`, or `Why it works` fields. Keep each option easy to compare. Establish the premise before writing the headline; never substitute three headline variants for three premises.

After option C, ask exactly:

> **Which premise should govern the article: A, B, or C? If none feels strong enough, say “Go wider.” You can also ask for one to be bolder or combine two.**

## Audit distinctness and objections

Before presenting the options:

- Confirm that each option uses a genuinely different persuasive strategy, not lexical variation.
- Give every option a substantive, reader-specific likely objection. Represent the strongest intelligent response, not a straw man or generic writing risk.
- Use the objection to expose what the eventual argument must answer, qualify, or accommodate and what proof burden it creates.
- Privately audit the actual appeal and posture for overclaiming, excessive alarm, weak evidence, audience mismatch, unfair blame, false reassurance, unsupported threat amplification, scapegoating, or distorted praise. Do not expose that machinery as option metadata.
- Reject or revise any option whose central claim cannot be responsibly supported from supplied or obtainable context.
- Keep all three options truthful, fair, audience-relevant, and faithful to the user's stated realization and urgency.
