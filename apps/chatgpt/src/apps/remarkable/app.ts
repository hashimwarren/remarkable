import { Editor } from '@tiptap/core';
import StarterKit from '@tiptap/starter-kit';
import { Markdown } from '@tiptap/markdown';
import { createAppClient, element, status } from '../shared/client';
import type { Document, Kind } from '../../mastra/mcp/document-store';

let current: Document | undefined;
let kind: Kind = 'article';
let dirty = false;
let setting = false;
let polling = false;
let stopping = false;
const source = element<HTMLTextAreaElement>('source');
const mode = element<HTMLSelectElement>('mode');
// The rich schema is deliberately small. Never silently round-trip unsupported syntax.
const needsSource = (text: string) => /<!--|^\s*\||!\[|^\s*\[[^\]]+\]:|^\s*[-*]\s+\[[ xX]\]|<\/?[A-Za-z]|^---\s*$/m.test(text);
const editor = new Editor({
  element: element('editor'), extensions: [StarterKit.configure({ link: { openOnClick: false } }), Markdown],
  content: '', contentType: 'markdown',
  editorProps: { attributes: { role: 'textbox', 'aria-label': 'Article editor', 'aria-multiline': 'true' } },
  onUpdate: () => { if (!setting) { dirty = true; status('Unsaved edits.'); } },
});
source.oninput = () => { dirty = true; status('Unsaved edits.'); };
const markdown = () => mode.value === 'source' ? source.value : editor.getMarkdown();
function displayMarkdown(value: string) {
  setting = true;
  source.value = value;
  if (needsSource(value)) mode.value = 'source';
  if (mode.value === 'rich') editor.commands.setContent(value, { contentType: 'markdown', emitUpdate: false });
  source.hidden = mode.value !== 'source'; element('editor').hidden = mode.value !== 'rich';
  setting = false;
}
function render(data: Document) {
  if (!data?.documentId || typeof data.article !== 'string') return;
  if (dirty && current && (data.documentId !== current.documentId || data.revision !== current.revision)) {
    status('A newer version is available. Your unsaved edits are preserved. Copy them before reloading; saving will report a conflict.', true); return;
  }
  const replace = !current || data.documentId !== current.documentId || data.revision !== current.revision;
  current = data;
  element<HTMLInputElement>('document-id').value = data.documentId;
  element('approval').textContent = data.outlineApproved ? 'Outline approved' : 'Outline needs approval';
  if (replace) { dirty = false; displayMarkdown(data[kind]); }
  document.querySelectorAll<HTMLButtonElement>('[data-kind]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.kind === kind)));
}
const client = createAppClient<Document>('Remarkable editor', render);
async function save() {
  if (!current) throw new Error('Open a document first.');
  if (!dirty) return;
  const data = await client.call('save_document', { documentId: current.documentId, expectedRevision: current.revision, kind, markdown: markdown() });
  dirty = false; render(data); status('Saved.');
}
element('save').onclick = () => client.run(save);
document.querySelectorAll<HTMLButtonElement>('[data-kind]').forEach(button => {
  button.onclick = () => {
    if (dirty) { status('Save your edits before switching files.', true); return; }
    kind = button.dataset.kind as Kind;
    if (current) { displayMarkdown(current[kind]); render(current); }
  };
});
mode.onchange = () => {
  const previous = mode.value === 'source' ? (dirty ? editor.getMarkdown() : current?.[kind] ?? '') : source.value;
  if (mode.value === 'rich' && needsSource(previous)) {
    mode.value = 'source'; status('Use Markdown source to preserve this document’s syntax.', true); return;
  }
  displayMarkdown(previous);
};
element('reload').onclick = () => client.run(async () => {
  if (!current) return;
  // Explicit reload is the only UI action allowed to discard unsaved text.
  const latest = await client.call('get_document', { documentId: current.documentId });
  dirty = false; current = undefined; render(latest); status('Loaded saved version.');
});
element('open').onclick = () => client.run(async () => {
  if (dirty) throw new Error('Save your edits before opening another document.');
  const documentId = element<HTMLInputElement>('document-id').value.trim();
  if (!documentId) throw new Error('Enter a document ID.');
  render(await client.call('open_document', { documentId }));
});
element('new').onclick = () => client.run(async () => {
  if (dirty) throw new Error('Save your edits before creating another document.');
  render(await client.call('open_document', { title: 'Untitled article' }));
});
element('approve').onclick = () => client.run(async () => {
  if (!current || kind !== 'outline') throw new Error('Open and review the Outline tab before approving.');
  await save();
  render(await client.call('approve_outline', { documentId: current.documentId, expectedRevision: current.revision }));
  status('Current outline approved. You can ask Remarkable to draft.');
});
element('ask').onclick = () => client.run(async () => {
  await save(); if (!current) return;
  const stage = element<HTMLSelectElement>('stage').value;
  const selection = mode.value === 'source' ? source.value.slice(source.selectionStart, source.selectionEnd)
    : editor.state.doc.textBetween(editor.state.selection.from, editor.state.selection.to, '\n');
  const prompt = `Use Remarkable (${stage}) for document ${current.documentId}. Read get_writing_guide and get_document first. Follow the user checkpoints. Preserve my edits and use update_document for the working files. Do not invent evidence or say that unavailable review or lint tools ran.`;
  const context = { documentId: current.documentId, revision: current.revision, file: kind, outlineApproved: current.outlineApproved, selectedText: selection.slice(0, 4000) };
  element<HTMLTextAreaElement>('copy-message').value = `${prompt}\n\n${JSON.stringify(context)}`;
  try { await client.share(prompt, context); element('fallback').hidden = true; }
  catch (error) { element('fallback').hidden = false; (element('fallback') as HTMLDetailsElement).open = true; throw error; }
});
async function start() {
await client.connect();
// Do not create on connect: inline tool results can arrive after initialization.
// A sidebar without a result offers explicit New/Open controls instead.
if (!current) status('Choose New to start writing, or open a document ID.');
const timer = setInterval(async () => {
  if (stopping || polling || client.busy || !current || document.hidden) return;
  polling = true;
  const before = current;
  try {
    const latest = await client.call('get_document', { documentId: before.documentId });
    if (!client.busy && current.documentId === before.documentId && current.revision === before.revision) render(latest);
  }
  catch (error) { status(String(error), true); }
  finally { polling = false; }
}, 1500);
window.addEventListener('pagehide', () => { stopping = true; clearInterval(timer); editor.destroy(); });
}
void start();
