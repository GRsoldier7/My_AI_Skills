---
name: portable-ai-instructions
description: |
  Generate project instruction files (CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules, copilot-instructions.md) tailored to any AI coding tool. This meta-skill understands the conventions, capabilities, and quirks of each tool and produces optimized instruction files that maximize the AI's effectiveness on your projects. Use this skill whenever the user mentions creating project instructions, setting up AI tool configs, writing CLAUDE.md, AGENTS.md, GEMINI.md, .cursorrules, copilot instructions, or wants to "set up a new project" for AI-assisted development. Also trigger when the user asks about making AI tools work better on their codebase, porting instructions between tools, or wants a consistent AI experience across multiple tools.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: core
  adjacent-skills: prompt-amplifier, polychronos-team, skill-builder
  last-reviewed: "2026-03-15"
  review-trigger: "New AI tool releases, Claude Code instruction format changes, AGENTS.md spec updates"
  capability-assumptions:
    - "No external tools required beyond standard Claude Code tools"
  fallback-patterns:
    - "If tools unavailable: provide text-based guidance"
  degradation-mode: "graceful"
---

# Portable AI Instructions Generator

You are helping create project instruction files that make AI coding tools maximally effective. Different tools use different file formats, but the underlying content is largely the same: project context, coding conventions, architecture decisions, and workflow preferences. This skill helps you write once and deploy everywhere.

## Why this matters

An AI coding tool with good project context produces dramatically better output than one without. The difference between "generic code that technically works" and "code that fits perfectly into your existing architecture, follows your naming conventions, uses your preferred libraries, and handles errors the way you like" is almost entirely about the context you provide.

## File format reference

### CLAUDE.md (Claude Code / Cowork)

**Location:** Project root, or `~/.claude/CLAUDE.md` for global preferences
**Loaded:** Automatically when Claude Code starts in the directory
**Capabilities:** Can reference skills (modular instruction bundles), supports MCP server configuration, layered (global + project-level)

**Unique strengths:**
- Skill system allows complex, multi-step workflows as separate loadable modules
- MCP integrations bring in external services (Slack, Calendar, GitHub, etc.)
- Memory system persists learnings across sessions

**Best practices:**
- Keep the main CLAUDE.md focused on project context and conventions
- Put complex workflows into separate skills rather than cramming everything into one file
- Use the memory system for things that evolve (learnings, preferences discovered over time)

### AGENTS.md (OpenAI Codex CLI)

**Location:** Project root (also checks parent directories)
**Loaded:** Automatically when Codex starts
**Capabilities:** Flat markdown file, no modular system, supports sandboxed execution

**Unique strengths:**
- Codex runs in a sandboxed environment with full autonomy
- Good at long-running autonomous tasks (it runs, you review)
- Can install dependencies and run tests within its sandbox

**Best practices:**
- Be explicit about the test commands and how to verify work
- Include clear boundaries about what files/directories are off-limits
- Specify the exact commands for building, testing, and linting
- Since there's no skill system, put everything in one well-organized file

### GEMINI.md (Gemini CLI)

**Location:** Project root
**Loaded:** Automatically when Gemini CLI starts
**Capabilities:** Markdown file with project instructions, supports tool configuration

**Unique strengths:**
- Deep integration with Google ecosystem (GCP, Firebase, etc.)
- Good context window for large files
- Strong at understanding complex codebases

**Best practices:**
- If using GCP, include specific project IDs, regions, and service account details
- Be explicit about Google-specific tooling preferences (gcloud CLI patterns, etc.)
- Include clear architecture diagrams in text format

### .cursorrules (Cursor)

**Location:** Project root
**Loaded:** Automatically when Cursor opens the project
**Capabilities:** Focused on coding style and conventions, short-form instructions

**Unique strengths:**
- Tightly integrated into the IDE experience
- Applies to both inline completions and chat
- Very fast context loading

**Best practices:**
- Keep it concise — Cursor works best with focused, specific rules
- Prioritize coding style (naming, patterns, error handling) over workflow instructions
- Include preferred import styles, file organization patterns, and testing conventions
- Think of it as "coding standards" rather than "project documentation"

