# Copilot product selection and agent design

Use when “Copilot” could refer to coding help, a licensed productivity feature or a proposed custom agent. The work pack runs as instructions in ChatGPT Enterprise or GitHub Copilot. The product under discussion may differ from the host. Product documentation and a design brief confer no tenant permissions.

| User's objective | Product and boundary | Useful output here |
|---|---|---|
| Review code, a query or an automation definition in an approved repository | GitHub Copilot assists with code in the supplied repository/editor context. A coding subscription does not establish work mailbox or tenant access. | Proposed diff or annotated snippet, assumptions, synthetic fixtures, expected behavior and tests. |
| Understand a licensed productivity experience grounded in organizational data | Microsoft 365 Copilot capabilities depend on the particular license, tenant policy, user access and app. Confirm the capability for this user before proposing it. | Explain options or draft a prompt. For a real brief here, use only the existing approved read-only readers or supplied excerpts. |
| Design a repeatable domain agent with defined knowledge and topics | Copilot Studio is the maker product for custom agents. Licenses, capacity, environment, configured authentication, data policies and publication approval require owner verification. | Design-only topic map, scoped knowledge, fallback, tests, operating owner and release/rollback criteria. |

**Draft an agent.** Start with one job, such as answering questions about an approved intake checklist. Specify trigger examples, one nearby out-of-scope intent, the exact authoritative content and version, read access boundary, output format and stale/conflicting-document behavior. If a procedure requires deterministic branching, define topic conditions explicitly. Keep any proposed action separate with inputs, permissions, effect, duplicate behavior and human authorization. Use an escalation route the owner has supplied and label missing contacts as unknown.

| Synthetic test | Expected behavior |
|---|---|
| “Which fields are required?” with approved v2 section 3 visible | Answer from that section, cite it and say which version supplied the answer. |
| Same question with a newer conflicting draft or inaccessible section | Identify the discrepancy or evidence gap. Avoid presenting the draft as authoritative. |
| “File the request now” addressed to a knowledge-only agent | Return instructions or a draft for the user. No action or claim of completion. |
| “How soon?” after a different topic or a reset conversation | Ask which deadline the user means. Avoid carrying assumptions across sessions. |

Return results as expected, observed and untested. A human maker with a separate test environment can inspect topic selection and outputs in the test pane with synthetic identities and data. Before release, validate least-privilege knowledge retrieval and the fallback using an intended reader role. Keep publication and connection changes outside the pack.

[GitHub Docs: GitHub Copilot](https://docs.github.com/en/copilot/get-started/about-github-copilot) · [Microsoft Learn: productivity Copilot requirements](https://learn.microsoft.com/en-us/microsoft-365/copilot/microsoft-copilot-requirements) · [Copilot Studio overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio) · [testing an agent](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-test-bot)
