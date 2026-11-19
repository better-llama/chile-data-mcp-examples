"""List the tools exposed by the Better Llama MCP server.

Usage: python list_tools.py
"""
from mcp_http import MCPClient

client = MCPClient()
info = client.initialize()
print(f"Server: {info['serverInfo']['name']} {info['serverInfo']['version']} "
      f"(protocol {info['protocolVersion']})")

tools = client.list_tools()
print(f"{len(tools)} tools:\n")
for t in tools:
    props = ", ".join(t["inputSchema"].get("properties", {}).keys())
    print(f"- {t['name']}: {t.get('title', '')}")
    print(f"    args: {props}")
