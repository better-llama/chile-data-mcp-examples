# chile-data-mcp-examples

Ejemplos ejecutables para usar el servidor MCP gratuito (beta) de [Better Llama](https://betterllama.com) con datos públicos de Chile: indicadores económicos (CMF, Banco Central), precios de bencina (CNE), sismos (USGS), Mercado Público, Chilexpress, Diario Oficial, mercado eléctrico, Bolsa de Santiago, feriados y RUT.

Runnable examples for Better Llama's free (beta) MCP server with Chilean public data. English below.

| | |
|---|---|
| Endpoint | `https://mcp.betterllama.com/mcp` |
| Transporte / Transport | Streamable HTTP, sin autenticación / anonymous |
| Header requerido / required | `Accept: application/json, text/event-stream` |
| Registry id | `com.betterllama/chile-data` |
| Herramientas / Tools | 11 (`tools/list`) |

---

## Español

### Inicio rápido

```bash
git clone https://github.com/better-llama/chile-data-mcp-examples
cd chile-data-mcp-examples
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd python
python list_tools.py       # lista las 11 herramientas
python indicadores.py      # UF, dólar, UTM (CMF) + TPM, IMACEC (Banco Central)
python bencina.py 93 Ñuñoa # bencina más barata en una comuna (CNE)
python agent_mcp_sdk.py    # SDK oficial "mcp": search_tools + sismos
```

Requiere Python 3.10+. Probado con Python 3.13, httpx 0.28 y mcp 2.3.0.

### Archivos

| Archivo | Qué hace |
|---|---|
| `python/mcp_http.py` | Cliente JSON-RPC mínimo con httpx (`initialize`, `tools/list`, `tools/call`), sin SDK. |
| `python/list_tools.py` | Lista herramientas y sus argumentos. |
| `python/indicadores.py` | `get_chile_financial_indicators` y `get_chile_central_bank_series`. |
| `python/bencina.py` | `find_chile_fuel_prices` ordenado por precio. |
| `python/agent_mcp_sdk.py` | Cliente con el SDK oficial de MCP para Python (streamable HTTP). |
| `config/` | Configuración para Cursor, VS Code y Claude Desktop. |

### Herramientas

- Sin clave: `search_tools`, `get_chile_financial_indicators`, `get_chile_central_bank_series`, `find_chile_fuel_prices`, `get_chile_electricity_market`, `search_chile_official_gazette`, `get_chile_earthquakes`, `chile_calendar_and_rut` (algunas usan una clave compartida del servidor; no necesitas la tuya).
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

---

## English

### Quick start

```bash
git clone https://github.com/better-llama/chile-data-mcp-examples
cd chile-data-mcp-examples
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd python
python list_tools.py        # list the 11 tools
python indicadores.py       # UF, USD, UTM (CMF) + policy rate, IMACEC (Central Bank)
python bencina.py 93 Ñuñoa  # cheapest gasoline in a comuna (CNE)
python agent_mcp_sdk.py     # official "mcp" SDK: search_tools + earthquakes
```

Python 3.10+. Tested with Python 3.13, httpx 0.28 and mcp 2.3.0. With mcp 1.x, import `streamablehttp_client` instead; it yields `(read, write, get_session_id)`.

### Notes

- The server is stateless Streamable HTTP; no auth. Every POST must send `Accept: application/json, text/event-stream`.
- Tool results come as a JSON string in `content[0].text`, with the official source attribution. Please cite the source when showing data.
- `search_chile_public_tenders` and `get_santiago_stock_exchange_data` need your own free provider key (bring your own key). All other tools work without a key.
- Client setup (Cursor, VS Code, Claude Desktop, n8n, curl): see the Spanish section above and `config/`.
- n8n: import [`n8n/chile-data-mcp-workflow.json`](n8n/chile-data-mcp-workflow.json) (*Import from File*): Chat Trigger + AI Agent + MCP Client Tool pointing to `https://mcp.betterllama.com/mcp` (HTTP Streamable, no auth). Just pick your chat-model credential.
- Free beta: the server applies per-IP rate limits; be gentle with loops.

---

## Salida real / Real output

Ejecutado el 2026-11-19 / Run on 2026-11-19 (Chile time). Los valores cambian a diario / values change daily.

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

## Licencia / License

MIT. Datos: propiedad de cada fuente oficial (CMF, Banco Central de Chile, CNE, USGS, ChileCompra, etc.); revisa sus términos.
