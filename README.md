# chile-data-mcp-examples

Ejemplos ejecutables para usar el servidor MCP gratuito (beta) de [Better Llama](https://betterllama.com) con datos públicos de Chile, Colombia, Perú y México: indicadores económicos (CMF, Banco Central), precios de bencina (CNE), sismos (USGS), Mercado Público, Chilexpress, Diario Oficial, mercado eléctrico, Bolsa de Santiago, feriados y RUT. Compras públicas de Colombia (SECOP II). Series del Banco Central de Reserva del Perú (BCRP) e indicadores del Banco de México (Banxico: tipo de cambio FIX, UDIS, TIIE, tasa objetivo, inflación). TRM de Colombia (tasa de cambio oficial COP/USD). Ejemplo CMF Chile (UF, dólar observado, euro, UTM, IPC y tasa máxima convencional). Feriados de Chile, días hábiles y plazos, validación de RUT y comunas con código CUT (`calendario_rut.py`, sin clave). Ejemplos en JavaScript para Node.js 18+ sin dependencias (carpeta [`node/`](node/)) y con el SDK oficial de MCP. Nuevo: agente con LangChain / LangGraph ([`python/langchain_agent.py`](python/langchain_agent.py)) y con Mastra ([`node/mastra_agent.mjs`](node/mastra_agent.mjs)).

Runnable examples (Python and Node.js) for Better Llama's free (beta) MCP server with Chilean, Colombian, Peruvian and Mexican public data. English below.

| | |
|---|---|
| Endpoint | `https://mcp.betterllama.com/mcp` |
| Transporte / Transport | Streamable HTTP, sin autenticación / anonymous |
| Header requerido / required | `Accept: application/json, text/event-stream` |
| Registry id | `com.betterllama/chile-data` |
| Herramientas / Tools | 15 (`tools/list`) |

---

## Español

### Inicio rápido

```bash
git clone https://github.com/better-llama/chile-data-mcp-examples
cd chile-data-mcp-examples
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd python
python list_tools.py       # lista las 15 herramientas
python indicadores.py      # UF, dólar, UTM (CMF) + TPM, IMACEC (Banco Central)
python bencina.py 93 Ñuñoa # bencina más barata en una comuna (CNE)
python secop_colombia.py software Antioquia 100000000  # contratos SECOP II (Colombia)
python bcrp_peru.py        # tipo de cambio y tasa de referencia (BCRP, Perú)
python banxico_mexico.py   # tipo de cambio FIX, UDIS y tasa objetivo (Banxico, México)
python trm_colombia.py     # TRM vigente, dólar oficial COP/USD (Colombia)
python cmf_chile.py        # UF, dólar observado, euro y UTM vigentes (CMF Chile)
python calendario_rut.py   # feriados que quedan del año; también plazo, habiles, rut, dv, comunas
python sismos.py           # sismos de la última semana; también hoy, fuertes, cerca, tsunami, percibidos
python agent_mcp_sdk.py    # SDK oficial "mcp": search_tools + sismos
```

Requiere Python 3.10+. Probado con Python 3.13, httpx 0.28 y mcp 2.3.0.

**LangChain / LangGraph** (en otro entorno virtual, porque `langchain-mcp-adapters` usa mcp 1.x):

```bash
python3 -m venv .venv-lc && source .venv-lc/bin/activate
pip install -r python/requirements-langchain.txt
python python/langchain_agent.py                  # carga las 15 herramientas como tools de LangChain y llama UF, dólar y TPM sin LLM
OPENAI_API_KEY=... python python/langchain_agent.py "¿Cuánto vale la UF hoy?"   # agente create_agent que elige las herramientas
```

Probado con langchain-mcp-adapters 0.3.2, langchain 1.5 y langgraph 1.2. Cualquier modelo de `init_chat_model` sirve con `LLM_MODEL` (p. ej. `anthropic:claude-sonnet-4-5`) y la clave de ese proveedor.

**OpenAI Agents SDK** (`openai-agents`, servidor MCP por Streamable HTTP):

```bash
pip install -r python/requirements-openai-agents.txt
python python/openai_agents_sdk.py                # lista las 15 herramientas y llama UF, dólar y TPM sin LLM
OPENAI_API_KEY=... python python/openai_agents_sdk.py "¿Cuánto vale la UF hoy?"   # Agent con mcp_servers que elige las herramientas
```

Probado con openai-agents 0.26 y mcp 2.3 (sirve el mismo entorno que el resto de los ejemplos Python). Cambia el modelo con `LLM_MODEL` (por defecto `gpt-4.1-mini`).

**Node.js 18+** (JavaScript, sin dependencias salvo los ejemplos del SDK de MCP y del Vercel AI SDK):

```bash
cd node
node list_tools.mjs        # lista las 15 herramientas
node indicadores.mjs       # UF, dólar, UTM (CMF) + TPM, IMACEC (Banco Central)
node sismos.mjs fuertes    # sismos M>=5 del último año; también hoy, cerca <lat> <lon> <km>
node calendario_rut.mjs    # feriados que quedan del año; también plazo <fecha> <n>, rut <rut>...
node latam.mjs            # Colombia TRM, Peru BCRP, Mexico Banxico (co | pe | mx)
npm install && node agent_mcp_sdk.mjs   # SDK oficial @modelcontextprotocol/sdk: search_tools + UF
```

Probado con Node.js 24 y @modelcontextprotocol/sdk 1.32.

**Vercel AI SDK** (`ai` + `@ai-sdk/mcp`, cliente MCP por Streamable HTTP):

```bash
cd node && npm install
node vercel_ai_sdk.mjs          # 15 herramientas como tools del AI SDK; UF, dólar (CMF) y TRM de Colombia sin LLM
node vercel_ai_sdk.mjs --mock   # prueba generateText con el modelo simulado de 'ai/test' (llamada real a la herramienta, sin LLM)
OPENAI_API_KEY=... node vercel_ai_sdk.mjs "¿Cuánto vale la UF hoy y cuál es la TRM en Colombia?"   # generateText elige las herramientas
```

Probado con ai 7.0, @ai-sdk/mcp 2.0 y @ai-sdk/openai 4.0 (`createMCPClient({ transport: { type: "http", url } })`; en AI SDK 5 se llama `experimental_createMCPClient` y se importa desde `ai`). Cambia el modelo con `LLM_MODEL` (por defecto `gpt-4.1-mini`).

**Mastra** (`@mastra/mcp` + `@mastra/core`, cliente MCP por Streamable HTTP; requiere Node.js 22.13+):

```bash
cd node && npm install
node mastra_agent.mjs          # 15 herramientas como tools de Mastra; UF, dólar (CMF) y TRM de Colombia sin LLM
node mastra_agent.mjs --mock   # prueba un Agent de Mastra con el modelo simulado de 'ai/test' (llamada real a la herramienta, sin LLM)
OPENAI_API_KEY=... node mastra_agent.mjs "¿Cuánto vale la UF hoy y cuál es la TRM en Colombia?"   # el Agent elige las herramientas
```

Probado con @mastra/mcp 2.11 y @mastra/core 1.86 (`new MCPClient({ servers: { betterllama: { url: new URL("https://mcp.betterllama.com/mcp") } } })`; `listTools()` antepone el nombre del servidor: `betterllama_get_chile_financial_indicators`). Cambia el modelo con `LLM_MODEL` en formato `proveedor/modelo` (por defecto `openai/gpt-4.1-mini`).

### Archivos

| Archivo | Qué hace |
|---|---|
| `python/mcp_http.py` | Cliente JSON-RPC mínimo con httpx (`initialize`, `tools/list`, `tools/call`), sin SDK. |
| `python/list_tools.py` | Lista herramientas y sus argumentos. |
| `python/indicadores.py` | `get_chile_financial_indicators` y `get_chile_central_bank_series`. |
| `python/bencina.py` | `find_chile_fuel_prices` ordenado por precio. |
| `python/secop_colombia.py` | `colombia_secop_search`: contratos o procesos de compras públicas de Colombia (SECOP II, datos.gov.co). |
| `python/bcrp_peru.py` | `peru_bcrp_series`: series del BCRP (tipo de cambio, tasa de referencia, inflación, PBI, reservas) por alias o código; `--catalog` lista alias. |
| `python/banxico_mexico.py` | `mexico_banxico_indicators`: tipo de cambio FIX, UDIS, TIIE, tasa objetivo e inflación del Banco de México; `--date` o `--from/--to` para series. |
| `python/trm_colombia.py` | `colombia_trm`: TRM de Colombia (pesos por dólar, Superintendencia Financiera vía datos.gov.co); sin argumentos la vigente, `--date` para un día o `--from/--to` para un rango. |
| `python/cmf_chile.py` | `get_chile_financial_indicators`: indicadores oficiales de la CMF Chile; sin argumentos UF, dólar observado, euro y UTM vigentes; `--indicator` (uf, dolar, euro, utm, ipc, tmc, tip), `--date` para un día, `--year`/`--month` para una serie y `--tmc` para la tasa máxima convencional. |
| `python/calendario_rut.py` | `chile_calendar_and_rut`: feriados de Chile (nacionales, regionales y comunales, 2022–2035), `es-feriado`, `plazo` (sumar N días hábiles), `habiles` (contar días hábiles entre dos fechas), `rut`/`dv` (validar RUT o calcular el dígito verificador) y `comunas` (códigos CUT por región). Opciones `--region`, `--comuna` y `--sabado`. Cálculo local, sin clave ni datos personales. |
| `python/sismos.py` | `get_chile_earthquakes`: sismos de Chile (USGS, dominio público) con hora de Chile; `hoy`, `fuertes` (M>=5 del último año por magnitud), `cerca <lat> <lon> <km>`, `tsunami` (últimos 10 años) y `percibidos`; opciones `--min`, `--max` e `--islas` (incluye Isla de Pascua y Juan Fernández). Sin clave. |
| `python/agent_mcp_sdk.py` | Cliente con el SDK oficial de MCP para Python (streamable HTTP). |
| `python/langchain_agent.py` | LangChain / LangGraph con `langchain-mcp-adapters`: las 15 herramientas como tools de LangChain, llamadas directas sin LLM (UF, dólar, TPM) y un agente `create_agent` si defines `OPENAI_API_KEY` o `LLM_MODEL`. Dependencias en `python/requirements-langchain.txt`. |
| `python/openai_agents_sdk.py` | OpenAI Agents SDK con `MCPServerStreamableHttp`: lista las 15 herramientas, llamadas directas sin LLM (UF, dólar, TPM) y un `Agent` con `mcp_servers` si defines `OPENAI_API_KEY`. Dependencias en `python/requirements-openai-agents.txt`. |
| `node/mcp_http.mjs` | Cliente JSON-RPC mínimo en JavaScript con `fetch` (Node.js 18+), sin dependencias; mismo contrato que `mcp_http.py`. |
| `node/list_tools.mjs`, `node/indicadores.mjs`, `node/sismos.mjs`, `node/calendario_rut.mjs` | Versiones en Node.js de los ejemplos de Python (herramientas, indicadores CMF/Banco Central, sismos, feriados/plazos/RUT). |
| `node/latam.mjs` | `colombia_trm`, `peru_bcrp_series` y `mexico_banxico_indicators` en un solo script: TRM de Colombia, tipo de cambio y tasa de referencia del BCRP (Perú), FIX, UDIS y tasa objetivo de Banxico (México). Argumentos `co`, `pe` o `mx` para un solo país. Sin clave. |
| `node/agent_mcp_sdk.mjs` | Cliente con el SDK oficial de MCP para TypeScript/JavaScript (`StreamableHTTPClientTransport`). |
| `node/vercel_ai_sdk.mjs` | Vercel AI SDK con `createMCPClient` (`@ai-sdk/mcp`): las 15 herramientas como tools del AI SDK, llamadas directas sin LLM (UF, dólar, TRM de Colombia) y `generateText` con las herramientas si defines `OPENAI_API_KEY` (`--mock` lo prueba sin LLM). Dependencias en `node/package.json`. |
| `node/mastra_agent.mjs` | Mastra con `MCPClient` (`@mastra/mcp`): las 15 herramientas como tools de Mastra, llamadas directas sin LLM (UF, dólar, TRM de Colombia) y un `Agent` de `@mastra/core` con las herramientas si defines `OPENAI_API_KEY` (`--mock` lo prueba sin LLM). Node.js 22.13+. Dependencias en `node/package.json`. |
| `config/` | Configuración para Cursor, VS Code, Claude Desktop, Windsurf, Gemini CLI y Codex. |

### Herramientas

- Sin clave: `search_tools`, `get_chile_financial_indicators`, `get_chile_central_bank_series`, `find_chile_fuel_prices`, `get_chile_electricity_market`, `search_chile_official_gazette`, `get_chile_earthquakes`, `chile_calendar_and_rut`, `colombia_secop_search`, `colombia_trm`, `peru_bcrp_series`, `mexico_banxico_indicators` (algunas usan una clave compartida del servidor; no necesitas la tuya).
- Trae tu clave gratuita: `search_chile_public_tenders` (ticket de [ChileCompra](https://www.chilecompra.cl/api/), argumento `ticket` o header `X-MercadoPublico-Ticket`), `get_santiago_stock_exchange_data` (`apiKey`). `chilexpress_shipping` acepta tus claves para cotizar y seguir envíos.

Las claves se envían por solicitud y el servidor no las guarda. No las subas a git: usa variables de entorno.

Consejo para agentes: llama primero `search_tools` con la tarea ("valor UF", "licitaciones", "sismos") y usa los `example_arguments` que devuelve.

### Conectar un cliente MCP

**Cursor** (`~/.cursor/mcp.json` o `.cursor/mcp.json`) y otros clientes que aceptan `url`: ver [`config/cursor-mcp.json`](config/cursor-mcp.json).

```json
{ "mcpServers": { "betterllama": { "url": "https://mcp.betterllama.com/mcp" } } }
```

**VS Code** (`.vscode/mcp.json`): [`config/vscode-mcp.json`](config/vscode-mcp.json) (`"type": "http"`).

**Claude Desktop / claude.ai**: Settings > Connectors > Add custom connector, URL `https://mcp.betterllama.com/mcp`. Si tu versión solo acepta servidores locales, usa el puente `mcp-remote` de [`config/claude_desktop_config.json`](config/claude_desktop_config.json) (requiere Node.js).

**Claude Code**: `claude mcp add --transport http betterllama https://mcp.betterllama.com/mcp`.

**Codex** (CLI y extensión): agrega a `~/.codex/config.toml` el bloque de [`config/codex-config.toml`](config/codex-config.toml) (`[mcp_servers.betterllama]` con `url`).

**Gemini CLI** (`~/.gemini/settings.json`): [`config/gemini-settings.json`](config/gemini-settings.json) (`"httpUrl"`).

**Windsurf** (`~/.codeium/windsurf/mcp_config.json`): [`config/windsurf-mcp_config.json`](config/windsurf-mcp_config.json) (`"serverUrl"`).

**n8n**: agrega el nodo *MCP Client Tool* a un AI Agent, Endpoint `https://mcp.betterllama.com/mcp`, Server Transport *HTTP Streamable*, Authentication *None*. Elige "All" o selecciona herramientas. O importa el workflow listo [`n8n/chile-data-mcp-workflow.json`](n8n/chile-data-mcp-workflow.json) (menú *Import from File*: Chat Trigger + AI Agent + MCP Client Tool; solo elige tu credencial del modelo).

**curl**:

```bash
curl -s https://mcp.betterllama.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_chile_financial_indicators","arguments":{"source":"uf"}}}'
```

### Guías

- [API Mercado Público](https://betterllama.com/guias/api-mercado-publico/)
- [API indicadores económicos de Chile](https://betterllama.com/guias/api-indicadores-economicos-chile/)
- [API bencina Chile](https://betterllama.com/guias/api-bencina-chile/)
- [API Chilexpress](https://betterllama.com/guias/api-chilexpress/)
- [API sismos Chile](https://betterllama.com/guias/api-sismos-chile/)
- [API SECOP II Colombia](https://betterllama.com/guias/api-secop-colombia/)
- [API BCRP Perú](https://betterllama.com/guias/api-bcrp-peru/)
- [API Banxico México](https://betterllama.com/guias/api-banxico-mexico/)
- [API TRM Colombia](https://betterllama.com/guias/api-trm-colombia/)
- [API CMF Chile: UF, dólar, euro, UTM y TMC](https://betterllama.com/guias/api-cmf-chile/)
- [API UF Chile](https://betterllama.com/guias/api-uf-chile/) · [API dólar observado](https://betterllama.com/guias/api-dolar-observado-chile/) · [API Banco Central de Chile](https://betterllama.com/guias/api-banco-central-chile/)
- [API feriados Chile](https://betterllama.com/guias/api-feriados-chile/) · [API días hábiles](https://betterllama.com/guias/api-dias-habiles-chile/) · [API para validar RUT](https://betterllama.com/guias/api-validar-rut-chile/) · [API comunas de Chile](https://betterllama.com/guias/api-comunas-chile/)
- [API Diario Oficial](https://betterllama.com/guias/api-diario-oficial-chile/) · [API Coordinador Eléctrico](https://betterllama.com/guias/api-coordinador-electrico-chile/)
- [Todas las APIs de datos abiertos de Chile](https://betterllama.com/guias/apis-datos-abiertos-chile/)

---

## English

### Quick start

```bash
git clone https://github.com/better-llama/chile-data-mcp-examples
cd chile-data-mcp-examples
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd python
python list_tools.py        # list the 15 tools
python indicadores.py       # UF, USD, UTM (CMF) + policy rate, IMACEC (Central Bank)
python bencina.py 93 Ñuñoa  # cheapest gasoline in a comuna (CNE)
python secop_colombia.py software Antioquia 100000000  # Colombia SECOP II contracts
python bcrp_peru.py         # Peru exchange rate + policy rate (BCRP)
python banxico_mexico.py    # Mexico FIX exchange rate, UDIS, policy rate (Banxico)
python trm_colombia.py      # Colombia official COP/USD exchange rate (TRM)
python cmf_chile.py         # Chile UF, observed USD, EUR and UTM (CMF)
python calendario_rut.py    # Chile holidays left this year; also plazo, habiles, rut, dv, comunas
python sismos.py            # Chile earthquakes, last 7 days; also hoy, fuertes, cerca, tsunami, percibidos
python agent_mcp_sdk.py     # official "mcp" SDK: search_tools + earthquakes
```

Python 3.10+. Tested with Python 3.13, httpx 0.28 and mcp 2.3.0. With mcp 1.x, import `streamablehttp_client` instead; it yields `(read, write, get_session_id)`.

**LangChain / LangGraph** (separate venv: `langchain-mcp-adapters` depends on mcp 1.x):

```bash
python3 -m venv .venv-lc && source .venv-lc/bin/activate
pip install -r python/requirements-langchain.txt
python python/langchain_agent.py                  # loads the 15 tools as LangChain tools; calls UF, USD and policy rate without an LLM
OPENAI_API_KEY=... python python/langchain_agent.py "What is the UF today?"   # create_agent picks the tools
```

Tested with langchain-mcp-adapters 0.3.2, langchain 1.5 and langgraph 1.2. Any `init_chat_model` id works via `LLM_MODEL` (e.g. `anthropic:claude-sonnet-4-5`) with that provider's key.

**OpenAI Agents SDK** (`openai-agents`, MCP server over Streamable HTTP):

```bash
pip install -r python/requirements-openai-agents.txt
python python/openai_agents_sdk.py                # lists the 15 tools; calls UF, USD and policy rate without an LLM
OPENAI_API_KEY=... python python/openai_agents_sdk.py "What is the UF today?"   # Agent with mcp_servers picks the tools
```

Tested with openai-agents 0.26 and mcp 2.3 (same environment as the other Python examples). Change the model with `LLM_MODEL` (default `gpt-4.1-mini`).

**Node.js 18+** (JavaScript, zero dependencies except the MCP SDK and Vercel AI SDK examples):

```bash
cd node
node list_tools.mjs        # list the 15 tools
node indicadores.mjs       # UF, USD, UTM (CMF) + policy rate, IMACEC (Central Bank)
node sismos.mjs fuertes    # Chile earthquakes M>=5 in the last year; also hoy, cerca <lat> <lon> <km>
node calendario_rut.mjs    # Chile holidays left this year; also plazo <date> <n>, rut <rut>...
node latam.mjs            # Colombia TRM, Peru BCRP, Mexico Banxico (co | pe | mx)
npm install && node agent_mcp_sdk.mjs   # official @modelcontextprotocol/sdk: search_tools + UF
```

`node/mcp_http.mjs` is a ~70-line client (built-in `fetch`, JSON and SSE responses) you can copy into any Node.js, Deno, Bun or edge project. Tested with Node.js 24 and @modelcontextprotocol/sdk 1.32.

**Vercel AI SDK** (`ai` + `@ai-sdk/mcp`, MCP client over Streamable HTTP):

```bash
cd node && npm install
node vercel_ai_sdk.mjs          # 15 tools as AI SDK tools; UF, USD (CMF) and Colombia's TRM without an LLM
node vercel_ai_sdk.mjs --mock   # checks generateText with the mock model from 'ai/test' (real tool call, no LLM)
OPENAI_API_KEY=... node vercel_ai_sdk.mjs "What is the UF today and Colombia's TRM?"   # generateText picks the tools
```

Tested with ai 7.0, @ai-sdk/mcp 2.0 and @ai-sdk/openai 4.0 (`createMCPClient({ transport: { type: "http", url } })`; in AI SDK 5 it is `experimental_createMCPClient`, imported from `ai`). Change the model with `LLM_MODEL` (default `gpt-4.1-mini`).

**Mastra** (`@mastra/mcp` + `@mastra/core`, MCP client over Streamable HTTP; needs Node.js 22.13+):

```bash
cd node && npm install
node mastra_agent.mjs          # 15 tools as Mastra tools; UF, USD (CMF) and Colombia's TRM without an LLM
node mastra_agent.mjs --mock   # checks a Mastra Agent with the mock model from 'ai/test' (real tool call, no LLM)
OPENAI_API_KEY=... node mastra_agent.mjs "What is the UF today and Colombia's TRM?"   # the Agent picks the tools
```

Tested with @mastra/mcp 2.11 and @mastra/core 1.86 (`new MCPClient({ servers: { betterllama: { url: new URL("https://mcp.betterllama.com/mcp") } } })`; `listTools()` prefixes the server name: `betterllama_get_chile_financial_indicators`). Change the model with `LLM_MODEL` as `provider/model` (default `openai/gpt-4.1-mini`).

### Notes

- The server is stateless Streamable HTTP; no auth. Every POST must send `Accept: application/json, text/event-stream`.
- Tool results come as a JSON string in `content[0].text`, with the official source attribution. Please cite the source when showing data.
- `search_chile_public_tenders` and `get_santiago_stock_exchange_data` need your own free provider key (bring your own key). All other tools work without a key.
- Client setup (Cursor, VS Code, Claude Desktop, Claude Code, Codex, Gemini CLI, Windsurf, n8n, curl): see the Spanish section above and `config/`. Claude Code: `claude mcp add --transport http betterllama https://mcp.betterllama.com/mcp`.
- n8n: import [`n8n/chile-data-mcp-workflow.json`](n8n/chile-data-mcp-workflow.json) (*Import from File*): Chat Trigger + AI Agent + MCP Client Tool pointing to `https://mcp.betterllama.com/mcp` (HTTP Streamable, no auth). Just pick your chat-model credential.
- Colombia: `colombia_secop_search` searches SECOP II signed contracts (`dataset: contratos`) or published processes (`procesos`) from datos.gov.co (CC BY-SA 4.0), no key. Guide: [Colombia SECOP API](https://betterllama.com/en/guides/colombia-secop-api/).
- Peru: `peru_bcrp_series` returns official BCRP series (exchange rate, policy rate, inflation, GDP, reserves) by alias or BCRP code, no key; `python bcrp_peru.py --catalog` lists aliases. Guide: [Peru BCRP API](https://betterllama.com/en/guides/peru-bcrp-api/).
- Mexico: `mexico_banxico_indicators` returns official Bank of Mexico (SIE) indicators: FIX MXN/USD exchange rate, UDIS, TIIE 28/91/182, overnight funding TIIE, policy target rate and annual inflation, no key (the server uses its own token; send `X-Banxico-Token` to use yours). Guide: [Mexico Banxico API](https://betterllama.com/en/guides/mexico-banxico-api/).
- Colombia TRM: `colombia_trm` returns Colombia's official COP/USD exchange rate (TRM) certified by the Superintendencia Financiera, via datos.gov.co (CC BY-SA 4.0), no key. No arguments: latest TRM; `date` for the TRM in force on a day (weekend/holiday rates are certified the previous business day, so each row has `date_from`/`date_to`); `fromDate`/`toDate` for a range (`python trm_colombia.py --from 2026-11-10 --to 2026-11-20`). Guide: [Colombia TRM API](https://betterllama.com/en/guides/colombia-trm-api/).
- Chile CMF: `get_chile_financial_indicators` returns official indicators from Chile's Comisión para el Mercado Financiero (CMF): UF, observed USD (dólar observado), EUR, UTM, CPI (IPC), maximum conventional interest rate (TMC) and TIP, no key (the server uses its own CMF key). `python cmf_chile.py` prints the latest UF, USD, EUR and UTM; `--indicator dolar --date 2026-11-20` for one day, `--indicator uf --year 2026 --month 11` for a series, `--tmc` for the TMC. USD and EUR are only published on banking days: on weekends you get the last published value plus a note, and when CMF has already published the next banking day's rate in advance, the note includes it. Guide: [Chile CMF API](https://betterllama.com/en/guides/chile-cmf-api/).
- Chile holidays, business days, RUT and communes: `chile_calendar_and_rut` is computed by the server from Chilean holiday laws and SUBDERE territorial codes (no key, no external calls, no personal data). `python calendario_rut.py` lists the holidays left this year; `feriados 2027` (national + regional, marked `[regional]`), `es-feriado 2026-12-08`, `plazo 2026-12-15 10` (add 10 business days, counted from the next day), `habiles 2026-12-01 2026-12-31`, `rut 12.345.678-5`, `dv 12345678` (compute the check digit), `comunas RM` (CUT codes). `--region`/`--comuna` apply regional or communal holidays (e.g. 20 August in Chillán); `--sabado` counts Saturdays as business days. Guides: [holidays](https://betterllama.com/en/guides/chile-holidays-api/), [business days](https://betterllama.com/en/guides/chile-business-days-api/), [RUT validation](https://betterllama.com/en/guides/chile-rut-validation-api/), [communes](https://betterllama.com/en/guides/chile-communes-api/). All guides: [Chile open data APIs](https://betterllama.com/en/guides/chile-open-data-apis/).
- Chile earthquakes: `get_chile_earthquakes` returns USGS (ComCat, public domain) events for Chile with UTC and Chile time, magnitude, depth, PAGER alert level, tsunami flag and felt reports, no key. `python sismos.py` lists the last 7 days (M>=2.5); `hoy`, `fuertes` (M>=5 in the last year, by magnitude), `cerca -33.45 -70.66 150` (radius search), `tsunami` (last 10 years), `percibidos` (felt reports); `--min`, `--max`, `--islas`. Guide: [Chile earthquakes API](https://betterllama.com/en/guides/chile-earthquakes-api/).
- Free beta: the server applies per-IP rate limits; be gentle with loops.

---

## Salida real / Real output

Ejecutado el 2026-11-19 / Run on 2026-11-19 (Chile time; antes de agregar SECOP, por eso 11 herramientas / before SECOP was added, hence 11 tools). Los valores cambian a diario / values change daily.

`python list_tools.py` (truncated):

```text
Server: betterllama 0.1.0 (protocol 2025-06-18)
11 tools:

- search_tools: Buscar herramientas de Better Llama
    args: query, category
- search_chile_public_tenders: Licitaciones y compras públicas de Chile (Mercado Público)
    args: ticket, source, codes, dateFrom, dateTo, tenderStatus, purchaseOrderStatus, buyerCode, supplierCode, agileStatuses, regions, keyword, buyerRut, fetchDetails, maxItems
- get_chile_financial_indicators: UF, dólar, euro, UTM, IPC y reportes bancarios (CMF Chile)
    args: source, period, year, month, day, yearTo, monthTo, dayTo, institutionCode, accountCode, listCatalog, adecuacionResource, regresionMonths, maxItems
- get_chile_central_bank_series: Series del Banco Central de Chile (BDE): dólar, TPM, IMACEC, PIB, desempleo
    args: operation, indicators, seriesIds, firstDate, lastDate, latestOnly, skipEmpty, frequency, query, maxItems
- find_chile_fuel_prices: Precios de bencina, diésel y gas por estación en Chile (CNE)
...
```

`python indicadores.py`:

```text
CMF Chile (get_chile_financial_indicators):
  Unidad de Fomento (UF): 41,364.17 CLP (2026-11-19)
  Dólar observado (USD): 1,002.07 CLP (2026-11-19)
  Unidad Tributaria Mensual (UTM): 72,440 CLP (2026-11-01)
  Fuente: Comisión para el Mercado Financiero (CMF Chile), API CMF Bancos — https://www.cmfchile.cl

Banco Central de Chile (get_chile_central_bank_series):
  Tasa de política monetaria (TPM) (porcentaje): 4.50 (2026-11-19)
  Imacec empalmado, serie original (índice 2018=100): 109.77 (2026-09-01)
  Fuente: Banco Central de Chile, Base de Datos Estadísticos — https://si3.bcentral.cl
```

`python bencina.py 93 Ñuñoa`:

```text
Top 5 cheapest '93' in Ñuñoa:
  $1,387 $/L  ARAMCO     José Pedro Alessandri 475 (asistido, updated 2026-11-12)
  $1,506 $/L  COPEC      Pedro de Valdivia 4298 (asistido, updated 2026-11-19)
  $1,514 $/L  ARAMCO     Avenida Grecia 1060 (asistido, updated 2026-11-19)
  $1,529 $/L  COPEC      Vicuña Mackenna 654 (asistido, updated 2026-11-19)
  $1,533 $/L  ARAMCO     Avenida Ricardo Lyon 2633 (autoservicio, updated 2026-11-19)

Fuente: Comisión Nacional de Energía (CNE), Bencina en Línea — https://api.cne.cl
```

`python agent_mcp_sdk.py`:

```text
Connected to betterllama 0.1.0
11 tools: search_tools, search_chile_public_tenders, get_chile_financial_indicators, get_chile_central_bank_series, find_chile_fuel_prices, chilexpress_shipping, get_chile_electricity_market, search_chile_official_gazette, get_chile_earthquakes, get_santiago_stock_exchange_data, chile_calendar_and_rut

search_tools('sismos') -> {"count":1,"tools":[{"name":"get_chile_earthquakes","title":"Sismos en Chile (USGS)","country":"CL","category":"geociencias","access":"none","provider":"USGS Earthquake Hazards Program","example_arguments":{"minMagnitude":4.5,"maxItems":5}}],"coverage":{"available":["CL"],"roadmap":["MX","PE","CO"," ...

Last 2 earthquakes M>=4.5 (Chile time):
  M4.5  2026-11-18T15:46:53-03:00  23 km SSW of Ollagüe, Chile  depth 134 km
  M4.6  2026-11-13T20:55:15-03:00  100 km WSW of Lebu, Chile  depth 10 km
```

`python secop_colombia.py software Antioquia 100000000` (2026-11-20):

```text
SECOP II contratos: 'software' in Antioquia (>= COP 100,000,000), 5 shown, newest first:

  2026-11-06  COP 373,227,554  [En ejecución]
  INSTITUCIÓN UNIVERSITARIA ITM (Medellín)
  RENOVACIÓN DEL SOPORTE Y GARANTÍA PARA SOFTWARE Y EQUIPOS DE MISIÓN CRÍTICA PARA LA INSTITUCIÓN UNIVERSITARIA ITM; DE ACUERDO CON LAS ESPECI
  Proveedor: AXIS IT (NIT 900733550)
  https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.11062770&isFromPublicArea=True&isModal=true&asPopupView=true

  2026-11-05  COP 168,510,895  [Aprobado]
  POLITECNICO COLOMBIANO JAIME ISAZA CADAVID (Medellín)
  Licenciamiento de software Microsoft bajo la modalidad OVS-ES (Open Value Subscription) para el Politécnico Colombiano Jaime Isaza Cadavid
  Proveedor: TEAM IT SAS (NIT 900446662)
  https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.11062487&isFromPublicArea=True&isModal=true&asPopupView=true

  ...

Fuente: Portal de Datos Abiertos www.datos.gov.co — SECOP II (Agencia Nacional de Contratación Pública – Colombia Compra Eficiente). Licencia CC BY-SA 4.0. La fecha de última actualización del conjunto viene en sourceUpdatedAt.

```

`python secop_colombia.py interventoría Bogotá 0 procesos` (2026-11-20):

```text
SECOP II procesos: 'interventoría' in Bogotá (>= COP 0), 5 shown, newest first:

  2026-11-17  COP 115,829,101  [Publicado]
  ALCALDIA LOCAL RAFAEL URIBE URIBE
  REALIZAR LA INTERVENTORÍA TÉCNICA; ADMINISTRATIVA; FINANCIERA; JURÍDICA; AMBIENTAL Y SOCIAL AL CONTRATO DE OBRA PUBLICA RESULTANTE DEL PROCE
  https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.11241314

  2026-11-17  COP 691,929,130  [Publicado]
  INSTITUTO DISTRITAL DE PATRIMONIO CULTURAL (Bogotá)
  Interventoría e iluminación Plaza Bolívar
  https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.11240793

  ...

Fuente: Portal de Datos Abiertos www.datos.gov.co — SECOP II (Agencia Nacional de Contratación Pública – Colombia Compra Eficiente). Licencia CC BY-SA 4.0. La fecha de última actualización del conjunto viene en sourceUpdatedAt.

```

### BCRP (Perú)

`python bcrp_peru.py` (2026-11-20, Chile time):

```text
Tipo de cambio - TC Interbancario (S/ por US$) - Venta [PD04638PD] (diaria, S/ por US$)
  Latest: 3.4321 on 2026-11-18
    2026-11-18  3.4321
    2026-11-17  3.4117
    2026-11-16  3.4136
    2026-11-13  3.4013
    2026-11-12  3.4059
  https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04638PD/html/2026-10-06/2026-11-20/esp

Tasas de interés - Tasa de Referencia de la Política Monetaria [PD12301MD] (diaria, %)
  Latest: 4.5000 on 2026-11-20
    2026-11-20  4.5000
    2026-11-19  4.5000
    2026-11-18  4.5000
    2026-11-17  4.5000
    2026-11-16  4.5000
  https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD12301MD/html/2026-10-06/2026-11-20/esp

Note: PD12301MD: se devuelven 5 de 33 datos (los más recientes). Sube maxItems o acota fechas.

Note: PD12301MD: 1 periodo(s) sin dato publicado ("n.d.", p. ej. días sin operación o dato aún no disponible) se omitieron.

Note: PD04638PD: se devuelven 5 de 31 datos (los más recientes). Sube maxItems o acota fechas.

Note: PD04638PD: 3 periodo(s) sin dato publicado ("n.d.", p. ej. días sin operación o dato aún no disponible) se omitieron.

Fuente: Banco Central de Reserva del Perú (BCRP), BCRPData — estadisticas.bcrp.gob.pe. Reproducción permitida citando la fuente (Condiciones de uso de BCRPData). En series de fuente externa (p. ej. IPC elaborado por el INEI) la responsabilidad del dato recae en la entidad que lo provee. Datos sin modificar salvo formato; no constituyen asesoramiento.
```

### Banxico (México)

`python banxico_mexico.py` (2026-11-21, hora de Chile / Chile time):

```text
Tipo de cambio FIX (pesos por dólar E.U.A., fecha de determinación) [SF43718] (diaria, MXN por 1 USD)
  Latest: 19.0228 on 2026-11-20

Valor de la UDI (Unidad de Inversión) [SP68257] (diaria, MXN por 1 UDI)
  Latest: 8.92318 on 2026-11-21
  Published ahead: 8.93248 for 2026-11-25

Tasa objetivo de política monetaria del Banco de México [SF61745] (diaria, % anual)
  Latest: 6.25 on 2026-11-21
  Published ahead: 6.25 for 2026-11-22

Note: udis: Banxico ya publicó el valor para 2026-11-25 (posterior a hoy, 2026-11-21 en Ciudad de México); latest es el vigente hoy (2026-11-21) y el adelantado va en "published_ahead".

Note: tasa_objetivo: Banxico ya publicó el valor para 2026-11-22 (posterior a hoy, 2026-11-21 en Ciudad de México); latest es el vigente hoy (2026-11-21) y el adelantado va en "published_ahead".
```

### TRM (Colombia)

`python trm_colombia.py` (2026-11-22, hora de Chile / Chile time):

```text
TRM Colombia (COP por 1 USD)
  Latest: 3,461.92 in force 2026-11-21 .. 2026-11-23

Source updated at: 2026-11-20T23:05:56.000Z

Fuente: Superintendencia Financiera de Colombia vía datos.gov.co (Portal de Datos Abiertos www.datos.gov.co, conjunto "Tasa de Cambio Representativa del Mercado - TRM", 32sa-8pi3). Licencia CC BY-SA 4.0. La fecha de última actualización del conjunto viene en sourceUpdatedAt.
```

`python trm_colombia.py --from 2026-11-10 --to 2026-11-20`:

```text
TRM Colombia (COP por 1 USD)
  Latest: 3,415.10 in force 2026-11-20 .. 2026-11-20
    2026-11-20 .. 2026-11-20  3,415.10
    2026-11-19 .. 2026-11-19  3,326.96
    2026-11-18 .. 2026-11-18  3,309.55
    2026-11-14 .. 2026-11-17  3,316.70
    2026-11-13 .. 2026-11-13  3,301.91
    2026-11-11 .. 2026-11-12  3,297.07
    2026-11-10 .. 2026-11-10  3,269.88
```

### CMF (Chile)

`python cmf_chile.py` (2026-11-22, domingo, hora de Chile / Sunday, Chile time):

```text
Unidad de Fomento (UF): 41,384.81 CLP (2026-11-22)
Dólar observado (USD): 1,008.79 CLP (2026-11-20)
  Note: Sin valor publicado para 2026-11-22 (la CMF publica el dólar observado solo en días hábiles bancarios; no hay valor en fines de semana ni feriados). Se entrega el último valor publicado, correspondiente al 2026-11-20. / No value published for 2026-11-22; returning the most recent published value, dated 2026-11-20.
Euro: 1,107.59 CLP (2026-11-20)
  Note: Sin valor publicado para 2026-11-22 (la CMF publica el euro solo en días hábiles bancarios; no hay valor en fines de semana ni feriados). Se entrega el último valor publicado, correspondiente al 2026-11-20. / No value published for 2026-11-22; returning the most recent published value, dated 2026-11-20.
Unidad Tributaria Mensual (UTM): 72,440.00 CLP (2026-11-01)

Fuente: Comisión para el Mercado Financiero (CMF Chile), API CMF Bancos — https://www.cmfchile.cl
```

`python cmf_chile.py --tmc` (extracto / excerpt):

```text
Tasa Máxima Convencional (TMC) (% anual, vigente desde 2026-11-14)
   46.89%  [26] Operaciones no reajustables en moneda nacional de menos de 90 días - Inferiores o iguales al equivalente de 5.000 unidades de fomento
    8.46%  [25] Operaciones no reajustables en moneda nacional de menos de 90 días - Superiores al equivalente de 5.000 unidades de fomento
   41.12%  [45] Operaciones no reajustables en moneda nacional 90 días o más - Inferiores o iguales al equivalente de 50 unidades de fomento
   ...  (12 filas / rows)

Fuente: Comisión para el Mercado Financiero (CMF Chile), API CMF Bancos — https://www.cmfchile.cl
```

Fuente: Comisión para el Mercado Financiero (CMF Chile), API CMF Bancos ([api.cmfchile.cl](https://api.cmfchile.cl/)). / Source: CMF Chile.

### Feriados, días hábiles y RUT (Chile) / Holidays, business days and RUT

Ejecutado el 2026-11-24, hora de Chile / Run on 2026-11-24, Chile time.

`python calendario_rut.py` (feriados que quedan en 2026 / holidays left in 2026):

```text
2026-12-08 martes    Inmaculada Concepción
2026-12-25 viernes   Navidad (irrenunciable)
```

`python calendario_rut.py plazo 2026-12-15 10`:

```text
2026-12-15 + 10 días hábiles = 2026-12-30 (miércoles)
  Se cuenta desde el día siguiente a startDate (excluido).
```

`python calendario_rut.py plazo 2026-12-15 10 --sabado` (sábado hábil / Saturday counts):

```text
2026-12-15 + 10 días hábiles = 2026-12-28 (lunes)
  Se cuenta desde el día siguiente a startDate (excluido).
```

`python calendario_rut.py habiles 2026-12-01 2026-12-31`:

```text
2026-12-01 a 2026-12-31: 21 días hábiles de 31 (8 de fin de semana, 2 feriados en día laboral)
  2026-12-08 Inmaculada Concepción
  2026-12-25 Navidad
```

`python calendario_rut.py rut 12.345.678-5 11.111.111-2` (RUT de ejemplo / sample RUTs):

```text
12.345.678-5   válido   12.345.678-5
11.111.111-2   inválido dígito verificador incorrecto (DV esperado 1)
```

Atribución / attribution: _Calculado por Better Llama a partir de leyes de feriados y la División Político-Administrativa publicadas por el Estado de Chile._

### Sismos (Chile) / Earthquakes

Ejecutado el 2026-11-24, hora de Chile / Run on 2026-11-24, Chile time.

`python sismos.py hoy`:

```
2 sismos (hoy):
  2026-11-24 17:27 (Chile)  M4.6     51 km  49 km SW of Ovalle, Chile
  2026-11-24 10:22 (Chile)  M4.8     33 km  71 km W of Vallenar, Chile

Fuente: U.S. Geological Survey (USGS), Earthquake Hazards Program — dominio público.
```

`python sismos.py fuertes --max 5` (M>=5, últimos 365 días / last 365 days):

```
5 sismos (fuertes):
  2026-05-25 17:52 (Chile)  M6.9    109 km  34 km ENE of Calama, Chile  [PAGER green, 85 reportes]
  2026-03-13 10:39 (Chile)  M6.2     24 km  71 km W of Vallenar, Chile  [PAGER green, 34 reportes]
  2026-02-12 10:34 (Chile)  M6.1     46 km  28 km SW of Ovalle, Chile  [PAGER green, 126 reportes]
  2026-05-31 17:34 (Chile)  M6       25 km  33 km NW of Valparaíso, Chile  [PAGER green, 159 reportes]
  2026-02-08 13:23 (Chile)  M5.7    114 km  79 km ENE of La Tirana, Chile  [PAGER green, 25 reportes]
stopReason: maxItems (raise --max)

Fuente: U.S. Geological Survey (USGS), Earthquake Hazards Program — dominio público.
```

`python sismos.py cerca -33.45 -70.66 150 --max 5` (150 km de Santiago, últimos 30 días / last 30 days):

```
3 sismos (cerca):
  2026-10-28 09:52 (Chile)  M4.2     52 km  31 km SSW of Melipilla, Chile
  2026-10-26 17:52 (Chile)  M4.6     48 km  18 km NNW of La Ligua, Chile  [2 reportes]
  2026-10-25 21:55 (Chile)  M4.2     22 km  40 km W of Valparaíso, Chile

Fuente: U.S. Geological Survey (USGS), Earthquake Hazards Program — dominio público.
```

### Node.js (25-11-2026)

```text
$ node indicadores.mjs
CMF Chile (get_chile_financial_indicators):
  Unidad de Fomento (UF): 41.405,45 CLP (2026-11-25)
  Dólar observado (USD): 1.025,06 CLP (2026-11-25)
  Unidad Tributaria Mensual (UTM): 72.440 CLP (2026-11-01)
  Fuente: Comisión para el Mercado Financiero (CMF Chile), API CMF Bancos — https://www.cmfchile.cl

Banco Central de Chile (get_chile_central_bank_series):
  Tasa de política monetaria (TPM) (porcentaje): 4.50 (2026-11-25)
  Imacec empalmado, serie original (índice 2018=100): 109.77 (2026-09-01)
  Fuente: Banco Central de Chile, Base de Datos Estadísticos — https://si3.bcentral.cl

$ node calendario_rut.mjs plazo 2026-12-15 10
2026-12-15 + 10 días hábiles = 2026-12-30 (miércoles)
  Se cuenta desde el día siguiente a startDate (excluido).

$ node agent_mcp_sdk.mjs
Connected to betterllama 0.5.1
15 tools: search_tools, search_chile_public_tenders, get_chile_financial_indicators, ...
Unidad de Fomento (UF): 41405.45 CLP (2026-11-25)

$ node latam.mjs
Colombia - TRM (colombia_trm):
  3,592.03 COP por 1 USD, in force 2026-11-25 .. 2026-11-25
  Fuente: Superintendencia Financiera de Colombia vía datos.gov.co (Portal de Datos Abiertos www.datos.gov.co, conjunto "Tasa de Cambio Representativa del Mercado - TRM", 32sa-8pi3)

Peru - BCRP (peru_bcrp_series):
  Tipo de cambio - TC Interbancario (S/ por US$) - Venta: 3.452 S/ por US$ (2026-11-23)
  Tasas de interés - Tasa de Referencia de la Política Monetaria: 4.5 % (2026-11-24)
  Fuente: Banco Central de Reserva del Perú (BCRP), BCRPData — estadisticas.bcrp.gob.pe

Mexico - Banxico (mexico_banxico_indicators):
  Tipo de cambio FIX (pesos por dólar E.U.A., fecha de determinación): 19.3668 MXN por 1 USD (2026-11-24)
  Valor de la UDI (Unidad de Inversión): 8.932476 MXN por 1 UDI (2026-11-25)
    published ahead: 8.980803 for 2026-12-10
  Tasa objetivo de política monetaria del Banco de México: 6.25 % anual (2026-11-25)
  Fuente: Banco de México (SIE), https://www.banxico.org.mx/SieAPIRest/ — reutilización permitida citando la fuente
```

### LangChain (25-11-2026)

```text
$ python python/langchain_agent.py
15 LangChain tools from https://mcp.betterllama.com/mcp:
  chile_calendar_and_rut, chilexpress_shipping, colombia_secop_search, colombia_trm, find_chile_fuel_prices, get_chile_central_bank_series, get_chile_earthquakes, get_chile_electricity_market, get_chile_financial_indicators, get_santiago_stock_exchange_data, mexico_banxico_indicators, peru_bcrp_series, search_chile_official_gazette, search_chile_public_tenders, search_tools

CMF uf    2026-11-25  41405.45
CMF dolar 2026-11-25  1025.06
BCCh TPM   2026-11-25  4.5 %

Set OPENAI_API_KEY (or LLM_MODEL + your provider key) to run the agent step.
```

### OpenAI Agents SDK (25-11-2026)

```text
$ python python/openai_agents_sdk.py
15 MCP tools from https://mcp.betterllama.com/mcp:
  chile_calendar_and_rut, chilexpress_shipping, colombia_secop_search, colombia_trm, find_chile_fuel_prices, get_chile_central_bank_series, get_chile_earthquakes, get_chile_electricity_market, get_chile_financial_indicators, get_santiago_stock_exchange_data, mexico_banxico_indicators, peru_bcrp_series, search_chile_official_gazette, search_chile_public_tenders, search_tools

CMF uf    2026-11-25  41405.45
CMF dolar 2026-11-25  1025.06
BCCh TPM   2026-11-25  4.5 %

Set OPENAI_API_KEY to run the agent step.
```

### Vercel AI SDK (26-11-2026)

```text
$ node vercel_ai_sdk.mjs
15 tools: search_tools, search_chile_public_tenders, get_chile_financial_indicators, get_chile_central_bank_series, find_chile_fuel_prices, chilexpress_shipping, get_chile_electricity_market, search_chile_official_gazette, get_chile_earthquakes, get_santiago_stock_exchange_data, chile_calendar_and_rut, colombia_secop_search, colombia_trm, peru_bcrp_series, mexico_banxico_indicators

CMF Chile (get_chile_financial_indicators):
  Unidad de Fomento (UF): 41.412,34 CLP (2026-11-26)
  Dólar observado (USD): 1.044,08 CLP (2026-11-26)
  Fuente: Comisión para el Mercado Financiero (CMF Chile), API CMF Bancos — https://www.cmfchile.cl

Colombia - TRM (colombia_trm):
  3.630,89 COP por 1 USD, 2026-11-26 .. 2026-11-27
  Fuente: Superintendencia Financiera de Colombia vía datos.gov.co (Portal de Datos Abiertos www.datos.gov.co, conjunto "Tasa de Cambio Representativa del Mercado - TRM", 32sa-8pi3). Licencia CC BY-SA 4.0. La fecha de última actualización del conjunto viene en sourceUpdatedAt.

Set OPENAI_API_KEY to run generateText with the tools (or --mock to check the wiring without an LLM).

$ node vercel_ai_sdk.mjs --mock   # (últimas líneas / last lines)
tool call: get_chile_financial_indicators({"source":"uf","period":"current"})
tool result: {"content":[{"type":"text","text":"{\"tool\":\"get_chile_financial_indicators\",\"count\":1,\"results\":[{\"indicator\":\"uf\",\"indicatorName\":\"Unidad de Fomento (UF)\",\"date\":\"2026-11-26\",\"ye...

Answer: (mock) UF 41412.34 CLP al 2026-11-26.
```

### Mastra (26-11-2026)

```text
$ node mastra_agent.mjs
15 tools: betterllama_search_tools, betterllama_search_chile_public_tenders, betterllama_get_chile_financial_indicators, betterllama_get_chile_central_bank_series, betterllama_find_chile_fuel_prices, betterllama_chilexpress_shipping, betterllama_get_chile_electricity_market, betterllama_search_chile_official_gazette, betterllama_get_chile_earthquakes, betterllama_get_santiago_stock_exchange_data, betterllama_chile_calendar_and_rut, betterllama_colombia_secop_search, betterllama_colombia_trm, betterllama_peru_bcrp_series, betterllama_mexico_banxico_indicators

CMF Chile (get_chile_financial_indicators):
  Unidad de Fomento (UF): 41.412,34 CLP (2026-11-26)
  Dólar observado (USD): 1.044,08 CLP (2026-11-26)
  Fuente: Comisión para el Mercado Financiero (CMF Chile), API CMF Bancos — https://www.cmfchile.cl

Colombia - TRM (colombia_trm):
  3.630,89 COP por 1 USD, 2026-11-26 .. 2026-11-27
  Fuente: Superintendencia Financiera de Colombia vía datos.gov.co (Portal de Datos Abiertos www.datos.gov.co, conjunto "Tasa de Cambio Representativa del Mercado - TRM", 32sa-8pi3). Licencia CC BY-SA 4.0. La fecha de última actualización del conjunto viene en sourceUpdatedAt.

Set OPENAI_API_KEY to run the Mastra Agent with the tools (or --mock to check the wiring without an LLM).

$ node mastra_agent.mjs --mock   # (últimas líneas / last lines)
tool call: betterllama_get_chile_financial_indicators({"source":"uf","period":"current"})
tool result: {"content":[{"type":"text","text":"{\"tool\":\"get_chile_financial_indicators\",\"count\":1,\"results\":[{\"indicator\":\"uf\",\"indicatorName\":\"Unidad de Fomento (UF)\",\"date\":\"2026-11-26\",\"ye...

Answer: (mock) UF 41412.34 CLP al 2026-11-26.
```

## Licencia / License

MIT. Datos: propiedad de cada fuente oficial (CMF, Banco Central de Chile, CNE, USGS, ChileCompra, Colombia Compra Eficiente / datos.gov.co, BCRP, Banco de México, Superintendencia Financiera de Colombia, etc.); revisa sus términos.