### .github/copilot-instructions.md (GitHub Copilot)

**Location:** `.github/copilot-instructions.md`
**Loaded:** When Copilot is active in the repo
**Capabilities:** Basic project context for completions and chat

**Unique strengths:**
- Works directly in VS Code, JetBrains, etc. (wherever Copilot is installed)
- Applies to inline code completions (not just chat)
- Native GitHub integration

**Best practices:**
- Focus on coding patterns and naming conventions
- Keep instructions action-oriented and specific
- Less effective for complex workflow orchestration — keep it to code style

## Generation process

When the user asks you to generate project instruction files:

### Step 1: Gather project context

Understand the project by asking about (or inferring from the codebase):

- **Tech stack:** Languages, frameworks, key libraries, database, infrastructure
- **Architecture:** Monolith vs. microservices, directory structure, key design patterns
- **Conventions:** Naming (camelCase vs. snake_case), file organization, import style, error handling patterns
- **Testing:** Test framework, test location conventions, coverage expectations
- **Build/Deploy:** Build commands, CI/CD, deployment targets
- **Code quality:** Linting, formatting (Prettier, Black, etc.), pre-commit hooks
- **Key decisions:** "We use X instead of Y because..." — the decisions that an AI tool might get wrong without context

### Step 2: Generate tool-specific files

For each requested tool, adapt the content to match the tool's conventions and capabilities:

**Shared content** (goes in all files):
- Project description and purpose
- Tech stack summary
- Directory structure overview
- Coding conventions (naming, style, patterns)
- Build and test commands
- Key architectural decisions

**Tool-specific additions:**

| Content | CLAUDE.md | AGENTS.md | GEMINI.md | .cursorrules | copilot-instructions |
|---------|-----------|-----------|-----------|--------------|---------------------|
| Skill references | Yes | No | No | No | No |
| MCP configuration | Yes | No | No | No | No |
| Sandbox commands | Brief | Detailed | Brief | No | No |
| GCP specifics | Yes | Yes | Emphasized | No | Brief |
| Coding patterns | Moderate | Moderate | Moderate | Primary focus | Primary focus |
| Workflow orchestration | Via skills | Inline | Inline | No | No |
| Architecture depth | Deep | Deep | Deep | Brief | Brief |

### Step 3: Write the files

**Structure for longer files (CLAUDE.md, AGENTS.md, GEMINI.md):**

```markdown
# Project: [Name]

## Overview
[2-3 sentences: what this project does and why]

## Tech Stack
[Bulleted list of key technologies]

## Architecture
[Directory structure, key patterns, data flow]

## Conventions
[Naming, style, import patterns, error handling]

## Commands
[Build, test, lint, deploy commands]

## Key Decisions
[The "why" behind architectural choices — this prevents the AI from "improving" things that are intentional]

## Common Patterns
[Code examples of patterns to follow in this project]

## What NOT to do
[Anti-patterns, deprecated approaches, things the AI might suggest that you don't want]
```

**Structure for shorter files (.cursorrules, copilot-instructions):**

```markdown
# [Project Name] Coding Standards

## Style
- [naming convention]
- [import style]
- [file organization]

## Patterns
- [preferred patterns with brief examples]

## Avoid
- [anti-patterns]

## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`
```

### Step 4: Cross-tool consistency check

After generating all requested files, verify:
- The same conventions are specified consistently across all files
- Tool-specific features are leveraged where available
- No contradictions between files
- Each file is appropriately sized for its tool (concise for Cursor/Copilot, detailed for Claude/Codex/Gemini)

## Template: Aaron's project defaults

Based on the user's profile, pre-populate these defaults when generating new project files:

```yaml
owner: Aaron DeYoung
stack_preferences:
  language: Python 3.12+
  database: PostgreSQL (Cloud SQL on GCP)
  cloud: Google Cloud Platform
  orm: SQLAlchemy or raw psycopg2 (depending on complexity)
  api_framework: FastAPI
  testing: pytest
  linting: ruff
  formatting: black
  type_checking: pyright
  containerization: Docker
  orchestration: Cloud Run / Cloud Run Jobs
  iac: Terraform
  ci_cd: GitHub Actions

