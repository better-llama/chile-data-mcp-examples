// Vercel AI SDK (AI SDK 7) + Better Llama MCP: Chile, Colombia, Peru and Mexico public data as AI SDK tools.
// 1) Connects with createMCPClient (@ai-sdk/mcp, Streamable HTTP transport) and lists the 15 tools.
// 2) Calls real tools directly, without an LLM: UF and dollar (CMF) and Colombia's TRM.
// 3) If OPENAI_API_KEY is set, runs generateText with the MCP tools so the model picks them.
//    Without a key, `--mock` checks the same wiring with the AI SDK's mock model (real tool call, no LLM).
// Usage (from node/):
//   npm install
//   node vercel_ai_sdk.mjs
//   node vercel_ai_sdk.mjs --mock
//   OPENAI_API_KEY=... node vercel_ai_sdk.mjs "¿Cuánto vale la UF hoy y cuál es la TRM en Colombia?"
//   OPENAI_API_KEY=... LLM_MODEL=gpt-4.1 node vercel_ai_sdk.mjs "..."
import { createMCPClient } from "@ai-sdk/mcp";
import { generateText, stepCountIs } from "ai";

const MCP = "https://mcp.betterllama.com/mcp";
const args = process.argv.slice(2);
const mock = args.includes("--mock");
const prompt = args.filter((a) => a !== "--mock").join(" ") || "¿Cuánto vale la UF hoy y cuál es la TRM en Colombia?";

// The MCP tools return JSON as text content: parse it.
const toolJson = (result) => JSON.parse(result.content.find((c) => c.type === "text").text);

const client = await createMCPClient({ transport: { type: "http", url: MCP } });
try {
  // 1) All server tools as AI SDK tools (schemas come from the server).
  const tools = await client.tools();
  const names = Object.keys(tools);
  console.log(`${names.length} tools: ${names.join(", ")}\n`);

  // 2) Direct calls (no LLM): each tool has an execute() like any AI SDK tool.
  const opts = { toolCallId: "direct", messages: [] };
  console.log("CMF Chile (get_chile_financial_indicators):");
  let data;
  for (const source of ["uf", "dolar"]) {
    data = toolJson(await tools.get_chile_financial_indicators.execute({ source, period: "current" }, opts));
    for (const row of data.results ?? []) {
      console.log(`  ${row.indicatorName}: ${row.value.toLocaleString("es-CL")} ${row.unit} (${row.date})`);
    }
  }
  console.log(`  ${data.attribution ?? ""}`);

  data = toolJson(await tools.colombia_trm.execute({}, opts));
  const t = data.latest ?? {};
  console.log("\nColombia - TRM (colombia_trm):");
  console.log(`  ${Number(t.value_cop_per_usd).toLocaleString("es-CO")} ${t.unit ?? "COP per USD"}, ${t.date_from} .. ${t.date_to}`);
  console.log(`  ${data.attribution ?? ""}\n`);

  // 3) generateText with the MCP tools.
  let model;
  if (process.env.OPENAI_API_KEY) {
    const { openai } = await import("@ai-sdk/openai");
    model = openai(process.env.LLM_MODEL ?? "gpt-4.1-mini");
  } else if (mock) {
    model = await mockModel();
  } else {
    console.log("Set OPENAI_API_KEY to run generateText with the tools (or --mock to check the wiring without an LLM).");
  }
  if (model) {
    const result = await generateText({ model, tools, prompt, stopWhen: stepCountIs(5) });
    for (const step of result.steps) {
      for (const call of step.toolCalls) console.log(`tool call: ${call.toolName}(${JSON.stringify(call.input)})`);
      for (const r of step.toolResults) console.log(`tool result: ${JSON.stringify(r.output).slice(0, 200)}...`);
    }
    console.log(`\nAnswer: ${result.text}`);
  }
} finally {
  await client.close();
}

// Mock model from 'ai/test': step 1 asks for get_chile_financial_indicators (executed for real
// against the MCP), step 2 answers with the value it got back. Only to check the wiring.
async function mockModel() {
  const { MockLanguageModelV4 } = await import("ai/test");
  const usage = { inputTokens: { total: 0, noCache: 0, cacheRead: 0, cacheWrite: 0 }, outputTokens: { total: 0, text: 0, reasoning: 0 } };
  let step = 0;
  return new MockLanguageModelV4({
    doGenerate: async ({ prompt: messages }) => {
      step += 1;
      if (step === 1) {
        return {
          content: [{ type: "tool-call", toolCallId: "call_1", toolName: "get_chile_financial_indicators", input: JSON.stringify({ source: "uf", period: "current" }) }],
          finishReason: { unified: "tool-calls", raw: "tool_calls" }, usage, warnings: [],
        };
      }
      const toolMsg = messages.findLast((m) => m.role === "tool");
      const out = toolMsg.content[0].output; // { type: "content", value: [{ type: "text", text: "<JSON>" }] }
      const uf = toolJson({ content: out.value }).results?.[0];
      return {
        content: [{ type: "text", text: `(mock) UF ${uf?.value} CLP al ${uf?.date}.` }],
        finishReason: { unified: "stop", raw: "stop" }, usage, warnings: [],
      };
    },
  });
}
