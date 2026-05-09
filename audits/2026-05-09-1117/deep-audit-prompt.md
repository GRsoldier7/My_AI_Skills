# Deep Skills Audit — Parallel Agent Prompt Template

The lint pass catches mechanical regressions. This deeper pass requires Claude
Code reasoning to catch routing collisions, scope overlaps, content currency,
and subjective quality issues. Run it with parallel agents — one per category.

## How to run

In a Claude Code session, dispatch 5 parallel Task() calls (one per group):

| Group | Categories | Skill count |
|---|---|---|
| 1 | core | 11 |
| 2 | engineering | 8 |
| 3 | growth + product | 15 |
| 4 | strategy + faith | 12 |
| 5 | microsoft + legal-financial + homelab-organizer | 11 |

## Per-agent prompt (template)

```
You are auditing the My_AI_Skills sub-library at /root/My_AI_Skills/skills/<CATEGORY>/.

For EACH SKILL.md in that category, evaluate against these axes:

1. ROUTING COLLISIONS — does this skill auto-trigger on requests that another
   skill in the library also auto-triggers on, with no precedence rule?
2. SCOPE OVERLAP — does this skill cover ground already covered by a native
   plugin skill (e.g. context7, supabase, cloudflare)? If so, does the SKILL.md
   explicitly say when to prefer this one vs the plugin?
3. CONTENT CURRENCY — are claims, model names, IPs, URLs, and version numbers
   current as of $(date +%Y-%m-%d)? Flag any "(coming soon)" or stale dates.
4. INTENT CLARITY — does the description tell the model precisely WHEN to fire
   AND when NOT to fire? Faith skills are the gold standard ("Do NOT use for X").
5. PHANTOM REFERENCES — does this skill reference skills that don't exist?
   (Lint catches the obvious ones; you catch the cross-skill mismatches.)
6. COMPOSABILITY — does the skill have a Composability Contract (input,
   output, hands-off-to)?

Output: per-skill JSON entry to a file at
  /tmp/aiskills_audit/<group>.json
with shape:
  { "skill": "name", "tier": "CRITICAL|HIGH|MEDIUM|LOW",
    "axes": ["routing","scope",...], "finding": "...", "fix": "..." }

End with a 1-paragraph executive summary listing only CRITICAL + HIGH.
```

## After the parallel pass

Aggregate the 5 per-group files into AUDIT.md following the structure used
on 2026-05-09 at /tmp/aiskills_audit/AUDIT.md.

## Tier definitions
- CRITICAL — wrong info, broken paths, will misroute users
- HIGH     — routing collisions, scope overlaps, stale claims with evidence
- MEDIUM   — quality improvements, missing gold-standard patterns
- LOW      — polish, minor inconsistencies
