"""Chile earthquakes via the Better Llama MCP server (tool: get_chile_earthquakes).

Data: USGS Earthquake Hazards Program (ComCat, public domain), filtered to Chile
and its islands. Times are returned in UTC and in Chile time. No key needed.

Usage: python sismos.py                        # last 7 days, M>=2.5
       python sismos.py hoy                    # today (Chile date)
       python sismos.py fuertes                # M>=5 in the last 365 days, by magnitude
       python sismos.py cerca -33.45 -70.66 150   # within 150 km of a point (Santiago)
       python sismos.py tsunami                # tsunami-flagged events, last 10 years
       python sismos.py percibidos             # felt reports, last 7 days

Options: --min <magnitude>   minimum magnitude (default 2.5; fuertes uses 5)
         --islas             mainland Chile plus its islands (Easter Island, Juan Fernández)
         --max <n>           max rows (default 20)
"""
import datetime
import sys

from mcp_http import MCPClient, tool_json

args = sys.argv[1:]
opts: dict = {}
for flag in ("--min", "--max"):
    if flag in args:
        i = args.index(flag)
        opts[flag] = args[i + 1]
        del args[i:i + 2]
islas = "--islas" in args
if islas:
    args.remove("--islas")

cmd = args[0] if args else "semana"
rest = args[1:]
today = datetime.date.today()
iso = lambda d: d.isoformat()
min_mag = float(opts.get("--min", 5 if cmd == "fuertes" else 2.5))
arguments: dict = {"minMagnitude": min_mag, "maxItems": int(opts.get("--max", 20))}

if cmd == "semana":
    pass  # server default: last 7 days
elif cmd == "hoy":
    arguments.update(fromDate=iso(today), toDate=iso(today))
elif cmd == "fuertes":
    arguments.update(fromDate=iso(today - datetime.timedelta(days=365)), toDate=iso(today),
                     orderBy="magnitude")
elif cmd == "cerca":
    lat, lon = float(rest[0]), float(rest[1])
    radius = float(rest[2]) if len(rest) > 2 else 100
    arguments.update(region="radio", latitude=lat, longitude=lon, radiusKm=radius,
                     fromDate=iso(today - datetime.timedelta(days=30)), toDate=iso(today))
elif cmd == "tsunami":
    arguments.update(fromDate=iso(today - datetime.timedelta(days=3650)), toDate=iso(today),
                     tsunamiOnly=True)
    arguments.pop("minMagnitude")
elif cmd == "percibidos":
    arguments.update(fromDate=iso(today - datetime.timedelta(days=7)), toDate=iso(today),
                     feltOnly=True)
    arguments.pop("minMagnitude")
else:
    sys.exit(__doc__)
if islas and cmd != "cerca":
    arguments["region"] = "chile_islas"

client = MCPClient()
client.initialize()
data = tool_json(client.call_tool("get_chile_earthquakes", arguments))
if isinstance(data, str):  # validation error from the server
    sys.exit(data)

print(f"{data.get('count', 0)} sismos ({cmd}):")
for r in data.get("results", []):
    when = r["timeChile"][:16].replace("T", " ")
    extra = []
    if r.get("alertLevel"):
        extra.append(f"PAGER {r['alertLevel']}")
    if r.get("tsunamiFlag"):
        extra.append("tsunami flag")
    if r.get("feltReports"):
        extra.append(f"{r['feltReports']} reportes")
    tail = f"  [{', '.join(extra)}]" if extra else ""
    print(f"  {when} (Chile)  M{r['magnitude']:<4} {r['depthKm']:>5.0f} km  {r['place']}{tail}")

for w in data.get("warnings", []):
    print(f"Note: {w}")
if data.get("stopReason") not in (None, "completed", "noData"):
    print(f"stopReason: {data['stopReason']} (raise --max)")
print(f"\n{data.get('attribution', '')}")
