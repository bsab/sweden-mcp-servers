# Runtime smoke verification — 2026-09-14

This report records **actual, bounded attempts for all 18 catalog entries**. It is
separate from the [documentation Ready score](CONTRIBUTING.md#rubric-v1): **40–100/100
is a documentation score range, not a runtime success rate**. In particular, a
100/100 entry can still require credentials and have no verified provider call.
Scores below are the documentation-assessment snapshot on this date.

A **passed** outcome requires initialize, the initialized notification, tools/list,
and at least one explicitly selected read-only call returning plausible non-error
**live provider data**. Discovery, local ping, static URL generation, mocks, HTTP200,
or an ordinary JSON-RPC response containing an upstream error do not qualify.
This is not an audit of all tools, security, service terms, reliability or complete
correctness. Failures describe this environment/time, not global service availability.

## Outcome matrix

Each row has one final catalog-entry outcome; earlier failed transports/dependency
selections remain documented below. Sweden Legal contains two separately launched
components, but is counted once. All dates/times are UTC.

**Totals:** **5 blocked_missing_credentials**; **1 blocked_network**; **1 failed_protocol**; **2 failed_tool**; **9 passed**. **18 entries total.**

| Server | Documentation /100 | Runtime outcome | Observed phases/result |
|---|---:|---|---|
| [Arbetsförmedlingen MCP Server](#arbetsformedlingen-mcp-server) | 90 | `passed` | 13 tools; public autocomplete returned 10 live occupation/skill suggestions. |
| [Bokio MCP](#bokio-mcp) | 82.5 | `blocked_missing_credentials` | Initialized; 40 tools; local ping=pong only, no provider data. |
| [BolagsAPI MCP Server](#bolagsapi-mcp-server) | 100 | `blocked_missing_credentials` | Launch guard: BOLAGSAPI_KEY required; no initialize response. |
| [Fortnox MCP](#fortnox-mcp) | 90 | `blocked_missing_credentials` | Launch guard: Fortnox client credentials required; no initialize response. |
| [ICA MCP (unofficial)](#ica-mcp) | 100 | `blocked_missing_credentials` | Initialized; 21 tools; stopped before account/private-API access. |
| [Kolada MCP](#kolada-mcp) | 80 | `passed` | 21 tools; get_kpi(N15033) returned a real public school staffing indicator. |
| [Sweden Legal MCP (Lifos and Rättspraxis)](#legal-mcp-sweden) | 92.5 | `blocked_network` | Both components initialized with 9 tools each; Lifos feed failed TLS, no live items. |
| [Lantmäteriet MCP](#mcp-lantmateriet) | 50 | `failed_tool` | 4 tools; anonymous lm_stac_search returned isError=true / HTTP404. |
| [Naturvårdsverket MCP](#mcp-nvv) | 40 | `passed` | 4 tools; nvv_search returned two public Judarskogen protected-area records. |
| [SMHI MCP](#mcp-smhi) | 40 | `passed` | 4 tools; smhi_get_forecast returned 82 live Stockholm temperatures. |
| [MCP Sweden](#mcp-sweden) | 85 | `passed` | Hosted DNS failure; local 58 tools; SCB subject lookup passed with system CA trust. |
| [Swedish Weather MCP](#mcp-swedish-weather) | 52.5 | `failed_tool` | 2 tools; current_weather(Stockholm) returned upstream SMHI HTTP404. |
| [Riksdag & Regering MCP](#riksdag-regering-mcp) | 95 | `failed_protocol` | 32 tools; search_dokument hit non-JSON stdout before a valid tool response. |
| [SCB Open Data MCP](#scb-opendata-mcp) | 77.5 | `passed` | 12 tools; SCB v2 table search returned TAB4552 with system CA trust. |
| [Skolverket MCP](#skolverket-mcp) | 85 | `passed` | 87 tools; search_subjects returned Bild (GRGRBIL01), one of 27 subjects. |
| [Swemo MCP — Riksbank](#swemo-mcp) | 75 | `passed` | 27 tools; 60 Riksbank policy rounds after selecting upstream-locked MCP1.6.0. |
| [Trafikverket MCP](#trafikverket-mcp) | 95 | `blocked_missing_credentials` | Launch guard: TRAFIKVERKET_API_KEY required; no initialize response. |
| [Traktamente MCP](#traktamente-mcp) | 75 | `passed` | 3 tools; one live Norway 2026 allowance row: 1,054 SEK/day. |

## Method, safety and reproduction

- Client: [`scripts/runtime_smoke.py`](scripts/runtime_smoke.py),
  `sweden-catalog-runtime-smoke/1.0`; requested MCP `2025-06-18`, accepting negotiated
  `2025-03-26` or `2024-11-05`. The sequence is initialize →
  notifications/initialized → tools/list (up to five pages) → one explicitly selected
  tools/call. HTTP supports JSON or SSE responses and session/protocol headers;
  stdio rejects non-JSON stdout rather than filtering it. This is a smoke client,
  **not a full MCP schema/conformance validator**. Its `tool_response_requires_review`
  result is deliberately not an automatic live pass; results below were reviewed.
- Runs used Windows, Python **3.13.14** and an owned portable Node **24.12.0**.
  Node's ZIP SHA256 was checked against its official distribution checksum file.
  Additional Bun/HTTP details, where applicable, appear in the individual records.
  Standard system-CA alternatives were tried after trust failures: Node used
  `NODE_USE_SYSTEM_CA=1` (and normal environment proxy handling), Bun used
  `--use-system-ca`, and the Python SCB/Lifos retries used `SSL_CERT_FILE` pointing
  to an owned PEM bundle exported from `ssl.create_default_context().get_ca_certs`.
  This contains public trusted CA certificates only, not private keys. Certificate
  and hostname verification remained enabled; no policy-denied host was bypassed.
- Sources came from the exact public commits linked below. Entrypoints, selected
  tool/client paths, package/build configuration and installation hooks were reviewed
  before execution. This was a shared machine, **not a security sandbox**. Source
  archives, dependencies and state stayed in owned temporary directories, outside
  the primary checkout and outside the public catalog.
- Node dependencies used the source lockfile's `npm ci`, or `npm install` without
  lock generation where none existed, with `--ignore-scripts --no-audit --no-fund`,
  isolated npm configuration/cache, and explicit reviewed build commands. Disabled
  dependency lifecycle hooks were not silently re-enabled. Python used individual
  venvs and `python -m pip install --only-binary=:all: .` (reviewed root package
  builds; binary dependencies). Windows long-path/build-residue failures were
  resolved using short owned TEMP/TMP directories, `--no-cache-dir`, and removal
  of only generated build residue; no system setting was changed.
- Credentials, user profiles, project dotenv files and app MCP configuration were
  not reused. Child environments allowlisted essential non-secret settings and
  redirected HOME/APPDATA/TEMP; credentialed proxy URLs were not passed to servers.
  No login, purchase, signup, invoice/payment/order creation, account-data read,
  notification delivery or other external write was performed. Mock data was not
  counted. TLS/proxy/access-policy restrictions were not bypassed.
- Requests had modest time/size limits; source startup/builds had separate bounded
  timeouts. Owned server processes were stopped by exact process ID/tree after use.
  Hosted session DELETE was intentionally not used. Raw outputs were reviewed
  locally; only sanitized summaries, not personal machine paths or bulk datasets,
  are published here. SDK versions below distinguish an upstream version choice
  from a source patch; no upstream server implementation was patched.

### Reproducing a reviewed call

The per-server launch arrays below use paths relative to that server's pinned
source root. `node.exe`/`bun.exe` mean the stated owned portable versions, and
`.venv\Scripts\...` means that server's isolated venv. The Riksdag launch uses
`mcp` as its working directory. These are **records, not permission to blindly
execute third-party code**: re-review source and dependency/build hooks, prepare an
isolated environment, and do not supply private credentials for this public-data smoke.
Where dependencies are not locked upstream, later resolution can differ; the main
package/SDK versions actually used are recorded below, not a reproducibility guarantee.

For example, after preparing and reviewing the pinned Kolada source, this Python
pattern runs only its public KPI lookup. Run from the catalog root, replace example
paths with owned paths, and review the result content rather than only its status:

```python
import json
from pathlib import Path
from scripts.runtime_smoke import StdioClient, smoke

node = Path(r'C:\owned\node.exe')
source = Path(r'C:\owned\Kolada-MCP')
client = StdioClient([str(node), str(source / 'dist' / 'index.js')],
                     source, Path(r'C:\owned\smoke-state'),
                     timeout=25, executable_dirs=[str(node.parent)])
result = smoke(client, 'get_kpi', {'kpi_id': 'N15033'})
Path(r'C:\owned\kolada-result.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
```

For a reviewed public Streamable HTTP endpoint, use `HttpClient(URL)` instead of
`StdioClient`, retaining explicit read-only tool selection. The equivalent manual
CLI exposes `--endpoint`, or `--command-json`/`--cwd`/`--state`, plus `--tool`,
`--arguments`, `--timeout` and `--report`.
A locally launched HTTP server must separately use the same restricted environment
and exact-PID cleanup; the helper does not launch/stop HTTP servers itself. Never
interpret the helper's exit code alone as provider success. Deterministic tests in
[`test_runtime_smoke.py`](scripts/test_runtime_smoke.py) use authored fixtures, not
these external services; no full network smoke is added to pull-request CI.

## Hosted endpoint attempts

All five cataloged hosted endpoints were actually attempted first. None initialized
in this environment. Deployment versions were **not exposed or tied to a source
commit**; later local attempts below are distinct deployments, not proof that the
hosted URLs work. The [initial three historical failures](VERIFICATION.md#remote-runtime-attempts)
remain separately recorded in the original verification report.

| Endpoint | Attempt start (UTC) | Initialize result |
|---|---|---|
| https://mcp-lantmateriet.vercel.app/mcp | `2026-09-14T12:22:37.827831+00:00` | HTTP403 access-policy HTML, not an MCP response. |
| https://mcp-nvv.vercel.app/mcp | `2026-09-14T12:22:37.828830+00:00` | HTTP403 access-policy HTML, not an MCP response. |
| https://mcp-smhi.vercel.app/mcp | `2026-09-14T12:22:37.829473+00:00` | HTTP403 access-policy HTML, not an MCP response. |
| https://sweden.mcp.namraks.com/mcp | `2026-09-14T12:22:38.202315+00:00` | DNS resolution failed: getaddrinfo failed (11001). |
| https://traktamente.app/mcp | `2026-09-14T12:22:38.202840+00:00` | HTTP403 access-policy HTML, not an MCP response. |

## Individual local attempts

<a id="arbetsformedlingen-mcp-server"></a>

### Arbetsförmedlingen MCP Server

- **Source:** [DanielErikssonCoder/arbetsformedlingen-mcp-server @ `b94dd02bcd884c16b26c1adb7feee39775ca98dd`](https://github.com/DanielErikssonCoder/arbetsformedlingen-mcp-server/tree/b94dd02bcd884c16b26c1adb7feee39775ca98dd).
- **Versions:** project 1.0.2; @modelcontextprotocol/sdk 1.26.0.
- **Attempt:** `2026-09-14T13:13:02.021298+00:00` → `2026-09-14T13:13:05.004390+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `["node.exe", "dist\\index.js"]`.
- **Non-secret configuration:** `{"NODE_USE_SYSTEM_CA": "1", "NODE_USE_ENV_PROXY": "1"}`.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 13 tools discovered.
- **Selected call:** `af_autocomplete` with `{"q": "sjuksk"}`.
- **Reviewed outcome: `passed`.** The first attempt returned isError=true / fetch failed. With the standard Node NODE_USE_SYSTEM_CA=1 and NODE_USE_ENV_PROXY=1 settings, the unchanged source returned 10 public suggestions for sjuksk, including sjukskoterska (1,980 listings) and occupation/skill categories. This tested aggregate public autocomplete only: no job/contact records or private account data were accessed. TLS verification and normal proxy policy remained enabled.

<a id="bokio-mcp"></a>

### Bokio MCP

- **Source:** [straycatse/bokio-mcp @ `cd48f56f606c069b9b5ef4c89814e2673af7d8f4`](https://github.com/straycatse/bokio-mcp/tree/cd48f56f606c069b9b5ef4c89814e2673af7d8f4).
- **Versions:** project 0.1.0; @modelcontextprotocol/sdk 1.30.0.
- **Attempt:** `2026-09-14T12:38:09.084674+00:00` → `2026-09-14T12:38:10.795056+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `["node.exe", "dist\\stdio.js"]`.
- **Credentials/config:** no provider credentials supplied; isolated state and common safety settings above.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 40 tools discovered.
- **Selected call:** `ping` with `{}`.
- **Reviewed outcome: `blocked_missing_credentials`.** BOKIO_INTEGRATION_TOKEN and BOKIO_COMPANY_ID, or a separately authorized OAuth flow, are required for company data. The unauthenticated local ping returned pong; this is not live accounting evidence. BOKIO_MOCK and BOKIO_ALLOW_WRITES remained unset. No finance, bank, contact or invoice tool was called; pricing/provider approval remain unverified.

<a id="bolagsapi-mcp-server"></a>

### BolagsAPI MCP Server

- **Source:** [HugoAndFriends/BolagsAPI-mcp-server @ `f7e21bd14e3c3917045db6de8374641d839e9ec0`](https://github.com/HugoAndFriends/BolagsAPI-mcp-server/tree/f7e21bd14e3c3917045db6de8374641d839e9ec0).
- **Versions:** project 0.1.2; @modelcontextprotocol/sdk 1.30.0.
- **Attempt:** `2026-09-14T12:38:10.865951+00:00` → `2026-09-14T12:38:12.201598+00:00`; transport `stdio`; negotiated protocol `not reached`.
- **Launch:** `["node.exe", "dist\\index.js"]`.
- **Credentials/config:** no provider credentials supplied; isolated state and common safety settings above.
- **Phases:** initialize `not completed`; initialized notification `not sent`; tools/list `not completed`; 0 tools discovered.
- **Selected call:** none; see blocker/limitations below.
- **Reviewed outcome: `blocked_missing_credentials`.** The actual source-built stdio launch exited with BOLAGSAPI_KEY environment variable is required. No token was fabricated or obtained and no company query was attempted. Quotas and prices remain unverified; this is BolagsAPI, not an official Bolagsverket service.

<a id="fortnox-mcp"></a>

### Fortnox MCP

- **Source:** [erp-mafia/fortnox-mcp @ `501ee1368f12ca4dd2e24a24bda8a47378b5c40a`](https://github.com/erp-mafia/fortnox-mcp/tree/501ee1368f12ca4dd2e24a24bda8a47378b5c40a).
- **Versions:** project 1.0.1; @modelcontextprotocol/sdk 1.25.3.
- **Attempt:** `2026-09-14T12:38:12.266357+00:00` → `2026-09-14T12:38:14.829862+00:00`; transport `stdio`; negotiated protocol `not reached`.
- **Launch:** `["node.exe", "dist\\index.js"]`.
- **Credentials/config:** no provider credentials supplied; isolated state and common safety settings above.
- **Phases:** initialize `not completed`; initialized notification `not sent`; tools/list `not completed`; 0 tools discovered.
- **Selected call:** none; see blocker/limitations below.
- **Reviewed outcome: `blocked_missing_credentials`.** The actual source-built launch reported Missing Fortnox credentials. Set FORTNOX_CLIENT_ID and FORTNOX_CLIENT_SECRET. FORTNOX_REFRESH_TOKEN is additionally needed for the documented local account flow. No OAuth login, financial read, invoice creation or bookkeeping call was attempted. Account/plan costs remain unverified.

<a id="ica-mcp"></a>

### ICA MCP (unofficial)

- **Source:** [kanylbullen/ica-mcp @ `1d9b9940890eabce348e30539c5d6a2ec7ecd80f`](https://github.com/kanylbullen/ica-mcp/tree/1d9b9940890eabce348e30539c5d6a2ec7ecd80f).
- **Versions:** project 0.5.0; mcp 1.30.0, httpx 0.28.1.
- **Attempt:** `2026-09-14T12:38:03.817659+00:00` → `2026-09-14T12:38:06.637406+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `[".venv\\Scripts\\python.exe", "-m", "ica_mcp", "serve"]`.
- **Credentials/config:** no provider credentials supplied; isolated state and common safety settings above.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 21 tools discovered.
- **Selected call:** none; see blocker/limitations below.
- **Reviewed outcome: `blocked_missing_credentials`.** Only python -m ica_mcp serve was launched in an empty isolated user profile. No login, token cache, personal shopping list or account tool was used. ICA account/session prerequisites, Swedish egress restrictions and further authorization for private data remain blockers. Its unofficial private API, possible service-terms conflicts and real-account writes remain material risks. ServerInfo version 1.30.0 is the SDK-reported value, not the project package version 0.5.0.

<a id="kolada-mcp"></a>

### Kolada MCP

- **Source:** [isakskogstad/Kolada-MCP @ `2bdcc29a019e24fe0d218f8191149701f4637ffd`](https://github.com/isakskogstad/Kolada-MCP/tree/2bdcc29a019e24fe0d218f8191149701f4637ffd).
- **Versions:** project 2.2.1; @modelcontextprotocol/sdk 1.24.3.
- **Attempt:** `2026-09-14T12:38:14.868888+00:00` → `2026-09-14T12:38:18.969870+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `["node.exe", "dist\\index.js"]`.
- **Credentials/config:** no provider credentials supplied; isolated state and common safety settings above.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 21 tools discovered.
- **Selected call:** `get_kpi` with `{"kpi_id": "N15033"}`.
- **Reviewed outcome: `passed`.** get_kpi with kpi_id=N15033 returned that ID, a Swedish title describing pupils per full-time teacher in compulsory school, a Skolverket source description and publication metadata. The reviewed handler performs a Kolada API v3 GET for this KPI; the isolated process did not use a pre-populated cache or mock. This verifies one metadata lookup, not time-series comparisons or every tool.

<a id="legal-mcp-sweden"></a>

### Sweden Legal MCP (Lifos and Rättspraxis)

- **Source:** [AvoccadoTech/legal-mcp-sweden @ `424f01a096157ab9e4f67c378c83c6bb80a96487`](https://github.com/AvoccadoTech/legal-mcp-sweden/tree/424f01a096157ab9e4f67c378c83c6bb80a96487).
- **Versions:** project 0.1.0; mcp 1.30.0, httpx 0.28.1.
- **Attempt:** `2026-09-14T13:13:21.055097+00:00` → `2026-09-14T13:13:33.506542+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `[".venv\\Scripts\\python.exe", "-m", "sweden_legal_mcp.lifos"]`.
- **Non-secret configuration:** `{"SSL_CERT_FILE": "<owned system-trust-public-ca.pem>"}`.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 9 tools discovered.
- **Selected call:** `lifos_recent` with `{"feed": "legal"}`.
- **Reviewed outcome: `blocked_network`.** The first launch of both modules failed with mcp 2.2.0 because mcp.server.fastmcp was removed. Retried unchanged source with mcp==1.30.0, within the declared range: Lifos and Rättspraxis each initialized and listed 9 tools. lifos_recent(feed=legal) reported CERTIFICATE_VERIFY_FAILED after the upstream client's 3 attempts and zero feed items, despite isError=false: this is a failed live call. Rättspraxis was discovery-only: no local corpus mirror existed, and its approximately 1,700-request sync was deliberately not run. No knowledge-base scan, ledger update or watch modification occurred. A further bounded attempt with the standard-system CA bundle still returned the same TLS error and zero items; the ordinary non-error JSON-RPC envelope is not a live success.

Rattspraxis discovery attempt: `2026-09-14T12:42:09.640688+00:00` to `2026-09-14T12:42:13.201904+00:00`, command `[".venv\\Scripts\\python.exe", "-m", "sweden_legal_mcp.rattspraxis"]`, stdio protocol `2025-06-18`, mcp `1.30.0`, initialize/initialized/tools-list completed, 9 tools; no tool call or mirror synchronization.

<a id="mcp-lantmateriet"></a>

### Lantmäteriet MCP

- **Source:** [furrytailapps/mcp-lantmateriet @ `22907c5b82978683c57d96d3569c9af2006d49d5`](https://github.com/furrytailapps/mcp-lantmateriet/tree/22907c5b82978683c57d96d3569c9af2006d49d5).
- **Versions:** project 1.0.0; @modelcontextprotocol/sdk 1.25.2; Next 15.5.11; mcp-handler 1.0.7.
- **Attempt:** `2026-09-14T12:51:04.995834+00:00` → `2026-09-14T12:51:21.444778+00:00`; transport `streamable-http`; negotiated protocol `2025-06-18`.
- **Launch:** `["node.exe", "node_modules\\next\\dist\\bin\\next", "dev", "--hostname", "127.0.0.1", "--port", "63626"]`.
- **Non-secret configuration:** `{"NODE_USE_SYSTEM_CA": "1", "NODE_USE_ENV_PROXY": "1", "NEXT_TELEMETRY_DISABLED": "1", "local_endpoint": "http://127.0.0.1:63626/mcp"}`.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 4 tools discovered.
- **Selected call:** `lm_stac_search` with `{"latitude": 59.33, "longitude": 18.07, "radius": 100, "maxResults": 1}`.
- **Reviewed outcome: `failed_tool`.** The unchanged Next development route initialized and listed 4 tools. lm_stac_search returned UPSTREAM_API_ERROR / HTTP404 from https://api.lantmateriet.se/stac-orto/v1/search, with isError=true and no live feature. This is protocol-only partial evidence, classified failed_tool for the selected operation. lm_map_url was not substituted because static URL generation is not provider verification. LANTMATERIET_CONSUMER_KEY and LANTMATERIET_CONSUMER_SECRET remain prerequisites for the untested property/elevation tools. Next warned about SWC 15.5.7 versus Next 15.5.11, but the route compiled; no source patch or production build was performed.

<a id="mcp-nvv"></a>

### Naturvårdsverket MCP

- **Source:** [furrytailapps/mcp-nvv @ `c67d45670db96aa1b5f5d8d716a06f34210d43d8`](https://github.com/furrytailapps/mcp-nvv/tree/c67d45670db96aa1b5f5d8d716a06f34210d43d8).
- **Versions:** project 1.0.0; @modelcontextprotocol/sdk 1.25.3; Next 14.2.35; mcp-handler 1.0.5.
- **Attempt:** `2026-09-14T12:51:24.795874+00:00` → `2026-09-14T12:51:34.594954+00:00`; transport `streamable-http`; negotiated protocol `2025-06-18`.
- **Launch:** `["node.exe", "node_modules\\next\\dist\\bin\\next", "dev", "--hostname", "127.0.0.1", "--port", "50518"]`.
- **Non-secret configuration:** `{"NODE_USE_SYSTEM_CA": "1", "NODE_USE_ENV_PROXY": "1", "NEXT_TELEMETRY_DISABLED": "1", "local_endpoint": "http://127.0.0.1:50518/mcp"}`.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 4 tools discovered.
- **Selected call:** `nvv_search` with `{"kommun": "0180", "limit": 1}`.
- **Reviewed outcome: `passed`.** The public Naturvardsverket geodata service returned a national reserve record (2000019) and Natura 2000 record (SE0110172), both Judarskogen, for municipality 0180. limit=1 applies per source, so two records were expected; Ramsar was empty and the upstream errors array was empty. This is a live search smoke, not comprehensive geospatial accuracy validation. The unchanged Next development route compiled with prebuilt SWC 14.2.33 and lifecycle scripts disabled; no production build was run. Hosted HTTP403 remains a separate failure.

<a id="mcp-smhi"></a>

### SMHI MCP

- **Source:** [furrytailapps/mcp-smhi @ `74bcfe15c314eb502c3b9983eab1dbb68c13e9e8`](https://github.com/furrytailapps/mcp-smhi/tree/74bcfe15c314eb502c3b9983eab1dbb68c13e9e8).
- **Versions:** project 1.0.0; @modelcontextprotocol/sdk 1.25.2; Next 14.2.35; mcp-handler 1.0.7.
- **Attempt:** `2026-09-14T12:50:25.558767+00:00` → `2026-09-14T12:50:34.027382+00:00`; transport `streamable-http`; negotiated protocol `2025-06-18`.
- **Launch:** `["node.exe", "node_modules\\next\\dist\\bin\\next", "dev", "--hostname", "127.0.0.1", "--port", "60058"]`.
- **Non-secret configuration:** `{"NODE_USE_SYSTEM_CA": "1", "NODE_USE_ENV_PROXY": "1", "NEXT_TELEMETRY_DISABLED": "1", "local_endpoint": "http://127.0.0.1:60058/mcp"}`.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 4 tools discovered.
- **Selected call:** `smhi_get_forecast` with `{"latitude": 59.33, "longitude": 18.07, "parameters": "temperature"}`.
- **Reviewed outcome: `passed`.** The unchanged Next development route called the public SMHI snow1g forecast endpoint and returned 82 timestamped temperatures, referenceTime=2026-09-14T12:30:00Z. The first value was 17.6 C at 13:00 UTC, not a fixture. This verifies one temperature forecast, not every weather/hydrology product. Hosted HTTP403 remains unresolved. Prebuilt SWC 14.2.33 loaded with lifecycle scripts disabled; no standalone production build was run.

<a id="mcp-sweden"></a>

### MCP Sweden

- **Source:** [Namraks-Labs/mcp-sweden @ `ed10cc3dce260830349c3aab3c3ae0891774e890`](https://github.com/Namraks-Labs/mcp-sweden/tree/ed10cc3dce260830349c3aab3c3ae0891774e890).
- **Versions:** project 0.1.0; mcp 2.2.0, fastmcp 4.0.3, httpx 0.28.1.
- **Attempt:** `2026-09-14T13:13:05.066195+00:00` → `2026-09-14T13:13:13.612659+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `[".venv\\Scripts\\python.exe", "-m", "mcp_sweden.server"]`.
- **Non-secret configuration:** `{"MCP_SWEDEN_TOOL_SEARCH": "none", "MCP_SWEDEN_HTTP_MAX_RETRIES": "0", "MCP_SWEDEN_HTTP_TIMEOUT": "15", "SSL_CERT_FILE": "<owned system-trust-public-ca.pem>"}`.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 58 tools discovered.
- **Selected call:** `scb_scb_list_subjects` with `{}`.
- **Reviewed outcome: `passed`.** The hosted endpoint failed DNS lookup. The first local scb_scb_list_subjects call failed CERTIFICATE_VERIFY_FAILED. Retrying unchanged source with SSL_CERT_FILE pointing to an owned bundle of public CAs from Python/Windows default trust returned live SCB v1 subject folders, including AA, AM and BE. MCP_SWEDEN_TOOL_SEARCH=none exposed 58 tools; MCP_SWEDEN_HTTP_MAX_RETRIES=0 and MCP_SWEDEN_HTTP_TIMEOUT=15 bounded the attempt. No certificate/hostname checks were disabled. This verifies the sampled SCB component only, not all aggregator integrations or optional authenticated services.

<a id="mcp-swedish-weather"></a>

### Swedish Weather MCP

- **Source:** [robobobby/mcp-swedish-weather @ `eeb6405964dc682c360151cc8a51a2a2251618bb`](https://github.com/robobobby/mcp-swedish-weather/tree/eeb6405964dc682c360151cc8a51a2a2251618bb).
- **Versions:** project 0.1.0; @modelcontextprotocol/sdk 1.26.0.
- **Attempt:** `2026-09-14T12:38:24.424636+00:00` → `2026-09-14T12:38:26.376256+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `["node.exe", "src\\index.js"]`.
- **Credentials/config:** no provider credentials supplied; isolated state and common safety settings above.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 2 tools discovered.
- **Selected call:** `current_weather` with `{"location": "Stockholm"}`.
- **Reviewed outcome: `failed_tool`.** A fresh dependency install replaced the upstream committed node_modules before execution. current_weather(location=Stockholm) returned isError=true, SMHI API error (404), and a short Varnish Not Found page rather than a weather observation. No endpoint substitution or upstream code patch was made.

<a id="riksdag-regering-mcp"></a>

### Riksdag & Regering MCP

- **Source:** [isakskogstad/Riksdag-Regering-MCP @ `32ceae410346fdb5ca215cdd94b2261038fce906`](https://github.com/isakskogstad/Riksdag-Regering-MCP/tree/32ceae410346fdb5ca215cdd94b2261038fce906).
- **Versions:** project 2.2.1; @modelcontextprotocol/sdk 1.30.0.
- **Attempt:** `2026-09-14T12:38:19.034102+00:00` → `2026-09-14T12:38:20.616085+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `["node.exe", "dist\\index.js"]`.
- **Credentials/config:** no provider credentials supplied; isolated state and common safety settings above.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 32 tools discovered.
- **Selected call:** `search_dokument` with `{"doktyp": "prop", "limit": 1}`.
- **Reviewed outcome: `failed_protocol`.** search_dokument(doktyp=prop, limit=1) was selected to read public government document metadata, not member/contact details. Initialization and discovery passed, then non-JSON stdout caused a JSON parse failure (line 1 column 6). The pinned logging utility writes informational messages with console.info, independently of the debug-only LOG_LEVEL setting. The client did not silently filter pollution or patch logging, so no valid live tool response was established. Workspace-hoisted TypeScript and Windows file-copy equivalents were used for the reviewed build; no server source was changed.

<a id="scb-opendata-mcp"></a>

### SCB Open Data MCP

- **Source:** [ashwinvis/scb-opendata-mcp @ `a13e0b5d915322cc0fffc6d77be9ac3f2ef77847`](https://github.com/ashwinvis/scb-opendata-mcp/tree/a13e0b5d915322cc0fffc6d77be9ac3f2ef77847).
- **Versions:** project 0.2.0; mcp 2.2.0, fastmcp 4.0.3, httpx 0.28.1.
- **Attempt:** `2026-09-14T13:13:13.697350+00:00` → `2026-09-14T13:13:20.987686+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `[".venv\\Scripts\\scb_opendata_mcp.exe", "--transport", "stdio"]`.
- **Non-secret configuration:** `{"SSL_CERT_FILE": "<owned system-trust-public-ca.pem>"}`.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 12 tools discovered.
- **Selected call:** `list_tables` with `{"lang": "en", "query": "population", "page_size": 1}`.
- **Reviewed outcome: `passed`.** The CLI explicitly used --transport stdio, not its HTTP default. The first list_tables call failed CERTIFICATE_VERIFY_FAILED. With SSL_CERT_FILE pointing to an owned standard-system public CA bundle, unchanged source returned SCB PxWeb v2 table TAB4552, Population connected to public network. Year 1960-2024, source Statistics Sweden, updated 2026-06-02T06:00:00Z, for the same bounded population query. This is a live catalog-metadata lookup, not verification of a complete statistical data query. TLS/hostname verification remained enabled; no upstream code was patched.

<a id="skolverket-mcp"></a>

### Skolverket MCP

- **Source:** [isakskogstad/Skolverket-MCP @ `5631a7fc7bc6cd0b0e2084981d6ac3886a5cb40e`](https://github.com/isakskogstad/Skolverket-MCP/tree/5631a7fc7bc6cd0b0e2084981d6ac3886a5cb40e).
- **Versions:** project 2.7.0; @modelcontextprotocol/sdk 1.20.2.
- **Attempt:** `2026-09-14T12:38:20.661524+00:00` → `2026-09-14T12:38:23.244815+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `["node.exe", "dist\\index.js"]`.
- **Credentials/config:** no provider credentials supplied; isolated state and common safety settings above.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 87 tools discovered.
- **Selected call:** `search_subjects` with `{"schooltype": "GR", "timespan": "LATEST", "limit": 1}`.
- **Reviewed outcome: `passed`.** search_subjects(schooltype=GR, timespan=LATEST, limit=1) returned totalElements=27, returned=1 and subject GRGRBIL01 / Bild, version 13. The source-built process called the public syllabus API without a key. The description field contained the string undefined, so this is a narrow live metadata smoke pass, not complete response-quality validation. The npm package is unpublished and remote service retired: neither was used. ServerInfo reports 2.5.0 while the project manifest is 2.7.0.

<a id="swemo-mcp"></a>

### Swemo MCP — Riksbank

- **Source:** [aerugo/swemo-mcp @ `602b2c383af97d86f519e0e4894641f895a291ce`](https://github.com/aerugo/swemo-mcp/tree/602b2c383af97d86f519e0e4894641f895a291ce).
- **Versions:** project 0.1.0; mcp 1.6.0, httpx 0.28.1.
- **Attempt:** `2026-09-14T12:42:13.304654+00:00` → `2026-09-14T12:42:17.884960+00:00`; transport `stdio`; negotiated protocol `2024-11-05`.
- **Launch:** `[".venv\\Scripts\\swemo-mcp.exe"]`.
- **Credentials/config:** no provider credentials supplied; isolated state and common safety settings above.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 27 tools discovered.
- **Selected call:** `list_policy_rounds` with `{}`.
- **Reviewed outcome: `passed`.** The initial unconstrained installation selected mcp 2.2.0 and failed importing FastMCP. Retrying unchanged source with mcp==1.6.0, the version in the pinned upstream uv.lock, initialized with protocol 2024-11-05 and listed 27 tools. list_policy_rounds returned 60 round records, starting at 2015:1; the server logged HTTP200 for the live Riksbank monetary-policy policy_rounds endpoint. A dependency selection was required; no server source was patched. This does not verify all forecast operations or the unimplemented SWEA/SWESTR/HTTP claims. A Pydantic forward-reference warning was emitted without preventing this call.

<a id="trafikverket-mcp"></a>

### Trafikverket MCP

- **Source:** [hniska/trafikverket-mcp @ `cade177741af8b5a4b2e924f00549d57a72c0484`](https://github.com/hniska/trafikverket-mcp/tree/cade177741af8b5a4b2e924f00549d57a72c0484).
- **Versions:** project 0.1.0; @modelcontextprotocol/sdk 1.20.1.
- **Attempt:** `2026-09-14T12:38:23.311840+00:00` → `2026-09-14T12:38:24.362811+00:00`; transport `stdio`; negotiated protocol `not reached`.
- **Launch:** `["node.exe", "dist\\index.js"]`.
- **Credentials/config:** no provider credentials supplied; isolated state and common safety settings above.
- **Phases:** initialize `not completed`; initialized notification `not sent`; tools/list `not completed`; 0 tools discovered.
- **Selected call:** none; see blocker/limitations below.
- **Reviewed outcome: `blocked_missing_credentials`.** The actual source-built stdio launch exited with TRAFIKVERKET_API_KEY environment variable is required. No token, signup or guessed credential was used and no traffic query was attempted. The guard is evidence of launch behavior, not a live Trafikverket pass.

<a id="traktamente-mcp"></a>

### Traktamente MCP

- **Source:** [johnie/traktamente-mcp @ `63a283b52fd47e6d43290f31a5307b0b53f5ca96`](https://github.com/johnie/traktamente-mcp/tree/63a283b52fd47e6d43290f31a5307b0b53f5ca96).
- **Versions:** project 1.1.0; @modelcontextprotocol/sdk 1.27.1; Bun 1.4.2; @hono/mcp 0.2.4.
- **Attempt:** `2026-09-14T12:53:50.141483+00:00` → `2026-09-14T12:53:51.734803+00:00`; transport `stdio`; negotiated protocol `2025-06-18`.
- **Launch:** `["bun.exe", "--no-install", "--no-env-file", "--use-system-ca", "src\\index.ts", "stdio"]`.
- **Non-secret configuration:** `{"TRANSPORT": "stdio", "LEFTHOOK": "0", "BUN_INSTALL": "<state>\\bun", "BUN_INSTALL_CACHE_DIR": "<state>\\cache"}`.
- **Phases:** initialize `passed`; initialized notification `sent`; tools/list `passed`; 3 tools discovered.
- **Selected call:** `traktamente_get_rates` with `{"landskod": "NO", "år": "2026", "limit": 1, "offset": 0, "response_format": "json"}`.
- **Reviewed outcome: `passed`.** The unchanged Bun stdio source returned Norge / NO / 2026 / normalbelopp=1054, with matching structuredContent and no error flag, from the Skatteverket EntryScape dataset. An initial provider preflight failed UNABLE_TO_GET_ISSUER_CERT_LOCALLY before any MCP tool call. Bun --use-system-ca then used the normal Windows trust store with certificate verification still enabled; a bounded public preflight returned HTTP200 and the subsequent actual MCP tool returned live data. --no-install and --no-env-file prevented automatic installs/dotenv loading. The package manifest says 1.1.0 while serverInfo reports 1.0.0. Rates are a dated data observation, not tax advice; source-license caveats remain. Hosted HTTP403 remains unresolved.

Dependency preparation used `bun install --production --frozen-lockfile --ignore-scripts` with an owned cache; the `lefthook install` prepare hook did not execute. Portable [Bun 1.4.2](https://github.com/oven-sh/bun/releases/download/bun-v1.4.2/bun-windows-x64-baseline.zip) SHA256 `78c221c2376f79731ccf4e4af0b3bb46d81fefa3296c5abee09ad8a1b21e68c6` matched the official release asset digest. No automatic latest-package execution was used.

## What remains blocked or unverified

Credentials/account authorization are still needed for **Fortnox**
(`FORTNOX_CLIENT_ID`, `FORTNOX_CLIENT_SECRET`, `FORTNOX_REFRESH_TOKEN`), **Bokio**
(`BOKIO_INTEGRATION_TOKEN`, `BOKIO_COMPANY_ID`, or authorized OAuth), **BolagsAPI**
(`BOLAGSAPI_KEY`), **Trafikverket** (`TRAFIKVERKET_API_KEY`) and **ICA**
(account/session prerequisites and separate authorization for private data).
Do not paste secret values into a catalog issue or chat. These prerequisites do not
turn a documentation score into zero. Optional authenticated tools in other servers
remain untested too; no full-catalog health guarantee is implied by any passing row.

Provider prices, quotas, permission scopes and terms may change. Local trust-chain,
access-policy and upstream API issues require appropriate maintainer/environment
follow-up, not insecure client workarounds. The source installation and license
caveats, overlapping coverage and retired package/deployment warnings remain in
[VERIFICATION.md](VERIFICATION.md). A future rerun should record a new date and
preserve this historical result rather than silently relabeling it.
