# Validation — October 9, 2026

## Passed

- `npm run typecheck`: TypeScript compilation, including tests.
- `npm test`: 2 tests passed. Store checks cover stale writes, pre-approval drafting rejection, explicit approval, approval invalidation, Markdown persistence, restart behavior, and path rejection. HTTP MCP checks cover tool discovery, sidebar metadata, served editor HTML, bundled guides, unknown-guide rejection, writer save, and stale-save rejection.
- `npm run build`: production Mastra bundle and dependency packaging completed.
- Started `node .mastra/output/index.mjs` and ran `npm run test:smoke`: verified the production `/api/mcp/remarkable/mcp` endpoint, editor resource, and guide tool.
- Started the preview server and fetched normal and sidebar bootstraps: verified a real MCP-created document, embedded editor HTML, guide tool, and sidebar startup without an initial result.
- `git diff --check`.

No model API was invoked; no provider key or paid model service was configured.

## Not verified

- `npm run test:ui` reached the Playwright runner, but all three tests stopped before page launch because the Chromium executable was missing. `npx playwright install chromium` returned invalid/empty archives. An alternate packaged Chromium dependency was also denied by the environment. These are **not passing UI tests**. Run the included suite in an environment with Playwright Chromium installed.
- Live ChatGPT connection, sidebar/panel placement, and host-specific behavior have not been tested. Extension metadata is present; it is not proof that the app has been installed in ChatGPT.
- This is not a multi-user or publicly exposed service. App-only visibility is not authorization. The explicit approval gate protects the normal model-facing update tool, but a raw MCP client can invoke UI-only tools. Authentication and per-document permissions are required before remote use with real data.
- Slopless, Roughdraft, web research, and model-quality evaluations are not executed by this prototype.

## Source verification

- The event code redirect resolved in the browser to the Mastra workshop's `examples/16-mcp-apps` directory. The implementation reuses its shared client, resource build strategy, metadata, and test harness.
- Remarkable was inspected at `7ce13da449fa50c2afddab751ed7882e4a70498b`; its original files were not changed.
- Roughdraft's package and editor/server sources were inspected. Its application uses Tiptap and local filesystem/Express review infrastructure. No Roughdraft code was copied.
- The recording redirect led toward YouTube video `6IgoXPs0HZ4`, where human verification blocked playback. No conclusions rely on watching the recording.
