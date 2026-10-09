import assert from 'node:assert/strict';
import { Client, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';

const base = process.env.MASTRA_BASE_URL ?? 'http://localhost:4111';
const client = new Client({ name: 'remarkable-smoke', version: '0.1.0' }, {
  versionNegotiation: { mode: { pin: '2026-07-28' } },
});
try {
  await client.connect(new StreamableHTTPClientTransport(new URL('/api/mcp/remarkable/mcp', base)));
  const { tools } = await client.listTools();
  const open = tools.find(tool => tool.name === 'open_document');
  assert.ok(open);
  const uri = open._meta.ui.resourceUri;
  const resource = await client.readResource({ uri });
  assert.match(resource.contents[0].text, /Approve outline/);
  const guide = await client.callTool({ name: 'get_writing_guide', arguments: {} });
  assert.notEqual(guide.isError, true);
  assert.match(JSON.stringify(guide), /governing premise/);
  console.log('Production endpoint, editor HTML, and Remarkable instructions verified.');
} finally { await client.close(); }
