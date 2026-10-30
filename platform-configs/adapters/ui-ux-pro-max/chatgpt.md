---
name: ui-ux-pro-max
description: Apply UI UX Pro Max design guidance without assuming the local Python search engine exists.
---

# UI UX Pro Max — ChatGPT guidance

Instruction-only adaptation of UI UX Pro Max, MIT, revision `28b3b8dee8c976df4fa3e94aed4e092ad43fcb03`. The full package has a Python search engine and local catalogs. This ChatGPT adaptation does not install or run them; do not claim a catalog search occurred. Use supplied data and available approved source-reading tools only.

Establish product type, audience, device context, existing design system, stack and the actual task. Reuse approved components and brand tokens. Apply these priorities in order:

1. Accessibility: semantic controls, accessible names, keyboard behavior, visible focus, contrast and non-color cues.
2. Touch and interaction: comfortable targets, clear feedback and complete loading, disabled, empty and error states.
3. Performance and resilience: reserve image space, avoid layout jumps, limit expensive motion and accommodate slow/failed requests.
4. Visual direction: one coherent style suited to the product; consistent spacing, type hierarchy and restrained color roles.
5. Layout: responsive reflow, realistic long/short content, readable line lengths and clear information hierarchy.
6. Motion: meaningful feedback, interruptibility and reduced-motion behavior.
7. Navigation/forms: predictable paths, clear labels, appropriate validation, preserved input and recovery.
8. Data display: honest scales and totals, units, timestamps, source labels and useful empty/zero states.

For a targeted issue, give a concrete recommendation and rationale. For a design system, specify typography, color roles, spacing, component/state rules and responsive behavior, distinguishing supplied evidence from proposed choices. Never invent search results or insist that a catalog recommendation overrides the user's brand.

Optional reference reading: [quick reference](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/28b3b8dee8c976df4fa3e94aed4e092ad43fcb03/.claude/skills/ui-ux-pro-max/references/quick-reference.md), [app quality rules](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/28b3b8dee8c976df4fa3e94aed4e092ad43fcb03/.claude/skills/ui-ux-pro-max/references/pro-rules.md). If those sources cannot be opened, report the limit rather than implying they were consulted. Saving project design decisions is an optional user-directed action; no automatic persistence or runtime setup.
