# Visual Placeholders

Use visual placeholders in the working outline to reduce copy density and begin the article's visual plan. These are concepts, not evidence and not finished editorial art.

## Choose useful placements

Create a header-image concept immediately after the working headline. Then evaluate the outline for up to two additional placements: a proof visual beside a claim, and a comprehension or story visual where a scene, process, comparison, or interface would become easier to understand or remember.

The header is standard. The other two are opportunities, not a quota. Omit a placement that would be merely decorative. Under each visual, add one short italic sentence stating its rhetorical job and suggesting the finished form.

When the article map contains an approved practical framework, evaluate its natural diagram as one of the two in-article opportunities. Use a system map, scorecard, progression, category map, or decision tree only when it reveals the framework's actual logic.

## Delegate image creation

When subagents and the Codex image-generation model are available, spawn one dedicated visual subagent. Give it bounded briefs containing the premise and relevant section, the visual's single job, intended form and aspect ratio, truth boundaries, and low-fidelity requirement.

Continue useful outline work while the visual subagent runs. It creates assets only and must not change the premise, claims, evidence, outline structure, captions, or final placement. Because image generation ends the worker's turn and does not accept a guaranteed project output path, assign one asset per turn. Reuse the same worker through follow-up tasks for later assets, or use multiple bounded visual workers when capacity permits.

The main agent collects each returned artifact and verifies it. Only insert a relative Markdown image path after confirming that the returned artifact exposes a usable local file or can be safely persisted under `drafts/assets/<article-stem>/`. If no local artifact is exposed, insert a clearly labeled textual placeholder and production note; never invent a path or imply that an image was saved.

If subagents are unavailable, generate the concepts in the main context when an image model is available. If image generation is unavailable, use a generic placeholder service or search the public web only for public-domain, Creative Commons, or otherwise reuse-permitted placeholder imagery. Record the source and license. Save it locally only when reuse permits; otherwise use a linked, attributed placeholder or a textual card. Attribution alone is not permission. Disclose the fallback briefly.

Do not block outline review indefinitely. If the outline is ready before an asset, insert a clearly labeled textual placeholder and production note, then integrate a verified local asset when it becomes available.

## Truth and accessibility

- Never generate exact statistics, quotations, real interface states, identifiable people, or documentary scenes as factual records.
- A chart-shaped placeholder must not contain invented values.
- Use relative Markdown paths so Roughdraft can render local assets.
- Provide concise alt text that labels the image as a concept.
- Preserve an italic production note beneath every placeholder.
