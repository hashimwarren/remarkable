# Visual Placeholders

Use visual placeholders in the working outline to reduce copy density and begin the article's visual plan. These are concepts, not evidence and not finished editorial art.

## Choose useful placements

Create a header-image concept immediately after the working headline. Then evaluate the outline for up to two additional placements: a proof visual beside a claim, and a comprehension or story visual where a scene, process, comparison, or interface would become easier to understand or remember.

The header is standard. The other two are opportunities, not a quota. Omit a placement that would be merely decorative. Under each visual, add one short italic sentence stating its rhetorical job and suggesting the finished form.

## Delegate image creation

When subagents and the Codex image-generation model are available, spawn one dedicated visual subagent. Give it bounded briefs containing the premise and relevant section, the visual's single job, intended form and aspect ratio, truth boundaries, low-fidelity requirement, and project-relative output path under `drafts/assets/<article-stem>/`.

Continue useful outline work while the visual subagent runs. It creates assets only and must not change the premise, claims, evidence, outline structure, captions, or final placement. The main agent verifies and integrates its output.

If subagents are unavailable, generate the concepts in the main context when an image model is available. If image generation is unavailable, search the public web for neutral placeholder imagery appropriate to the requested format. Preserve source attribution and disclose the fallback briefly. Do not block outline review indefinitely; insert a clearly labeled textual placeholder if the outline is ready first.

## Truth and accessibility

- Never generate exact statistics, quotations, real interface states, identifiable people, or documentary scenes as factual records.
- A chart-shaped placeholder must not contain invented values.
- Use relative Markdown paths so Roughdraft can render local assets.
- Provide concise alt text that labels the image as a concept.
- Preserve an italic production note beneath every placeholder.
