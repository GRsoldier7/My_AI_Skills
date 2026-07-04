---
name: yt-knowledge
description: |
  How to query Aaron's YouTube knowledge DB (Echelon DB2) — supplements, protocols,
  claims, guests, comments, evidence, video moments. Canonical schema map and
  copy-paste SQL patterns so agents use verified query shapes instead of
  spelunking 70+ tables (verify columns first when deviating from the patterns).

  EXPLICIT TRIGGER on: "knowledge DB", "what did <person/channel> say about",
  "find every protocol/supplement mention", "video moments", "timestamp deep link",
  "Echelon DB2 query", "search transcripts", "supplement consensus", "guest
  appearances", "which videos mention", "dosage recommendations across channels",
  "evidence-backed vs bro-science", "commenter reports".

  Also trigger whenever an agent needs biohacking/health entities extracted from
  YouTube content, or Temple Protocol needs citation evidence from videos.
metadata:
  author: aaron-deyoung
  version: "0.9"
  domain-category: product
  adjacent-skills: biohacking-data-pipeline, database-design, yt-pipeline-ops
  last-reviewed: "2026-07-04"
  review-trigger: "P1 chunks land (add moments), P4 views land (v1: swap raw joins for v_knowledge_*)"
  capability-assumptions:
    - "MCP postgres-echelon-db2-ro (read-only) registered in Claude Code"
    - "DB2 = 192.0.2.12:5433/postgres (Supabase CT105)"
    - "Semantic search needs LAN API (agents cannot generate embeddings via MCP)"
  fallback-patterns:
    - "If RO MCP absent: STOP and register postgres-echelon-db2-ro (wrapper in ~/.config/claude-mcp/) — do NOT fall back to the unrestricted admin MCP for Q&A"
    - "If column doubt: verify with list_objects/describe before complex joins"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: a question about YouTube-sourced health/biohacking knowledge (entities, people, evidence, moments)
- Output produces: SQL over DB2 via MCP, or curl to the LAN semantic API, with cited rows
- Can chain from: health-biohacking-protocol (needs community evidence), master-orchestrator
- Can chain into: yt-pipeline-ops (data missing/stale → pipeline fix), anti-hallucination (verify claims)
- Orchestrator notes: prefer this skill's canned patterns over freeform SQL against raw tables

---

## Connection Facts

| Fact | Value |
|---|---|
| MCP server | `postgres-echelon-db2-ro` (read-only role `echelon_ro`) — use for ALL agent queries |
| Admin MCP | `postgres-echelon-db2` (unrestricted R/W) — ops sessions only, never for agent Q&A |
| Physical DB | `192.0.2.12:5433/postgres` — ONE database, four schemas that matter |
| Schema map | `public` = extraction entities + masters + marts + scraped_videos/fact_videos · `core` = transcripts/chunks + evidence (pubmed/trials/safety/scores) · `ops` = pipeline state (extraction_status) · `analytics` = (reserved) |
| Row-count anchors (2026-07-04) | extracted_supplements 10.9k · extracted_claims 31.9k · master_supplements 3.2k · core.video_transcripts 11.1k (100% embedded, vector 1536) · comment_insights 11.6k |
| Coverage caveat | Biohacking topic ≈86% transcribed; ALL other topics <35%. Extraction ≈5.7k distinct videos. Absence of rows ≠ absence of mentions. |

## Data-Trust Legend

- `extracted_*` rows = LLM output; check `ops.extraction_status.extraction_model` per video for provenance (tier prefixes: `local/`, `orfree/`, `cli/`, bare = legacy gemini-flash-lite).
- Entity resolution: raw names → `public.standardized_aliases(raw_name, master_id, confidence_score)` → `master_*`. Join via alias, do NOT string-match master names directly.
- Consensus: `supplement_consensus_v2` (weighted_score, unique_channels, common_dosages, top_channels) — community signal, NOT clinical evidence.
- Clinical evidence: `core.supplement_evidence_score` (4-pillar 0-100 + evidence_spectrum), `core.safety_profiles` (grade A+..F), junctions `core.study_supplements`/`core.trial_supplements` (use `match_confidence >= 0.8`).
- Temple export gate: `mart_protocol_export.published` — unpublished rows are NOT business-approved.
- Timestamps: `core.transcript_chunks.start_seconds` (post-P1). Anchored mentions: `extracted_*.source_chunk_id` (post-P3). NULL anchor = legacy extraction, video-level provenance only.

