// Mastra + Better Llama MCP: Chile, Colombia, Peru and Mexico public data as Mastra tools.
// 1) Connects with MCPClient (@mastra/mcp, Streamable HTTP) and lists the 15 tools.
// 2) Calls real tools directly, without an LLM: UF and dollar (CMF) and Colombia's TRM.
// 3) If OPENAI_API_KEY is set, builds a Mastra Agent (@mastra/core) with the MCP tools and asks a question.
//    Without a key, `--mock` checks the same Agent wiring with the AI SDK's mock model (real tool call, no LLM).
// Requires Node.js 22.13+ (@mastra/core engine requirement).
// Usage (from node/):
//   npm install
//   node mastra_agent.mjs
//   node mastra_agent.mjs --mock
//   OPENAI_API_KEY=... node mastra_agent.mjs "¿Cuánto vale la UF hoy y cuál es la TRM en Colombia?"
//   OPENAI_API_KEY=... LLM_MODEL=openai/gpt-4.1 node mastra_agent.mjs "..."
import { MCPClient } from "@mastra/mcp";
import { Agent } from "@mastra/core/agent";

const MCP = "https://mcp.betterllama.com/mcp";
const args = process.argv.slice(2);
const mock = args.includes("--mock");
const prompt = args.filter((a) => a !== "--mock").join(" ") || "¿Cuánto vale la UF hoy y cuál es la TRM en Colombia?";

// The MCP tools return JSON as text content: parse it.
const toolJson = (result) => JSON.parse(result.content.find((c) => c.type === "text").text);

// Server key "betterllama" -> tools are namespaced as betterllama_<tool>.
const mcp = new MCPClient({ servers: { betterllama: { url: new URL(MCP) } } });
try {
  // 1) All server tools as Mastra tools (schemas come from the server).
  const tools = await mcp.listTools();
  const names = Object.keys(tools);
  console.log(`${names.length} tools: ${names.join(", ")}\n`);

  // 2) Direct calls (no LLM): each tool has an execute(input, context) like any Mastra tool.
  console.log("CMF Chile (get_chile_financial_indicators):");
  let data;
  for (const source of ["uf", "dolar"]) {
    data = toolJson(await tools.betterllama_get_chile_financial_indicators.execute({ source, period: "current" }, {}));
    for (const row of data.results ?? []) {
      console.log(`  ${row.indicatorName}: ${row.value.toLocaleString("es-CL")} ${row.unit} (${row.date})`);
    }
  }
  console.log(`  ${data.attribution ?? ""}`);

  data = toolJson(await tools.betterllama_colombia_trm.execute({}, {}));
  const t = data.latest ?? {};
  console.log("\nColombia - TRM (colombia_trm):");
  console.log(`  ${Number(t.value_cop_per_usd).toLocaleString("es-CO")} ${t.unit ?? "COP per USD"}, ${t.date_from} .. ${t.date_to}`);
  console.log(`  ${data.attribution ?? ""}\n`);

  // 3) A Mastra Agent with the MCP tools.
  let model;
  if (process.env.OPENAI_API_KEY) {
    model = process.env.LLM_MODEL ?? "openai/gpt-4.1-mini"; // Mastra model router: "provider/model"
  } else if (mock) {
    model = await mockModel();
  } else {
    console.log("Set OPENAI_API_KEY to run the Mastra Agent with the tools (or --mock to check the wiring without an LLM).");
  }
  if (model) {
    const agent = new Agent({
      id: "chile-data-agent",
      name: "Chile data agent",
      instructions: "Answer with official public data from Chile, Colombia, Peru and Mexico. Use the tools; cite the source and date.",
      model,
      tools,
    });
    const result = await agent.generate(prompt, { maxSteps: 5 });
    for (const step of result.steps ?? []) {
      for (const call of step.toolCalls ?? []) {
        const c = call.payload ?? call;
        console.log(`tool call: ${c.toolName}(${JSON.stringify(c.args ?? c.input)})`);
      }
      for (const r of step.toolResults ?? []) {
        const o = r.payload ?? r;
        console.log(`tool result: ${JSON.stringify(o.result ?? o.output).slice(0, 200)}...`);
      }
    }
    console.log(`\nAnswer: ${result.text}`);
  }
} finally {
  await mcp.disconnect();
}

// Mock model from 'ai/test': step 1 asks for get_chile_financial_indicators (executed for real
// against the MCP by the Agent), step 2 answers with the value it got back. Only to check the wiring.
async function mockModel() {
  const { MockLanguageModelV4 } = await import("ai/test");
  const usage = { inputTokens: { total: 0, noCache: 0, cacheRead: 0, cacheWrite: 0 }, outputTokens: { total: 0, text: 0, reasoning: 0 } };
  let step = 0;
  return new MockLanguageModelV4({
    doGenerate: async ({ prompt: messages }) => {
      step += 1;
      if (step === 1) {
        return {
          content: [{ type: "tool-call", toolCallId: "call_1", toolName: "betterllama_get_chile_financial_indicators", input: JSON.stringify({ source: "uf", period: "current" }) }],
          finishReason: { unified: "tool-calls", raw: "tool_calls" }, usage, warnings: [],
        };
      }
      const toolMsg = messages.findLast((m) => m.role === "tool");
      const out = toolMsg.content[0].output; // { type: "json", value: { content: [{ text: "<JSON>" }] } }
      const uf = JSON.parse(out.value.content.find((c) => c.text).text).results?.[0];
      return {
        content: [{ type: "text", text: `(mock) UF ${uf?.value} CLP al ${uf?.date}.` }],
        finishReason: { unified: "stop", raw: "stop" }, usage, warnings: [],
      };
    },
  });
}
