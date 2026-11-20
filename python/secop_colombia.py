"""Colombia public procurement (SECOP II) via the Better Llama MCP server.

Data: Portal de Datos Abiertos datos.gov.co (SECOP II, CC BY-SA 4.0). No key needed.

Usage: python secop_colombia.py [query] [department] [min_value_cop] [dataset]
       python secop_colombia.py software Antioquia 100000000
       python secop_colombia.py interventoría Bogotá 0 procesos
dataset: contratos (signed contracts, default) | procesos (published processes)
"""
import sys

from mcp_http import MCPClient, tool_json

query = sys.argv[1] if len(sys.argv) > 1 else "software"
department = sys.argv[2] if len(sys.argv) > 2 else "Antioquia"
min_value = float(sys.argv[3]) if len(sys.argv) > 3 else 100_000_000
dataset = sys.argv[4] if len(sys.argv) > 4 else "contratos"

args = {"dataset": dataset, "query": query, "maxItems": 5}
if department:
    args["department"] = department
if min_value > 0:
    args["minValue"] = min_value

client = MCPClient()
client.initialize()
data = tool_json(client.call_tool("colombia_secop_search", args))

print(f"SECOP II {dataset}: '{query}' in {department or 'Colombia'} (>= COP {min_value:,.0f}), "
      f"{data['count']} shown, newest first:")
for row in data["results"]:
    ent = row.get("entidad", {})
    value = row.get("valor_contrato") or row.get("precio_base") or 0
    date = (row.get("fecha_firma") or row.get("fecha_publicacion") or "")[:10]
    print(f"\n  {date}  COP {value:,.0f}  [{row.get('estado', '')}]")
    city = f" ({ent['ciudad']})" if ent.get("ciudad") else ""
    print(f"  {ent.get('nombre', '')}{city}")
    print(f"  {(row.get('objeto') or row.get('nombre') or '')[:140]}")
    if prov := row.get("proveedor"):
        print(f"  Proveedor: {prov.get('nombre', '')} (NIT {prov.get('nit', '')})")
    print(f"  {row.get('url', '')}")

for w in data.get("warnings", []):
    print(f"\nNote: {w}")
print(f"\n{data.get('attribution', '')}")