## Deep-Link Rule

`https://www.youtube.com/watch?v=<video_id>&t=<floor(start_seconds)>s` — only from chunk/anchor rows. Never invent offsets. Pre-P1: link without `&t=`.

## Canonical Query Patterns

Q1/Q3/Q4 need P1/P3 (chunks + anchors). Q2 and Q5–Q10 work TODAY.

**Q5 — Guest appearances + authority** ("every Rhonda Patrick appearance"; DISTINCT — multiple aliases/rows per video otherwise duplicate):
```sql
SELECT DISTINCT mg.canonical_name, ga.authority_tier, ga.appearance_count,
       eg.video_id, fv.title, fv.published_at
FROM public.master_guests mg
JOIN public.view_guest_authority ga ON ga.master_id = mg.id
JOIN public.guest_aliases gal ON gal.master_id = mg.id
JOIN public.extracted_guests eg ON lower(eg.guest_name) = lower(gal.raw_name)
JOIN public.fact_videos fv ON fv.video_id = eg.video_id
WHERE mg.canonical_name ILIKE '%rhonda patrick%'
ORDER BY fv.published_at DESC NULLS LAST;
```

**Q6 — Product recs w/ affiliate links** (URL grain and supplement grain are SEPARATE — joining them on video_id fan-outs and pairs wrong discount codes; run as two queries):
```sql
-- 6a: affiliate URLs for a product
SELECT eau.likely_product, eau.affiliate_network, eau.full_url, eau.discount_code,
       fv.title, sv.channel_name
FROM public.extracted_affiliate_urls eau
JOIN public.fact_videos fv ON fv.video_id = eau.video_id
LEFT JOIN public.scraped_videos sv ON sv.video_id = fv.video_id
WHERE eau.likely_product ILIKE '%<product>%';
-- 6b: supplement mentions flagged affiliate w/ discount codes
SELECT es.supplement_name, es.discount_code, fv.title, sv.channel_name
FROM public.extracted_supplements es
JOIN public.fact_videos fv ON fv.video_id = es.video_id
LEFT JOIN public.scraped_videos sv ON sv.video_id = es.video_id
WHERE es.is_affiliate AND es.supplement_name ILIKE '%<name>%';
```
(`fact_videos` has NO channel_name — join `scraped_videos` for it.)

**Q7 — Evidence-backed vs bro-science filter** (supplement level):
```sql
SELECT ms.canonical_name, ses.combined_score, ses.evidence_spectrum,
       sp.overall_safety_grade, scv.weighted_score AS community_score, scv.unique_channels
FROM public.master_supplements ms
LEFT JOIN core.supplement_evidence_score ses ON ses.master_supplement_id = ms.id
LEFT JOIN core.safety_profiles sp ON sp.master_supplement_id = ms.id
LEFT JOIN public.supplement_consensus_v2 scv ON scv.master_supplement_id = ms.id
WHERE ms.canonical_name ILIKE '%<supplement>%';
```

**Q8 — Commenter anecdotes** (LLM summaries of comments — anecdotal signal, NOT validation; filter content, not just title):
```sql
SELECT ci.analysis_type, ci.confidence, ci.content, ci.source_comment_ids
FROM public.comment_insights ci
JOIN public.fact_videos fv ON fv.video_id = ci.video_id
WHERE ci.analysis_type IN ('experience_report','side_effect')
  AND (ci.content::text ILIKE '%<topic>%' OR fv.title ILIKE '%<topic>%')
ORDER BY ci.confidence DESC LIMIT 25;
```

