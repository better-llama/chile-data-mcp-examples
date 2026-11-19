"""Chile economic indicators via the Better Llama MCP server.

- CMF: current UF, dollar (dolar observado), UTM
- Banco Central (BDE): latest TPM and IMACEC

Usage: python indicadores.py
"""
from mcp_http import MCPClient, tool_json

client = MCPClient()
client.initialize()

print("CMF Chile (get_chile_financial_indicators):")
for source in ["uf", "dolar", "utm"]:
    data = tool_json(client.call_tool("get_chile_financial_indicators",
                                      {"source": source, "period": "current"}))
    for row in data.get("results", []):
        print(f"  {row['indicatorName']}: {row['value']:,} {row['unit']} ({row['date']})")

print(f"  {data.get('attribution', '')}")

print("\nBanco Central de Chile (get_chile_central_bank_series):")
data = tool_json(client.call_tool("get_chile_central_bank_series", {
    "operation": "series",
    "indicators": ["tpm", "imacec"],
    "latestOnly": True,
    # Monthly series (IMACEC) are published with a lag: look back far enough.
    "firstDate": "2026-01-01",
}))
for row in data.get("results", []):
    print(f"  {row['title']}: {row['value']:.2f} ({row['date']})")
print(f"  {data.get('attribution', '')}")
