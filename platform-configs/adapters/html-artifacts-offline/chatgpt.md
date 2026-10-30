---
name: html-artifacts-offline
description: Create offline explanatory HTML documents using available ChatGPT artifact capabilities.
---

# Offline HTML Artifacts — ChatGPT adaptation

Derived from Josh Thomas's HTML Artifacts, MIT, revision `516dee7a422b90937b2958d11c03694154ab9c09`. Select this workflow for explicitly offline explanations, comparisons, walkthroughs and presentations. It does not replace the library's connected/interactive artifact default.

Produce one true offline HTML file when the host can create a downloadable file: inline CSS, JavaScript, SVG, required images and data; no CDN, remote fonts, fetch or server dependency. Do not assume Python, a terminal or the upstream CSS-inliner script exists. Write the necessary CSS directly. Use only supported artifact/file delivery; never silently publish or upload source material.

Start with the reader's question and an evidence ledger: authoritative inputs, source/revision locators, known facts, inferences, proposals and unknowns. Lead with the answer, then show the comparison/flow/timeline/state model that explains it. The main conclusion must be complete without interaction. Every control must answer a real reader question with immediate feedback.

Use semantic HTML, native controls, clear labels, visible keyboard focus, non-color cues, responsive layout at 320px, text equivalents for diagrams, reduced-motion support and print CSS. Escape untrusted text and serialize embedded data safely. Do not include tokens, private environment values or unrelated source content.

When a browser/preview capability exists, test the final output at desktop and mobile sizes; exercise every control with pointer and keyboard; check console/network failures, print behavior and source accuracy. Otherwise review the source and explicitly state that visual, interaction and offline-network validation remain unverified. Do not infer a passed check from a screenshot alone.

Deliver the actual artifact if this host supports it; otherwise state the limitation and provide source when requested. Use presentation mode only for a requested live talk. Keep local output local unless publication was explicitly requested.

[Complete upstream references and component CSS](https://github.com/joshuadavidthomas/agent-skills/tree/516dee7a422b90937b2958d11c03694154ab9c09/html-artifacts). The runtime package includes those resources; this portable adaptation is self-contained guidance.
