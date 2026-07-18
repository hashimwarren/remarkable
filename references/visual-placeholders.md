# Visual Placeholders

Begin visual planning in the article map, then turn the surviving positions into low-fidelity concepts in the working outline. These are concepts, not evidence and not finished editorial art.

## Reserve the positions in the article map

Create three planning positions:

1. **Header image:** express the article's central tension, promise, or emotional posture.
2. **Proof visual:** make the strongest suitable claim visible through a chart, screenshot, source excerpt, demonstration, quotation, or comparison.
3. **Comprehension or story visual:** reveal a framework, process, distinction, interface, or consequential personal scene.

Write a specific suggested form and one-sentence rhetorical job under each position. Move both in-article positions beside the claims or sections they would strengthen. The header is standard; the other two are opportunities, not a quota. Remove either in-article position when it would be decorative.

During proof development, refine the proof visual against verified evidence. A chart-shaped placeholder must contain no invented values. During framework design, let the framework's natural form inform the comprehension position.

## Choose useful placements

Carry the map's header-image concept immediately after the working headline. Then carry forward up to two additional placements: a proof visual beside a claim, and a comprehension or story visual where a scene, process, comparison, or interface would become easier to understand or remember.

Under each visual, add one short italic sentence stating its rhetorical job and suggesting the finished form. Re-evaluate rather than mechanically copying a position whose job disappeared while the map or proof changed.

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
