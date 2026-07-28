# Skill Recommendations by Project Type

Use this during Step 8 of organize-project to select and document the right skill stack.

---

## Universal (all project types)

| Skill | When to invoke |
|-------|----------------|
| `/superpowers:writing-plans` | Before starting any non-trivial task |
| `/superpowers:brainstorming` | Exploring options or architecture decisions |
| `/learn` | Session start — recall prior learnings |
| `/wrapup` | Session end — summarize what was done + what's next |
| `/checkpoint` | Before risky operations — save working state |

---

## Network / Infrastructure / Automation

| Skill | When to invoke |
|-------|----------------|
| `/investigate` | Diagnosing intermittent issues, root cause analysis |
| `/superpowers:systematic-debugging` | Deep structured debugging with hypothesis tracking |
| `/cso` | Security posture review — network configs, credentials |
| `/knowledge-management` | Organizing runbooks, research notes, references |
| `/careful` | Before any config change that could break connectivity |
| `/guard` | Full safety mode for destructive network operations |

---

## Python Package / Library

| Skill | When to invoke |
|-------|----------------|
| `/superpowers:test-driven-development` | All feature development — write tests first |
| `/health` | Before every commit — linter, type checker, tests |
| `/review` or `/my-code-review` | Before merging a PR |
| `/testing-strategy` | Designing a test plan for a new component |
| `/benchmark` | Before/after performance-sensitive changes |
| `/document-release` | After shipping a release |

---

## Python Scripts / Automation

| Skill | When to invoke |
|-------|----------------|
| `/investigate` | When a script behaves unexpectedly |
| `/health` | Periodically — lint and check script quality |
| `/knowledge-management` | Maintaining runbooks and reference docs |
| `/careful` | Before running destructive or irreversible scripts |

---

## Node / TypeScript Web App

| Skill | When to invoke |
|-------|----------------|
| `/superpowers:test-driven-development` | All feature development |
| `/health` | Type check + lint + test runner |
| `/qa` or `/qa-only` | Browser-based QA testing of the UI |
| `/design-review` | Visual QA — does the UI match the design? |
| `/review` | Pre-PR code review |
| `/app-security-architect` | Auth, data handling, API exposure review |
| `/canary` | Post-deploy monitoring |

---

## API / Backend Service

| Skill | When to invoke |
|-------|----------------|
| `/superpowers:test-driven-development` | All feature development |
| `/database-design` | Schema design and migration planning |
| `/app-security-architect` | Auth, authorization, input validation, secrets |
| `/health` | Run all checks |
| `/review` | Pre-PR code review |

---

## Data / ML Project

| Skill | When to invoke |
|-------|----------------|
| `/superpowers:writing-plans` | Experiment planning and hypothesis design |
| `/health` | Code quality checks on pipeline code |
| `/knowledge-management` | Organizing experiment notes and findings |
| `/review` | Reviewing pipeline and model code |

---

## Documentation / Knowledge Base

| Skill | When to invoke |
|-------|----------------|
| `/knowledge-management` | Designing and maintaining information architecture |
| `/document-release` | Post-ship documentation updates |
| `/learn` | Reviewing and pruning accumulated project learnings |

---

## Quick Cheat Sheet

| Situation | Skill |
|-----------|-------|
| Plan something complex | `/superpowers:writing-plans` |
| Bug I can't track down | `/investigate` or `/superpowers:systematic-debugging` |
| Code quality check | `/health` |
| About to do something risky | `/careful` or `/guard` |
| Pre-merge review | `/review` or `/my-code-review` |
| Organize information | `/knowledge-management` |
| What did we learn before? | `/learn` |
| Done for the day | `/wrapup` |
| Think through options | `/superpowers:brainstorming` |
| Test the UI in a browser | `/qa` |
| Security check | `/app-security-architect` or `/cso` |
