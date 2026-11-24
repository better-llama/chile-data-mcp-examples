"""Chile holidays, business days, communes and RUT validation via the Better Llama MCP server.

Tool: chile_calendar_and_rut (no key, computed by the server from Chilean holiday
laws and SUBDERE's official territorial codes; no external calls, no personal data).

Usage: python calendario_rut.py                              # remaining holidays this year
       python calendario_rut.py feriados 2027               # all 2027 holidays
       python calendario_rut.py es-feriado 2026-12-08 2026-12-09
       python calendario_rut.py plazo 2026-12-15 10         # add 10 business days
       python calendario_rut.py habiles 2026-12-01 2026-12-31
       python calendario_rut.py rut 12.345.678-5 11.111.111-2
       python calendario_rut.py dv 12345678                 # compute the check digit
       python calendario_rut.py comunas RM                  # communes (CUT codes) of a region

Options: --region <code|name> applies regional holidays (e.g. --region 16 for Ñuble);
         --comuna <name|CUT> applies communal holidays (Chillán, 20 Aug);
         --sabado counts Saturdays as business days (some legal deadlines).
"""
import datetime
import sys

from mcp_http import MCPClient, tool_json

args = sys.argv[1:]
extra: dict = {}
for flag, key in (("--region", "region"), ("--comuna", "comuna")):
    if flag in args:
        i = args.index(flag)
        extra[key] = args[i + 1]
        del args[i:i + 2]
if "--sabado" in args:
    args.remove("--sabado")
    extra["saturdayIsBusinessDay"] = True

cmd = args[0] if args else "feriados"
rest = args[1:]
today = datetime.date.today().isoformat()

if cmd == "feriados":
    if rest:
        arguments = {"operation": "feriados", "years": rest, "maxItems": 200}
    else:
        arguments = {"operation": "feriados", "years": [today[:4]],
                     "fromDate": today, "toDate": f"{today[:4]}-12-31"}
elif cmd == "es-feriado":
    arguments = {"operation": "es_feriado", "dates": rest or [today]}
elif cmd == "plazo":
    arguments = {"operation": "sumar_dias_habiles", "startDate": rest[0],
                 "businessDays": int(rest[1]) if len(rest) > 1 else 10}
elif cmd == "habiles":
    arguments = {"operation": "dias_habiles", "fromDate": rest[0], "toDate": rest[1]}
elif cmd in ("rut", "dv"):
    arguments = {"operation": "validar_rut", "ruts": rest, "rutBodyOnly": cmd == "dv"}
elif cmd == "comunas":
    arguments = {"operation": "comunas", "maxItems": 400}
    if rest:
        arguments["region"] = " ".join(rest)
else:
    sys.exit(__doc__)
arguments.update(extra)

client = MCPClient()
client.initialize()
data = tool_json(client.call_tool("chile_calendar_and_rut", arguments))
if isinstance(data, str):  # validation error from the server
    sys.exit(data)

for r in data.get("results", []):
    kind = r.get("kind")
    if kind == "feriado":
        flag = " (irrenunciable)" if r.get("irrenunciable") else ""
        scope = "" if r.get("scope") == "nacional" else f" [{r.get('scope')}]"
        print(f"{r['date']} {r['weekday']:<9} {r['name']}{flag}{scope}")
    elif kind == "fecha":
        state = "feriado: " + ", ".join(r["holidays"]) if r["isHoliday"] else (
            "fin de semana" if r["isWeekend"] else "día hábil")
        print(f"{r['date']} {r['weekday']:<9} {state}")
    elif kind == "sumar_dias_habiles":
        print(f"{r['startDate']} + {r['businessDays']} días hábiles = {r['resultDate']} ({r['resultWeekday']})")
        print(f"  {r.get('note', '')}")
    elif kind == "dias_habiles":
        print(f"{r['fromDate']} a {r['toDate']}: {r['businessDays']} días hábiles de {r['calendarDays']} "
              f"({r['weekendDays']} de fin de semana, {r['holidaysOnWorkdays']} feriados en día laboral)")
        for h in r.get("holidays", []):
            print(f"  {h}")
    elif kind == "rut":
        if r.get("valid"):
            print(f"{r['input']:<14} válido   {r['formatted']}")
        else:
            print(f"{r['input']:<14} inválido {r.get('error', '')} (DV esperado {r.get('expectedDv', '?')})")
    elif kind == "comuna":
        print(f"{r['code']}  {r['name']:<24} {r['provinceName']} / {r['regionName']}")
    else:
        print(r)

for w in data.get("warnings", []):
    print(f"Note: {w}")
if data.get("stopReason") not in (None, "completed"):
    print(f"stopReason: {data['stopReason']} (raise maxItems)")
print(f"\n{data.get('attribution', '')}")
