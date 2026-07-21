# Slopless Hygiene

## Purpose

Use Slopless as a deterministic prose-hygiene diagnostic while preserving the governing premise, factual meaning, project style, and useful rhetorical force.

## Required inputs

- The project root.
- The absolute path to the canonical English article for linting.
- The approved outline and discovered style constraints needed to judge findings in context.

## Process

Before substantive English drafting, run:

```bash
python3 <skill-directory>/scripts/run_slopless.py --preflight --project-root "$PWD"
```

The wrapper prefers an installed Slopless and otherwise acquires pinned `slopless@0.2.23` through `npx --yes` without modifying project dependencies. Continue drafting only when preflight reports `ready`.

After drafting, run:

```bash
python3 <skill-directory>/scripts/run_slopless.py <absolute-draft-path> --project-root "$PWD"
```

Record the initial finding count, rule-type count, rule IDs, and total lint runs. Consider every finding in context. Accept or rewrite it only when the change preserves the premise, calibrated certainty, applicable style guidance, and rhetorical force. Rerun until clean or only deliberate exceptions remain, then reread the article as an argument.

## User checkpoint

Slopless findings do not require a separate decision unless a proposed hygiene edit would materially alter meaning, certainty, voice constraints, or rhetorical force. Escalate that consequential choice to the writer instead of silently applying it.

## Artifact or state effects

Patch the canonical article Markdown. Keep the run metrics for the final handoff; do not create a lint report artifact or a second draft.

## Degraded and failure behavior

If preflight is blocked by Node.js, network, or execution permissions, stop before substantive English drafting and explain the blocker. Never silently produce an unlinted English article. Skip Slopless for a non-English article and state the language limitation. Preserve deliberate exceptions and report their actual count and reason.

## Completion criterion

Slopless completes on a clean result, a transparently reported set of deliberate exceptions, or an explained non-English skip.

## Next-stage handoff

Offer Remarkable critique after the first completed pass. After substantive accepted critique edits, rerun this stage before returning to review.

Report Slopless transparently in no more than three grouped improvement themes. When findings were fixed, use real numbers:

> **Slopless:** It flagged [initial count] issues across [rule-type count] patterns. I revised the draft, ran Slopless [run count] times in total, and it now passes clean. The main improvements were [up to three grouped outcomes].

If the first run was clean, say so without implying revisions. Do not recite a rule-by-rule changelog unless asked.
