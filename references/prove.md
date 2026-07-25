# Prove Claims

## Purpose

Turn consequential claims into a premise-governed research plan, test them against the strongest available evidence and counterevidence, and decide what the article may responsibly claim. Truth constrains persuasion: narrow, qualify, or remove a claim when evidence cannot carry it.

## Required inputs

- The initial working outline and selected route.
- Writer-owned and discovered evidence with provenance and confidence.
- The premise, objection response, and explicit truth boundaries.

## Process

Build the compact claim ledger below inside the outline. Set the proof burden before searching, research adversarially, grade the evidence, validate quantitative material, and revise structure whenever findings change what the article may responsibly claim. Read [evidence-design.md](evidence-design.md) for the shared evidence-quality contract.

## User checkpoint

For an unsupported central claim, offer **Add my evidence**, **Research the gaps**, or **Narrow or remove the claim**. For only non-central gaps, replace the third option with **Keep explicit placeholders**. Require an explicit choice and repeat while any central gap remains.

## Artifact or state effects

Write the compact claim ledger, accepted placeholders, and accepted visual briefs into the canonical working outline. Create no separate proof artifact in this release.

## Degraded and failure behavior

Ask before materially expanding into connected private sources. If proof remains unavailable, narrow or remove the claim rather than manufacturing support. Never allow a central unsupported claim to pass as a placeholder.

## Completion criterion

Every central claim is supported, honestly narrowed, or removed; each remaining non-central gap is explicit and writer-accepted.

## Next-stage handoff

After claim and section jobs are stable, read [informational-images.md](informational-images.md) and privately test Legitimacy and Numbers opportunities. Preserve only earned visual briefs, then read [visual-placeholders.md](visual-placeholders.md) for production or fallback handling. Use its dedicated visual subagent when available without blocking main-thread outline work. Return the corrected outline, proof state, and strongest visible-proof assignment to [outline.md](outline.md) for structural review and approval.

In the guided workflow, run this stage after the initial working outline and before outline review. The selected route and outline establish what the article intends to say; proof development determines what it may say credibly. Add a compact claim ledger to the same outline, then revise the structure when evidence narrows, contradicts, or removes a planned claim.

Use this evidence order:

1. User-owned evidence: analytics, telemetry, customer calls, support tickets, CRM notes, internal documents, email, Slack, Drive, GitHub, and case studies.
2. First-party public evidence: documentation, changelogs, filings, official benchmarks, product pages, and primary research.
3. Independent evidence: credible studies, reporting, reviews, analysts, and expert commentary.
4. Ask the user when essential evidence is private, missing, or ambiguous.

Before searching, label each claim's argumentative role and proof burden: what a skeptical reader would need to see, what would falsify or materially weaken it, and how central it is to the premise. Search for disconfirmation, competing explanations, base rates, and credible contrary examples as deliberately as confirming evidence. Do not treat search-result repetition as independent corroboration.

For each claim record the source, a usable URL or file path plus section or location, published or accessed date when relevant, evidence type, what it supports, confidence, limitations, contradictions, strongest supported wording, and status. Separate verified fact, source-backed interpretation, inference, and uncertainty. Prefer original or first-party records for facts, independent sources for external validation, and transparent reasoning for synthesis. Never invent statistics, quotations, customer outcomes, benchmarks, events, or causal relationships.

For quantitative evidence, verify definitions, unit and grain, denominator, time period, sample, missingness, comparison baseline, calculation, and whether selection or survivorship bias could change the conclusion. Distinguish correlation, contribution, and causation. Preserve important uncertainty in the planned wording rather than hiding it in a source note.

For a normal guided article, keep the plan compact:

```markdown
## Claim ledger

- **Claim:** [Consequential assertion]
  - **Role and burden:** [Why it matters and what a skeptic would need]
  - **Evidence:** [Verified source, URL or file path + locator, relevant date, type, and what it supports]
  - **Counterevidence or limits:** [Contradiction, competing explanation, uncertainty, or none found]
  - **Strongest supported wording:** [Exact defensible claim]
  - **Status:** [Supported, writer input, researchable, narrow, or remove]
  - **Visible proof:** [Accepted visual brief or none]
```

Attach any proof visual to the claim it advances rather than creating a freestanding decorative evidence section. A verified finding may later support a stronger headline during critique, but do not recraft the headline automatically here. Stop before outline approval when a central claim remains unsupported. Preserve non-central gaps as explicit placeholders when the writer chooses to proceed.

When invoked on a complete article, return a compact claim-to-evidence map before editing. Ask approval before conducting expansive connected-source research or changing a central claim beyond the user's stated intent.