**Q9 — Safety/interaction check**:
```sql
SELECT sp.overall_safety_grade, sp.known_side_effects, sp.drug_interactions,
       sp.contraindications, sp.max_safe_dose
FROM core.safety_profiles sp
JOIN public.master_supplements ms ON ms.id = sp.master_supplement_id
WHERE ms.canonical_name ILIKE '%<supplement>%';
```

**Q10 — Coverage/ops** ("what's extracted, what's stale"):
```sql
SELECT extraction_status, count(*) FROM ops.extraction_status GROUP BY 1;
-- per-video detail: public.mart_video_intelligence (pipeline_state, extraction_model, per-entity counts)
```

**Q2 — Dosage consensus (works today, dosage drilldown improves post-P3)**:
```sql
SELECT scv.common_dosages, scv.weighted_score, scv.unique_channels, scv.top_channels
FROM public.supplement_consensus_v2 scv
JOIN public.master_supplements ms ON ms.id = scv.master_supplement_id
WHERE ms.canonical_name ILIKE '%magnesium glycinate%';
-- drilldown to raw mentions. TRAP: form-specific masters (e.g. 'Magnesium Glycinate')
-- are alias-sparse — mentions normalize under the BASE master with the form in
-- es.specific_form. Resolve base master exactly, filter form separately:
SELECT DISTINCT es.dosage_amount, es.dosage_frequency, es.timing, es.specific_form,
       es.recommendation_strength, es.sentiment, sv.channel_name, fv.title
FROM public.extracted_supplements es
JOIN public.standardized_aliases sa ON lower(sa.raw_name) = lower(es.supplement_name)
                                   AND sa.confidence_score >= 0.8
JOIN public.fact_videos fv ON fv.video_id = es.video_id
LEFT JOIN public.scraped_videos sv ON sv.video_id = es.video_id
WHERE sa.master_id = (SELECT id FROM public.master_supplements WHERE canonical_name = 'Magnesium')
  AND es.specific_form ILIKE '%glycinate%';   -- validated: 22 distinct dosage/form rows
```

**Q1 — "Every protocol <person> recommended for <goal>, with timestamps"** (post-P3/P4; pattern):
protocols via `extracted_protocols` + channel via `scraped_videos.channel_name` (host) or Q5 join (guest) + timestamp via `source_chunk_id → core.transcript_chunks.start_seconds`.

**Q3 — Moment lookup / Q4 — cross-video claim comparison** (semantic, see below).

## Semantic Access (agents cannot embed via MCP)

1. **LAN API** (embedding handled server-side, TTL-cached): `curl -s -X POST http://192.0.2.10/search -H "X-API-Key: $ECHELON_API_KEY" -H 'Content-Type: application/json' -d '{"query":"<text>","search_type":"transcripts","match_count":10}'` — post-P4 also `POST /moments`.
2. **Stored-embedding self-join** (pure SQL, no embedding call) — claim-to-claim similarity:
```sql
WITH seed AS (
  SELECT id, embedding FROM public.extracted_claims
  WHERE claim_text ILIKE '%creatine timing%' AND embedding IS NOT NULL
  ORDER BY id LIMIT 1                          -- deterministic seed
)
SELECT ec.claim_text, ec.evidence_type, ec.strength, fv.title,
       1 - (ec.embedding <=> s.embedding) AS similarity
FROM seed s                                    -- join FROM seed: empty seed → zero rows, not arbitrary rows
JOIN public.extracted_claims ec ON ec.embedding IS NOT NULL AND ec.id <> s.id
JOIN public.fact_videos fv ON fv.video_id = ec.video_id
ORDER BY ec.embedding <=> s.embedding LIMIT 15;
```

## Do-Nots

- No writes, ever, from this skill's context — RO MCP enforces it; don't reach for the admin MCP.
- No `SELECT *` on `public.video_comments` (partitioned, huge) — always filter video_id + LIMIT.
- No string-matching `master_*.canonical_name` from raw extracted names — go through `standardized_aliases`.
- No fabricated timestamps — no chunk row, no `&t=`.
- No trusting `pg_stat_user_tables` estimates here — stale; use count(*) on small tables only.
- Search fns: sane params — `match_threshold 0.5`, `match_count ≤ 20`.
