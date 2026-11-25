// List the tools exposed by the Better Llama MCP server.
// Usage: node list_tools.mjs
import { MCPClient } from "./mcp_http.mjs";

const client = new MCPClient();
const info = await client.initialize();
console.log(`Server: ${info.serverInfo.name} ${info.serverInfo.version} (protocol ${info.protocolVersion})`);

const tools = await client.listTools();
console.log(`${tools.length} tools:\n`);
for (const t of tools) {
  console.log(`- ${t.name}: ${t.title ?? ""}`);
  console.log(`    args: ${Object.keys(t.inputSchema?.properties ?? {}).join(", ")}`);
}
