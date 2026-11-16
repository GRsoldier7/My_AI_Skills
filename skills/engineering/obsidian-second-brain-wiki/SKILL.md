---
name: obsidian-second-brain-wiki
description: >-
  Use when initializing, ingesting sources into, querying, or health-checking an
  Obsidian vault run as an LLM-maintained second-brain wiki.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Obsidian Second-Brain Wiki

Sources are ingested once, summarized, and cross-linked into notes so knowledge compounds.

## Layout
`raw/` holds the user's immutable sources (read only). `wiki/` is assistant-maintained: `index.md`, `log.md`, `entities/`, `concepts/`, `sources/`, `comparisons/`, `synthesis/`. `README.md` describes the schema. Adapt to the vault's existing conventions (e.g., PARA folders) instead of forcing this layout.

## Operations
1. **INIT:** confirm the target and that it isn't already a vault; create the folders, README (purpose, frontmatter schema, kebab-case naming), index, and a log entry. Never overwrite an existing vault without confirmation.
2. **INGEST:** read the source in `raw/`; share a TL;DR, 3-5 key claims, entities and concepts to create or update, contradictions, and a proposed filename. **Wait for approval**, then write the source page, create or append entity and concept pages (mark appends `<!-- Updated YYYY-MM-DD -->`), cross-link contradictions, update the index, and append to the log. Warn and ask if more than 15 pages would change.
3. **QUERY:** read the index, then 3-10 relevant pages; answer in 2-5 paragraphs citing `[[page]]` for every claim; mark gaps (VERIFY)/(INCOMPLETE). Offer to file the answer as a synthesis page. Use vault content only.
4. **LINT:** find orphans, broken links, duplicate concepts, stale pages (>90 days or draft), missing sources, contradictions, and isolated clusters. Report with a fix plan; no auto-deletes.

## Frontmatter
```yaml
tags: [entity|concept|source|comparison|synthesis]
date: YYYY-MM-DD
source: "[[sources/page]]"
status: draft|processed|stale
related: []
```

## Output
```
# <Operation> complete: <title>
Summary | Pages created | Pages updated (change) | Contradictions | Next steps
```

## Guardrails
- Never edit, move, or delete anything in `raw/`.
- Show diffs before writing; confirm bulk changes; no deletes without approval.
- Never write secrets or keys into notes; keep sensitive areas the user marks local-only away from cloud models.
- Mark uncertain facts (VERIFY).

_Adapted from: alirezarezvani/claude-skills (llm-wiki, wiki-ingest), MIT; Karpathy's LLM-wiki concept._
