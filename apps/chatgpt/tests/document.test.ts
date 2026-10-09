import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { DocumentStore } from '../src/mastra/mcp/document-store';
import { remarkableServer } from '../src/mastra/mcp/remarkable';
import { withMcpClient } from './helpers';

test('revision conflicts, explicit outline gate, invalidation, and restart behavior', () => {
  const directory = mkdtempSync(join(tmpdir(), 'remarkable-test-'));
  try {
    const store = new DocumentStore(directory);
    let doc = store.create('An article');
    const stale = doc.revision;
    doc = store.save(doc.documentId, doc.revision, 'premise', 'The writer selected this premise.', 'model');
    assert.throws(() => store.save(doc.documentId, stale, 'outline', 'stale write', 'model'), /Conflict/);
    assert.throws(() => store.save(doc.documentId, doc.revision, 'article', '# Generated prose', 'model'), /approve/);
    doc = store.save(doc.documentId, doc.revision, 'outline', '# Plan\n\nBlocking: missing proof', 'model');
    assert.throws(() => store.approve(doc.documentId, doc.revision), /Blocking/);
    doc = store.save(doc.documentId, doc.revision, 'outline', '# Plan\n\n- Establish the problem\n- Show evidence', 'model');
    assert.throws(() => store.approve(doc.documentId, stale), /Conflict/);
    doc = store.approve(doc.documentId, doc.revision);
    assert.equal(doc.outlineApproved, true);
    doc = store.save(doc.documentId, doc.revision, 'article', '# Draft\n\nA supported claim.', 'model');
    assert.equal(new DocumentStore(directory).get(doc.documentId).outlineApproved, false);
    doc = store.save(doc.documentId, doc.revision, 'premise', 'A different premise', 'human');
    assert.equal(doc.outlineApproved, false);
    assert.throws(() => store.get('../../etc/passwd'), /not found/);
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('actual MCP transport exposes the resource, guides, editor saves and model restrictions', async () => {
  await withMcpClient(remarkableServer, async client => {
    const listed = (await client.listTools()).tools;
    const tool = listed.find(tool => tool.name === 'open_document')!;
    assert.ok(tool);
    assert.deepEqual((tool._meta?.['openai/ui'] as { entrypoints: unknown[] }).entrypoints, [{ type: 'global' }, { type: 'thread' }]);
    const ui = tool._meta?.ui as { resourceUri: string };
    const resource = await client.readResource({ uri: ui.resourceUri });
    assert.ok('text' in resource.contents[0] && resource.contents[0].text.includes('Approve outline'));
    const guide = await client.callTool({ name: 'get_writing_guide', arguments: {} });
    assert.match(JSON.stringify(guide), /governing premise/);
    const badGuide = await client.callTool({ name: 'get_writing_guide', arguments: { file: '../../.env' } });
    assert.equal(badGuide.isError, true);
    const opened = await client.callTool({ name: 'open_document', arguments: { title: 'Transport test' } });
    const doc = opened.structuredContent as { documentId: string; revision: string };
    assert.ok(doc.documentId);
    const blocked = await client.callTool({ name: 'update_document', arguments: { ...doc, expectedRevision: doc.revision, kind: 'article', markdown: 'No approval' } });
    assert.equal(blocked.isError, true);
    const saved = await client.callTool({ name: 'save_document', arguments: { documentId: doc.documentId, expectedRevision: doc.revision, kind: 'article', markdown: '# Human edit' } });
    assert.notEqual(saved.isError, true);
    assert.equal((saved.structuredContent as { article: string }).article, '# Human edit');
    const conflict = await client.callTool({ name: 'save_document', arguments: { documentId: doc.documentId, expectedRevision: doc.revision, kind: 'article', markdown: 'Overwrite' } });
    assert.equal(conflict.isError, true);
  });
});
