// Chile holidays, business days and RUT via the Better Llama MCP server (tool: chile_calendar_and_rut).
// Computed by the server from Chilean holiday laws; no key, no personal data.
//
// Usage: node calendario_rut.mjs                       # holidays left this year
//        node calendario_rut.mjs plazo 2026-12-15 10    # add 10 business days
//        node calendario_rut.mjs rut 12.345.678-5 11.111.111-2   # validate RUTs
import { MCPClient, toolJson } from "./mcp_http.mjs";

const [cmd = "feriados", ...rest] = process.argv.slice(2);
const today = new Date().toLocaleDateString("en-CA", { timeZone: "America/Santiago" });

let args;
if (cmd === "feriados") args = { operation: "feriados", years: [today.slice(0, 4)], fromDate: today, toDate: `${today.slice(0, 4)}-12-31` };
else if (cmd === "plazo") args = { operation: "sumar_dias_habiles", startDate: rest[0], businessDays: Number(rest[1]) };
else if (cmd === "rut") args = { operation: "validar_rut", ruts: rest };
else {
  console.error("Usage: node calendario_rut.mjs [feriados | plazo <date> <n> | rut <rut>...]");
  process.exit(1);
}

const client = new MCPClient();
await client.initialize();
const data = toolJson(await client.callTool("chile_calendar_and_rut", args));
if (typeof data === "string") throw new Error(data);

for (const r of data.results ?? []) {
  if (cmd === "feriados") {
    const flag = r.irrenunciable ? " (irrenunciable)" : "";
    const scope = r.scope === "nacional" ? "" : ` [${r.scope}]`;
    console.log(`${r.date} ${r.weekday.padEnd(9)} ${r.name}${flag}${scope}`);
  } else if (cmd === "plazo") {
    console.log(`${r.startDate} + ${r.businessDays} días hábiles = ${r.resultDate} (${r.resultWeekday})`);
    if (r.note) console.log(`  ${r.note}`);
  } else if (r.valid) {
    console.log(`${r.input.padEnd(14)} válido   ${r.formatted}`);
  } else {
    console.log(`${r.input.padEnd(14)} inválido ${r.error ?? ""} (DV esperado ${r.expectedDv ?? "?"})`);
  }
}
console.log(`\n${data.attribution ?? ""}`);
