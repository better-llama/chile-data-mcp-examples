// Chile economic indicators via the Better Llama MCP server.
// - CMF: current UF, dollar (dólar observado), UTM
// - Banco Central (BDE): latest TPM and IMACEC
// Usage: node indicadores.mjs
import { MCPClient, toolJson } from "./mcp_http.mjs";

const client = new MCPClient();
await client.initialize();

console.log("CMF Chile (get_chile_financial_indicators):");
let data;
for (const source of ["uf", "dolar", "utm"]) {
  data = toolJson(await client.callTool("get_chile_financial_indicators", { source, period: "current" }));
  for (const row of data.results ?? []) {
    console.log(`  ${row.indicatorName}: ${row.value.toLocaleString("es-CL")} ${row.unit} (${row.date})`);
  }
}
console.log(`  ${data.attribution ?? ""}`);

console.log("\nBanco Central de Chile (get_chile_central_bank_series):");
data = toolJson(await client.callTool("get_chile_central_bank_series", {
  operation: "series",
  indicators: ["tpm", "imacec"],
  latestOnly: true,
  // Monthly series (IMACEC) are published with a lag: look back far enough.
  firstDate: "2026-01-01",
}));
for (const row of data.results ?? []) {
  console.log(`  ${row.title}: ${row.value.toFixed(2)} (${row.date})`);
}
console.log(`  ${data.attribution ?? ""}`);
