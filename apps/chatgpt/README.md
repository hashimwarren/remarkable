# Remarkable in ChatGPT — working prototype

This adapts Mastra’s October 8, 2026 MCP Apps workshop into a writing workspace. ChatGPT is the writing agent. Mastra exposes the document tools and serves a Tiptap editor through an MCP App. No model API key is needed for this path.

## Run

Requires Node 22.13+ and npm. From this directory:

```sh
npm ci
npm run preview
```

Open http://127.0.0.1:4173. This is a local test host using the **real HTTP MCP server and official AppBridge**. It is not ChatGPT and does not run an LLM. Its “Simulate chat agent update” button exercises an external tool update without forwarding a new result into the iframe; the editor discovers it by polling.

For the actual Mastra server:

```sh
npm run dev
```

MCP endpoint: `http://localhost:4111/api/mcp/remarkable/mcp`. Production build: `npm run build`, then `npm run start`.

Connect the endpoint using an MCP Apps-capable host. For ChatGPT, follow the current [connect-and-test guide](https://developers.openai.com/plugins/deploy/connect-chatgpt). The server advertises `global` and `thread` entrypoints. Placement and extension availability are host-controlled. A remote ChatGPT host needs reachable HTTPS; **do not tunnel this unauthenticated prototype onto the public Internet with real writing**. Authentication, ownership authorization, and shared transactional storage are prerequisites for a real remote deployment. Live ChatGPT installation is a separate acceptance test, not implied by the local preview.

Try in a connected host:

> Use Remarkable to develop an article. Open its editor, read the writing guide, and start by helping me choose a premise.

Keep the document ID to reopen a workspace. The editor can open it directly. The server saves only `PREMISE.md`, `outline.md`, and `article.md` under `workspace/<id>/`. Set `REMARKABLE_WORKSPACE` to choose a persistent volume. This prototype assumes one trusted writer and one server process.

## Why Tiptap, and where Roughdraft fits

| Option | Fit for this prototype | Tradeoff |
| --- | --- | --- |
| Tiptap directly | Chosen. Browser editor bundled into the workshop’s self-contained HTML resource; small adapter owns host calls. | We own save/conflict UX. Basic rich text only; unsupported Markdown remains in source mode. |
| Embed the whole Roughdraft application | Not chosen for the first working slice. Its local CLI/Express server, filesystem review lifecycle, and application UI require a hosted adapter and path/ownership redesign. | Better existing review/comment UX, more integration work and a larger surface. |
| Keep Roughdraft as a local review companion | Compatible with the canonical Markdown files. | Its CLI and watched review flow are not executed by this prototype. |

Roughdraft already uses Tiptap internally (`@roughdraft/app` declares Tiptap 3.x), so these are not competing editor engines. The distinction is embedding an editor component versus porting an entire review application. No Roughdraft code was copied.

## Communication and workflow

1. ChatGPT calls `get_writing_guide` for the current checked-out Remarkable instructions and stage references.
2. `open_document` returns structured document state and the editor resource URI. The host renders the resource.
3. ChatGPT reads `get_document`, then writes one Markdown file through `update_document` with its expected revision.
4. The human edits through `save_document`. The app calls tools through the host bridge, never through a direct network request.
5. Clicking **Ask Remarkable in chat** saves first and sends document ID, revision, file, and optional selected text. Hosts without messaging get a copyable prompt.
6. The editor polls `get_document` for model edits. Unsaved human text is retained on conflicts; there is no blind overwrite.
7. The human reviews the Outline tab and clicks **Approve outline**. The model cannot write the article through its normal tool until that gate is satisfied. Any premise/outline edit invalidates approval. Restarting the server also requires approval again; the persisted Markdown remains.

The full Remarkable lifecycle is still guided by the skill: premise, objection, personal authority, framework, route, working outline, proof, approval, draft, hygiene, critique. Only revision checks and outline approval are enforced in code. Other checkpoints remain explicit conversation decisions. Approval state is in memory, not inferred from an `approved` string in model-authored Markdown. `outlineApproved` is the adapter’s authoritative outline-approval signal.

This prototype does **not** execute web research, Slopless, Roughdraft, subagents, or a second model. The guide adapter tells ChatGPT to report these limitations instead of pretending those steps passed. It does not add a proprietary document format or replace the original skill.

## Validation

```sh
npm run typecheck
npm test
npx playwright install chromium
npm run test:ui
npm run build
```

Tests cover the real HTTP MCP protocol, resource metadata and HTML, bundled instructions, stale saves, pre-approval drafting rejection, approval invalidation, persistence across store instances, sidebar startup, rich/source editing, messaging fallback, and unsaved-edit protection under incoming model changes.

## Reused source and provenance

Verified event code destination: https://github.com/mastra-ai/workshops/tree/main/examples/16-mcp-apps (the provided `https://luma.link/HWy7HA8hn2` redirected there). Snapshot: `c4a31a8c20471d0abaa34c7d6b8f3dd5f9caf193` for the repository tree; sample commit shown by GitHub: `5771b49ad9eb7569afed6a449ea912ac49201d02`. The recording redirect was not used to establish implementation details.

Reused/adapted workshop files:

- `src/apps/shared/client.ts`: official bridge initialization, structured-result parsing, themes, busy/error handling, messaging fallback.
- `scripts/build-apps.mjs`, `scripts/mcp-browser-shim.mjs`: bundled self-contained resources; added checked-out skill bundling.
- `tests/host/*`, `tests/helpers.ts`, `playwright.config.ts`: official AppBridge test host and actual HTTP MCP test client.
- Shared CSS and package/TypeScript configuration.
- Revision checks adapted from the tic-tac-toe example; sidebar metadata from product metrics.

The workshop package declares Apache-2.0. See [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md). The original Remarkable root files are unchanged.

Primary references:

- [Mastra workshop](https://mastra.ai/workshops/build-a-chatgpt-extension-with-mastra-2026-10-08)
- [Workshop source](https://github.com/mastra-ai/workshops/tree/main/examples/16-mcp-apps)
- [OpenAI extension metadata](https://developers.openai.com/plugins/build/extensions)
- [Tiptap Markdown API](https://tiptap.dev/docs/editor/markdown/getting-started/basic-usage)
- [Roughdraft source](https://github.com/Lex-Inc/roughdraft)

Before shipping: authenticated writer identity and per-document authorization, multi-instance compare-and-swap storage, durable approval auditing, sanitization/Markdown round-trip coverage for a broader schema, and real ChatGPT connection tests. Tool visibility is a host hint, not an authorization boundary; a raw MCP client can call app-only tools. Use this locally with trusted clients only.
