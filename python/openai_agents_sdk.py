"""OpenAI Agents SDK agent with Better Llama's MCP (MCPServerStreamableHttp).

1) Connects to the MCP and lists its tools (no API key needed).
2) Calls two of them directly, without an LLM: today's UF and dollar (CMF)
   and the TPM (Central Bank of Chile).
3) If OPENAI_API_KEY is set, runs an Agent that gets the MCP as a tool
   server and lets the model pick the tools.

Install (separate venv is recommended):
    pip install -r requirements-openai-agents.txt
Usage:
    python openai_agents_sdk.py                     # steps 1 and 2
    OPENAI_API_KEY=... python openai_agents_sdk.py "¿Cuánto vale la UF hoy y cuál es la TPM?"
    OPENAI_API_KEY=... LLM_MODEL=gpt-4.1 python openai_agents_sdk.py "..."
"""
import asyncio
import json
import os
import sys

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

URL = "https://mcp.betterllama.com/mcp"
DEFAULT_QUESTION = "¿Cuánto vale hoy la UF y el dólar observado en Chile, y cuál es la TPM vigente? Cita la fuente."


def as_json(result):
    """Better Llama returns JSON inside the text content of each tool result."""
    return json.loads("".join(getattr(c, "text", "") for c in result.content))


async def main() -> None:
    async with MCPServerStreamableHttp(
        name="better-llama",
        params={"url": URL},
        cache_tools_list=True,
        client_session_timeout_seconds=60,
    ) as server:
        tools = await server.list_tools()
        print(f"{len(tools)} MCP tools from {URL}:")
        print("  " + ", ".join(sorted(t.name for t in tools)) + "\n")

        # Direct calls (no LLM): the same tools the agent will use.
        for source in ("uf", "dolar"):
            data = as_json(await server.call_tool("get_chile_financial_indicators", {"source": source}))
            row = data["results"][-1]
            print(f"CMF {source:5} {row['date']}  {row['value']}")
        data = as_json(await server.call_tool("get_chile_central_bank_series", {"indicators": ["tpm"], "latestOnly": True}))
        row = data["results"][-1]
        print(f"BCCh TPM   {row['date']}  {row['value']} %\n")

        if not os.environ.get("OPENAI_API_KEY"):
            print("Set OPENAI_API_KEY to run the agent step.")
            return

        agent = Agent(
            name="Chile data assistant",
            instructions=(
                "Answer with data from the Better Llama tools. If unsure which tool to use, call search_tools first. "
                "Always state the date of each value and the source."),
            model=os.environ.get("LLM_MODEL", "gpt-4.1-mini"),
            mcp_servers=[server],
        )
        question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION
        result = await Runner.run(agent, question)
        used = [getattr(i.raw_item, "name", "") for i in result.new_items if i.type == "tool_call_item"]
        print("Tools used by the agent:", ", ".join(used) or "(none)")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
