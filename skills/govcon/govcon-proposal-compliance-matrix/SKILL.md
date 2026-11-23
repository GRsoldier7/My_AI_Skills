---
name: govcon-proposal-compliance-matrix
description: >-
  Use when a government RFP/RFQ arrives and needs a compliance matrix from
  Sections L, M, and C/PWS, an outline mirroring the evaluation factors, CO
  questions, and red-team and submission checklists. Drafts only.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# GovCon Proposal Compliance Matrix

## Inputs (flag missing items [REQUIRED] or [VERIFY])
Solicitation number and type, agency, NAICS/set-aside, due date and time zone (flag if <10 business days), Sections L/M/C plus amendments, page limits, submission method, evaluation factors and weights, past-performance references, win themes, known gaps or teaming needs.

## Workflow
1. **Extract requirements:** every shall/must/will in L, M, and C/PWS becomes a row: Req ID, source, text, type (mandatory/evaluated), volume/section, owner, status, evidence. Ambiguous items go to the Q&A list.
2. **Outline from Section M:** volumes and headers mirror the M hierarchy; pages allocated by weight; each section notes which Req IDs it covers and its proof points (or [VERIFY]).
3. **Win themes and discriminators:** each must appear in at least 2 volumes with proof, or it's decorative. VOSB/SDVOSB only if certified; AI or automation claims only if the SOW calls for them and proof exists.
4. **Q&A list:** 6-10 prioritized questions citing the section and the ambiguity. [DRAFT - USER SUBMITS].
5. **Red-team checklist:** compliance (traceability, page limits, format), responsiveness (all factors covered), quality (themes proven, no unsupported claims), consistency (labor categories, resumes, contracts), pricing (basis of estimate, rates [VERIFY with accountant]), registrations (SAM active, certs current), and open gaps.
6. **Submission checklist:** 24 hours before (volumes final, files named, portal tested), 4 hours before (upload, verify, submit, capture the confirmation), after (file confirmation, watch for amendments). [DRAFT - USER SUBMITS].

## Output
```
1 Compliance matrix: Req ID | Source | Text | Type | Vol/Sec | Owner | Status | Evidence
2 Annotated outline by volume, mapped to M factors and page limits
3 Q&A list | Red-team checklist | Submission checklist
```

## Guardrails
- Never submit, email, post, sign, or bind the company; the user executes submission.
- Mark unsupported claims [VERIFY]; never fabricate past performance.
- If a mandatory L requirement can't be met, flag it as a no-bid trigger.
- No credentials or proprietary pricing in outputs.

_Adapted from: alirezarezvani/claude-skills (rfp-responder, contract-and-proposal-writer), MIT._
