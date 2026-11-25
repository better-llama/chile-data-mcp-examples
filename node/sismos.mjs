// Chile earthquakes via the Better Llama MCP server (tool: get_chile_earthquakes).
// Data: USGS Earthquake Hazards Program (ComCat, public domain), filtered to Chile. No key.
//
// Usage: node sismos.mjs              # last 7 days, M>=2.5
//        node sismos.mjs hoy          # today (Chile date)
//        node sismos.mjs fuertes      # M>=5 in the last 365 days, by magnitude
//        node sismos.mjs cerca -33.45 -70.66 150   # within 150 km of a point (Santiago), last 30 days
import { MCPClient, toolJson } from "./mcp_http.mjs";

const [cmd = "semana", ...rest] = process.argv.slice(2);
// Chile date (YYYY-MM-DD), whatever the machine's time zone is.
const chileDate = (d) => d.toLocaleDateString("en-CA", { timeZone: "America/Santiago" });
const daysAgo = (n) => chileDate(new Date(Date.now() - n * 86_400_000));
const today = chileDate(new Date());

const args = { minMagnitude: cmd === "fuertes" ? 5 : 2.5, maxItems: 20 };
if (cmd === "hoy") Object.assign(args, { fromDate: today, toDate: today });
else if (cmd === "fuertes") Object.assign(args, { fromDate: daysAgo(365), toDate: today, orderBy: "magnitude" });
else if (cmd === "cerca") {
  const [lat, lon, km = "100"] = rest.map(Number);
  Object.assign(args, { region: "radio", latitude: lat, longitude: lon, radiusKm: Number(km),
    fromDate: daysAgo(30), toDate: today });
} else if (cmd !== "semana") {
  console.error("Usage: node sismos.mjs [semana | hoy | fuertes | cerca <lat> <lon> <km>]");
  process.exit(1);
}

const client = new MCPClient();
await client.initialize();
const data = toolJson(await client.callTool("get_chile_earthquakes", args));
if (typeof data === "string") throw new Error(data); // validation error from the server

console.log(`${data.count ?? 0} sismos (${cmd}):`);
for (const q of data.results ?? []) {
  const when = q.timeChile.slice(0, 16).replace("T", " ");
  const extra = [q.alertLevel && `PAGER ${q.alertLevel}`, q.tsunamiFlag && "tsunami flag"].filter(Boolean);
  console.log(`  M${q.magnitude.toFixed(1)}  ${when}  ${q.place}  ${Math.round(q.depthKm)} km` +
    (extra.length ? `  (${extra.join(", ")})` : ""));
}
for (const w of data.warnings ?? []) console.log(`  aviso: ${w}`);
console.log(`\n${data.attribution ?? ""}`);
