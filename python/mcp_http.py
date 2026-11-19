"""Minimal JSON-RPC client for the Better Llama MCP server (streamable HTTP, anonymous).

No SDK needed: plain HTTP POSTs with httpx. Handles both JSON and SSE responses.
"""
import json
import os

import httpx

ENDPOINT = os.environ.get("BETTERLLAMA_MCP_URL", "https://mcp.betterllama.com/mcp")
HEADERS = {
    "Content-Type": "application/json",
    # Required by the streamable-http transport:
    "Accept": "application/json, text/event-stream",
}


class MCPClient:
    def __init__(self, endpoint: str = ENDPOINT, extra_headers: dict | None = None):
        self.endpoint = endpoint
        self.headers = {**HEADERS, **(extra_headers or {})}
        self.http = httpx.Client(timeout=60)
        self._id = 0

    def _post(self, payload: dict) -> dict | None:
        r = self.http.post(self.endpoint, headers=self.headers, json=payload)
        r.raise_for_status()
        # Keep the session id / protocol version if the server assigns them.
        if sid := r.headers.get("mcp-session-id"):
            self.headers["Mcp-Session-Id"] = sid
        if not r.content:
            return None
        if r.headers.get("content-type", "").startswith("text/event-stream"):
            for line in r.text.splitlines():
                if line.startswith("data:"):
                    return json.loads(line[5:])
            return None
        return r.json()

    def request(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        msg = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params is not None:
            msg["params"] = params
        resp = self._post(msg)
        if resp is None:
            raise RuntimeError("empty response")
        if "error" in resp:
            raise RuntimeError(f"JSON-RPC error: {resp['error']}")
        return resp["result"]

    def initialize(self) -> dict:
        result = self.request("initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "chile-data-mcp-examples", "version": "0.1.0"},
        })
        self.headers["MCP-Protocol-Version"] = result["protocolVersion"]
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return result

    def list_tools(self) -> list[dict]:
        return self.request("tools/list")["tools"]

    def call_tool(self, name: str, arguments: dict) -> dict:
        return self.request("tools/call", {"name": name, "arguments": arguments})


def tool_json(result: dict):
    """Return structuredContent if present, else parse the first text block as JSON."""
    if result.get("structuredContent") is not None:
        return result["structuredContent"]
    for block in result.get("content", []):
        if block.get("type") == "text":
            try:
                return json.loads(block["text"])
            except json.JSONDecodeError:
                return block["text"]
    return result
