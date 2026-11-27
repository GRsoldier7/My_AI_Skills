---
name: claims-guardrail-check
description: >-
  Use when reviewing any health-adjacent or commercial draft (site copy, offer,
  lead magnet, email, testimonial, affiliate mention, subscription or billing
  copy) before it reaches Aaron. Returns a structured pass/fail checklist
  against verified FDA, FTC, and ROSCA sources. Not legal advice; flags items
  for counsel. Never sends or publishes.
metadata:
  version: "1.0.0"
  domain-category: growth
  last-reviewed: "2026-11-26"
  origin: custom
  origin-path: none
  origin-sha: none
  license: none
---

# Claims guardrail check

This is a checklist for counsel review, not legal advice, and not a substitute for counsel. It is a custom skill; no equivalent SKILL.md in coreyhaines31/marketingskills covers this checklist. Use only the sources listed in each section. Never invent a case name, CFR, Federal Register cite, or URL.

## Guardrails

- Drafts only. Never send, post, publish, email, purchase, change a live price, or start payment or ad spend.
- Never invent facts, prices, metrics, quotes, or citations. Mark unverified items `[VERIFY]`.
- No secrets, credentials, RFC1918 or tailnet IPs, lab hostnames, lab paths, connection IDs, surnames, or private client names. Refer to a pending prospect as "the named prospect in the bot's CONTEXT."
- Heavy analysis (for example, a substantiation pass over cited studies) goes through `/home/box/agent-os/scripts/llm.sh` (OpenRouter `:free` first, then Claude or OpenAI on their own keys, never through OpenRouter). Grok only routes and checks.

## Workflow

1. Take the draft text, a draft type (site copy, offer, lead magnet, email, testimonial, affiliate mention, subscription/billing, or other), and optional context notes.
2. For each checklist section below, scan the draft. Quote matching or problematic phrases verbatim. Record Pass, Fail, or N/A with that evidence.
3. Apply the verdict logic. Output the verdict, the table, quoted problem phrases, and rewrite guidance.
4. Do not present a BLOCK or REVISE draft as publishable copy. The failed checklist may still be shown to Aaron.

## Checklist

### 3.1 Disease / treat / cure / prevent language

- Rule: A dietary supplement (and, by the same FTC advertising principles, promotional copy about a supplement, peptide, or similar product) must not claim to diagnose, treat, cure, or prevent any disease. Structure/function claims may describe the role of a nutrient or dietary ingredient intended to affect normal structure or function (FDA example: "calcium builds strong bones") but, on supplement labeling, must carry the required disclaimer and must not imply disease treatment. Educational evidence reviews may describe published findings with sources and limits; they must not imply efficacy for a person or condition.
- Sources: FDA, "Structure/Function Claims," https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/structurefunction-claims ; 21 CFR 101.93, https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-101/subpart-F/section-101.93 (required disclaimer includes: "This product is not intended to diagnose, treat, cure, or prevent any disease."). Also FDA, "Dietary Supplement Labeling Guide: Chapter VI. Claims," https://www.fda.gov/food/dietary-supplements-guidance-documents-regulatory-information/dietary-supplement-labeling-guide-chapter-vi-claims
- Check: Scan for diagnose, treat, cure, prevent, and implied disease claims (for example, "for arthritis," "anti-cancer"). Word hits in a cited study description are not an automatic Fail if the draft clearly attributes the finding to a source, states its limits, and does not apply the result to a reader as a treatment. Fail if the draft implies the site, product, or compound will treat, cure, or prevent a disease or condition.

### 3.2 Extra caution: BPC-157 and TB-500

- Rule: Neither BPC-157 (free base or acetate) nor TB-500 (free base or acetate) is a component of an FDA-approved drug, and neither has a USP or NF monograph. FDA's July 2026 Pharmacy Compounding Advisory Committee briefing proposes that they NOT be included on the 503A Bulks List. An HHS notice at 91 FR 68526 (Oct 30, 2026) announces a draft enforcement-discretion policy for compounding certain peptides listed in that policy's Appendix A. The notice states that compounded drugs are not FDA-approved and that the policy "does not establish any rights for any person and is not binding on HHS or the public." Enforcement discretion is not FDA approval and does not authorize treat, cure, or prevent claims. Confirm Appendix A membership against the current HHS policy document before stating that a named peptide is or is not listed; the policy PDF was not independently retrieved in the 2026-11-26 source check (HTTP 403).
- Sources: FDA PCAC briefing, July 23-24, 2026, https://www.fda.gov/media/193773/download ; HHS, 91 FR 68526, https://www.federalregister.gov/documents/2026/10/30/2026-22192/enforcement-discretion-policy-regarding-503a-compounding-using-certain-peptide-bulk-drug-substances ; FDA, "Bulk Drug Substances Used in Compounding," https://www.fda.gov/drugs/human-drug-compounding/bulk-drug-substances-used-compounding
- Check: Fail if the draft implies FDA approval, safety, or therapeutic efficacy for BPC-157 or TB-500, or treats compounding as approval, or asserts Appendix A status without a live re-check note.

