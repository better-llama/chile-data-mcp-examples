"""Peru public procurement (SEACE / OECE) via the Better Llama MCP server.

Data: OECE (ex OSCE) SEACE open data in OCDS format, from the Open Contracting
Partnership Data Registry (CC BY 4.0). Monthly snapshot: processes from the last
4-8 weeks are not there yet (see the coverage warning). Awarded suppliers are
companies only (RUC 20); natural persons are omitted. No key needed.

Usage: python seace_peru.py [query] [--region R] [--category bienes|servicios|obras]
                            [--method M] [--from YYYY-MM-DD] [--to YYYY-MM-DD]
                            [--min PEN] [--max N]
       python seace_peru.py computadoras --category bienes
       python seace_peru.py --category obras --region Cusco --min 1000000
       python seace_peru.py --method "Licitación Pública" --category obras --min 20000000 --from 2026-09-01
"""
import sys

from mcp_http import MCPClient, tool_json

FLAGS = {"--region": "region", "--category": "category", "--method": "method",
         "--from": "fromDate", "--to": "toDate", "--min": "minValue", "--max": "maxItems"}

args = sys.argv[1:]
arguments: dict = {"maxItems": 5}
for flag, key in FLAGS.items():
    if flag in args:
        i = args.index(flag)
        value = args[i + 1]
        arguments[key] = float(value) if key == "minValue" else int(value) if key == "maxItems" else value
        del args[i:i + 2]
if args:
    arguments["query"] = " ".join(args)
if len(arguments) == 1:  # no filters: a default example
    arguments["query"] = "computadoras"

client = MCPClient()
client.initialize()
data = tool_json(client.call_tool("peru_public_procurement_search", arguments))

filters = ", ".join(f"{k}={v}" for k, v in arguments.items() if k != "maxItems")
print(f"SEACE Peru ({filters}): {data['count']} shown, newest first")
for p in data["results"]:
    value = p.get("valorReferencial")
    value_txt = f"S/ {value:,.0f}" if value is not None else "no reference value"
    print(f"\n  {p['fechaPublicacion']}  {value_txt}  [{p['categoria']}] {p['metodo']}")
    print(f"  {p['entidad']} ({p['region']})  {p['nomenclatura'].strip()}")
    print(f"  {p['objeto'][:140]}")
    if p.get("adjudicatarios"):
        winners = ", ".join(f"{a['name']} (RUC {a['ruc']})" for a in p["adjudicatarios"])
        amount = p.get("montoAdjudicado")
        amount_txt = f"S/ {amount:,.0f}" if amount is not None else "-"
        print(f"  Bidders: {p.get('postores', '-')}  Awarded: {amount_txt}  to {winners}")

for w in data.get("warnings", []):
    print(f"\nNote: {w}")
print(f"\n{data.get('attribution', '')}")
print(f"Source: {data.get('source', '')} (updated {data.get('sourceUpdatedAt', '')})")
