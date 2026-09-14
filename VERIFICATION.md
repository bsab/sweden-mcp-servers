# Verification record

**Review date: 2026-09-14.** This is a dated evidence record, not a certificate of
availability, safety, accuracy or maintenance. There are **eight catalog entries in
seven categories**, each backed by a public implementation. One entry (Sweden Legal
MCP) contains two separately launched servers; the catalog count is a count of entries,
not processes, tools or upstream APIs.

## What was checked

- Public GitHub repository identity, default branch, commit, primary language and stars.
- Actual MCP registration/transport code, documented configuration and exact tool names.
- Applicable code-license text where available, distinct from data-provider terms.
- Pinned documentation and source links in each entry's `quality.evidence`.
- Three documented remote endpoints were attempted without credentials. **None completed
  initialization from the review environment; no `tools/list` or `tools/call` succeeded.**
- No third-party package was installed or launched, and no local MCP server was executed.
  Repository build/test results concern this catalog, not the listed implementations.

All entries remain **unassessed** for rubric v1: this metadata/source review is not a
complete six-criterion readiness assessment. Reasons and sources are visible in the
README's score links, the web catalog and the source JSON. `last_verified` refers to
metadata consultation only. Stars were read from the public GitHub repository API;
they can change independently of the pinned source commit.

## Source snapshots and operational limitations

### MCP Sweden — statistics and multiple Swedish services

