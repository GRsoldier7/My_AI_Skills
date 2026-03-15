---
name: brand-website-strategy
description: |
  Build and refine brand identity, website strategy, and digital presence for a tech/health startup. This skill covers brand positioning, visual identity systems (colors, typography, logo direction), website architecture and content strategy, SEO fundamentals, conversion optimization, and competitive positioning in the health tech and AI consulting space. Use this skill whenever the user mentions branding, website, logo, colors, fonts, brand voice, brand guidelines, landing pages, SEO, website copy, content strategy, marketing materials, visual identity, or wants to "get the website together" or "build out branding." Also trigger when the user asks about positioning, messaging, taglines, or how to present their business to the world — even if they frame it as "how do I look professional" or "what should my site say."
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: product
  adjacent-skills: business-genius, market-intelligence, portable-ai-instructions
  last-reviewed: "2026-03-15"
  review-trigger: "Significant brand pivot, target audience change, major shift in web tech stack landscape"
---

# Brand Identity & Website Strategy

You are helping build the brand and digital presence for a business that spans two domains: AI consulting (helping companies grow with automation and AI, especially Power Platform) and a biohacking/health tech product (personalized health protocols powered by data and AI). These may end up as one unified brand or two separate brands — the strategy work here helps make that decision and execute either way.

## Brand strategy fundamentals

Before touching colors, fonts, or websites, nail down the strategic foundation. Every visual and content decision flows from this.

### Brand positioning framework

Work through these questions with the user:

**1. Who is the customer?**
- For AI consulting: What size companies? What industries? Who's the decision-maker (CTO, CEO, operations manager)?
- For the biohacking tool: Who's the target user? Biohackers? General wellness consumers? Practitioners? Athletes?
- Understanding the customer deeply determines everything — tone, channels, pricing, visual style.

**2. What's the core value proposition?**
- Not "what do you do" but "what transformation do you deliver?"
- For consulting: "We don't just build automations — we teach your team to think in systems, so AI becomes a competitive advantage you own, not a dependency on consultants."
- For biohacking: "Your blood work tells a story. We use AI to read it and write you a personalized protocol backed by real evidence."
- Help the user craft their own versions of these — they need to be authentic and specific.

**3. What makes this different?**
- The intersection of deep technical skill AND teaching ability is rare in AI consulting
- For the biohacking tool, the data quality and evidence-based approach is the differentiator
- Identify 2-3 things competitors can't easily copy

**4. Brand personality**
- Where on the spectrum: Clinical ↔ Approachable? Technical ↔ Accessible? Corporate ↔ Startup?
- For health tech: trustworthy and evidence-based but not cold or medical-industrial
- For AI consulting: expert and forward-thinking but not intimidating or jargon-heavy
- The brand should feel like talking to someone who's genuinely brilliant but also genuinely helpful

### One brand or two?

Help the user evaluate:

**One unified brand** works if the consulting and the product share a common thesis (e.g., "We use AI to make complex systems understandable and actionable — whether that's your business operations or your biology").

**Two separate brands** work if the audiences are completely different and cross-pollination would confuse either audience. A CTO hiring an AI consultant might be put off by supplement recommendations in the sidebar.

**Hybrid approach:** One parent brand with distinct sub-brands or product lines. This is often the most flexible option for a solo founder who might add more products later.

## Visual identity system

When designing or discussing visual identity:

### Color palette

A strong brand needs:
- **1 primary color** — the color people associate with the brand
- **1-2 secondary colors** — complementary colors for variety
- **1 accent color** — for CTAs, highlights, important UI elements
- **Neutral palette** — grays, near-whites, near-blacks for text and backgrounds

For health/biotech, effective palettes often include:
- Greens and teals (health, growth, vitality)
- Deep blues (trust, science, reliability)
- Clean whites (clinical precision, clarity)
- Warm accents (orange, amber) to avoid feeling cold

Provide specific hex codes, not vague descriptions. Check contrast ratios for accessibility (WCAG AA minimum: 4.5:1 for text).

### Typography

Recommend specific Google Fonts (free, web-ready) pairings:
- **Heading font:** Something with character — the personality carrier
- **Body font:** Something highly readable — the workhorse
- **Mono font** (optional): For technical content, data displays, code

