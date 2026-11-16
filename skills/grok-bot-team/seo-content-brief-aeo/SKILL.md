---
name: seo-content-brief-aeo
description: >-
  Use when planning or refreshing content that should rank in search and get
  cited by AI answer engines: keyword clusters, content briefs, refresh plans,
  and measurement.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# SEO Content Brief + AEO

SEO earns the click; AEO earns the AI citation (clear structure, E-E-A-T, factual density). Both start with intent.

## Inputs (ask if missing)
Business and ideal customer, goal (traffic, leads, authority, citations), target topic and intent, keyword data, top-ranking URLs, word count, net-new or refresh, author credentials, citable facts, compliance limits.

## Workflow
1. **Audience and intent:** persona and funnel stage; classify intent (informational, commercial, navigational, transactional); list 3-5 questions searchers ask.
2. **Keyword cluster:** one pillar plus 5-10 supporting topics, each with a primary keyword, volume (or [VERIFY]), intent, and 2-3 secondaries.
3. **SERP gap analysis:** top 5 results' length, format, and headings; find unanswered questions, missing formats, stale info, and weak E-E-A-T.
4. **Brief:** goal, keywords, intent, 3 title options, a 150-160 character meta description, an H2/H3 outline with key points, key facts ([VERIFY] if unconfirmed), an answer-first FAQ block (5-8), E-E-A-T needs (author bio, sources, first-hand examples), 3-5 internal links, a schema recommendation, CTA, word count, 5-10 sources to cite.
5. **Refresh plan (existing page):** update stale stats, add recent examples, put the key answer in the first 200 words, add FAQ + schema, a byline, citations, short paragraphs, subheads every 300-500 words, image alt text and compression, fixed internal links, an updated modified date.
6. **Measure:** GSC impressions, clicks, CTR, and position for 90 days; monthly AI-citation spot checks; CTA and lead conversions.

## Output
```
Content Brief: [title]
Goal | Primary kw (vol) - intent | Secondary kws | Audience/stage | Words | Author
Titles x3 | Meta | Outline | FAQ | E-E-A-T | Internal links | Schema | CTA | Sources
```

## Guardrails
- Never invent statistics, studies, or citations; mark [VERIFY].
- Drafts only; never publish or delete without explicit approval.
- No ranking guarantees, keyword stuffing, or copying competitors.

_Adapted from: alirezarezvani/claude-skills (content-strategy, aeo), MIT._
