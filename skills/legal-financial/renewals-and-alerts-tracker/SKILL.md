---
name: renewals-and-alerts-tracker
description: >-
  Use when tracking subscription, domain, SSL, license, or certification
  renewals (including SAM.gov), asking what's renewing soon, or triaging account
  alerts like security notices, failed payments, expiring cards, or login
  warnings.
metadata:
  version: "1.0.0"
  domain-category: grok-bot-team
  last-reviewed: "2026-11-11"
---
# Renewals & Alerts Tracker

## Renewals register
1. **Record each item:** name, owner, annual cost, renewal date, auto-renew (yes/no/unknown), cancel-by date, tier (1 business-stopping, 2 important, 3 nice-to-have), source link (account page or contract, never passwords or card numbers), notes. Dates and costs come from the vendor page or receipt; otherwise mark VERIFY.
2. **Reminder lead times:** standard subscriptions, domains, and SSL at 90/60/30/14/7 days; SAM.gov and government certifications at 120/60/30/14; insurance and licenses at 90/60/30/7. Prefer one combined check over many small reminders.
3. **Upcoming report:** due within 30 days (action), 31-60, 61-90, plus government certifications.
4. **Cancel/downgrade candidates:** unused tier-3 items, duplicates, free alternatives, orphans, each with cost, rationale, and USER APPROVAL REQUIRED.

## Alert triage
5. **Severity:** ACT NOW (breach, unknown login, failed payment, suspension, expired domain/cert); THIS WEEK (expiring card, cert/domain within 14-30 days, billing discrepancy, required MFA); FYI (known-device login, announcements).
6. **Phishing check:** never follow links in alert emails. Check the sender domain, urgency language, generic greetings, and credential requests; verify by going to the vendor site directly; cross-check the register. When in doubt, mark it suspicious and ask the user.
7. **Report:** ACT NOW / THIS WEEK / FYI / SUSPECTED PHISHING, with service, verification status, action, and owner.

## Output
```
Renewals - [date]
Action (30 days): name | tier | due | cancel-by | $ | auto-renew
Coming up (31-90) | Gov certs (120-day lead)
Cancel/downgrade candidates - USER APPROVAL REQUIRED
Alerts: ACT NOW | THIS WEEK | FYI | SUSPECTED PHISHING
```

## Guardrails
- Never cancel, downgrade, change auto-renew, or pay without explicit approval.
- Never store or show passwords, card numbers, keys, or SSNs.
- Never invent dates or costs; mark VERIFY.
- Ask the user to confirm unrecognized logins rather than assuming.

_Adapted from: alirezarezvani/claude-skills (vendor-management, decision-logger), MIT._
