import { createHash, randomUUID } from 'node:crypto';
import { mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { z } from 'zod';

export const kindSchema = z.enum(['premise', 'outline', 'article']);
export type Kind = z.infer<typeof kindSchema>;
export const documentSchema = z.object({
  documentId: z.string().uuid(), revision: z.string(),
  premise: z.string(), outline: z.string(), article: z.string(),
  outlineApproved: z.boolean(),
});
export type Document = z.infer<typeof documentSchema>;
const files = { premise: 'PREMISE.md', outline: 'outline.md', article: 'article.md' };
const hash = (value: string) => createHash('sha256').update(value).digest('hex');

// Deliberately single-process. All read/check/write operations are synchronous.
// Only the three Markdown files hold article decisions. Approval is conservative:
// it is invalidated on outline/premise edits and forgotten on process restart.
export class DocumentStore {
  private approvals = new Map<string, string>();
  constructor(private root = resolve(process.env.REMARKABLE_WORKSPACE ?? './workspace')) {}
  private directory(id: string) { return resolve(this.root, z.string().uuid().parse(id)); }
  create(title: string): Document {
    const id = randomUUID();
    mkdirSync(this.directory(id), { recursive: true });
    for (const kind of kindSchema.options) writeFileSync(resolve(this.directory(id), files[kind]), kind === 'article' ? `# ${title.replace(/[\r\n]/g, ' ')}\n\n` : '', 'utf8');
    return this.get(id);
  }
  get(id: string): Document {
    let content: Record<Kind, string>;
    try { content = Object.fromEntries(kindSchema.options.map(kind => [kind, readFileSync(resolve(this.directory(id), files[kind]), 'utf8')])) as Record<Kind, string>; }
    catch { throw new Error('Document not found. Open an existing document ID or create one.'); }
    const revision = hash(JSON.stringify(content));
    return { documentId: id, revision, ...content, outlineApproved: this.approvals.get(id) === hash(content.premise + '\0' + content.outline) };
  }
  save(id: string, expectedRevision: string, kind: Kind, markdown: string, actor: 'human' | 'model'): Document {
    const current = this.get(id);
    if (current.revision !== expectedRevision) throw new Error('Conflict: document changed. Read the latest revision and reconcile your edits; do not overwrite blindly.');
    if (actor === 'model' && kind === 'article' && !current.outlineApproved) throw new Error('The writer must approve the current outline in the editor before model drafting.');
    if (markdown.length > 200_000) throw new Error('Document exceeds the 200,000 character prototype limit.');
    const file = resolve(this.directory(id), files[kind]);
    const temp = file + '.tmp';
    writeFileSync(temp, markdown, 'utf8'); renameSync(temp, file);
    if (kind !== 'article' && current[kind] !== markdown) this.approvals.delete(id);
    return this.get(id);
  }
  approve(id: string, expectedRevision: string): Document {
    const doc = this.get(id);
    if (doc.revision !== expectedRevision) throw new Error('Conflict: reload and review the current outline before approving.');
    if (!doc.premise.trim() || !doc.outline.trim()) throw new Error('A selected premise and working outline are required before approval.');
    if (/^\s*(?:[-*]\s*)?Blocking\s*:/im.test(doc.outline)) throw new Error('Resolve Blocking: entries in the outline before approval.');
    this.approvals.set(id, hash(doc.premise + '\0' + doc.outline));
    return this.get(id);
  }
}
