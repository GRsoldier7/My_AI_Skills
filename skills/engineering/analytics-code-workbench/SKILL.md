---
name: analytics-code-workbench
description: Build, diagnose or review analytics code in Python, Azure SQL T-SQL and PowerShell. Use for a BI transform, reporting query, Windows automation or general code change when the user needs a small safe implementation and a fixture that demonstrates its result.
metadata:
  version: "1.0.0"
  domain-category: engineering
  last-reviewed: "2026-11-21"
  adjacent-skills: code-review, validate-data, power-bi
  review-trigger: "A failed work fixture, changed host permissions or changed upstream guidance."
---

# Analytics code workbench

Start with the observable contract. Identify the input schema, intended grain, runtime or dialect, transformation, expected result and allowed side effects. In an approved work chat, draft code and expected results using synthetic or explicitly approved inputs. Label checks that someone still needs to run.

| Deliverable | Read |
| --- | --- |
| A repeatable Python transform or reconciliation | [Python](references/python.md) |
| An Azure SQL report, total or query review | [T-SQL](references/tsql.md) |
| A Windows inventory or administrative change | [PowerShell](references/powershell.md) |
| A change in another language or a pull-request review | Apply the review steps below to the supplied diff and its public entry point. |

For general coding, reproduce the smallest failing case first. Trace the caller through the function being changed. Preserve other callers and existing data. Prefer the narrowest fix that maintains the contract. Look for wrong results, retry or failure effects, permissions and missing evidence. Group findings by user impact, show the affected input, and give a regression case. When code already works for the task, say so and show the confirming check.

For example, if the aggregate rate changes after a label table is joined, run the same tiny fixture before and after that join. Multiple matching labels per item can inflate the count. Verify both the result and the number of source entities represented.

Return the minimal patch or query, the fixture, expected versus observed results, and any deployment assumption. Flag a write or environment change separately. If you lack runtime access, give the owner an exact check to run in Dev or QA. Retain the prior implementation until the normal entry point passes.

For Google Cloud reporting or a BigQuery cost or access question, use the [Google Cloud analytics workflow](references/google-cloud.md).
