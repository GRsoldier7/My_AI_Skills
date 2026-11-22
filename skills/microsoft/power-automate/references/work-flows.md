# Cloud flow design and failure review

Use for a proposed Power Automate flow or a review of supplied, redacted run evidence. Return a design draft. Existing read-only Outlook, calendar and SharePoint access is never used to create, enable, run or repair flows. Do not create connections, post messages or change source items.

**Intake.** Record the business outcome, trigger, representative payload, volume/burst, expected latency, owner, intended connector actions, and effect of duplicate or missed events. A list view or scheduled human review may meet a low-volume need. Document any required environment, connector license, permissions and data policies as owner-verification items. Keep credentials, payload bodies and tenant identifiers out of samples.

| Stage | Design the owner can review |
|---|---|
| Trigger | Specify event, filter and stable business key. For an intake row use source-list identity + item ID + business transition/version. Exclude a flow's own bookkeeping updates if they can retrigger it. |
| Validate | Check required fields and compare the transition with stored state. Describe null/invalid input and quarantine behavior. Record correlation key and stage in diagnostics. |
| Perform once | Claim the operation using a durable unique key/conditional insert. A read-then-create check can race. Use the same idempotency key with the destination where supported. If the effect succeeds but recording it fails, reconcile by key before replay. If the destination cannot resolve ambiguous outcomes, stop for owner review. |
| Recover | Outline Try and Catch scopes with run-after on failure/timeout. Retry transient throttling and temporary failures with a bounded backoff that honors connector guidance. Stop on bad payloads or denied access. Preserve a failed outcome even if error handling completes. |
| Operate | Document connection references, environment-specific settings, expected pages and concurrency, run history field to inspect, owner and escalation. Mark a truncated retrieval incomplete. Name the last known-good version and how an owner would pause intake, reconcile in-flight effects and restore that version. |

**Synthetic dry run.** Event `ListA/42/submitted/v3` arrives twice concurrently. One claim succeeds and one is a duplicate. The destination acknowledges the first event, then the receipt write times out. Expect a lookup by the original key, one destination effect, and one reconciled receipt. With no reliable lookup, expect a pending investigation and zero automatic replays. A malformed event should produce a validation failure before any effect.

**Deliver.** Return trigger/conditions, action map, failure/retry decisions, owner and dependency list, and expected vs. observed test results. Use “design only” when working from a prompt or excerpt.

[Microsoft Learn: scopes, run-after and error handling](https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/error-handling) · [limits, concurrency, retry and pagination](https://learn.microsoft.com/en-us/power-automate/limits-and-config)
