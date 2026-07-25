# Visual Placeholders

Begin visual planning in the working outline after the article route and major section jobs are stable. Read [informational-images.md](informational-images.md) first. These are accepted concepts and briefs, not proof by themselves and not finished editorial art.

## Reserve earned positions in the outline

Always create one editorial framing position:

1. **Header image:** deepen the headline's framing by expressing the article's central tension, promise, or emotional posture without merely restating it.

Add either in-article position only after the writer accepts the earned offer from `informational-images.md`:

- **Proof visual:** a Legitimacy or Numbers image that makes the strongest suitable verified claim inspectable.
- **Comprehension visual:** an Explanation or Steps image that reveals a framework, process, distinction, interface, or application.

Write a specific suggested form and one-sentence rhetorical job under each accepted position. Place it beside the claim or section it strengthens. The header is editorial framing, not automatically evidence. The other two are opportunities, not a quota; never create empty positions merely to remove them later.

During proof development, refine the proof visual against verified evidence and revise its placement when the argument changes. A chart-shaped placeholder must contain no invented values. During framework design, let the framework's natural form inform the comprehension position.

## Choose useful placements

Place the header-image concept immediately after the working headline. Add up to two accepted additional placements: a proof visual beside a claim, and a comprehension visual where a process, comparison, interface, or application becomes easier to understand or remember.

Under each visual, add one short italic sentence stating its rhetorical job and suggesting the finished form. Re-evaluate rather than mechanically preserving a position whose job disappeared during proof development.

When an approved practical framework belongs in the selected route, evaluate its natural diagram through the Explanation or Steps job. Use a system map, scorecard, progression, category map, or decision tree only when it reveals the framework's actual logic.

## Delegate image creation

Only after the writer chooses **Make this image** or otherwise explicitly requests production, use a dedicated visual subagent when subagents and the Codex image-generation model are available. Give it the compact accepted brief from `informational-images.md`, plus aspect ratio and low-fidelity requirement.

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
