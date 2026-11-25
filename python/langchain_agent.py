"""LangChain / LangGraph agent with Better Llama's MCP (langchain-mcp-adapters).

1) Loads the 15 MCP tools as LangChain tools (no API key needed).
2) Calls two of them directly, without an LLM: today's UF and dollar (CMF)
   and the TPM (Central Bank of Chile).
3) If OPENAI_API_KEY (or another provider key) is set, builds an agent with
   langchain.agents.create_agent and lets the model pick the tools.

Install (separate venv: langchain-mcp-adapters uses mcp 1.x):
    pip install -r requirements-langchain.txt
Usage:
    python langchain_agent.py                       # steps 1 and 2
    OPENAI_API_KEY=... python langchain_agent.py "¿Cuánto vale la UF hoy y cuál es la TPM?"
    LLM_MODEL=anthropic:claude-sonnet-4-5 python langchain_agent.py "..."   # any init_chat_model id
"""
import asyncio
import json
import os
import sys

from langchain_mcp_adapters.client import MultiServerMCPClient

URL = "https://mcp.betterllama.com/mcp"
DEFAULT_QUESTION = "¿Cuánto vale hoy la UF y el dólar observado en Chile, y cuál es la TPM vigente? Cita la fuente."


def as_json(result):
    """MCP tool results come back as text blocks; Better Llama returns JSON."""
    if isinstance(result, str):
        return json.loads(result)
    if isinstance(result, list):  # list of content blocks
        text = "".join(b.get("text", "") if isinstance(b, dict) else getattr(b, "text", "") for b in result)
        return json.loads(text)
    return result


async def main() -> None:
    client = MultiServerMCPClient({
        "better-llama": {"transport": "streamable_http", "url": URL},
    })
    tools = await client.get_tools()
    by_name = {t.name: t for t in tools}
    print(f"{len(tools)} LangChain tools from {URL}:")
    print("  " + ", ".join(sorted(by_name)) + "\n")

    # Direct calls (no LLM): the same tools an agent would use.
    for source in ("uf", "dolar"):
        data = as_json(await by_name["get_chile_financial_indicators"].ainvoke({"source": source}))
        row = data["results"][-1]
        print(f"CMF {source:5} {row['date']}  {row['value']}")
    data = as_json(await by_name["get_chile_central_bank_series"].ainvoke({"indicators": ["tpm"], "latestOnly": True}))
    row = data["results"][-1]
    print(f"BCCh TPM   {row['date']}  {row['value']} %\n")

    model = os.environ.get("LLM_MODEL", "openai:gpt-4.1-mini")
    if not (os.environ.get("OPENAI_API_KEY") or os.environ.get("LLM_MODEL")):
        print("Set OPENAI_API_KEY (or LLM_MODEL + your provider key) to run the agent step.")
        return

    from langchain.agents import create_agent  # pip install langchain

    agent = create_agent(model, tools, system_prompt=(
        "Answer with data from the Better Llama tools. If unsure which tool to use, call search_tools first. "
        "Always state the date of each value and the source."))
    question = " ".join(sys.argv[1:]) or DEFAULT_QUESTION
    out = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    used = [c["name"] for m in out["messages"] for c in (getattr(m, "tool_calls", None) or [])]
    print("Tools used by the agent:", ", ".join(used) or "(none)")
    print(out["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
