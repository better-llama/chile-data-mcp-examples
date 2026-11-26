// Use the official MCP TypeScript/JavaScript SDK (streamable HTTP transport) against Better Llama.
// Needs `npm install` (like vercel_ai_sdk.mjs); the other examples have no dependencies.
// Usage: npm install && node agent_mcp_sdk.mjs
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const URL_MCP = new URL("https://mcp.betterllama.com/mcp");

const client = new Client({ name: "chile-data-mcp-examples-node", version: "0.1.0" });
await client.connect(new StreamableHTTPClientTransport(URL_MCP));
const server = client.getServerVersion();
console.log(`Connected to ${server.name} ${server.version}`);

const { tools } = await client.listTools();
console.log(`${tools.length} tools: ${tools.map((t) => t.name).join(", ")}\n`);

// 1) Let the server suggest the right tool for a task (what an agent would do).
const found = await client.callTool({ name: "search_tools", arguments: { query: "valor UF" } });
console.log("search_tools('valor UF') ->", found.content[0].text.slice(0, 300), "...\n");

// 2) Call it: today's UF from the CMF.
const result = await client.callTool({
  name: "get_chile_financial_indicators",
  arguments: { source: "uf", period: "current" },
});
const data = JSON.parse(result.content[0].text);
for (const row of data.results) console.log(`${row.indicatorName}: ${row.value} ${row.unit} (${row.date})`);
console.log(data.attribution);

await client.close();
