"""Bank of Mexico (Banxico) indicators via the Better Llama MCP server.

Data: Banxico SIE API (banxico.org.mx/SieAPIRest). No key needed: the server uses
its own token; reuse allowed citing the source (Banxico usage policy).

Usage: python banxico_mexico.py                          # FIX exchange rate + UDIS + policy rate
       python banxico_mexico.py fix tiie_28 inflacion_anual
       python banxico_mexico.py fix --from 2026-11-01 --to 2026-11-20
       python banxico_mexico.py udis --date 2026-11-15

Indicators: fix, udis, tiie_28, tiie_91, tiie_182, tiie_fondeo, tasa_objetivo, inflacion_anual
"""
import sys

from mcp_http import MCPClient, tool_json

args = sys.argv[1:]
arguments: dict = {}
for flag, key in (("--from", "fromDate"), ("--to", "toDate"), ("--date", "date")):
    if flag in args:
        i = args.index(flag)
        arguments[key] = args[i + 1]
        del args[i:i + 2]
arguments["indicators"] = args or ["fix", "udis", "tasa_objetivo"]

client = MCPClient()
client.initialize()
data = tool_json(client.call_tool("mexico_banxico_indicators", arguments))

for s in data["results"]:
    latest = s.get("latest") or {}
    print(f"\n{s['name']} [{s['seriesId']}] ({s['frequency']}, {s['unit']})")
    if latest:
        print(f"  Latest: {latest['value']:,.6g} on {latest['date']}")
    ahead = s.get("published_ahead")
    if ahead:
        print(f"  Published ahead: {ahead['value']:,.6g} for {ahead['date']}")
    for p in s.get("points", []):
        print(f"    {p['date']}  {p['value']:,.6g}")

for w in data.get("warnings", []):
    print(f"\nNote: {w}")
print(f"\n{data.get('attribution', '')}")