- Repository: [Namraks-Labs/mcp-sweden](https://github.com/Namraks-Labs/mcp-sweden).
- Inspected commit: [`ed10cc3dce260830349c3aab3c3ae0891774e890`](https://github.com/Namraks-Labs/mcp-sweden/tree/ed10cc3dce260830349c3aab3c3ae0891774e890).
- Python, MIT, 1 star. [Entry and evidence](servers/mcp-sweden.json).
- Python 3.10+; documented source installation uses `pip install -e .`. Local stdio
  uses `fastmcp run mcp_sweden.server:mcp`; HTTP uses `--transport http`.
  The entry records Streamable HTTP because it links the advertised hosted instance.
- `MCP_SWEDEN_API_TOKEN` can enable authentication. Discovery defaults to a BM25
  transformation; component servers are mounted under namespaces. Only the explicitly
  registered root name `list_features` is listed in the catalog, not guessed names for
  mounted SCB tools. This is not an exhaustive inventory.
- Covers SCB, Riksdagen, municipal indicators and other Swedish services. The inspected
  SCB client still targets PxWebApi v1; [SCB's migration notice](https://www.scb.se/vara-tjanster/oppna-data/pxwebapi/)
  says v1 stops working at the 2026/2027 year boundary. Future compatibility is unverified.

### Riksdag & Regering MCP — parliament and government material

- Repository: [isakskogstad/Riksdag-Regering-MCP](https://github.com/isakskogstad/Riksdag-Regering-MCP).
- Inspected commit: [`32ceae410346fdb5ca215cdd94b2261038fce906`](https://github.com/isakskogstad/Riksdag-Regering-MCP/tree/32ceae410346fdb5ca215cdd94b2261038fce906).
- TypeScript, MIT from **`mcp/LICENSE`**, 31 stars. [Entry and evidence](servers/riksdag-regering-mcp.json).
- Node 20+; documentation gives `npx -y @isak.skogstad/riksdag-regering-mcp`, or source
  installation/build through `npm run mcp:install` and `npm run mcp:build`.
- SDK stdio transport and 32 tool registrations are present. Only stdio is cataloged:
  the optional custom HTTP implementation's interoperability was not established.
- Parliamentary data is queried directly; Government Offices material is mediated by
  **g0v.se**, not an official Regeringskansliet API. Package installation, upstream calls
  and the project's optional HTTP authentication behavior were not runtime-tested.

### SMHI MCP — weather and hydrology

- Repository: [furrytailapps/mcp-smhi](https://github.com/furrytailapps/mcp-smhi).
- Inspected commit: [`74bcfe15c314eb502c3b9983eab1dbb68c13e9e8`](https://github.com/furrytailapps/mcp-smhi/tree/74bcfe15c314eb502c3b9983eab1dbb68c13e9e8).
- TypeScript, license not verified, 0 stars. [Entry and evidence](servers/mcp-smhi.json).
- The Next.js route uses `createMcpHandler` and registers `smhi_get_forecast`,
  `smhi_get_observations`, `smhi_get_current_conditions` and `smhi_describe_data`.
- Developer documentation (`CLAUDE.md`) advertises the production endpoint and says
  no environment variables are required. Source scripts provide `npm run dev`,
  `npm run build` and `npm start`; no end-user installation README or LICENSE was found.
- Administrative location codes are not interchangeable with place names. Tool behavior,
  warnings, radar, lightning and hydrological data coverage were not verified at runtime.

### Trafikverket MCP — traffic and road conditions

- Repository: [hniska/trafikverket-mcp](https://github.com/hniska/trafikverket-mcp).
- Inspected **master** commit: [`cade177741af8b5a4b2e924f00549d57a72c0484`](https://github.com/hniska/trafikverket-mcp/tree/cade177741af8b5a4b2e924f00549d57a72c0484).
- TypeScript, license not verified, 0 stars. [Entry and evidence](servers/trafikverket-mcp.json).
- Node 18+; documented local setup uses `npm install`, `npm run build`, then an absolute
  path to `dist/index.js` with `node` as the MCP command. Ten stdio tools are registered.
- **`TRAFIKVERKET_API_KEY` is required**, and the source checks it before constructing the
  client. Obtain access from [Trafikverket](https://api.trafikinfo.trafikverket.se/).
  No key was obtained or used, and no public deployment was documented.
- README/package metadata declares MIT, but no applicable LICENSE file was found.
  `license: null` conservatively records that the terms were not verified.

### Arbetsförmedlingen MCP Server — employment and JobTech

- Repository: [DanielErikssonCoder/arbetsformedlingen-mcp-server](https://github.com/DanielErikssonCoder/arbetsformedlingen-mcp-server).
- Inspected commit: [`b94dd02bcd884c16b26c1adb7feee39775ca98dd`](https://github.com/DanielErikssonCoder/arbetsformedlingen-mcp-server/tree/b94dd02bcd884c16b26c1adb7feee39775ca98dd).
- TypeScript, MIT, 1 star. [Entry and evidence](servers/arbetsformedlingen-mcp-server.json).
- Node 18+; documented MCP command is `npx -y arbetsformedlingen-mcp-server`. Defaults
  to stdio, which is the cataloged transport. Optional `TRANSPORT=http` exposes local
  Streamable HTTP; no public hosted endpoint is documented.
- Thirteen tool registrations cover jobs, history, taxonomy, enrichment and education.
  README says no API key; inspected request construction has no authorization header.
- Published package execution and upstream API availability were not checked. Package
  version 1.0.2 differs from the source's `serverInfo` version 2.0.0; parity is unverified.

### Lantmäteriet MCP — Swedish geodata

- Repository: [furrytailapps/mcp-lantmateriet](https://github.com/furrytailapps/mcp-lantmateriet).
- Inspected commit: [`22907c5b82978683c57d96d3569c9af2006d49d5`](https://github.com/furrytailapps/mcp-lantmateriet/tree/22907c5b82978683c57d96d3569c9af2006d49d5).
- **JavaScript** is GitHub's primary-language snapshot, despite TypeScript implementation
  files. License not verified, 0 stars. [Entry and evidence](servers/mcp-lantmateriet.json).
- Next.js MCP handler registers `lm_property_search`, `lm_elevation`, `lm_map_url` and
  `lm_stac_search`. Source scripts expose local development/build/start commands;
  end-user installation documentation and a LICENSE file were not found.
- Property/elevation access requires server-side `LANTMATERIET_CONSUMER_KEY` and
  `LANTMATERIET_CONSUMER_SECRET`. [Geotorget](https://geotorget.lantmateriet.se/)
  handles access registration. STAC discovery does not imply anonymous downloads.
- `lm_map_url` documents unauthenticated map URL generation. It was not executed.
- The entry follows the production URL in `CLAUDE.md`. Test documentation instead
  names `https://lantmateriet-mcp.vercel.app/mcp`; this conflict is unresolved and the
  alternative was not silently substituted or tested to circumvent the network block.

### Sweden Legal MCP — Lifos and Rättspraxis

- Repository: [AvoccadoTech/legal-mcp-sweden](https://github.com/AvoccadoTech/legal-mcp-sweden).
- Inspected commit: [`424f01a096157ab9e4f67c378c83c6bb80a96487`](https://github.com/AvoccadoTech/legal-mcp-sweden/tree/424f01a096157ab9e4f67c378c83c6bb80a96487).
- Python, Apache-2.0, 0 stars. [Entry and evidence](servers/legal-mcp-sweden.json).
- Python 3.11+ and `pip install -e .`. **Two separate stdio servers** start with
  `python -m sweden_legal_mcp.lifos` and `python -m sweden_legal_mcp.rattspraxis`;
  nine tools belong to each, not to a single combined endpoint.
- Upstream public sources need no account according to the documentation. Lifos uses
  `LIFOS_STATE_DIR` and optional `LIFOS_KB_PATH`. `RATTSPRAXIS_DB` names a **directory**
  in the source, which appends `rattspraxis.sqlite3`.
- Lifos has a five-item rolling window without backfill. Court monitoring needs initial
  synchronization and depends on newest-first upstream ordering. **Some tools write
  local state** (tracking, scans, watches and synchronization); the integration must
  not be described as universally read-only. No local mirrors were created or populated.

### Swedish Weather MCP — local SMHI alternative

- Repository: [robobobby/mcp-swedish-weather](https://github.com/robobobby/mcp-swedish-weather).
- Inspected commit: [`eeb6405964dc682c360151cc8a51a2a2251618bb`](https://github.com/robobobby/mcp-swedish-weather/tree/eeb6405964dc682c360151cc8a51a2a2251618bb).
- JavaScript, license not verified, 0 stars. [Entry and evidence](servers/mcp-swedish-weather.json).
- Included as a small **local stdio alternative**, rather than another hosted endpoint.
  Documentation configures `node` with an absolute path to `src/index.js`; dependencies
  are declared, but the README lacks a complete installation walkthrough.
- `current_weather` and `weather_forecast` are registered. No key is configured.
  Unknown place names use Open-Meteo geocoding with a Sweden-country check.
- **Current weather is forecast-derived**, not a station observation. The declared MIT
  identifier lacks a LICENSE file; no license terms or local runtime were verified.
  An old SMHI documentation link returned 404, which does not prove the data API is down.

## Remote runtime attempts

Tests were made on **2026-09-14 at approximately 09:58 UTC**, using Python's standard
HTTP client with certificate verification, a 25-second timeout, no credentials and
`User-Agent: sweden-mcp-servers-verification/1.0`. No upstream project code was executed.

| Documented endpoint | Initialization result from this environment | Tools listed / called |
|---------------------|---------------------------------------------|-----------------------|
| `https://sweden.mcp.namraks.com/mcp` | DNS resolution failed (`getaddrinfo`; independently reproduced by curl) | No / no |
| `https://mcp-smhi.vercel.app/mcp` | HTTP 403 with an HTML network-policy “Access Denied” page, not JSON-RPC | No / no |
| `https://mcp-lantmateriet.vercel.app/mcp` | HTTP 403 with an HTML network-policy “Access Denied” page, not JSON-RPC | No / no |

These results **do not establish whether the remote deployments work from another
network**, nor whether they enforce authentication. The network block was not bypassed.
No deployment version was obtained. Pinned GitHub revisions above describe reviewed
source, not necessarily what a hosted endpoint is running. Local stdio entries were
not installed or executed; Trafikverket additionally requires an API key.

### Exact procedure and safe follow-up

The first POST used `Content-Type: application/json` and
`Accept: application/json, text/event-stream` with this body:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"sweden-mcp-servers-verification","version":"1.0"}}}
```

Because initialization failed, the following steps were **not reached**. A future
maintainer working on a permitted network should:

1. Record the negotiated protocol version and returned `serverInfo`. Keep any session
   identifier private and use it in subsequent `Mcp-Session-Id` headers; send the
   negotiated version as `MCP-Protocol-Version`.
2. Send `{"jsonrpc":"2.0","method":"notifications/initialized"}`.
3. Send `{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}` and follow any
   pagination. Inspect the actual advertised input schemas rather than guessing them.
4. Call one benign read-only tool with valid bounded arguments: for example the
   advertised root `list_features`, an SMHI descriptive/forecast query, or `lm_map_url`
   for a public area. Confirm both JSON-RPC success and that the tool has not returned
   `isError: true`; inspect the content before claiming useful data was returned.
5. Record the exact arguments, timestamp, server version, result summary and limitations.
   One successful call proves only that sampled operation at that time, not the whole server.

The inherited scheduled checker (`python scripts/check_mcp_endpoints.py check`) performs
**only step 1** on listed remote endpoints. It assumes unauthenticated Streamable HTTP;
legacy SSE/authenticated services must not be treated as equivalent. No arbitrary
health fields or fabricated runtime scores are stored in entry JSON.

## Exclusions and coverage gaps

- [pipeworx-io/mcp-scb-se](https://github.com/pipeworx-io/mcp-scb-se/tree/b027f4d79238a795a5ceb9f57e513a935c73ad6d):
  deferred gateway pack. Inspected source exports tools/call dispatch but does not
  initialize an MCP transport; its advertised and implemented inventories differ.
  The hosted gateway was not independently established from that source.
- [alexatnordnet/mcp-scb-server](https://github.com/alexatnordnet/mcp-scb-server/tree/ad3d6b6b6b7bbcc36a612827b5455ed9ad937186):
  a genuine MCP implementation, deferred because documented generation references
  missing `scripts/fix-imports.js` and a Kubb dependency absent from the inspected package.
- [Ansvar-Systems/Swedish-law-mcp](https://github.com/Ansvar-Systems/Swedish-law-mcp/tree/281dea10e09572db722672ae25280faf5cce19ee):
  archived at review time. Current docs direct users to an OAuth gateway and do not
  redistribute the prebuilt corpus; an old deployment URL was not treated as anonymous
  working access. Exclusion is not a claim that the underlying implementation is fake.
- Business/company sources and other categories remain incomplete. Roadmap references
  to Bolagsverket, Riksdagen or Lantmäteriet in other projects were not counted as
  implemented integrations. This is a useful initial selection, not exhaustive coverage.

## Licensing boundaries

Catalog infrastructure and original descriptions are MIT-licensed. Four entries have
verified code-license files; four use `null` because applicable terms were not established.
A README/package license declaration is noted above but is not silently converted into
verified terms. GitHub's automatic repository license detection is not decisive: for
Riksdag & Regering the relevant license is in the `mcp` subdirectory.

External datasets have separate conditions. [SCB's open-data guidance](https://www.scb.se/vara-tjanster/oppna-data/)
includes CC0 and qualifications for statistics supplied by other agencies. Lantmäteriet
access and reuse terms vary by product. Other provider terms were not comprehensively
reviewed: consult the provider before redistribution or consequential use. Nothing here
certifies legal, travel, weather or employment advice.
