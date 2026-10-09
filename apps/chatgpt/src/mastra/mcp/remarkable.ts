import { createTool } from '@mastra/core/tools';
import { MCPServer } from '@mastra/mcp';
import { z } from 'zod';
import html from './generated/remarkable';
import sources from './generated/skill';
import { DocumentStore, documentSchema, kindSchema } from './document-store';

const store = new DocumentStore();
const resourceUri = 'ui://remarkable/editor.html';
const idInput = z.object({ documentId: z.string().uuid() });
const revisionInput = idInput.extend({ expectedRevision: z.string() });
const saveInput = revisionInput.extend({ kind: kindSchema, markdown: z.string().max(200_000) });
const readHints = { readOnlyHint: true, openWorldHint: false, idempotentHint: true };
const writeHints = { readOnlyHint: false, destructiveHint: false, openWorldHint: false, idempotentHint: false };
const appMeta = { ui: { resourceUri, visibility: ['model', 'app'] }, 'openai/ui': { entrypoints: [{ type: 'global' }, { type: 'thread' }] } };

export const openDocument = createTool({
  id: 'open_document', description: 'Open the Remarkable editor for an existing document ID. With no ID, create a new article workspace. Preserve the returned ID for every subsequent call.',
  inputSchema: z.object({ documentId: z.string().uuid().optional(), title: z.string().min(1).max(200).default('Untitled article') }),
  outputSchema: documentSchema, mcp: { annotations: writeHints, _meta: appMeta },
  execute: async ({ documentId, title }) => documentId ? store.get(documentId) : store.create(title),
});
export const getDocument = createTool({
  id: 'get_document', description: 'Read authoritative Markdown and revision before editing. Includes premise, outline, article, and current human outline approval.',
  inputSchema: idInput, outputSchema: documentSchema,
  mcp: { annotations: readHints, _meta: { ui: { visibility: ['model', 'app'] } } },
  execute: async ({ documentId }) => store.get(documentId),
});
export const updateDocument = createTool({
  id: 'update_document', description: 'Save one canonical Remarkable Markdown file using the revision from get_document. Preserve writer edits. Article drafting requires human outline approval in the editor. Premise/outline changes revoke approval. On conflict, re-read and reconcile.',
  inputSchema: saveInput, outputSchema: documentSchema,
  mcp: { annotations: writeHints, _meta: { ui: { visibility: ['model'] } } },
  execute: async ({ documentId, expectedRevision, kind, markdown }) => store.save(documentId, expectedRevision, kind, markdown, 'model'),
});
export const saveDocument = createTool({
  id: 'save_document', description: 'Save a writer edit from the editor.', inputSchema: saveInput, outputSchema: documentSchema,
  mcp: { annotations: writeHints, _meta: { ui: { visibility: ['app'] } } },
  execute: async ({ documentId, expectedRevision, kind, markdown }) => store.save(documentId, expectedRevision, kind, markdown, 'human'),
});
export const approveOutline = createTool({
  id: 'approve_outline', description: 'Record the writer clicking Approve outline after reviewing the current premise and outline.',
  inputSchema: revisionInput, outputSchema: documentSchema,
  mcp: { annotations: writeHints, _meta: { ui: { visibility: ['app'] } } },
  execute: async ({ documentId, expectedRevision }) => store.approve(documentId, expectedRevision),
});
export const getWritingGuide = createTool({
  id: 'get_writing_guide', description: 'Read Remarkable SKILL.md first, then read the stage-owned reference files it names. All user checkpoints remain required; do not auto-run the whole lifecycle. Reads are restricted to bundled skill files.',
  inputSchema: z.object({ file: z.string().default('SKILL.md') }),
  outputSchema: z.object({ file: z.string(), markdown: z.string(), adapter: z.string() }),
  mcp: { annotations: readHints },
  execute: async ({ file }) => {
    if (!Object.hasOwn(sources, file)) throw new Error('Unknown guide file. Use SKILL.md or the exact references/*.md paths it names.');
    return { file, markdown: sources[file as keyof typeof sources], adapter: 'ChatGPT is the writing agent. Use get_document/update_document in place of filesystem edits, and the embedded editor for review. Do not claim local Roughdraft, research, Slopless, or subagents ran: this prototype does not execute those tools. Preserve every user checkpoint. A click on Approve outline supplies the outline approval gate only; premise, objection, story, framework, and route choices still require explicit conversation confirmation. Use Markdown source mode for tables, comments, or other syntax the rich editor cannot preserve.' };
  },
});
export const remarkableTools = { open_document: openDocument, get_document: getDocument, update_document: updateDocument, save_document: saveDocument, approve_outline: approveOutline, get_writing_guide: getWritingGuide };
export const remarkableServer = new MCPServer({
  id: 'remarkable', name: 'Remarkable writing editor', version: '0.1.0',
  instructions: 'When the writer invokes Remarkable, call get_writing_guide first and follow the skill. Open/reuse one document workspace. Read the current document before each update and preserve human edits. Never call app-only tools or infer approval from file text. The writer approves the outline in the editor. The existing editor polls for your updates. This is an unauthenticated single-writer local prototype; do not expose it publicly or claim a complete production integration.',
  tools: remarkableTools,
  appResources: { [resourceUri]: { name: 'Remarkable editor', html, meta: { prefersBorder: false, csp: { connectDomains: [], resourceDomains: [] } } } },
});
