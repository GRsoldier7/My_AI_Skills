# Firecrawl runtime and activation

Canonical skills come from the official ISC catalog at https://github.com/firecrawl/skills/tree/2bf714d9f45e85085036a533ceb943c8577aef2b: 13 complete core packages, five build packages, and market-research, competitive-intel, lead-research workflows. The core packages stay siblings so their references resolve; build packages likewise stay siblings.

The application https://github.com/firecrawl/firecrawl is primarily AGPL-3.0 with separately licensed SDKs. It remains an external runtime reference; this library does not vendor the server.

Reviewed CLI: firecrawl-cli 1.26.24, source `a9a46fe23af001d726a05d8448d25a7188b42fdc`, ISC, Node >=22. CLI/API operation needs no MCP server. Use an approved existing installation or separately approved pinned installation. Do not run the upstream global init/install workflow automatically.

The hosted API needs network access and task-appropriate account/credits. Limited keyless operations are available; other endpoints require browser login or FIRECRAWL_API_KEY. Keep credentials in the runtime's private secret facility, never in this repository or HTML. Do not use command-line key literals. Set FIRECRAWL_NO_ENDPOINT_FEEDBACK=1 and do not issue search/Alexandria feedback automatically. Monitoring schedules, forms, authenticated sessions and uploads require explicit task scope.

Use optional Consulting/E7 profiles. Private enterprise dashboards and database connections use the connected-artifact architecture, not hosted scraping by default. Runtime activation is unverified by this import. Validate one bounded public scrape, denied authentication, exhausted credits, source attribution and ignored private output before enabling it on a real host.
