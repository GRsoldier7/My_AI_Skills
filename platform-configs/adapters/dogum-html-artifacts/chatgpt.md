---
name: dogum-html-artifacts
description: Build interactive HTML reports and tools using only the receiving host’s supported capabilities.
---

# Dogum HTML Artifacts — ChatGPT adaptation

Derived from Dogum HTML Artifacts 2.0.0, Apache-2.0, revision `d54982f5da13392481f122b533b4ab9a8b2dc3d9`. Use this as the library's default for interactive reports, comparisons, charts, diagrams and one-off editors when HTML materially helps. Honor requests for prose, Markdown or another format. Do not manufacture an HTML deliverable for a short answer.

1. Identify the reader's task and authoritative evidence. Pick a meaningful layout: comparison columns, a timeline, a labeled diagram, an honest chart or controls that change a visible answer.
2. Produce one self-contained HTML artifact when the host supports it, with inline styles/scripts and local data. A clear title and framing sentence precede the substantive content. Reuse the user's visual system; otherwise use restrained typography and meaningful color.
3. Support phone widths and light/dark themes; semantic controls, labels, keyboard access, visible focus, non-color cues and useful print behavior are baseline requirements.
4. Editors must export changed state as usable Markdown, JSON or text. Include reset, empty, invalid-input and export-failure behavior. Do not silently store private data in browser persistence.
5. Connected data is allowed only through explicitly approved authenticated services. Preserve identity and row-level controls; use a secure backend where secrets are required. Never embed credentials or client secrets in HTML, use public publishing for private reports, or imply a data connection was verified without testing it.
6. Use this host's documented artifact/CDN/storage rules. Claude-specific artifact capabilities do not transfer to ChatGPT. If a capability is missing, use a supported fallback and state the limitation.
7. If rendering/browser tools are available, check the actual final artifact at desktop/mobile widths, console/network errors, keyboard/pointer controls and export behavior. Otherwise perform source review and explicitly label runtime/visual verification unverified.

Deliver the generated artifact/file through the available host tool, or source when requested. Publishing and account connections are separate actions. For an explicitly offline explanatory document, choose `html-artifacts-offline` instead.

[Complete pinned source and category references](https://github.com/dogum/html-artifacts/tree/d54982f5da13392481f122b533b4ab9a8b2dc3d9/skills/html-artifacts).
