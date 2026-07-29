#!/usr/bin/env python3
"""Regression tests for lint_phantom_refs precision AND recall.

Run: python3 scripts/test-phantom-refs.py   (exit 0 = pass)

Why this exists: the phantom-ref rule is pure heuristic, and heuristics fail in
BOTH directions. Two adversarial review rounds found five separate defects — a
whole-line invocation test that counted a "Supply Chain" table row as a skill
reference, and a whole-line example-marker test that silently swallowed a real
dangling reference because an unrelated "(e.g. ...)" appeared later in the same
sentence. A rule that under-reports is worse than one that is noisy, because it
reads as a clean pass. Every case below is a real shape, not a hypothetical.
"""
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("lint_skills", REPO / "scripts" / "lint-skills.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["lint_skills"] = mod  # @dataclass resolves the owning module by name
spec.loader.exec_module(mod)

KNOWN = {"todo-create", "ce-pr-description", "safe-auto", "optional-helper"}

# Real reference shapes. Each MUST report `missing-skill` as a phantom ref.
MUST_FLAG = [
    "Use `missing-skill` for normal commits.",
    "See `missing-skill` before editing.",
    "Route to `missing-skill` for PDF-heavy inputs.",
    "Delegate to `missing-skill` for browser checks.",
    "Hand off to `missing-skill` after extraction.",
    "Compose with `missing-skill` and more.",
    "Required skill: `missing-skill`.",
    "Adjacent skills: `missing-skill`, `other-thing`.",
    "| skill | `missing-skill` |",
    "The `missing-skill` skill handles extraction.",
    "load the `missing-skill` skill with a target description",
    # A guard covering a DIFFERENT token must not excuse this one.
    "If the `optional-helper` skill is available, invoke `missing-skill`.",
    # An unrelated conditional or "optional" elsewhere on the line must not excuse it.
    "Invoke `missing-skill`; if the issue has no labels, stop.",
    "Call `missing-skill`; optional output files may be attached.",
    # An example marker that introduces something else must not excuse it.
    "When files such as package.json change, invoke `missing-skill`.",
    # Bare availability wording is a statement, not a guard.
    "Invoke `missing-skill` available during setup.",
    "Use `missing-skill` skill is available.",
    # Verb-object-preposition: the verb is not adjacent to the token.
    "Route image tasks to `missing-skill`.",
    "Delegate PDF work to `missing-skill`.",
    "Hand off the failing cases to `missing-skill`.",
    "Dispatch the request to `missing-skill`.",
    # Second-model review round: ordinary English verbs the first pass omitted.
    "Apply the `missing-skill` for validation.",
    "Execute the `missing-skill` on each file.",
    "Trigger the `missing-skill` after the build.",
    "Launch the `missing-skill` in a worktree.",
]

# Non-references. Each MUST report nothing. The first four are verbatim shapes
# from this repo that the old whole-line heuristic wrongly failed.
MUST_SKIP = [
    "findings whose final owner is `review-fixer`. Load the `todo-create` skill for it",
    "| T7 | **Supply Chain** | `source-repo` pointing to unverified forks, pinning removed |",
    "- **verdict**: `fixed`, `fixed-differently`, `replied`, or `needs-human`",
    "**Naming rationale:** `ce-pr-description`, not `git-pr-description`. Stacking is a GitHub feature.",
    "1. **Optional:** If the `ralph-loop` skill is available, run the loop.",
    "Pass a token, e.g. `some-example`, to the helper.",
    # Prose ABOUT skills is not an invocation.
    "`missing-skill` skills are useful for triage.",
    "`missing-skill` skill names should be lowercase.",
    # A genuine guard is a documented contract, not a defect.
    "Invoke `maybe-helper` if available.",
    "Route to `maybe-helper` only when enabled.",
    "Use `maybe-helper` where available.",
    "Use `maybe-helper` if the skill is available.",
    # More prose ABOUT skills.
    "`missing-skill` skill description should be under 1024 chars.",
    "`missing-skill` skill instructions live in the body.",
    # A noun after the token names what it IS, and none of these are skills. The
    # first line is real: broadening invocation detection made it a false positive.
    "Pass the resulting path list to the `project-standards` persona inside a block.",
    "Route the findings to the `review-fixer` owner for triage.",
    "Delegate the check to the `standards-check` sub-agent.",
]


def refs(line: str) -> set[str]:
    found = mod.lint_phantom_refs(Path("x/SKILL.md"), [line], KNOWN)
    return {f.rule.split(":", 1)[1] for f in found}


def main() -> int:
    failures = []
    for line in MUST_FLAG:
        hits = refs(line)
        if "missing-skill" not in hits:
            failures.append(f"MISSED (should flag): {line!r} -> {sorted(hits)}")
    for line in MUST_SKIP:
        hits = refs(line)
        if hits:
            failures.append(f"FALSE POSITIVE: {line!r} -> {sorted(hits)}")

    print(f"MUST_FLAG={len(MUST_FLAG)}  MUST_SKIP={len(MUST_SKIP)}  failures={len(failures)}")
    for f in failures:
        print("  " + f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
