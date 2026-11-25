// Minimal JSON-RPC client for the Better Llama MCP server (streamable HTTP, anonymous).
// No dependencies: uses the built-in fetch of Node.js 18+. Handles JSON and SSE responses.

export const ENDPOINT = process.env.BETTERLLAMA_MCP_URL ?? "https://mcp.betterllama.com/mcp";

export class MCPClient {
  constructor(endpoint = ENDPOINT, extraHeaders = {}) {
    this.endpoint = endpoint;
    this.headers = {
      "Content-Type": "application/json",
      // Required by the streamable-http transport:
      Accept: "application/json, text/event-stream",
      ...extraHeaders,
    };
    this.id = 0;
  }

  async #post(payload) {
    const res = await fetch(this.endpoint, {
      method: "POST",
      headers: this.headers,
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    // Keep the session id if the server assigns one.
    const sid = res.headers.get("mcp-session-id");
    if (sid) this.headers["Mcp-Session-Id"] = sid;
    const text = await res.text();
    if (!text) return null;
    if ((res.headers.get("content-type") ?? "").startsWith("text/event-stream")) {
      const line = text.split("\n").find((l) => l.startsWith("data:"));
      return line ? JSON.parse(line.slice(5)) : null;
    }
    return JSON.parse(text);
  }

  async request(method, params) {
    const msg = { jsonrpc: "2.0", id: ++this.id, method };
    if (params !== undefined) msg.params = params;
    const resp = await this.#post(msg);
    if (!resp) throw new Error("empty response");
    if (resp.error) throw new Error(`JSON-RPC error: ${JSON.stringify(resp.error)}`);
    return resp.result;
  }

  async initialize() {
    const result = await this.request("initialize", {
      protocolVersion: "2025-06-18",
      capabilities: {},
      clientInfo: { name: "chile-data-mcp-examples-node", version: "0.1.0" },
    });
    this.headers["MCP-Protocol-Version"] = result.protocolVersion;
    await this.#post({ jsonrpc: "2.0", method: "notifications/initialized" });
    return result;
  }

  async listTools() {
    return (await this.request("tools/list")).tools;
  }

  async callTool(name, args) {
    return this.request("tools/call", { name, arguments: args });
  }
}

// Return structuredContent if present, else parse the first text block as JSON.
export function toolJson(result) {
  if (result.structuredContent != null) return result.structuredContent;
  const block = (result.content ?? []).find((b) => b.type === "text");
  if (!block) return result;
  try {
    return JSON.parse(block.text);
  } catch {
    return block.text;
  }
}
