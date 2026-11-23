---
name: technical-seo-baseline
description: >-
  Use when making or reviewing any SEO change (page edits, schema, redirects,
  robots, sitemap, an SEO PR) or when asked for a technical SEO check: capture
  a public-signal baseline before and after, triage findings by severity, and
  feed metric rows to outcome-effect-closeout.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---
# Technical SEO Baseline

Public signals only. Search Console and field data rows stay "blocked: D2" or "blocked: no CrUX/PSI key"; never estimate them.

## Steps
1. **Baseline before.** Run `python3 scripts/seo_baseline.py https://<site> --sample 5 --json runs/<slug>/baseline-before.json`. Re-run with the same sample size after the change (`baseline-after.json`). Exit 2 means the home page was unreachable: report it, do not continue as if measured.
2. **Closeout rows.** Give outcome-effect-closeout these metrics, before vs after, each with `measured_at` (CT): home status, sitemap URL count, robots status, Sitemap lines, title present, meta description present, canonical self, noindex flag, JSON-LD parse errors, per-bot "/" allowed. A metric not re-measured is "not re-measured", never copied forward.
3. **Triage every finding.**
   - Critical: home not 200 or redirect loop; robots.txt disallows "/" for Googlebot or Bingbot unintentionally; stray noindex on a money page; canonical pointing off-site or to a non-200; 5xx on robots.txt; HTTPS broken; sitemap missing or listing non-200 URLs.
   - High: canonical missing or not self-referencing on key pages; redirect chain over 1 hop; missing title; JSON-LD parse error; search/citation bot blocked (OAI-SearchBot, Claude-SearchBot, PerplexityBot) against intent; key content absent from raw HTML.
   - Medium: no meta description; title over 60 or meta over 160 chars; zero or multiple H1; no Sitemap line in robots.txt; duplicate or conflicting JSON-LD; FAQPage kept without visible Q&A.
   - Low: llms.txt absent (no weight); FAQPage present (no rich result since 2026-05-07); HowTo present (deprecated); training bots allowed or blocked (licensing preference, not an error).
4. **Core Web Vitals:** report LCP, INP, CLS as "blocked: no CrUX/PSI key" unless a key exists; with a key, quote field data with its date. Never estimate from page weight or feel.
5. **Triage output** to `runs/<slug>/seo-findings.md`: `| severity | finding | URL | evidence | fix | owner |`.

## Pre-merge checklist (SEO PRs on the Next.js site)
Run on the Vercel preview URL, not production:
1. Pages render with JS off for the changed content, title, canonical, meta robots, JSON-LD.
2. Sitemap includes new URLs and drops removed ones; every sitemap URL returns 200.
3. Redirects: old URL to new URL in 1 hop, 301, no chains or loops.
4. Canonical is self-referencing and absolute; no conflicting noindex.
5. Schema matches visible text exactly (names, prices, dates, Q&A); validates in the Rich Results Test.
6. Forms and CTAs exercised end to end on the preview: submit, success state, destination, no console errors. If it cannot be exercised, state "not exercised".
7. `seo_baseline.py` on preview vs production shows no new Critical or High findings.
For the static consulting site (repo not on the box), deliver changes as drafts with the same checklist for the owner to run.

## Guardrails
- Drafts and PRs only; never merge, deploy, publish, change robots/DNS/redirects live, or submit forms with real data without Aaron's explicit per-action approval.
- Never invent measurements; mark unverified items [VERIFY]; the script sends GET/HEAD only. No credentials.

_Adapted from: AgriciDaniel/claude-seo (seo-technical), MIT; seo_baseline.py checks are original to this team._
