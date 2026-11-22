"""Chile's official financial indicators (CMF) via the Better Llama MCP server.

Data: Comisión para el Mercado Financiero (CMF Chile), API CMF Bancos, no key
needed (the server uses its own key). Please cite the CMF when showing data.

Usage: python cmf_chile.py                                   # latest UF, dólar, euro, UTM
       python cmf_chile.py --indicator dolar --date 2026-11-20
       python cmf_chile.py --indicator uf --year 2026 --month 11
       python cmf_chile.py --indicator ipc --year 2026        # whole year
       python cmf_chile.py --tmc                              # tasa máxima convencional

Indicators: uf, dolar, euro, utm, ipc, tmc, tip. UF, dólar and euro have daily
values (--date); UTM, IPC, TMC and TIP are monthly (--year/--month).
"""
import sys

from mcp_http import MCPClient, tool_json

args = sys.argv[1:]
opts: dict = {}
for flag in ("--indicator", "--date", "--year", "--month"):
    if flag in args:
        i = args.index(flag)
        opts[flag] = args[i + 1]
        del args[i:i + 2]
if "--tmc" in args:
    opts["--indicator"] = "tmc"

arguments: dict = {"period": "current"}
if "--date" in opts:
    y, m, d = (int(x) for x in opts["--date"].split("-"))
    arguments = {"period": "date", "year": y, "month": m, "day": d}
elif "--month" in opts:
    arguments = {"period": "month", "year": int(opts["--year"]), "month": int(opts["--month"])}
elif "--year" in opts:
    arguments = {"period": "year", "year": int(opts["--year"]), "maxItems": 500}

indicators = [opts["--indicator"]] if "--indicator" in opts else ["uf", "dolar", "euro", "utm"]

client = MCPClient()
client.initialize()

data: dict = {}
for source in indicators:
    data = tool_json(client.call_tool("get_chile_financial_indicators", {"source": source, **arguments}))
    rows = data.get("results", [])
    if not rows:
        print(f"{source}: no data")
    elif source in ("tmc", "tip"):
        print(f"{rows[0]['indicatorName']} (% anual, vigente desde {rows[0]['date']})")
        for r in rows:
            label = " - ".join(x for x in (r.get("title"), r.get("subtitle")) if x)
            print(f"  {r['value']:>6.2f}%  [{r.get('typeCode', '')}] {label}")
    elif len(rows) == 1:
        r = rows[0]
        print(f"{r['indicatorName']}: {r['value']:,.2f} {r['unit']} ({r['date']})")
    else:
        print(f"{rows[0]['indicatorName']} ({rows[0]['unit']}, {len(rows)} values)")
        for r in rows:
            print(f"    {r['date']}  {r['value']:,.2f}")
    for w in data.get("warnings", []):
        print(f"  Note: {w}")

print(f"\n{data.get('attribution', '')}")
