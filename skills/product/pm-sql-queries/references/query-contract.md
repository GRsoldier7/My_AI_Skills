# Local SQL validation contract

This repository's deliberate adaptation strengthens the upstream generator.

Before writing SQL, state dialect/version, source schema assumptions, metric
definition, result grain, business timezone, coverage, parameter types and
permitted action. Keep unanswered semantics explicit.

Check join fanout, denominator population, null/duplicate keys, missing periods
and filter/security effects. Supply validation queries with expected values for
normal and edge cases, then report what actually ran. A generated test is not
an executed test. Use synthetic inputs where source access is absent.

Return candidate SQL, assumptions, expected-result tests, observed evidence and
next check. Do not call a candidate production-ready without reconciliation.
For BigQuery, verify cost/pruning with approved evidence and explicit limits.
For SQL Server, plan/index advice requires actual workload and plan evidence.
Keep actual project definitions and outputs in their approved context.
