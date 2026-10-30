---
name: web-artifacts-builder
description: Create and refine web artifacts with the capabilities available in ChatGPT.
---

# Web artifacts in ChatGPT

Use available artifact/file tools to produce the requested HTML interface. Clarify
only choices that change the output; infer ordinary defaults from the request.
Plan content hierarchy, typography, color, spacing, accessible controls and mobile
behavior before implementation. Match complexity to the deliverable: a standalone
HTML file with embedded CSS/JavaScript for a portable report; a framework project
only when the receiving environment supports its build workflow.

Use original or authorized assets. Include useful empty, loading and error states.
Use semantic HTML, keyboard-operable controls, visible focus, readable contrast
and reduced-motion behavior. Review at a narrow mobile width and a desktop width
when browser access exists. Check every visible control and inspect console errors.
If no browser is available, report static review and unverified behavior separately.

Do not run upstream shell initializers, install Node packages or claim local CLI
access in this instruction-only delivery. Produce the files supported by the host,
and describe any additional build step that remains for an approved environment.
Connected private data needs an approved authentication/API or Power BI embedding
arrangement; never put secrets or direct database credentials into delivered HTML.
Use a synthetic snapshot when a live connection has not been authorized and tested.

Source: https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder
License: Apache-2.0; the canonical package's license accompanies this adaptation.
