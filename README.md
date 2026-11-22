# chile-data-mcp-examples

Ejemplos ejecutables para usar el servidor MCP gratuito (beta) de [Better Llama](https://betterllama.com) con datos públicos de Chile, Colombia, Perú y México: indicadores económicos (CMF, Banco Central), precios de bencina (CNE), sismos (USGS), Mercado Público, Chilexpress, Diario Oficial, mercado eléctrico, Bolsa de Santiago, feriados y RUT. Compras públicas de Colombia (SECOP II). Series del Banco Central de Reserva del Perú (BCRP) e indicadores del Banco de México (Banxico: tipo de cambio FIX, UDIS, TIIE, tasa objetivo, inflación). TRM de Colombia (tasa de cambio oficial COP/USD). Nuevo: ejemplo CMF Chile (UF, dólar observado, euro, UTM, IPC y tasa máxima convencional).

Runnable examples for Better Llama's free (beta) MCP server with Chilean, Colombian, Peruvian and Mexican public data. English below.

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
| `python/secop_colombia.py` | `colombia_secop_search`: contratos o procesos de compras públicas de Colombia (SECOP II, datos.gov.co). |
| `python/bcrp_peru.py` | `peru_bcrp_series`: series del BCRP (tipo de cambio, tasa de referencia, inflación, PBI, reservas) por alias o código; `--catalog` lista alias. |
| `python/banxico_mexico.py` | `mexico_banxico_indicators`: tipo de cambio FIX, UDIS, TIIE, tasa objetivo e inflación del Banco de México; `--date` o `--from/--to` para series. |
| `python/trm_colombia.py` | `colombia_trm`: TRM de Colombia (pesos por dólar, Superintendencia Financiera vía datos.gov.co); sin argumentos la vigente, `--date` para un día o `--from/--to` para un rango. |
| `python/cmf_chile.py` | `get_chile_financial_indicators`: indicadores oficiales de la CMF Chile; sin argumentos UF, dólar observado, euro y UTM vigentes; `--indicator` (uf, dolar, euro, utm, ipc, tmc, tip), `--date` para un día, `--year`/`--month` para una serie y `--tmc` para la tasa máxima convencional. |
| `python/agent_mcp_sdk.py` | Cliente con el SDK oficial de MCP para Python (streamable HTTP). |
| `config/` | Configuración para Cursor, VS Code y Claude Desktop. |

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
- [CMF Chile: UF, dólar, euro, UTM y TMC](https://betterllama.com/herramientas/cmf-chile-indicadores/) (ficha de la herramienta)

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
python agent_mcp_sdk.py     # official "mcp" SDK: search_tools + earthquakes
```

Python 3.10+. Tested with Python 3.13, httpx 0.28 and mcp 2.3.0. With mcp 1.x, import `streamablehttp_client` instead; it yields `(read, write, get_session_id)`.

### Notes

- The server is stateless Streamable HTTP; no auth. Every POST must send `Accept: application/json, text/event-stream`.
- Tool results come as a JSON string in `content[0].text`, with the official source attribution. Please cite the source when showing data.
- `search_chile_public_tenders` and `get_santiago_stock_exchange_data` need your own free provider key (bring your own key). All other tools work without a key.
- Client setup (Cursor, VS Code, Claude Desktop, n8n, curl): see the Spanish section above and `config/`.
- n8n: import [`n8n/chile-data-mcp-workflow.json`](n8n/chile-data-mcp-workflow.json) (*Import from File*): Chat Trigger + AI Agent + MCP Client Tool pointing to `https://mcp.betterllama.com/mcp` (HTTP Streamable, no auth). Just pick your chat-model credential.
- Colombia: `colombia_secop_search` searches SECOP II signed contracts (`dataset: contratos`) or published processes (`procesos`) from datos.gov.co (CC BY-SA 4.0), no key. Guide: [Colombia SECOP API](https://betterllama.com/en/guides/colombia-secop-api/).
- Peru: `peru_bcrp_series` returns official BCRP series (exchange rate, policy rate, inflation, GDP, reserves) by alias or BCRP code, no key; `python bcrp_peru.py --catalog` lists aliases. Guide: [Peru BCRP API](https://betterllama.com/en/guides/peru-bcrp-api/).
- Mexico: `mexico_banxico_indicators` returns official Bank of Mexico (SIE) indicators: FIX MXN/USD exchange rate, UDIS, TIIE 28/91/182, overnight funding TIIE, policy target rate and annual inflation, no key (the server uses its own token; send `X-Banxico-Token` to use yours). Guide: [Mexico Banxico API](https://betterllama.com/en/guides/mexico-banxico-api/).
- Colombia TRM: `colombia_trm` returns Colombia's official COP/USD exchange rate (TRM) certified by the Superintendencia Financiera, via datos.gov.co (CC BY-SA 4.0), no key. No arguments: latest TRM; `date` for the TRM in force on a day (weekend/holiday rates are certified the previous business day, so each row has `date_from`/`date_to`); `fromDate`/`toDate` for a range (`python trm_colombia.py --from 2026-11-10 --to 2026-11-20`). Guide: [Colombia TRM API](https://betterllama.com/en/guides/colombia-trm-api/).
- Chile CMF: `get_chile_financial_indicators` returns official indicators from Chile's Comisión para el Mercado Financiero (CMF): UF, observed USD (dólar observado), EUR, UTM, CPI (IPC), maximum conventional interest rate (TMC) and TIP, no key (the server uses its own CMF key). `python cmf_chile.py` prints the latest UF, USD, EUR and UTM; `--indicator dolar --date 2026-11-20` for one day, `--indicator uf --year 2026 --month 11` for a series, `--tmc` for the TMC. USD and EUR are only published on banking days: on weekends you get the last published value plus a note. Tool page: [Chile CMF indicators](https://betterllama.com/en/tools/cmf-chile-indicadores/).
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

## Licencia / License

MIT. Datos: propiedad de cada fuente oficial (CMF, Banco Central de Chile, CNE, USGS, ChileCompra, Colombia Compra Eficiente / datos.gov.co, BCRP, Banco de México, Superintendencia Financiera de Colombia, etc.); revisa sus términos.
