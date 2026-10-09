import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { build } from 'esbuild';
import { Client, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';
import { remarkableServer } from '../../src/mastra/mcp/remarkable';

const servers = new Map([[remarkableServer.id, remarkableServer]]);
const port = Number(process.env.PREVIEW_PORT ?? 4173);
const base = `http://127.0.0.1:${port}`;
const clients = new Map<string, Client>();
const script = (await build({ entryPoints: ['tests/host/host.ts'], bundle: true, write: false, format: 'esm', platform: 'browser', target: 'es2022' })).outputFiles[0].text;
const html = await readFile(new URL('./index.html', import.meta.url), 'utf8');

async function clientFor(id: string) {
  let client = clients.get(id);
  if (!client) {
    if (!servers.has(id)) throw new Error('Unknown server');
    client = new Client({ name: 'local-example-host', version: '1.0.0' }, { versionNegotiation: { mode: { pin: '2026-07-28' } } });
    await client.connect(new StreamableHTTPClientTransport(new URL(`/mcp/${id}`, base)));
    clients.set(id, client);
  }
  return client;
}

const http = createServer(async (req, res) => {
  try {
    const url = new URL(req.url ?? '/', base);
    // This is a local development harness, not an exposed production host.
    if (req.headers.host !== new URL(base).host || (req.headers.origin && req.headers.origin !== base)) {
      res.writeHead(403).end('Local requests only'); return;
    }
    if (url.pathname.startsWith('/mcp/')) {
      const server = servers.get(url.pathname.slice(5));
      if (!server) { res.writeHead(404).end(); return; }
      await server.startHTTP({ url, httpPath: url.pathname, req, res }); return;
    }
    if (url.pathname === '/') { res.setHeader('Content-Type', 'text/html'); res.end(html); return; }
    if (url.pathname === '/host.js') { res.setHeader('Content-Type', 'text/javascript'); res.end(script); return; }
    if (url.pathname === '/api/bootstrap') {
      const kind = url.searchParams.get('app') ?? 'remarkable';
      const id = 'remarkable';
      const name = 'open_document';
      const args = {};
      const client = await clientFor(id);
      const tools = (await client.listTools()).tools;
      const tool = tools.find(tool => tool.name === name)!;
      const ui = tool._meta?.ui as { resourceUri: string };
      const { contents } = await client.readResource({ uri: ui.resourceUri });
      const result = kind === 'sidebar' ? undefined : await client.callTool({ name, arguments: args });
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ id, tools, tool, args, result, html: 'text' in contents[0] ? contents[0].text : '' })); return;
    }
    if (url.pathname === '/api/call' && req.method === 'POST') {
      let body = '';
      for await (const chunk of req) {
        body += chunk;
        if (body.length > 65536) { res.writeHead(413).end(); return; }
      }
      const { id, name, args } = JSON.parse(body);
      const client = await clientFor(id);
      const result = await client.callTool({ name, arguments: args });
      res.setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(result)); return;
    }
    res.writeHead(404).end();
  } catch (error) {
    res.writeHead(500, { 'Content-Type': 'application/json' }); res.end(JSON.stringify({ error: String(error) }));
  }
});
http.listen(port, '127.0.0.1', () => console.log(`MCP Apps local test host: ${base}`));

async function shutdown() {
  for (const client of clients.values()) await client.close();
  for (const server of servers.values()) await server.close();
  http.closeAllConnections(); http.close();
}
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