Pairings that work well for tech/health:
- Inter (headings) + Source Sans Pro (body) — clean, modern, techy
- Space Grotesk (headings) + DM Sans (body) — distinctive, contemporary
- Outfit (headings) + Plus Jakarta Sans (body) — friendly but professional

### Logo direction

Don't design logos (that's a designer's job), but provide strategic direction:
- What should the logo communicate at a glance?
- Wordmark vs. symbol vs. combination?
- What should it look like at 16px (favicon) vs. full size?
- Recommend that the user work with a designer on Fiverr, 99designs, or similar once the strategic direction is clear

## Website architecture

### Site structure

For a combined consulting + product business:

```
Homepage
├── About (story, credentials, mission)
├── AI Consulting
│   ├── Services (what you offer)
│   ├── Case Studies (results you've delivered)
│   └── Contact / Book a Call
├── [Product Name] (the biohacking tool)
│   ├── How It Works
│   ├── Features
│   ├── Pricing
│   └── Sign Up / Waitlist
├── Blog / Resources
│   ├── AI & Automation articles
│   └── Biohacking & Health articles
└── Footer (legal, social links, newsletter)
```

### Homepage framework

The homepage is the most critical page. Structure it as:

1. **Hero section** — Bold headline (value prop), supporting subhead, primary CTA. This needs to answer "what is this and why should I care" in under 5 seconds.
2. **Social proof** — Client logos, testimonials, data points ("500+ biomarkers tracked", "20+ companies transformed")
3. **Problem → Solution** — Briefly articulate the pain point and how you solve it
4. **Services/Products overview** — Cards or sections for each offering
5. **Trust builders** — Certifications, media mentions, testimonials with photos
6. **CTA** — Clear next step (book a call, join waitlist, etc.)

### Tech stack recommendation for the website

For a founder who codes and needs something that can grow:

- **Next.js** (React framework) — great for SEO (server-side rendering), fast, flexible
- **Tailwind CSS** — utility-first CSS, rapid development, consistent design
- **Vercel** (hosting) — seamless with Next.js, excellent performance, generous free tier
- **Sanity or Contentlayer** (CMS) — for blog content management
- **Plausible or PostHog** (analytics) — privacy-friendly, better than Google Analytics for trust in health space

Alternatively, if speed-to-launch matters more:
- **Framer** or **Webflow** — visual builders that produce clean code, fast to iterate, no coding required for content updates

### SEO fundamentals

For a new site, focus on these high-impact basics:

- **Keyword research:** For each page, identify 1-2 target keywords using free tools (Google Keyword Planner, Ubersuggest, or AnswerThePublic)
- **On-page SEO:** Title tags, meta descriptions, H1/H2 structure, image alt text
- **Content strategy:** Blog posts targeting long-tail keywords in both domains (AI consulting and biohacking). Aim for depth over frequency — one excellent article per week beats five thin ones
- **Technical SEO:** Fast loading times (< 2s), mobile responsive, proper sitemap, structured data (Schema.org)
- **Local SEO:** If consulting has a geographic focus, claim Google Business Profile

### Conversion optimization

Every page should have a clear purpose and a clear CTA:
- Homepage → Book a consultation call OR Join the product waitlist
- Blog posts → Newsletter signup (lead magnet: free guide, checklist, etc.)
- Product page → Sign up / Join waitlist
- Consulting page → Book a discovery call (embed Calendly or Cal.com)

## Content strategy

### Brand voice guidelines

Help the user define how the brand "talks":

- **Tone:** Confident but not arrogant. Expert but accessible. Passionate but grounded.
- **Language:** Avoid jargon when possible. When technical terms are necessary, define them naturally.
- **Point of view:** First person ("I/we") for consulting (personal relationship), third person for the product ("the platform analyzes...").
- **Banned phrases:** "leverage synergies," "disrupting," "revolutionary" — anything that sounds like empty startup speak. Be specific and concrete instead.

### Content pillars

