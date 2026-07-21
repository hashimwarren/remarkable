# Roughdraft Review Handoff

## Purpose

Use Roughdraft as the watched human review surface without making it a workflow dependency or treating an incomplete session as approval.

## Required inputs

- The absolute path to the canonical Markdown outline or article.
- The project root.
- A small set of consequential inline questions or CriticMarkup interventions, when the stage calls for them.
- The stage-specific decision that follows review.

## Process

Before launch, explain:

> Roughdraft is open for your review. You can edit the text directly, leave inline comments, or suggest changes. When you’re finished, click **Done Reviewing**; Remarkable will automatically resume here with your feedback.

Launch watched review mode:

```bash
python3 <skill-directory>/scripts/open_roughdraft.py <absolute-markdown-path> --project-root "$PWD"
```

Do not use `--no-watch` for a review handoff. Wait for the wrapper result, then reread the canonical Markdown before interpreting feedback.

## User checkpoint

Roughdraft review is input, not approval. After a completed review, present the checkpoint owned by the calling stage: outline approval, critique revision authority, or final-review continuation. Require an explicit decision there.

## Artifact or state effects

Roughdraft edits the canonical Markdown in place. It does not create a second article, a review artifact, or a durable approval record. Stage owners persist only their own approved state changes.

## Degraded and failure behavior

- `review_completed`: reread the Markdown, incorporate explicit feedback, and continue to the calling stage's checkpoint.
- `missing` or `unsupported`: say Roughdraft is unavailable, keep Markdown canonical, surface consequential questions in chat, and continue through the same checkpoint.
- `error`, `review_ended`, or `review_abandoned`: preserve the file, explain that no completed handoff arrived, and offer to retry or continue the same review in chat.

Never strand the article, imply approval, or discard feedback because Roughdraft is missing or fails. A closed window, timeout, or abandoned session is not `review_completed`.

## Completion criterion

The handoff completes only when the wrapper reports machine-readable `review_completed`, or the writer explicitly chooses the equivalent chat/Markdown fallback. Review completion alone never satisfies the calling stage's approval criterion.

## Next-stage handoff

Return the reviewed canonical Markdown, the actual wrapper status, and a compact summary of accepted, rejected, or clarified feedback to the calling stage. Let that stage present its own decision control.
