"""Colombia's official exchange rate (TRM, COP/USD) via the Better Llama MCP server.

Data: Superintendencia Financiera de Colombia via datos.gov.co (dataset 32sa-8pi3),
no key needed. License CC BY-SA 4.0.

Usage: python trm_colombia.py                                  # latest TRM
       python trm_colombia.py --date 2026-11-15                # TRM in force that day
       python trm_colombia.py --from 2026-11-10 --to 2026-11-20

A weekend/holiday TRM is certified on the previous business day and stays in
force for several days: each row has date_from and date_to (validity range).
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

client = MCPClient()
client.initialize()
data = tool_json(client.call_tool("colombia_trm", arguments))

latest = data.get("latest") or {}
if latest:
    print(f"TRM Colombia ({latest.get('unit', 'COP por 1 USD')})")
    print(f"  Latest: {latest['value_cop_per_usd']:,.2f} in force {latest['date_from']} .. {latest['date_to']}")
if data.get("count", 0) > 1:
    for r in data["results"]:
        print(f"    {r['date_from']} .. {r['date_to']}  {r['value_cop_per_usd']:,.2f}")

for w in data.get("warnings", []):
    print(f"\nNote: {w}")
print(f"\nSource updated at: {data.get('sourceUpdatedAt', '')}")
print(f"\n{data.get('attribution', '')}")
