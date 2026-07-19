# Remarkable

Remarkable gives AI agents the architecture of persuasion.

Most AI writing tools start with prose. Remarkable starts with the decision that makes the prose matter: what should this reader see differently? It helps a writer choose a governing premise, pressure-test the objection, turn experience into authority, structure the argument, design the proof, and revise the finished article—without replacing the writer's voice or inventing evidence.

**Bring your own style. Remarkable strengthens the persuasion.**

## Install

```bash
npx skills add https://github.com/hashimwarren/remarkable --skill remarkable
```

Then start naturally:

```text
Use $remarkable to turn this idea into a persuasive article.
```

You can also focus the work with requests such as `$remarkable premise`, `$remarkable outline`, `$remarkable draft`, `$remarkable prove`, or `$remarkable critique`. Exact command syntax is not required.

## What it does

Remarkable guides an article through:

**Premise → Objection → Personal Authority → Framework → Map → Proof → Outline → Draft → Slopless → Critique**

Instead of polishing a generic claim such as “better prompts produce better AI writing,” Remarkable looks for a premise with consequence, such as:

> The people who get remarkable writing from AI are not necessarily better prompters; they know how to direct the editorial work that must happen before prose is polished.

The writer chooses the premise and approves consequential decisions. Remarkable keeps a durable `PREMISE.md`, treats truth as a constraint, and distinguishes verified evidence from claims that still need support.

## Runtime and optional tools

Remarkable is tested in Codex and includes metadata for ChatGPT, Codex, API, and Atlas runtimes. It requires Python 3 for its bundled helper scripts. English article drafting also requires Slopless: use Node.js 22.13 or newer and allow `npx` network access when no compatible local Slopless command is installed.

- **Slopless** handles deterministic prose hygiene and is required before Remarkable drafts English prose. Remarkable can run the pinned package with `npx` when no local command is installed.
- **Roughdraft** provides an optional inline-review surface. When it is unavailable, the complete workflow remains usable in chat and Markdown.
- **Subagents** improve premise exploration when the runtime supports them; a capacity-aware single-context fallback is included.

Roughdraft and subagents are optional integrations. Slopless is part of the English drafting workflow. Each external tool retains its own license.

## Documentation and feedback

The full workflow is in [SKILL.md](SKILL.md). Focused design references live in [references/](references/).

Trying the first public release? Add your experience to the [Remarkable 1.0 launch feedback thread](https://github.com/hashimwarren/remarkable/issues/31). For a separate report, [open a structured feedback or bug issue](https://github.com/hashimwarren/remarkable/issues/new/choose).

## License

[MIT](LICENSE)
