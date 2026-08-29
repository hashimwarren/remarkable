# Slopless Hygiene

## Purpose

Use one pinned Slopless ruleset as a deterministic prose-hygiene diagnostic while preserving the governing premise, factual meaning, approved rhetorical contract, project style, and useful rhetorical force. Slopless detects patterns; it does not determine editorial intent.

## Required inputs

- The project root.
- The absolute path to the canonical English article for linting.
- The approved outline, its rhetorical contract, and discovered style constraints needed to judge findings in context.

## Process

Before substantive English drafting, run:

```bash
python3 <skill-directory>/scripts/run_slopless.py --preflight --project-root "$PWD"
```

The wrapper uses an installed Slopless only after `--version` verifies exact version `0.2.36`; otherwise it acquires pinned `slopless@0.2.36` through `npx --yes` without modifying project dependencies. It never substitutes an unverified or mismatched installed ruleset. Continue drafting only when preflight reports `ready`.

After drafting, run:

```bash
python3 <skill-directory>/scripts/run_slopless.py <absolute-draft-path> --project-root "$PWD"
```

Record the initial finding count, rule-type count, rule IDs, and total lint runs. Read [rhetorical-contract.md](rhetorical-contract.md), then adjudicate every finding in context using this authority order:

1. Governing premise and argument
2. Factual meaning and calibrated certainty
3. Approved rhetorical contract and writer voice
4. Slopless finding

Before applying a rhetoric-sensitive finding, ask:

> Is this an empty instance of the pattern, or is it executing the approved rhetorical move?

Preserve deliberate anaphora when repeated openings create the intended momentum; remove accidental repetition elsewhere. Preserve antithesis when it clarifies the premise; remove decorative `not X, but Y` constructions. Preserve narrative tension when delayed resolution follows the approved question-and-reveal design; remove a generic tease that withholds no consequential answer. Preserve a maxim when it crystallizes an approved framework; remove it when it substitutes for proof. Preserve signposting when it performs an approved turn; remove generic announcements of importance.

Accept or rewrite a finding only when the change preserves the higher authorities. Rerun after edits until every finding is either addressed or deliberately preserved, then reread the article as an argument and run the rhetorical-contract integrity check.

## User checkpoint

Slopless findings do not require a separate decision unless a proposed hygiene edit would materially alter meaning, certainty, voice constraints, or an approved rhetorical direction. Escalate that consequential choice to the writer instead of silently applying it. Follow [rhetorical-contract.md](rhetorical-contract.md) when the proposed edit would change direction rather than strengthen execution.

## Artifact or state effects

Patch the canonical article Markdown. Keep the run metrics for the final handoff; do not create a lint report artifact or a second draft.

## Degraded and failure behavior

If preflight is blocked by Node.js, network, or execution permissions, stop before substantive English drafting and explain the blocker. Never silently produce an unlinted English article or fall back to an unverified Slopless version. Skip Slopless for a non-English article and state the language limitation. Preserve deliberate exceptions and report their actual count and reason.

## Completion criterion

Slopless completes when every finding has been considered and either addressed or deliberately preserved, or on an explained non-English skip. Zero findings are not required when a reported exception executes the approved rhetorical contract.

## Next-stage handoff

Offer Remarkable critique after the first completed pass. After substantive accepted critique edits, rerun this stage before returning to review.

Report Slopless transparently in no more than three grouped improvement themes. When findings were fixed, use real numbers:

> **Slopless:** It flagged [initial count] issues across [rule-type count] patterns. I revised the draft and ran Slopless [run count] times in total. Every finding is now adjudicated; [exception count] intentional pattern(s) remain because they execute the approved rhetorical contract. The main improvements were [up to three grouped outcomes].

When no exceptions remain, say it now passes clean. If the first run was clean, say so without implying revisions. Do not recite a rule-by-rule changelog unless asked.