### 3.3 Extra caution: methylene blue

- Rule: PROVAYBLUE (methylene blue) injection is FDA-approved for the treatment of pediatric and adult patients with acquired methemoglobinemia. The label includes a boxed warning for serotonin syndrome with concomitant serotonergic drugs and opioids, and contraindications for severe hypersensitivity to methylene blue and for G6PD deficiency (hemolytic anemia risk). Wellness, cognitive, anti-aging, or other unapproved uses are not this indication. Copy must not imply that unapproved uses are approved, safe, or effective.
- Source: PROVAYBLUE (methylene blue) injection label, revised Feb 2024, NDA 204630, https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/204630Orig1s023correctedlbl.pdf
- Check: Fail if the draft presents wellness, cognitive, or anti-aging use as approved or effective, or omits that the approved indication is acquired methemoglobinemia when it discusses the drug's approved status.

### 3.4 Substantiation of health-benefit or safety claims

- Rule: Advertising must be truthful and not misleading, and advertisers must have adequate substantiation for all objective product claims before disseminating an ad. Health-benefit and safety claims generally require competent and reliable scientific evidence. In this guidance, "advertising" includes packaging, internet and digital content, social and influencer marketing, and press, not only traditional ads. The document is staff business guidance; it does not have the force of law and is not a safe harbor.
- Source: FTC, Health Products Compliance Guidance (Dec 2022), https://www.ftc.gov/system/files/ftc_gov/pdf/Health-Products-Compliance-Guidance.pdf (a direct GET of this PDF from the author's environment returned HTTP 403; the title, date, URL, and principles above were verified from the official FTC document text).
- Check: For each health-benefit or safety claim, require a specific citation. Fail "studies show" with no reference, or anecdotal support presented as sufficient substantiation.

### 3.5 Affiliate / material-connection disclosure

- Rule: A material connection (payment, free product, affiliate commission, or another connection consumers would not reasonably expect) must be disclosed clearly and conspicuously. The disclosure must be hard to miss and understandable; it does not require the complete details of the connection. Place it adjacent to the link or endorsement, not only in a footer.
- Source: 16 CFR 255.5, https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255/section-255.5
- Check: Scan for affiliate links, referral codes, and sponsored or commission arrangements. Fail a missing, vague, or footer-only disclosure.

### 3.6 Testimonials and endorsements

- Rule: Endorsements must reflect the honest opinions, findings, beliefs, or experience of the endorser, and may not convey a representation that would be deceptive if made by the advertiser. Consumer endorsements that convey product performance need substantiation (16 CFR 255.2). An endorser represented as a user must have been a bona fide user at the time of the endorsement.
- Source: 16 CFR Part 255, https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255
- Check: Fail fabricated, composite, or atypical results presented without the required disclosure; endorsements that imply use without a bona fide user; and testimonial performance claims without substantiation.

### 3.7 Negative-option / auto-renew billing

