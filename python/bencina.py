"""Cheapest fuel in a Chilean comuna via the Better Llama MCP server (data: CNE).

Usage: python bencina.py [fuel] [comuna]
       python bencina.py 93 Ñuñoa
Fuel codes: 93, 95, 97, DI (diesel), KE, GLP, GNC
"""
import sys

from mcp_http import MCPClient, tool_json

fuel = sys.argv[1] if len(sys.argv) > 1 else "93"
comuna = sys.argv[2] if len(sys.argv) > 2 else "Ñuñoa"

client = MCPClient()
client.initialize()

data = tool_json(client.call_tool("find_chile_fuel_prices", {
    "output": "precios",
    "fuels": [fuel],
    "comunas": [comuna],
    "sortBy": "precio",
    "maxItems": 5,
}))

print(f"Top {data['count']} cheapest '{fuel}' in {comuna}:")
for row in data["results"]:
    print(f"  ${row['price']:,} {row['unit']}  {row['brand']:<10} {row['address']} "
          f"({row['serviceType']}, updated {row['priceUpdatedAt'][:10]})")
print(f"\n{data.get('attribution', '')}")
