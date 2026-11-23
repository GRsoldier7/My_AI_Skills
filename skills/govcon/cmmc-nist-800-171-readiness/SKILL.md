---
name: cmmc-nist-800-171-readiness
description: >-
  Use when a solicitation or contract involves CUI, DFARS
  252.204-7012/7019/7020/7021, FAR 52.204-21, CMMC levels, SPRS scores, or when
  building an SSP or POA&M. Planning aid, not certification or legal advice.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# CMMC & NIST 800-171 Readiness

Produce a readiness gap analysis, SPRS-style score estimate, and remediation plan. Planning only.

## Inputs
Solicitation clauses and CMMC level; business profile (people, locations, IT, cloud); CUI types and where it flows; current controls (MFA, encryption, logging, patching, IR plan, physical); existing SSP/POA&M.

## Workflow
1. **Applicability:** FAR 52.204-21 only means basic safeguarding (15 requirements); DFARS 7012/7019 means NIST 800-171 (110 controls) plus SPRS; DFARS 7021 means CMMC Level 1/2/3. If no clause and no CUI, say compliance is likely not required and stop.
2. **Scope the CUI boundary:** systems, people, locations, and data flows (ingress, storage, transmission, destruction); list out-of-scope systems. Shrinking the boundary (e.g., an enclave) is usually the cheapest win.
3. **Cloud/ESP check:** every in-boundary provider needs FedRAMP Moderate-equivalent or better. Flag commercial tools (standard M365, Google Workspace, Dropbox) as BLOCKING for CUI.
4. **Gap assessment** across the 14 families: mark each control MET / PARTIAL / NOT MET / N/A with evidence and effort.
5. **SPRS-style estimate:** start at 110 and subtract per the DoD assessment methodology (5/3/1-point weights). Mark the score [VERIFY]; only the Affirming Official self-attests.
6. **SSP and POA&M skeletons:** POA&M items only for deferrable controls, with owner and a date within 180 days.
7. **Right-sized plan for a small firm:** enclave or GCC High, MFA everywhere, FIPS encryption, audit logging and review, a written IR plan with 72-hour DoD reporting, physical CUI storage, annual training.
8. **Rough cost and timeline,** all [VERIFY with vendors].

## Output
```
CMMC/800-171 Readiness - [org] - DRAFT, PLANNING ONLY
Clauses / level / CUI types | Boundary summary
Cloud check: [provider - status]
Gaps: MET # | PARTIAL # | NOT MET # ; BLOCKING: [list]
SPRS estimate: #/110 [VERIFY]
Roadmap: P1 blocking -> P2 -> P3 (owner, date) | Rough cost [VERIFY]
```

## Guardrails
- Mark every DFARS/NIST/SPRS citation, control count, and score [VERIFY] against the current official source.
- Read-only: never change systems, submit SPRS scores, or contact assessors without explicit approval.
- Never request or store credentials or real CUI; use placeholders.
- Not legal advice; recommend counsel or a registered practitioner for final decisions.

_Adapted from: alirezarezvani/claude-skills (cmmc-readiness), MIT._
