// Latin American macro data via the Better Llama MCP server (no API keys needed).
// - Colombia: official exchange rate TRM (colombia_trm, Superfinanciera via datos.gov.co)
// - Peru: BCRP exchange rate and policy rate (peru_bcrp_series, BCRPData)
// - Mexico: Banxico FIX exchange rate, UDIS and target rate (mexico_banxico_indicators, Banxico SIE)
// Usage: node latam.mjs [co|pe|mx ...]      (default: all three)
import { MCPClient, toolJson } from "./mcp_http.mjs";

const wanted = new Set(process.argv.slice(2).map((a) => a.toLowerCase()));
const want = (c) => wanted.size === 0 || wanted.has(c);
const num = (v, d = 4) => Number(v).toLocaleString("en-US", { maximumFractionDigits: d });

const client = new MCPClient();
await client.initialize();

if (want("co")) {
  const data = toolJson(await client.callTool("colombia_trm", {}));
  const t = data.latest ?? {};
  console.log("Colombia - TRM (colombia_trm):");
  console.log(`  ${num(t.value_cop_per_usd, 2)} ${t.unit ?? "COP per USD"}, in force ${t.date_from} .. ${t.date_to}`);
  console.log(`  ${data.attribution ?? ""}`);
}

if (want("pe")) {
  const data = toolJson(await client.callTool("peru_bcrp_series", {
    series: ["tc_interbancario_venta", "tasa_referencia"],
    maxItems: 1,
  }));
  console.log("\nPeru - BCRP (peru_bcrp_series):");
  for (const s of data.results ?? []) {
    const l = s.latest ?? {};
    console.log(`  ${s.name}: ${num(l.value)} ${s.unit} (${l.date})`);
  }
  console.log(`  ${data.attribution ?? ""}`);
}

if (want("mx")) {
  const data = toolJson(await client.callTool("mexico_banxico_indicators", {
    indicators: ["fix", "udis", "tasa_objetivo"],
  }));
  console.log("\nMexico - Banxico (mexico_banxico_indicators):");
  for (const s of data.results ?? []) {
    const l = s.latest ?? {};
    console.log(`  ${s.name}: ${num(l.value, 6)} ${s.unit} (${l.date})`);
    if (s.published_ahead) {
      console.log(`    published ahead: ${num(s.published_ahead.value, 6)} for ${s.published_ahead.date}`);
    }
  }
  console.log(`  ${data.attribution ?? ""}`);
}
