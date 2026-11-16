---
name: evidence-before-claims
description: Use when about to claim anything is done, fixed, passing, live, sent, or verified; before sending a report, proposal, audit, or handoff; before quoting a file or web source; or before stating another bot's state or that a routine ran.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-16"
---

# Evidence Before Claims

No claim without evidence gathered in this run. A fact you cite must trace to a source you opened in this run.

## The gate

Run before every completion claim, report, proposal, audit, handoff, or quote:

1. IDENTIFY the command or source that proves the claim.
2. RUN or OPEN it now, in full. A prior run does not count.
3. READ the whole output: exit code, failure counts, the actual text.
4. COMPARE: does it confirm the claim exactly?
5. YES: state the claim with the evidence. NO: state the real status with the evidence.
6. Only then write "done", "fixed", "passing", "live", "sent", or "verified".

## Claim-to-evidence table

| Claim | Counts as evidence | Does not count |
|---|---|---|
| Tests pass | This run's test output with 0 failures and exit 0 | Earlier run, "should pass", linter result |
| Deploy live | Fetch of the live URL or status check this run showing the new state | Deploy command exited 0, a log line |
| File changed | `git diff` or a re-read of the file after the edit | Edit tool said success |
| Routine ran | A runs/<slug>/history.jsonl record for that run, read this run | Schedule exists, "it usually runs" |
| Quote | Exact text found in the opened source, cited with path:line or URL | Memory, a model's paraphrase |
| Statistic, price | Exact figure quoted from the source page, with access date | Search snippet, blog roundup |
| Regulation | Primary text (eCFR, FAR, Google Search Central, vendor docs), exact quote of the rule | Blog or summary of the rule |
| Another bot's state | Its run record read this run, or Aaron's confirmation | Inference, older handoff note, its own chat claim |

## Fresh vs reused

Label every checked fact in the output:
- `fresh (this run)`: you ran or opened it this run.
- `reused (YYYY-MM-DD)`: carried from earlier work; give the original date and do not call it verified.

Model output, yours or another model's, is never evidence of a fact. Route heavy model work through scripts/llm.sh, then confirm every fact it returns against a source before using it.

## Citation format

- File quote: `` `path:line`: "exact text" `` . Copy the text, never retype from memory.
- Web fact: `[title](url) (accessed YYYY-MM-DD)`. Any number, price, date, or rule gets an exact quote beside the link.
- Prefer primary sources (eCFR, FAR, Google Search Central, vendor docs) over blogs. If only a secondary source exists, say so and mark [VERIFY].
- Cite the deepest page or anchor, not a homepage.

## Quote check

Before sending any file that contains file quotes, run:

```
python3 scripts/quote_check.py FILE... [--root DIR]
```

Exit 1 means a NOT_FOUND or MISSING_FILE. Fix each one (correct the quote or drop it), then rerun until exit 0. LINE_DRIFT is acceptable only after you update the line number to the reported one. Include the summary line in your Verified field.

## Red-flag words: stop and verify

"should work", "probably", "seems", "I believe", "I think", "looks right", "likely", and "done!", "all set", or "great!" written before the check ran. Replace each with the check and its result, or with `[VERIFY]` and what remains unchecked.

## Close-out

End with `Shipped: ... · Verified: ... · Effect: ...`. In Verified, name each command or source opened this run and mark reused items with their date. If a claim failed its gate, report the real status in Shipped.

## Guardrails

- Drafts only; never send, post, publish, deploy, purchase, or delete without Aaron's explicit per-action approval.
- Never invent facts, quotes, URLs, or run records. Mark unverified items [VERIFY].
- Never state another bot's live state without a run record or Aaron's confirmation.
- No credentials in outputs or citations.
- Output longer than ~25 lines goes to a file; reply with the path and a short summary.

_Adapted from: obra/superpowers (verification-before-completion), MIT; addyosmani/agent-skills (source-driven-development), MIT; claim table, quote_check.py, and house rules are original to this team._