Organize all content around 3-4 recurring themes:
1. **AI that works** (consulting: practical AI adoption, automation wins, Power Platform tips)
2. **Evidence-based health** (biohacking: science-backed protocols, biomarker education, myth-busting)
3. **Building in public** (founder journey: lessons, wins, transparency about the process)
4. **Data-driven decisions** (cross-cutting: how data changes outcomes in business and health)

## What good output looks like

When this skill triggers, depending on what the user needs:

- **Brand strategy session:** Walk through the positioning framework, help articulate value props, make recommendations on brand personality and architecture
- **Visual identity:** Provide specific color palettes (hex codes), font pairings, and logo direction
- **Website plan:** Deliver a complete site map, page-by-page content outline, tech stack recommendation, and SEO strategy
- **Content:** Write actual website copy, blog post outlines, or social media content that matches the brand voice
- **Competitive positioning:** Research competitors' websites and brands, identify gaps, recommend differentiation strategies

Always be specific and actionable. "Your brand should feel premium" is useless. "Use a dark teal (#0D4F4F) primary with warm cream (#FFF8F0) backgrounds, Space Grotesk headings at 700 weight, and keep sentence length under 20 words in hero copy" is useful.

---

## Anti-Patterns

**Anti-Pattern 1: Building Before Positioning**
Designing logos, choosing colors, and building the website before the positioning and value proposition
are locked down. Visual decisions made without a strategic foundation have to be redone when the brand
positioning clarifies.
Fix: Always nail the answers to the four positioning framework questions first. Only start visual
identity work after "what makes this different" has a crisp, specific answer.

**Anti-Pattern 2: Appealing to Everyone**
Writing brand copy and designing visuals that are "professional" but bland — trying not to alienate
anyone and ending up not resonating with anyone. This is especially tempting for a founder who spans
two audiences (consulting clients and biohacking consumers).
Fix: Pick a primary audience for each brand touchpoint and speak directly to them. Accept that the
brand will repel some people — that's evidence it's connecting with the right people.

**Anti-Pattern 3: Launching Without a Clear CTA**
Building a beautiful website with no dominant call to action, or multiple competing CTAs of equal
visual weight. Visitors don't know what to do, so they leave.
Fix: Every page has exactly one primary CTA. Everything else is secondary. For a pre-launch product
site, the CTA is always "join waitlist" or "book a call" — never "learn more" (which goes nowhere).

---

## Quality Gates

- [ ] Four positioning framework questions answered before any visual work begins
- [ ] One-brand vs. two-brand decision made explicitly with documented rationale
- [ ] Color palette has specific hex codes and passes WCAG AA contrast ratio (4.5:1 for text)
- [ ] Every page has exactly one dominant CTA
- [ ] Tech stack recommendation matches founder's technical skill level and launch timeline
- [ ] Content pillars defined and at least 3 blog post topics identified per pillar

---

## Failure Modes and Fallbacks

**Failure: Brand identity doesn't convert visitors to leads/signups**
Detection: Website traffic is reasonable but conversion to newsletter signups, waitlist joins, or
consultation bookings is <2%.
Fallback: The problem is almost always one of three things: unclear value proposition (visitor
doesn't understand what they get), weak CTA (visitor doesn't know what to do), or wrong audience
(traffic doesn't match ideal customer profile). Run a 5-second test: show the homepage to someone
unfamiliar with the business and ask "what does this company do and who is it for?"

**Failure: Consulting and product brands confuse each other's audiences**
Detection: Consulting prospects ask about the biohacking product before engaging on the consulting
work. Product users reach out to the consulting page.
Fallback: If one brand is consistently cannibalizing the other, separate them more clearly.
The hybrid approach still works but needs cleaner routing: the homepage nav should have "For businesses"
(consulting) and "For individuals" (product) as top-level paths with distinct visual language.

---

## Composability

**Hands off to:**
- `market-intelligence` — when competitive positioning requires deep competitor brand analysis
- `portable-ai-instructions` — when the website is being built and AI tool configs need to be set up for the project

**Receives from:**
- `business-genius` — business strategy decisions (one brand vs. two, target audience) inform brand positioning
- `market-intelligence` — competitive landscape analysis informs differentiation strategy and messaging
