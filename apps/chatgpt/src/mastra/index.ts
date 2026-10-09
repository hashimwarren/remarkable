import { Mastra } from '@mastra/core/mastra';
import { remarkableServer, remarkableTools } from './mcp/remarkable';

// The host supplies the writing model, as in the workshop. No second model bill,
// unrestricted shell agent, scheduler, or filesystem tool is exposed here.
export const mastra = new Mastra({ tools: remarkableTools, mcpServers: { remarkable: remarkableServer } });
