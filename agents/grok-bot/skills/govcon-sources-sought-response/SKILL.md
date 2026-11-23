---
name: govcon-sources-sought-response
description: >-
  Use when a federal sources sought notice or RFI (market research) screened
  SHAPE or better needs a response: checklist, notice-fact check, proof-point
  matrix, set-aside compliance, response draft, capability statement, and agency
  feedback. Not for RFPs; those go to govcon-proposal-compliance-matrix.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---
# GovCon Sources Sought Response

Firm baseline (do not exceed): use only the operator-provided firm profile (registration, certifications, past performance, headcount, and contract vehicles). Do not invent facts or exceed that baseline.

## Inputs
Notice text and attachments; the verified firm facts file; the govcon-bid-no-bid-screening result (must be SHAPE or better). If any is missing, mark [REQUIRED] and stop.

## Workflow
1. **Response checklist.** Parse the notice's own response instructions. Every shall/should/"respondents should identify" becomes a numbered row, in the agency's order and wording: Item | Notice section | Our section | Status | Evidence.
2. **Verify notice facts.** Check solicitation number vs the SAM record, due date/time converted to CT (name the source zone; for ET notices get EST vs EDT and the CT time with `TZ=America/Chicago date -d 'TZ="America/New_York" <YYYY-MM-DD> <HH:MM>'`, never from memory), NAICS and size standard (current fiscal year), and set-aside language. List every discrepancy; do not resolve silently.
3. **Proof-point matrix.** For each requested capability rate STRONG / PARTIAL / GAP. STRONG and PARTIAL need a verifiable source (firm facts file, SBA certification letter, SAM record). Keep GAPs visible and answer them honestly, including how the gap would close through similarly situated teaming partners; name a partner only when Aaron has confirmed the relationship in writing, else write [CONFIRM partner].
4. **Set-aside compliance.** Address limitations on subcontracting (13 CFR 125.6); for VA set-asides also VAAR 852.219-73/-74; and the ostensible subcontractor rule (13 CFR 121.103(h)) for any planned partner role. Mark each [VERIFY] against current text. Never imply a vehicle, certification, staff, or past performance the firm lacks.
5. **Draft the response.** Follow the checklist order. Buyer-focused and specific; no marketing language; every claim traceable to evidence. Unverified items become [VERIFY] or [CONFIRM ...]. Contact data stays as placeholders.
6. **Capability statement (1 page).** Core competencies tied to this notice; differentiators that are true; firm data block; NAICS; certifications; POC placeholders. No UEI/CAGE in this skill; pull from the facts file or leave placeholders.
7. **Agency feedback** (only where the notice invites it). Flag restrictive requirements; recommend set-aside and contract type; give a reason for each.
8. **Reviewer notes for Aaron.** Open [VERIFY] items, decisions needed, submission method, and deadline in CT.

Before handoff run output-quality-no-slop and evidence-before-claims on the full draft.

## Output
```
SOURCES SOUGHT RESPONSE: [notice ID - title] | agency | due [date time CT]
Screening: [result]
1 Checklist | 2 Notice-fact discrepancies | 3 Proof-point matrix
4 Set-aside compliance notes | 5 Response draft | 6 Capability statement
7 Agency feedback | 8 Reviewer notes
```
Over ~25 lines: write to a file, reply with the path and a short summary. Log to runs/<slug>/history.jsonl; close with `Shipped: ... · Verified: ... · Effect: ...`.

## Guardrails
- Mark every deliverable DRAFT - USER SUBMITS.
- Never submit, email, post, or contact the CO or any partner; Aaron does that per action.
- Never fabricate or imply past performance, staff, vehicles, or certifications.
- Never invent facts; mark unverified items [VERIFY]; no credentials in outputs.
- Times in America/Chicago with a "CT" label.

_Adapted from: alirezarezvani/claude-skills (rfp-responder), MIT; ThomasMoreAI/legal-skills-open us/government-contracts (rfp-response; originally CaseMark/skills), Apache-2.0; condensed and restructured for sources sought and RFI responses._
