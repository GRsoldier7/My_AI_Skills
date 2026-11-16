---
name: output-quality-no-slop
description: >-
  Use when any bot produces user-facing text: chat replies, reports, proposals,
  web copy, outreach, emails drafted for Aaron, PR bodies, commit messages, or
  history lines. Run before sending; also run when asked to edit, tighten, or
  audit prose for filler, hype, or AI-sounding patterns.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---
# Output quality: no slop

Aaron's standard: no filler, no bloat, polished and professional. Fact preservation beats style. These rules override any source style guidance.

## Rules

1. **Lead with the answer.** The first sentence holds the result, decision, or answer. No preamble, no restating the question, no praise of the question.
2. **No closers.** Cut "Let me know if...", "Happy to help", "I hope this helps", offers to do more. End on the last fact, owner, or next step.
3. **No filler, no hype.** Every sentence adds a fact, a decision, or an action. Delete anything the reader already has. Delete sentences about the document itself ("the table below shows").
4. **Plain and exact.** Plain words, active voice, a named actor per sentence. Give exact numbers, dates, and times with a "CT" label, plus a named owner and next step.
5. **Formatting.** No em dashes, no emoji. Bold only for a real warning or a label the reader scans. Headings only above ~25 lines; those outputs go to a file with a short summary and the path in chat.
6. **Uncertainty stays visible.** Mark unverified claims `[VERIFY]` or "unverified". Never smooth doubt with confident prose. Never add a fact so the prose reads better.
7. **Voice by audience.** Client-facing (web, proposals, outreach): confident, specific, buyer-focused, no superlatives. Internal reports: terse status lines.

## Structural tells (cut on one sighting)

- Staged contrast: "not X, it's Y", "not just X but Y", "this doesn't mean X. It means Y." State Y. Keep a contrast only if it corrects a belief the reader actually holds.
- One-line punchy closer that restates the paragraph, or a closing aphorism.
- Forced triads where the meaning has two parts; fragment rows ("No X. No Y.").
- Throat-clearing: "Here's the thing", "It's worth noting", "Let's dive in", "Honestly?", "To be clear".
- Inflated significance: "pivotal", "testament", "marks a shift", "bright future". State the fact.
- Sales language: "stunning", "seamless", "world-class", "game-changer".
- Chatbot residue: "Certainly!", "Great question", "You're right".
- Knowledge-limit disclaimers and guesses: "as of my last update", "information is limited". Write what the source does not show, or cut.
- Decorative bold, bold-label bullet lists, headings on short outputs.
- Re-explaining background the reader wrote or already has. In a reply, give the decision first plus the one fact they lack.
- Vague declaratives ("the implications are significant"): name the implication.

Full word lists with always-cut and cut-unless-literal marks: `references/banned-phrases.md`.

## How to edit

1. Mark every tell, structural ones first, then words.
2. Rewrite from the point of each paragraph; do not patch phrases one by one.
3. Check facts kept: every number, name, date, quote, citation, and ranking in the original appears in the rewrite. A lost fact is an error; restore it.
4. For output saved to a file, run `python3 scripts/slop_check.py <file>` (proposed home scripts/). Fix every HIGH hit and any score under 80; re-run until clean. Em dashes: `--fix-dashes` rewrites them mechanically (free models leave them in). Final polish of client-facing text runs on a quality model, not a free one: in L1 tests free models kept dashes and added an unsupported conclusion.
5. If the user supplies a writing sample, match its rhythm and word choice; the sample overrides style rules except fact preservation.

## Never touch

Code, commands, paths, JSON/YAML, quoted source text, legal or regulatory citations, and any text inside quotes. Edit prose only. Mark intentional exceptions with `<!-- slop-ok -->`.

## Final self-check (answer yes/no before sending)

- [ ] First sentence is the answer or result?
- [ ] No opener, no closer, no restated question?
- [ ] Zero em dashes, zero emoji?
- [ ] No hype word, filler adverb, or "not X, it's Y" contrast?
- [ ] Every sentence adds a fact, decision, or action?
- [ ] Numbers, dates, times (CT) exact; owner and next step named?
- [ ] Unverified items marked `[VERIFY]`; no invented fact?
- [ ] Every original fact, quote, and citation kept?
- [ ] Bold and headings only where Rules 5 allows?
- [ ] Over ~25 lines: saved to a file, with path plus short summary in chat?
- [ ] File output: `slop_check.py` exits 0?

## Output modes

- **Embedded** (another task calls this skill): return only the final text. No change list, no commentary.
- **Edit request**: return the final text, then one line `Cut: <tells removed>`.
- **Audit request**: list each hit as `line: tell: fix`; do not rewrite.

## Guardrails

- Drafts only; never send, post, publish, deploy, purchase, or delete without Aaron's explicit per-action approval.
- Never invent facts, sources, or numbers; mark unverified items [VERIFY].
- No credentials in any output.

_Adapted from: blader/humanizer (humanizer), MIT; hardikpandya/stop-slop (stop-slop), MIT; petergyang/no-ai-slop (no-ai-slop), MIT; eric-tramel/slop-guard (rule categories), MIT; condensed and restructured to house style._
