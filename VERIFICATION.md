# Verification record

**Review date: 2026-09-14.** This is a dated evidence record, not a certificate of
availability, safety, accuracy or maintenance. There are **26 catalog entries in
nine categories**, each backed by a public implementation. One entry (Sweden Legal
MCP) contains two separately launched servers; the catalog count is a count of entries,
not processes, tools or upstream APIs.

## Current assessment and runtime follow-up

All 26 entries have separate, evidence-based assessments under the unchanged
six-criterion **documentation readiness** rubric v1. Criterion statuses, original notes
and pinned public sources are in each entry's `quality.criteria`; generated scores are
not runtime pass rates, security ratings or certificates.

The [runtime smoke report](RUNTIME.md) records actual installation, launch,
initialization, discovery and selected read-only tool attempts for the original
18-entry catalog, including failures, credential blockers and dependency adjustments.
It supersedes those entries' initial source-only runtime scope below, not the source
evidence or access cautions. The later [curated-list additions](#curated-list-additions)
are **source/documentation-reviewed only; no runtime tests were attempted for them**.
Catalog unit tests remain distinct from tests of third-party implementations.

`last_verified` refers to metadata consultation only. Stars were read from the public
GitHub repository API and can change independently of the pinned source commit.

## Initial review scope (historical, before the runtime follow-up)

- Public GitHub repository identity, default branch, commit, primary language and stars.
- Actual MCP registration/transport code, documented configuration and exact tool names.
- Applicable code-license text where available, distinct from data-provider terms.
- Pinned documentation and source evidence; initially all entries were unassessed.
- Three documented remote endpoints were attempted without credentials. **None completed
  initialization in that initial pass; no `tools/list` or `tools/call` succeeded then.**
- The ten additions were initially **source/documentation-only**: no endpoint requests,
  initialization, login or tool calls had yet been attempted for them.
- No third-party package had been installed or launched during the initial review.

The initial three failures are preserved below as dated history; they do not describe
the subsequent local runtime results for all 18 entries.

## Source snapshots and operational limitations

These source-review observations preserve the initial review context. Statements
about work not yet executed refer to that stage; the later [runtime report](RUNTIME.md)
is authoritative for actual launch/tool attempts and outcomes. Source, license,
authentication and scope caveats below continue to apply.

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

## Additional source-only entries

The following **ten additions** were initially reviewed on **2026-09-14**, without
installing packages, connecting MCP clients, contacting hosted endpoints or accessing
accounts. These paragraphs preserve that source-only review; later documentation
assessments are in the entry JSON and actual attempts are in [RUNTIME.md](RUNTIME.md).
All ten repositories were public, non-forks and non-archived in the metadata snapshot.
Each entry links its pinned documentation, actual MCP registrations and license evidence.
Tool arrays are representative source-confirmed names, not exhaustive live inventories.
They were unassessed at initial inclusion, before the follow-up rubric review.

### Fortnox MCP — accounting with write-enabled tools

- Repository snapshot: [erp-mafia/fortnox-mcp at `501ee13`](https://github.com/erp-mafia/fortnox-mcp/tree/501ee1368f12ca4dd2e24a24bda8a47378b5c40a).
  TypeScript, MIT, 39 stars. [Entry and pinned evidence](servers/fortnox-mcp.json).
- Documented local command: `npx -y fortnox-mcp-server`, using **stdio**. Source also
  implements Streamable HTTP. The advertised remote endpoint is
  `https://fortnox-mcp.vercel.app/mcp`, **not tested** in this review.
- Requires a Fortnox account and an application configured with `FORTNOX_CLIENT_ID`,
  `FORTNOX_CLIENT_SECRET` and `FORTNOX_REFRESH_TOKEN`, or remote OAuth authorization.
  Remote browser authorization is not anonymous access to another company's accounts.
- **Write-enabled:** registered tools include `fortnox_create_invoice` and
  `fortnox_bookkeep_invoice`, alongside `fortnox_list_invoices`. These can change
  accounting records, not merely retrieve data. No operation was executed.
- The required commercial plan/API access and its cost were not verified. Stdio is
  cataloged and the authenticated hosted endpoint is deliberately documented here
  rather than put in `mcp_endpoint`, which feeds the unauthenticated scheduled checker.

### Bokio MCP — one-company accounting, read-only by default

- Repository snapshot: [straycatse/bokio-mcp at `cd48f56`](https://github.com/straycatse/bokio-mcp/tree/cd48f56f606c069b9b5ef4c89814e2673af7d8f4).
  TypeScript, MIT, 0 stars. [Entry and pinned evidence](servers/bokio-mcp.json).
- Documented `npx -y bokio-mcp` starts **stdio**. `bokio-mcp serve --http` supports
  self-hosted Streamable HTTP; no public hosted service is asserted.
- Requires a Bokio company and `BOKIO_INTEGRATION_TOKEN` plus `BOKIO_COMPANY_ID`, or
  OAuth using `BOKIO_CLIENT_ID` and `BOKIO_CLIENT_SECRET`. One company per instance.
  Real-account prerequisites differ from the README's account-free mock demonstration.
- **Read-only by default:** the source omits mutating tools unless
  `BOKIO_ALLOW_WRITES` is enabled. The catalog lists only sample read tools:
  `bokio_list_invoices`, `bokio_get_invoice` and `bokio_download_invoice`.
- `BOKIO_MOCK=true` serves fixtures, not live Bokio data. Bank-payment access requires
  additional provider approval/scopes. No tokens, payments or mock tests were run;
  the required commercial plan/API costs remain unverified.

### BolagsAPI MCP Server — company data from a distinct provider

- Repository snapshot: [HugoAndFriends/BolagsAPI-mcp-server at `f7e21bd`](https://github.com/HugoAndFriends/BolagsAPI-mcp-server/tree/f7e21bd14e3c3917045db6de8374641d839e9ec0).
  TypeScript, MIT, 0 stars. [Entry and pinned evidence](servers/bolagsapi-mcp-server.json).
- Node 18+; documented `npx -y @bolagsapi/mcp-server` uses **stdio**. Source also
  supports Streamable HTTP through `npm run start:http`, with bearer authentication.
- `BOLAGSAPI_KEY` is required. `lookup_company` and `search_companies` use the
  BolagsAPI provider's backend; financial statements and company history are also
  documented. Prices, quotas and availability of a free tier were not verified.
- The project's claim to be official refers to **BolagsAPI, not Bolagsverket**.
  No official government affiliation, account access or live results are certified.
  Company services use the existing `design-other` category, not a new taxonomy.

### SCB Open Data MCP — dedicated PxWebApi v2 alternative

- Repository snapshot: [ashwinvis/scb-opendata-mcp at `a13e0b5`](https://github.com/ashwinvis/scb-opendata-mcp/tree/a13e0b5d915322cc0fffc6d77be9ac3f2ef77847).
  Python, MIT, 1 star. [Entry and pinned evidence](servers/scb-opendata-mcp.json).
- Python 3.11+; documented installation is `pip install scb-opendata-mcp`, or use
  `uvx scb_opendata_mcp`. **Select `--transport stdio` explicitly** for an MCP client:
  the inspected CLI defaults to HTTP on port 6767 and host `0.0.0.0`.
- The catalog records stdio, not a guessed remote URL. HTTP examples in the README
  are inconsistent; binding, package installation and connectivity were not tested.
- `list_tables` is an actual registered tool, not an ordinary HTTP API relabeled MCP.
  The source targets SCB **PxWebApi v2**, with no key configured in the client.
  This overlaps MCP Sweden's statistics coverage but avoids assuming its v1 client
  has already migrated. Neither implementation's current data results were exercised.

### Kolada MCP — dedicated municipal and regional indicators

- Repository snapshot: [isakskogstad/Kolada-MCP at `2bdcc29`](https://github.com/isakskogstad/Kolada-MCP/tree/2bdcc29a019e24fe0d218f8191149701f4637ffd).
  TypeScript, MIT, 12 stars. [Entry and pinned evidence](servers/kolada-mcp.json).
- Current documentation recommends `npx -y kolada-mcp-server`, using **stdio**.
  The client targets **Kolada API v3** with no key in its standard configuration.
- Registered tools span KPI metadata, municipalities, organizational units, data and
  comparisons. The catalog's five KPI names are only a source-confirmed selection.
- Legacy HTTP/SSE code exists, but it is not evidence of a current public deployment;
  no remote endpoint is advertised here. This is a distinct alternative to the
  existing aggregator's Kolada v2 integration, not a newly discovered data provider.

### Skolverket MCP — source installation, not the retired service

- Repository snapshot: [isakskogstad/Skolverket-MCP at `5631a7f`](https://github.com/isakskogstad/Skolverket-MCP/tree/5631a7fc7bc6cd0b0e2084981d6ac3886a5cb40e).
  TypeScript, MIT, 10 stars. [Entry and pinned evidence](servers/skolverket-mcp.json).
- **Clone and build locally:** documented steps are `npm install`, `npm run build`,
  then configure the MCP client to launch `node` with the absolute path to
  `dist/index.js`. This is a **stdio** integration; no installation was performed.
- The inspected README removes a **retired hosted service and unpublished npm
  package**. Do not reuse old remote URLs or `npx` instructions from other directories.
- Standard requests do not require a key; `SKOLVERKET_API_KEY` is optional in the source.
  Actual registrations include `search_subjects`, `search_courses`,
  `search_school_units` and `get_school_unit_details`. This is an independent
  implementation of education coverage that also exists in MCP Sweden.

### Naturvårdsverket MCP — protected-area geodata

- Repository snapshot: [furrytailapps/mcp-nvv at `c67d456`](https://github.com/furrytailapps/mcp-nvv/tree/c67d45670db96aa1b5f5d8d716a06f34210d43d8).
  TypeScript, license not verified, 0 stars. [Entry and pinned evidence](servers/mcp-nvv.json).
- Next.js `mcp-handler` route and four registrations: `nvv_lookup`, `nvv_search`,
  `nvv_detail` and `nvv_extent`. Coverage includes Swedish reserves, national parks,
  Natura 2000 and Ramsar areas through Naturvårdsverket geodata sources.
- Documented **Streamable HTTP** endpoint: `https://mcp-nvv.vercel.app/mcp`;
  **not contacted or tested**. Local instructions use `npm install` and `npm run dev`.
  No stdio launch or API key requirement is documented in the inspected configuration.
- No LICENSE exists in the inspected tree: do not infer MIT from neighboring projects.
  A source-level workaround calculates extents locally after an upstream extent API
  problem; it does not prove present-day operation or failure of the full server.

### Traktamente MCP — Swedish foreign-travel allowance rates

- Repository snapshot: [johnie/traktamente-mcp at `63a283b`](https://github.com/johnie/traktamente-mcp/tree/63a283b52fd47e6d43290f31a5307b0b53f5ca96).
  TypeScript, license not verified, 1 star. [Entry and pinned evidence](servers/traktamente-mcp.json).
- `traktamente_get_rates`, `traktamente_list_countries` and `traktamente_search`
  retrieve Skatteverket's EntryScape data about **Swedish allowances for foreign
  business travel**, not generic travel recommendations or complete tax advice.
- Documented **Streamable HTTP** endpoint: `https://traktamente.app/mcp`;
  **not contacted or tested**. Local stdio requires **Bun**, even though the README
  includes `npx traktamente-mcp` examples. Node alone is not established as sufficient.
- No key/account is configured in the data client. README and manifest declare MIT,
  but the LICENSE file listed in the manifest is absent from the inspected tree.
  Consequently `license` is `null`, not verified MIT. Rates and applicable tax rules
  should be confirmed with the authority before expense reporting.

### Swemo MCP — Riksbank monetary-policy data, dated instructions

- Repository snapshot: [aerugo/swemo-mcp at `602b2c3`](https://github.com/aerugo/swemo-mcp/tree/602b2c383af97d86f519e0e4894641f895a291ce).
  Python, Apache-2.0, 2 stars. [Entry and pinned evidence](servers/swemo-mcp.json).
- Python 3.12+; documented `uvx swemo-mcp`, with **stdio** confirmed in the entry point.
  No key is configured in the monetary-policy API client.
- Registers policy-round and series discovery plus inflation, GDP, unemployment and
  policy-rate tools, backed by Riksbank's monetary-policy forecast API. The catalog
  uses six representative names rather than claiming an exhaustive live inventory.
- Last source activity found in the review was April 2025. The README's local example
  incorrectly names `kolada-mcp`; it is not copied as a valid setup instruction.
  Package-description references to **SWEA/SWESTR** and diagram references to HTTP/SSE
  do not establish those features in the inspected registrations. Runtime, installation
  and current upstream compatibility remain unverified.

### ICA MCP — unofficial private API, personal data and writes

- Repository snapshot: [kanylbullen/ica-mcp at `1d9b99`](https://github.com/kanylbullen/ica-mcp/tree/1d9b9940890eabce348e30539c5d6a2ec7ecd80f).
  Python, MIT, 2 stars. [Entry and pinned evidence](servers/ica-mcp.json).
- Python 3.10+; project instructions describe `uv tool install ica-mcp`, an initial
  `ica-mcp login`, then **stdio** with `ica-mcp serve`. These commands are documentation,
  **not steps performed in this review**. No login or personal-data access was attempted.
- **Unofficial, undocumented private ICA API.** The README warns that using it may
  conflict with ICA service terms. It requires an ICA account with **personnummer and
  password**; BankID-only accounts are unsupported. The project also requires a Swedish
  egress IP. That restriction was not tested or bypassed.
- Authentication tokens are cached in a per-user state directory. Tools can read
  personal lists, recipes, offers and products, and **modify or delete shopping lists**.
  Source-confirmed examples include `list_shopping_lists`, `get_offers`, `add_items`
  and `remove_item`. No credentials, sessions or account contents are published here.
- MIT covers the project code, **not permission to use ICA's private service**.
  Confirm service terms and account-data handling yourself; inclusion is not an
  endorsement, official integration claim or guarantee of availability.

### Overlaps and selection boundaries

The first ten additions do **not** mean ten entirely new Swedish data providers. The pinned
MCP Sweden aggregator already contains [SCB v1](https://github.com/Namraks-Labs/mcp-sweden/blob/ed10cc3dce260830349c3aab3c3ae0891774e890/src/mcp_sweden/data/scb/__init__.py),
[Kolada v2](https://github.com/Namraks-Labs/mcp-sweden/blob/ed10cc3dce260830349c3aab3c3ae0891774e890/src/mcp_sweden/data/kolada/__init__.py)
and [Skolverket](https://github.com/Namraks-Labs/mcp-sweden/blob/ed10cc3dce260830349c3aab3c3ae0891774e890/src/mcp_sweden/data/skolverket/__init__.py)
modules. The new dedicated implementations provide alternatives, including SCB v2 and
Kolada v3. BolagsAPI partly overlaps the company-information domain of the aggregator's
[Bolagsverket client](https://github.com/Namraks-Labs/mcp-sweden/blob/ed10cc3dce260830349c3aab3c3ae0891774e890/src/mcp_sweden/data/bolagsverket/client.py),
but is a **different provider/API**, not an official Bolagsverket MCP server.

## Curated-list additions

The subsequently supplied list contains nine projects, but
[Riksdag & Regering MCP](servers/riksdag-regering-mcp.json) is already cataloged.
It is preserved, not duplicated. The other eight are distinct implementations,
including alternatives for providers already covered elsewhere.

**Review date: 2026-09-14. Runtime status for all eight additions: `not_attempted`.**
This batch inspected public metadata, pinned documentation, implementation and license
sources only. No upstream installation, server launch, MCP endpoint connection, login
or tool execution was performed. Documentation Ready scores use the same rubric as the
existing entries and do not inherit runtime passes from another implementation.

### SCB MCP — TypeScript PxWebAPI v2 alternative

- Repository: [isakskogstad/SCB-MCP](https://github.com/isakskogstad/SCB-MCP).
  Pin: [`4f071256ed39ff3b20c820c79ed9fc75aa2888cb`](https://github.com/isakskogstad/SCB-MCP/tree/4f071256ed39ff3b20c820c79ed9fc75aa2888cb).
  TypeScript, 7 stars; [catalog entry and assessment](servers/scb-mcp.json).
- [README](https://github.com/isakskogstad/SCB-MCP/blob/4f071256ed39ff3b20c820c79ed9fc75aa2888cb/README.md)
  documents source cloning, `npm install`, `npm run build` and stdio through
  `node <absolute-path>/dist/index.js`; the
  [manifest](https://github.com/isakskogstad/SCB-MCP/blob/4f071256ed39ff3b20c820c79ed9fc75aa2888cb/package.json)
  declares Node 18+ and version 2.5.3. `npm start` selects different HTTP source,
  so it is not substituted for the documented stdio launch. No hosted endpoint is cataloged.
- [Actual registrations](https://github.com/isakskogstad/SCB-MCP/blob/4f071256ed39ff3b20c820c79ed9fc75aa2888cb/src/index.ts)
  include `scb_search_tables`, `scb_get_table_data`, `scb_find_region_code` and
  `scb_preview_data`. README function-style examples are conceptual; the MCP names
  have `scb_` prefixes, not the dotted shorthand used there.
- The [client](https://github.com/isakskogstad/SCB-MCP/blob/4f071256ed39ff3b20c820c79ed9fc75aa2888cb/src/api-client.ts)
  targets SCB API v2 and configures no API key. Table-specific codes, selection sizes
  and rate limits still apply. This differs from both the existing Python SCB v2
  implementation and the aggregator's SCB v1 component; shared data is not duplicate code.
- **License null:** package metadata says MIT, but the pinned tree contains no
  applicable full license terms. Upstream compatibility and production-readiness
  claims are not independent runtime evidence.

### Kolada MCP (aerugo) — Python municipal indicators and semantic search

- Repository: [aerugo/kolada-mcp](https://github.com/aerugo/kolada-mcp).
  Pin: [`3b7d6aef5feb59be52e17dacc2626dba45e40b04`](https://github.com/aerugo/kolada-mcp/tree/3b7d6aef5feb59be52e17dacc2626dba45e40b04).
  Python, 16 stars; [catalog entry and assessment](servers/kolada-mcp-python.json).
- [README](https://github.com/aerugo/kolada-mcp/blob/3b7d6aef5feb59be52e17dacc2626dba45e40b04/README.md)
  gives source installation via `pip install -e .` followed by `kolada-mcp` or
  `python -m kolada_mcp`, defaulting to stdio. The
  [manifest](https://github.com/aerugo/kolada-mcp/blob/3b7d6aef5feb59be52e17dacc2626dba45e40b04/pyproject.toml)
  requires Python 3.11+ and declares version 1.0.0. Its extensive Python/model dependencies
  are not contradicted by the README's narrower claim of no external infrastructure.
- [Registered tools](https://github.com/aerugo/kolada-mcp/blob/3b7d6aef5feb59be52e17dacc2626dba45e40b04/src/kolada_mcp/server.py)
  cover KPI discovery, semantic search, municipality filtering, data retrieval and
  cross-municipality comparison. Startup fetches KPI/municipality catalogs and loads
  embeddings; error fallbacks can leave empty data or unavailable semantic search.
- [Settings](https://github.com/aerugo/kolada-mcp/blob/3b7d6aef5feb59be52e17dacc2626dba45e40b04/src/kolada_mcp/config.py)
  target **Kolada API v2**, with `KBLab/sentence-bert-swedish-cased` and a package-local
  embedding cache. No API credential is configured. First-run model downloads,
  CPU/memory and writable caches are additional prerequisites, not runtime-tested here.
  The [model loader](https://github.com/aerugo/kolada-mcp/blob/3b7d6aef5feb59be52e17dacc2626dba45e40b04/src/kolada_mcp/services/embeddings.py)
  is source evidence for those requirements.
- Only stdio is cataloged. The optional HTTP
  [bootstrap](https://github.com/aerugo/kolada-mcp/blob/3b7d6aef5feb59be52e17dacc2626dba45e40b04/src/kolada_mcp/__main__.py)
  was inspected, not validated for interoperability. This is separate from the
  existing isakskogstad TypeScript Kolada API v3 server.
- **License null:** README/manifest declare Apache-2.0, but applicable full terms are
  absent from the pinned tree. The package's Beta status and limited operational
  guidance are reflected in the documentation assessment.

### Apiverket MCP — curated gateway, not unrestricted agency access

- [vinvuk/apiverket-mcp](https://github.com/vinvuk/apiverket-mcp), pin
  [`945a0103add6d5017d367f29a1560827dc8369d7`](https://github.com/vinvuk/apiverket-mcp/tree/945a0103add6d5017d367f29a1560827dc8369d7).
  TypeScript, 2 stars, verified MIT; [entry and assessment](servers/apiverket-mcp.json).
- The [README](https://github.com/vinvuk/apiverket-mcp/blob/945a0103add6d5017d367f29a1560827dc8369d7/README.md)
  documents Node 18+, `npx apiverket-mcp-server` and local stdio client configurations.
  Explicitly set `GOVDATA_API_URL` and `GOVDATA_API_KEY`: the
  [client](https://github.com/vinvuk/apiverket-mcp/blob/945a0103add6d5017d367f29a1560827dc8369d7/src/api-client.ts)
  defaults to localhost rather than the hosted default claimed by the README.
- [Three registered tools](https://github.com/vinvuk/apiverket-mcp/blob/945a0103add6d5017d367f29a1560827dc8369d7/src/index.ts)
  discover a built-in endpoint catalog, make permitted GET queries and inspect account
  quotas. The REST API base is **not** an MCP endpoint. Several domains overlap existing
  entries, but this is a separate gateway implementation.
- The published sandbox identifier does **not** establish live production data.
  Real data needs an Apiverket live key; access, prices and quotas were not verified.
  Company board/officer/owner/UBO subresources are unsupported; responses may be truncated
  and reads consume quota. No key, account or endpoint was accessed.

### Storstockholms Lokaltrafik (SL) MCP Server — journeys and departures

- [henrrrik/sl-mcp-server](https://github.com/henrrrik/sl-mcp-server), pin
  [`6f70dea44b078c2d02363f4c14f2291c2c743be9`](https://github.com/henrrrik/sl-mcp-server/tree/6f70dea44b078c2d02363f4c14f2291c2c743be9).
  Go, 1 star, verified MIT; [entry and assessment](servers/sl-mcp-server.json).
- The [README](https://github.com/henrrrik/sl-mcp-server/blob/6f70dea44b078c2d02363f4c14f2291c2c743be9/README.md)
  documents a hosted SSE connection and self-hosting with `go build -o sl-mcp-server`,
  setting `PORT` and launching that binary. The
  [module](https://github.com/henrrrik/sl-mcp-server/blob/6f70dea44b078c2d02363f4c14f2291c2c743be9/go.mod)
  specifies Go 1.26.1. The README explicitly says no API key is needed.
- [Eleven registrations](https://github.com/henrrrik/sl-mcp-server/blob/6f70dea44b078c2d02363f4c14f2291c2c743be9/server.go)
  include genuine journey planning, departures, disruptions and stop discovery.
  [Journey code](https://github.com/henrrrik/sl-mcp-server/blob/6f70dea44b078c2d02363f4c14f2291c2c743be9/tools/journeyplanner.go)
  calls SL's trip API; this capability is not inferred from a transit category label.
- [Transport source](https://github.com/henrrrik/sl-mcp-server/blob/6f70dea44b078c2d02363f4c14f2291c2c743be9/main.go)
  uses **legacy SSE**. The advertised `/sse` service was not contacted and is deliberately
  omitted from `mcp_endpoint`, whose scheduled checker assumes Streamable HTTP.
- Results have documented caps; long IDs require strings, disruption text is Swedish,
  facility alerts are opt-in and nearest stops cannot be filtered by mode. No ticket
  purchase or booking tools were found. Hosting availability and cost are unverified.

### SMHI Weather Forecast MCP Server — educational forecast and observation project

- [ribomation/smhi-weather-forecast-mcp-server](https://github.com/ribomation/smhi-weather-forecast-mcp-server), pin
  [`5f23510e8ba939a919210103905964e2a2e73905`](https://github.com/ribomation/smhi-weather-forecast-mcp-server/tree/5f23510e8ba939a919210103905964e2a2e73905).
  TypeScript, 0 stars; [entry and assessment](servers/smhi-weather-forecast-mcp.json).
- The [README](https://github.com/ribomation/smhi-weather-forecast-mcp-server/blob/5f23510e8ba939a919210103905964e2a2e73905/README.md)
  documents Node 18+, npm install/build/start and Claude Desktop stdio configuration.
  The [manifest](https://github.com/ribomation/smhi-weather-forecast-mcp-server/blob/5f23510e8ba939a919210103905964e2a2e73905/package.json)
  starts `dist/smhi-weather-forcast-mcp-server.js`; the `forcast` spelling is intentional
  in these instructions because it matches the actual build output.
- [Source registrations](https://github.com/ribomation/smhi-weather-forecast-mcp-server/blob/5f23510e8ba939a919210103905964e2a2e73905/src/server.ts)
  cover forecasts, observations, stations and parameters. The
  [API client](https://github.com/ribomation/smhi-weather-forecast-mcp-server/blob/5f23510e8ba939a919210103905964e2a2e73905/src/services/smhi-api.ts)
  uses unauthenticated SMHI calls. SSE is a future-plan item, not the cataloged transport.
- The author labels this an educational experiment and warns of spring-2026 API changes.
  Source retains older forecast/observation paths; current availability and corrected
  archive formats were not checked. This is neither a confirmed shutdown nor a working
  endpoint claim. **License null:** README says MIT without applicable full terms.

### Annual Report MCP Server — approved company-data access and local indexing

- [Pomilo-AI/annual_report_mcp_server](https://github.com/Pomilo-AI/annual_report_mcp_server), pin
  [`6b903a268d0bf2936334129f3e471a86ffad4512`](https://github.com/Pomilo-AI/annual_report_mcp_server/tree/6b903a268d0bf2936334129f3e471a86ffad4512).
  Python, 2 stars; [entry and assessment](servers/annual-report-mcp-server.json).
- The [README](https://github.com/Pomilo-AI/annual_report_mcp_server/blob/6b903a268d0bf2936334129f3e471a86ffad4512/README.md)
  gives dependency installation and Claude Desktop MCP CLI launch instructions, but
  includes a placeholder clone URL, a hyphenated filename that differs from the actual
  underscored module, and an unprepared venv/uv fallback. Python version and transport
  are not explicit; no transport or complete-installation claim is invented.
- [Three FastMCP tools](https://github.com/Pomilo-AI/annual_report_mcp_server/blob/6b903a268d0bf2936334129f3e471a86ffad4512/annual_report_mcp_server.py)
  query a matching digitally filed report, fetch organization data and search company
  names. Report processing requires a ZIP containing XHTML; this is **not all company
  filings**. Company-name lookup returns Tavily search results, not a validated ID alone.
- Approved Bolagsverket access requires `BV_CLIENT_ID` and `BV_CLIENT_SECRET`, alongside
  `OPENAI_API_KEY` and `TAVILY_API_KEY`. Eligibility, commercial prices and quotas are
  unverified. This is a separate provider path from the BolagsAPI entry.
- The demo downloads reports and persists local LlamaIndex indexes, and uses OpenAI
  rather than being an offline/no-write reader. The author warns against production use.
  No personal/company account data was accessed. **License null:** MIT declaration only.

### Swedish Law MCP (archived) — local legal corpus and replacement gateway

- [Ansvar-Systems/Swedish-law-mcp](https://github.com/Ansvar-Systems/Swedish-law-mcp), pin
  [`281dea10e09572db722672ae25280faf5cce19ee`](https://github.com/Ansvar-Systems/Swedish-law-mcp/tree/281dea10e09572db722672ae25280faf5cce19ee).
  TypeScript, 0 stars, verified Apache-2.0; [entry and assessment](servers/swedish-law-mcp.json).
- **GitHub marks the repository archived.** It was deferred during initial catalog
  selection and is now included on explicit request with that caveat in its name,
  description and tags. Historical daily-update claims are not maintenance guarantees.
- [README](https://github.com/Ansvar-Systems/Swedish-law-mcp/blob/281dea10e09572db722672ae25280faf5cce19ee/README.md)
  and [setup guide](https://github.com/Ansvar-Systems/Swedish-law-mcp/blob/281dea10e09572db722672ae25280faf5cce19ee/CONTRIBUTING.md)
  provide Node 18+, npm 9+, clone/install/build/start and corpus ingestion/rebuild commands.
  The tracked database is an empty file: **a usable corpus must be rebuilt or supplied**,
  despite older prebuilt-database wording. `SWEDISH_LAW_DB_PATH` selects a local database.
- The [registry](https://github.com/Ansvar-Systems/Swedish-law-mcp/blob/281dea10e09572db722672ae25280faf5cce19ee/src/tools/registry.ts)
  implements statutes, provisions, citations, EU references and dataset-dependent case-law
  and preparatory-work tools. [Coverage notes](https://github.com/Ansvar-Systems/Swedish-law-mcp/blob/281dea10e09572db722672ae25280faf5cce19ee/TOOLS.md)
  do not promise a comprehensive live court archive. EU-reference validation is not a
  substantive legal-compliance opinion; version tools need additional corpus data/settings.
- Local source supports stdio and reads SQLite without mutation; separate ingestion/build
  commands would write corpus files. The replacement hosted service requires an account,
  OAuth and suitable tier access. No account-gated endpoint is cataloged, and no entitlement,
  price, current legal accuracy or hosted availability was verified.

### Begagnad MCP — second-hand searches, not transaction or tracking automation

- [bjesus/begagnad-mcp](https://github.com/bjesus/begagnad-mcp), pin
  [`cc45e8cb23b5f36e5d4b1ccb831cd561717270b5`](https://github.com/bjesus/begagnad-mcp/tree/cc45e8cb23b5f36e5d4b1ccb831cd561717270b5).
  TypeScript, 8 stars; [entry and assessment](servers/begagnad-mcp.json).
- [README](https://github.com/bjesus/begagnad-mcp/blob/cc45e8cb23b5f36e5d4b1ccb831cd561717270b5/README.md)
  documents a public-instance `mcp-remote` Claude Desktop configuration, local npm
  install/start and Cloudflare login/deployment. Source verifies legacy SSE for that
  advertised route; it was not contacted or put into the Streamable HTTP checker.
- [Five tools](https://github.com/bjesus/begagnad-mcp/blob/cc45e8cb23b5f36e5d4b1ccb831cd561717270b5/src/index.ts)
  search and retrieve Blocket items through **blocket-api.se**, and Tradera items through
  its API. The intermediary's affiliation and terms were not established. There are
  **no purchase, bidding, seller-messaging, saved-search or change-tracking tools**,
  nor dedicated price/location filter parameters.
- Tradera requires `TRADERA_APP_ID` and `TRADERA_APP_KEY`; public-instance credentials,
  Cloudflare/Tradera eligibility, prices and quotas are unknown. Combined search fails
  if either provider fails. Tools do not mutate marketplace listings, but the Cloudflare
  agent uses service state, so no blanket no-write claim is made.
- **License null:** README/manifest say MIT, without full applicable license terms.
  No deployment, login, endpoint connection or marketplace query was performed.

## Remote runtime attempts (historical initial pass)

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
source, not necessarily what a hosted endpoint is running. Local stdio entries had
not been installed or executed in this initial pass; their later attempts are recorded
in [RUNTIME.md](RUNTIME.md). Trafikverket additionally requires an API key.

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
4. Call one benign read-only tool with valid bounded arguments that actually retrieves
   public provider data. Confirm both JSON-RPC success and that the tool has not returned
   `isError: true`; inspect the content for masked upstream failures before claiming
   live data was returned. Static `lm_map_url` generation or a local ping alone is not
   a live-provider pass.
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
- Business/company coverage now includes BolagsAPI, with the provider distinction
  explained above. Coverage remains incomplete: roadmap-only references in other
  projects were not counted as implemented integrations. This is a curated selection,
  not an exhaustive list or a claim of official agency affiliation.
- [Leopaexd/stockholm-public-transport-mcp](https://github.com/Leopaexd/stockholm-public-transport-mcp)
  remains excluded from this expansion: the reviewed implementation passes dictionary
  parameters into an `lru_cache`-decorated function, which requires hashable arguments.
- [wirn/mcp-elpris](https://github.com/wirn/mcp-elpris) remains deferred because setup
  documentation is insufficient and stdout logging complicates its transport setup;
  no LICENSE was established. Neither excluded project was runtime-tested here.

## Licensing boundaries

Catalog infrastructure and original descriptions are MIT-licensed. **Fifteen entries have
verified code-license files; eleven use `null`** because applicable terms were not established.
The initial 18-entry catalog had twelve verified and six unverified licenses. The curated
list adds three verified licenses (Apiverket and SL: MIT; Swedish Law: Apache-2.0) and
five unverified licenses (SCB MCP, aerugo's Kolada, ribomation's SMHI, Annual Report and
Begagnad), preserving all existing license values.
A README/package license declaration is noted above but is not silently converted into
verified terms. GitHub's automatic repository license detection is not decisive: for
Riksdag & Regering the relevant license is in the `mcp` subdirectory.

External datasets have separate conditions. [SCB's open-data guidance](https://www.scb.se/vara-tjanster/oppna-data/)
includes CC0 and qualifications for statistics supplied by other agencies. Lantmäteriet
access and reuse terms vary by product. Other provider terms were not comprehensively
reviewed: consult the provider before redistribution or consequential use. Nothing here
certifies legal, travel, weather or employment advice.
