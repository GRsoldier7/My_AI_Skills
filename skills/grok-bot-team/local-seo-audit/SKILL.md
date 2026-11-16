---
name: local-seo-audit
description: >-
  Use when auditing a small business's local search visibility: Google Business
  Profile, NAP consistency, local on-page and technical SEO, citations, reviews,
  and AI-answer visibility, ending in a 30-day plan.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Local SEO Audit

Score seven layers and rate each issue Critical/High/Medium/Low.

1. **Google Business Profile:** most specific primary category plus relevant secondaries; real business name (no keyword stuffing); NAP identical to the site; hours and service areas; services with descriptions; a keyword-first description naming the city; logo, cover, and 10+ fresh photos; weekly posts; seeded Q&A; review count, rating, and response rate (<48h). Critical: unclaimed, NAP mismatch, stuffed name.
2. **NAP consistency:** Google, Apple Maps, Bing Places, Yelp, Facebook, BBB, plus industry directories. Record the exact name, address, phone, URL, and claimed/duplicate status for each. Critical: site/GBP mismatch or duplicate GBPs.
3. **On-page:** homepage title and H1 with service + city; meta description with a CTA; NAP in the footer; click-to-call; a map; one page per service (`[Service] in [City] | [Brand]`); unique location pages with real local detail; FAQ sections.
4. **Technical:** key pages indexed, no stray noindex, sitemap submitted, canonicals, mobile-friendly, Core Web Vitals (LCP <=2.5s, INP <=200ms, CLS <=0.1), HTTPS, LocalBusiness/FAQ schema validated.
5. **Citations:** presence and correctness on tier-1, tier-2, industry, and local (chamber, city) directories; note gaps where competitors appear.
6. **Reviews:** volume, recency (3+ in 30 days), average, response rate and quality, and a real request process (3-7 days after service, Google first).
7. **AI answers (AEO):** FAQ content and schema, natural-language questions, brand + NAP together, author/About pages (E-E-A-T), local backlinks; spot-check "[service] near [city]" in AI assistants and note who gets cited.

**Weighted health score:** GBP 25, NAP 15, on-page 20, technical 15, citations 10, reviews 10, AEO 5.

## Output
```
LOCAL SEO AUDIT - [business] | [url] | [date] | overall X%
Scores by layer
Critical issues (impact, fix) | High priority (effort, expected lift)
30-day plan by week with owner | VERIFY list (what couldn't be checked)
```

## Guardrails
- Recommendations and drafts only: never edit the site or GBP, claim or delete listings, request reviews, or publish without explicit approval.
- Mark anything you couldn't check (no GSC/GBP access, page wouldn't load) as VERIFY.
- Never fabricate reviews or business details. No credentials in outputs.

_Adapted from: alirezarezvani/claude-skills (local-seo-manager, seo-audit), MIT._