coding_conventions:
  naming: snake_case for Python, lowercase-with-hyphens for files/directories
  docstrings: Google style
  error_handling: Explicit exception types, never bare except
  logging: structlog or standard logging with structured output
  config: Environment variables via pydantic-settings
  secrets: Never in code, always Secret Manager or .env (local only)

project_types:
  data_pipeline: biohacking data ingestion and processing
  api: FastAPI serving health protocols
  web: Next.js + Tailwind for marketing/product site
  consulting: Power Platform, PowerBI, Power Automate, Power Apps
```

When generating files for a new project, start from these defaults and adjust based on the specific project's needs.

## Output

Always generate complete, ready-to-use files — not templates or fragments. The user should be able to copy each file directly into their project root. If generating multiple files, clearly label which file goes where:

```
📄 CLAUDE.md → project root
📄 AGENTS.md → project root
📄 GEMINI.md → project root
📄 .cursorrules → project root
📄 .github/copilot-instructions.md → .github/ directory
```

---

## Anti-Patterns

**Anti-Pattern 1: Copy-Paste Across All Files**
Generating CLAUDE.md, AGENTS.md, GEMINI.md, and .cursorrules with identical content because "they
all need the same conventions." Each tool has distinct strengths and optimal file structures.
Fix: Use the tool-specific additions table. CLAUDE.md gets skill references and MCP config.
.cursorrules stays concise and coding-pattern-focused. AGENTS.md gets detailed sandbox commands.

**Anti-Pattern 2: One-Time Generation, Never Updated**
Creating project instruction files once at project start and never updating them as the project
evolves. Instruction files that don't reflect current reality confuse AI tools and produce worse output.
Fix: Treat instruction files as living documents. Update CLAUDE.md in the same session as any
significant architectural decision, convention change, or new tech stack addition.

**Anti-Pattern 3: Overcrowding CLAUDE.md With Workflow**
Cramming complex multi-step workflows, full agent rosters, and domain-specific protocols directly
into CLAUDE.md instead of using the skill system. Results in a bloated file that loads 5,000 tokens
of context on every session, most of it irrelevant to the current task.
Fix: CLAUDE.md should reference skills, not contain their content. Keep CLAUDE.md focused on project
context and conventions. Complex workflows belong in SKILL.md files.

---

## Quality Gates

- [ ] Each generated file is complete and ready-to-use (no placeholders requiring manual fill-in)
- [ ] CLAUDE.md references skills instead of inlining their full content
- [ ] .cursorrules and copilot-instructions are concise (≤100 lines) and coding-pattern-focused
- [ ] All files share consistent conventions with no contradictions between them
- [ ] Tool-specific features are leveraged (MCP config in CLAUDE.md, sandbox commands in AGENTS.md)
- [ ] Cross-tool consistency check is completed before delivering files

---

## Failure Modes and Fallbacks

**Failure: Generated instructions contradict each other across tools**
Detection: CLAUDE.md says use `black` for formatting, .cursorrules says use `ruff`.
Fallback: Run the cross-tool consistency check (Step 4) explicitly. Pick the authoritative source
(usually CLAUDE.md for Python projects) and propagate to all other files. Flag any deliberate
differences with comments explaining the tool-specific rationale.

**Failure: Instruction file is too long and loads irrelevant context**
Detection: CLAUDE.md exceeds 500 lines, or the user reports that every Claude session starts with
heavy context that slows responses.
Fallback: Apply the DRY principle. Move reusable domain knowledge to SKILL.md files. Move
project-specific history to memory files. CLAUDE.md should only contain what needs to be present
in every session for this project.

---

## Composability

**Hands off to:**
- `polychronos-team` — once instruction files are generated, the Polychronos team operates within
  the context those files establish
- `skill-builder` — when reviewing CLAUDE.md reveals gaps in the skill library that should be filled

**Receives from:**
- `prompt-amplifier` — when the user's request to generate instruction files needs more specificity
  before generation can begin
- `polychronos-team` — when the PM identifies that a new project needs instruction files set up
