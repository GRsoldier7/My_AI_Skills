---
name: schema-markup-jsonld
description: >-
  Use when adding, auditing, or fixing JSON-LD / schema.org structured data
  (Organization, LocalBusiness, Service, Article, FAQPage, QAPage, Product,
  BreadcrumbList, Person) or when a page claims rich results from markup.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---
# Schema Markup (JSON-LD)

## Gather
Existing schema and Search Console errors (or "blocked: D2" if no access); CMS and whether `<head>` is editable; the real visible content for each type (org name/logo/address/phone/profiles; article headline/author/dates/image; visible Q&A text; LocalBusiness hours/geo; Person title/profiles).

## Type status (per claude-seo, checked Oct 2026; FAQ/HowTo rows verified against Google sources)
| Status | Types |
|---|---|
| Recommend | Organization, WebSite, LocalBusiness, Service, Article, BlogPosting, Person, ProfilePage, BreadcrumbList, Product + Offer, Review/AggregateRating (real visible reviews only), VideoObject, Event, JobPosting |
| Keep, no Google rich result | FAQPage: no Google rich result since May 7, 2026 (Search Console Help). Keep only if the Q&A is visible and helps users or AI answers; never promise a rich result. Use QAPage for genuinely user-answered questions. Dataset: Dataset Search only |
| Deprecated, never recommend | HowTo (rich results removed Sept 2023); SpecialAnnouncement, CourseInfo, EstimatedSalary, LearningVideo, VehicleListing (retired 2025); ClaimReview for SERP features |

Existing FAQPage on a page: report as Info, not Critical; do not recommend removal if the Q&A is visible and useful.

## Pick types
Homepage: Organization + WebSite. Service page: Service + Organization + BreadcrumbList. Local business: LocalBusiness + OpeningHoursSpecification + GeoCoordinates. Article: BlogPosting + Person + BreadcrumbList. Product: Product + Offer. Add BreadcrumbList only when breadcrumbs are visible.

## Workflow
1. **Mode:** audit, implement, or fix.
2. **Audit:** check each `application/ld+json` block: JSON parses; `@context` present once (a `@graph` container needs no `@type`; its entries inherit `@context`); correct `@type`; required fields; absolute URLs; ISO 8601 dates; matches visible content.
3. **One entity graph:** a single `@graph` with `@id` references (Organization `@id` reused as publisher/provider/author affiliation). Flag duplicate disconnected blocks that describe the same entity, and plugin plus hand-written duplicates.
4. **Generate** from real content; `[PLACEHOLDER]` for gaps. `sameAs` only to profiles verified as real and owned (open each URL); never guess profile URLs.
5. **Validate:** no empty or "N/A" values, no conflicting types, nothing describing invisible content, no placeholder text left.
6. **Render location:** Product, Offer, price, availability and other time-sensitive markup must be in the initial server-rendered HTML, not injected by JS or a tag manager. Same for canonical and meta robots. Confirm with a raw-HTML fetch (`seo_baseline.py` reads raw HTML, no JS).
7. **Test** in Google's Rich Results Test and validator.schema.org; monitor Search Console 1-2 weeks after deploy (rows "blocked: D2" until access exists).
8. **Deploy notes** per platform (direct `<head>`, Next.js server component, plugin). Prefer server-side over tag-manager injection.

For AI visibility: schema helps engines parse pages; no study isolates a citation lift, so state none. Prioritize Organization with verified `sameAs`, authors as Person with `sameAs`, accurate dates.

## Output
```
SCHEMA FOR: [page type]
<script type="application/ld+json">{ "@context": ..., "@graph": [ ... ] }</script>
PLACEHOLDERS: [list] | VALIDATION: [checks passed]
NEXT: fill placeholders -> test -> paste in <head> -> monitor
```

## Guardrails
- Never fabricate facts, reviews, ratings, or awards; never mark up invisible content.
- Draft code only; never publish or deploy without Aaron's explicit per-action approval.
- Never promise rich results or ranking lift. No credentials. Mark unverified values [VERIFY].

_Adapted from: alirezarezvani/claude-skills (schema-markup), MIT; AgriciDaniel/claude-seo (seo-schema), MIT; Google Search Console Help and Search Central blog (FAQ/HowTo changes)._
