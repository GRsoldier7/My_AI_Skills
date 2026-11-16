---
name: schema-markup-jsonld
description: >-
  Use when adding, auditing, or fixing JSON-LD / schema.org structured data
  (Organization, LocalBusiness, Service, Article, FAQPage, Product,
  BreadcrumbList, Person) for rich results and AI search visibility.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Schema Markup (JSON-LD)

## Gather
Existing schema and Search Console errors; CMS and whether `<head>` can be edited; the real visible content for each type (organization name/logo/address/phone/social; article headline/author/dates/image; FAQ Q&A as shown on the page; LocalBusiness hours and geo; Person title and profiles).

## Pick types
Homepage: Organization + WebSite. Service page: Service + Organization + BreadcrumbList. Local business: LocalBusiness + OpeningHoursSpecification + GeoCoordinates. Blog post: BlogPosting + Person + BreadcrumbList. FAQ: FAQPage. Product: Product + Offer (AggregateRating only with real visible reviews). Add BreadcrumbList when breadcrumbs are visible; link entities with `@id`.

## Workflow
1. **Mode:** audit, implement, or fix.
2. **Audit:** review each `application/ld+json` block for `@context`, correct `@type`, required fields, absolute URLs, ISO 8601 dates, and a match with visible content; cross-check Search Console.
3. **Generate** JSON-LD from real content; use `[PLACEHOLDER]` for missing values.
4. **Validate:** required fields present, no empty or "N/A" values, no duplicate or conflicting types, nothing describing invisible content.
5. **Test** in Google's Rich Results Test and validator.schema.org; monitor Search Console for 1-2 weeks after deploy.
6. **Deploy notes** per platform (direct `<head>`, WordPress plugin, Webflow custom code). Avoid duplicating plugin-generated schema; prefer server-side over tag-manager injection.

For AI visibility, prioritize FAQPage, Organization `sameAs` to verified profiles, authors as Person with `sameAs`, and accurate dates.

## Output
```
SCHEMA FOR: [page type]
<script type="application/ld+json">{ ... }</script>
PLACEHOLDERS: [list] | VALIDATION: [checks passed]
NEXT: fill placeholders -> test -> paste in <head> -> monitor
```

## Guardrails
- Never fabricate facts, reviews, ratings, or awards; never mark up invisible content.
- Draft code only; never publish or deploy without explicit approval.
- No credentials. Mark unverified values [VERIFY].

_Adapted from: alirezarezvani/claude-skills (schema-markup), MIT._
