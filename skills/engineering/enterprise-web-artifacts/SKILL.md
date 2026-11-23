---
name: enterprise-web-artifacts
description: Create or improve an accessible HTML report, interactive operations brief or SharePoint web artifact for an internal business audience. Choose a portable snapshot, permissioned Power BI report, SharePoint Framework web part or Power Apps component based on the required interaction and hosting.
metadata:
  version: "1.0.0"
  domain-category: engineering
  last-reviewed: "2026-11-21"
  adjacent-skills: sharepoint, power-bi, power-apps
  review-trigger: "A failed work fixture, changed host permissions or changed upstream guidance."
---

# Enterprise web artifacts

Start with the decision the reader has to make, the approved fields, the data-as-of time and the allowed interaction. Choose a delivery mode before choosing a framework. For a self-contained brief, keep the data and assets local and supply a useful static table. For authenticated, multiuser work, make ownership and write permissions explicit.

1. [Choose the host](references/delivery.md) using audience, persistence, permissions and update frequency.
2. [Design and verify the result](references/artifact-quality.md) using a synthetic fixture and a representative reader task. The upstream visual-design reference is available for a deeper critique.
3. Deliver an HTML file or reviewed component draft, the input contract, and a short acceptance record. Mark unexecuted host, accessibility or permission checks explicitly.

The included standalone operations brief has one filter, a weighted total, an accessible data table and a zero-eligibility state. Open `assets/operations-brief.html` in a browser. Its data is synthetic. Use the file as a working starting point for a report with the same interaction model.
