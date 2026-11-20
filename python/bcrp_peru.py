"""Peru central bank statistics (BCRP) via the Better Llama MCP server.

Data: BCRPData (estadisticas.bcrp.gob.pe), no key needed. Reproduction allowed
citing the source (BCRPData terms of use).

Usage: python bcrp_peru.py [series ...] [--points N]
       python bcrp_peru.py                                  # exchange rate + policy rate
       python bcrp_peru.py inflacion_12m tc_sbs_venta --points 6
       python bcrp_peru.py PD04638PD                        # any BCRP series code
       python bcrp_peru.py --catalog "tipo de cambio"       # list aliases
"""
import sys

from mcp_http import MCPClient, tool_json

args = sys.argv[1:]
client = MCPClient()
client.initialize()

if args and args[0] == "--catalog":
    query = " ".join(args[1:])
    data = tool_json(client.call_tool("peru_bcrp_series", {"operation": "catalogo", "query": query} if query else {"operation": "catalogo"}))
    print(f"BCRP catalog{f' ({query!r})' if query else ''}:")
    for row in data["results"]:
        print(f"  {row.get('alias', ''):<32} {row.get('code', ''):<11} {row.get('name', '')}")
    sys.exit(0)

points = 5
if "--points" in args:
    i = args.index("--points")
    points = int(args[i + 1])
    del args[i:i + 2]
series = args or ["tc_interbancario_venta", "tasa_referencia"]

data = tool_json(client.call_tool("peru_bcrp_series", {"series": series, "maxItems": points}))

for s in data["results"]:
    latest = s.get("latest") or {}
    print(f"\n{s['name']} [{s['code']}] ({s['frequency']}, {s['unit']})")
    print(f"  Latest: {latest.get('value', 0):,.4f} on {latest.get('date', '')}")
    for p in s["points"]:
        print(f"    {p['date']}  {p['value']:,.4f}")
    print(f"  {s['sourceUrl']}")

for w in data.get("warnings", []):
    print(f"\nNote: {w}")
print(f"\n{data.get('attribution', '')}")
