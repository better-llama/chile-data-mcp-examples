"""Use the official MCP Python SDK (streamable HTTP transport) against Better Llama.

Tested with mcp==2.3.0. (In mcp 1.x the transport is `streamablehttp_client`
and yields three values: read, write, get_session_id.)

Usage: python agent_mcp_sdk.py
"""
import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "https://mcp.betterllama.com/mcp"


async def main() -> None:
    async with streamable_http_client(URL) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            print(f"Connected to {init.server_info.name} {init.server_info.version}")

            tools = await session.list_tools()
            print(f"{len(tools.tools)} tools: {', '.join(t.name for t in tools.tools)}\n")

            # 1) Let the server suggest the right tool for a task (what an agent would do).
            found = await session.call_tool("search_tools", {"query": "sismos"})
            print("search_tools('sismos') ->", found.content[0].text[:300], "...\n")

            # 2) Call it: last earthquakes in Chile, magnitude >= 4.5.
            result = await session.call_tool("get_chile_earthquakes", {
                "minMagnitude": 4.5,
                "orderBy": "time",
                "maxItems": 3,
            })
            data = json.loads(result.content[0].text)
            print(f"Last {data['count']} earthquakes M>=4.5 (Chile time):")
            for q in data["results"]:
                print(f"  M{q['magnitude']}  {q['timeChile']}  {q['place']}  depth {q['depthKm']:.0f} km")


if __name__ == "__main__":
    asyncio.run(main())
