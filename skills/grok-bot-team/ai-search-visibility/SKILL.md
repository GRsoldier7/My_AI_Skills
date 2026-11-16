---
name: ai-search-visibility
description: >-
  Use when auditing or improving how a site is found and cited in AI answer
  surfaces (Google AI Overviews and AI Mode, ChatGPT search, Perplexity, Claude,
  Copilot): AI crawler access, citable passages, entity consistency, brand
  presence, llms.txt questions, or a citation spot-check baseline.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---
# AI Search Visibility

Google's stance: optimizing for generative AI search is still SEO; no special markup or AI files are needed for AI Overviews or AI Mode. When community advice conflicts with Google or other primary sources, follow the primary source and note the conflict in the report. Other engines reward extractable structure, so apply it without writing separate "AI-only" content.

## Steps
1. **Crawler access.** Fetch robots.txt (run `technical-seo-baseline` first) and report each bot on its own. Search/citation bots and training bots are separate controls.
   | Claim | Check this bot | Not this one |
   |---|---|---|
   | Citable in ChatGPT search | OAI-SearchBot | GPTBot (training) |
   | Citable in Claude search | Claude-SearchBot | ClaudeBot (training) |
   | Citable in Perplexity | PerplexityBot | - |
   | In Google Search, AI Overviews, AI Mode | Googlebot | Google-Extended |
   | Gemini/Vertex training and grounding | Google-Extended | Googlebot |
   | Apple search surfaces | Applebot | Applebot-Extended (training opt-out) |
   Rule: report each claim with its own bot; never merge into one "AI allowed" line. User-triggered fetchers (ChatGPT-User, Claude-User) are separate; robots.txt may not govern them. Check CDN/WAF blocks when robots.txt allows but fetches fail [VERIFY].
2. **llms.txt.** Report present yes/no only. It gets no ranking or citation weight; Google says it does not help or hurt visibility.
3. **Rendering.** Fetch raw HTML (no JS). Key content, title, canonical, meta robots and JSON-LD must be in it; many AI crawlers do not run JS.
4. **Citability checks per priority page:**
   - Answer-first passage of 40-60 words directly under a question-style H2/H3 (a readability heuristic, not a Google rule; do not chunk pages into fragments).
   - Specific numbers, each with a named source and date; no unsourced stats.
   - Visible published and updated dates; refresh only pages whose facts changed.
   - Named author with credentials; working About page; real contact details.
   - Entity consistency: same name, address, phone, descriptions on site, schema, and profiles.
   - One owning page per fact (price, scope, method); no conflicting copies.
5. **Spot-check baseline (manual).** Pick 5-10 buyer-intent queries per site, phrased as users type them. Run each in Google (AI Overviews/AI Mode), ChatGPT search, Perplexity at least 3 times, since answers vary run to run. Record in a dated table:
   `| date CT | query | engine | runs cited/total | domains cited | our page | competitors |`
   Report a rate with its sample size ("cited 2/3"), never a single run. Repeat monthly; compare rates, not anecdotes.
6. **Presence actions (recommend only).** Make third-party profiles (directories, review sites, LinkedIn, Crunchbase) match the About page; list real publications and communities where the entity is already discussed; propose original data or research worth citing. Shortlist recommendations lean on third-party consensus, so citation of our own page does not equal recommendation.
7. **Do not recommend:** mention farming or bulk forum posting, keyword stuffing, fake or incentivized-undisclosed reviews, doorway or location-spam pages, content written only for bots, invented awards or stats.
8. Search Console has a Generative AI performance report (Google AI optimization guide, updated 2026-07-10); those rows stay "blocked: D2" until access exists.

## Output
```
AI VISIBILITY: [site] | [date CT]
Crawler table (one row per bot, status, capability) | llms.txt: yes/no (no weight)
Rendering: raw-HTML content ok? | Citability findings by page (Critical..Low)
Spot-check table | Presence gaps | Next 3 actions | [VERIFY] list
```
Long output: write to a file, reply with path plus short summary.

## Guardrails
- Drafts and recommendations only; never edit robots.txt, post, publish, deploy, or contact third parties without Aaron's explicit per-action approval.
- Never invent citations, stats, or engine behavior; mark unverified items [VERIFY]. No ranking or citation promises. No credentials.

_Adapted from: AgriciDaniel/claude-seo (seo-geo), MIT; coreyhaines31/marketingskills (ai-seo), MIT; Google Search Central AI features guidance (facts cited as stated there)._