- Rule: For goods or services sold on the internet through a negative-option feature, ROSCA (15 U.S.C. 8403) makes it unlawful to charge or attempt to charge a consumer unless the seller (1) clearly and conspicuously discloses all material terms before obtaining billing information, (2) obtains express informed consent before charging, and (3) provides simple mechanisms for the consumer to stop recurring charges. ROSCA remains in force.
- The 2024 FTC amendments to the Negative Option Rule, often called "Click to Cancel," were vacated by the Eighth Circuit in Custom Commc'ns, Inc. v. FTC, 142 F.4th 1060 (8th Cir. 2025). The Commission restored the pre-2024 Negative Option Rule effective Feb 12, 2026 (91 FR 6507). Do not cite the vacated 2024 rule as current law. The restored 16 CFR Part 425 text is the older prenotification negative-option-plans rule (classic club-style plans). It is not the primary federal rule for a general internet subscription. ROSCA is.
- An advance notice of proposed rulemaking was published at 91 FR 12318 (Mar 13, 2026), with comments due Apr 13, 2026. That notice is not itself a new final rule. Re-check the Federal Register before relying on any later replacement rule.
- Sources: 15 U.S.C. 8403, https://www.govinfo.gov/content/pkg/USCODE-2023-title15/html/USCODE-2023-title15-chap110-sec8403.htm ; 91 FR 6507, https://www.federalregister.gov/documents/2026/02/12/2026-02866/revision-of-the-negative-option-rule-withdrawal-of-the-cars-rule-removal-of-the-non-compete-rule-to ; 91 FR 12318, https://www.federalregister.gov/documents/2026/03/13/2026-04952/rule-concerning-the-use-of-prenotification-negative-option-plans
- Check: For any auto-renew or negative-option offer, verify that material terms (price, frequency, what is being purchased, how to cancel) are disclosed before billing capture, that express consent is obtained before a charge, and that a simple cancellation mechanism is described. ROSCA requires a "simple mechanism" but does not, in the statute, define that as one-click or same-method cancellation; those specifics were in the vacated 2024 amendments and are not current binding federal law. Still flag hard-to-cancel designs (phone-only paths, retention mazes) for counsel, because ROSCA's "simple mechanisms" duty remains. Fail any citation of the vacated 2024 rule as if it were in force.

### 3.8 No dosing, protocol, or outcome promises; no medical advice

- Rule: This is a team contract rule (growth-architect boundary), not a standalone statute: drafts must not specify dosages, treatment protocols, or promised outcomes for a person, and must not give medical advice. Educational descriptions of what a cited study dosed are allowed only when clearly attributed to that study and not turned into a reader instruction.
- Sources: growth-architect contract; apply sections 3.1 and 3.4 if the same language is also a disease claim or an unsubstantiated health-benefit claim.
- Check: Fail "take 500 mg daily," "follow this 8-week cycle," or "you will recover in 4 weeks" as reader instructions. Fail language that reads as medical advice.

## Verdict logic

- BLOCK: any Fail in 3.1, 3.2, 3.3, 3.7, or 3.8. The draft must not go to Aaron as publishable copy until revised. The failed checklist may still be shown.
- REVISE: any Fail in 3.4, 3.5, or 3.6, and no BLOCK trigger.
- PASS-WITH-COUNSEL-FLAG: every section is Pass or N/A, and health-adjacent or commercial billing content is present. Add: "Not legal advice. Forward to qualified counsel before anything goes live."

## Output format

```
VERDICT: BLOCK | REVISE | PASS-WITH-COUNSEL-FLAG

CHECKLIST:
| Section | Rule summary | Source | Result | Evidence quote from draft |
|---|---|---|---|---|
| 3.1 | Disease / treat / cure / prevent | FDA Structure/Function; 21 CFR 101.93 | Pass/Fail/N/A | "quote" or "None found" |
| 3.2 | BPC-157 / TB-500 extra caution | FDA PCAC Jul 2026; HHS 91 FR 68526 | Pass/Fail/N/A | |
| 3.3 | Methylene blue extra caution | PROVAYBLUE label, NDA 204630 | Pass/Fail/N/A | |
| 3.4 | Substantiation | FTC Health Products Guidance, Dec 2022 | Pass/Fail/N/A | |
| 3.5 | Affiliate / material connection | 16 CFR 255.5 | Pass/Fail/N/A | |
| 3.6 | Testimonials / endorsements | 16 CFR Part 255 | Pass/Fail/N/A | |
| 3.7 | Negative-option / auto-renew | ROSCA 15 U.S.C. 8403; 91 FR 6507; 91 FR 12318 | Pass/Fail/N/A | |
| 3.8 | No dosing / protocol / outcome promises | Team contract; see 3.1 and 3.4 | Pass/Fail/N/A | |

QUOTED PROBLEM PHRASES:
- <section>: "<verbatim phrase>"

REQUIRED REWRITE GUIDANCE:
- <section>: <specific fix, citing the rule>

COUNSEL NOTE: Not legal advice. Forward health-adjacent or commercial copy to qualified counsel before anything goes live.
```

## Credit

Custom skill drafted for Aaron's Grok Bot team. No upstream SKILL.md in https://github.com/coreyhaines31/marketingskills (commit `2bf95edb4ebd37198ab7fd18b99ba95c2145ec64`, MIT) is a health-claims, FTC, FDA, or ROSCA checklist. Affiliate and testimonial themes appear in that repo's referrals materials; legal rules in this skill come only from the sources listed above. Provided "AS IS", without warranty of any kind.
