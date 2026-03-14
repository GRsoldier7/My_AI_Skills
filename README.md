# Aaron's AI Skill Library

A library of 17 AI specialist skills and cross-platform configuration files for AI-assisted development. Each skill is a deep-domain expert that activates on demand, designed to work across Claude Code, Google Antigravity (Gemini CLI), OpenAI Codex, and Cursor.

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/GRsoldier7/My_AI_Slills.git
cd My_AI_Slills

# 2. Register all skills as Claude Code slash commands
./scripts/register-commands.sh

# 3. Verify
./scripts/register-commands.sh --list
```

After registration, use any skill in Claude Code with its slash command (e.g., `/polychronos-team`, `/power-bi`).

## Skill Catalog

### Core Orchestration (`skills/core/`) -- 3 skills

| Skill | Description |
|-------|-------------|
| `polychronos-team` | Multi-agent orchestration with B.L.A.S.T. protocol deploying 13 specialist roles |
| `prompt-amplifier` | Transforms prompts into precision-engineered instructions for maximum AI output |
| `portable-ai-instructions` | Generates project instruction files (CLAUDE.md, AGENTS.md, GEMINI.md, etc.) |

### AI & Strategy (`skills/strategy/`) -- 3 skills

| Skill | Description |
|-------|-------------|
| `ai-agentic-specialist` | Bleeding-edge AI/LLM landscape intelligence, tool evaluation, and agentic team design |
| `business-genius` | Entrepreneurial strategy, niche identification, and AI-amplified moat building |
| `market-intelligence` | Market research with TAM/SAM/SOM analysis, competitive landscaping, opportunity scoring |

### Product & Infrastructure (`skills/product/`) -- 3 skills

| Skill | Description |
|-------|-------------|
| `biohacking-data-pipeline` | Data pipeline architecture for health/supplement/biomarker data with provenance tracking |
| `brand-website-strategy` | Brand positioning, visual identity, website architecture, SEO, conversion optimization |
| `cloud-migration-playbook` | Proxmox homelab to GCP migration: Docker, Cloud Run, Cloud SQL, Terraform, security |

### Microsoft Power Platform (`skills/microsoft/`) -- 8 skills

| Skill | Description |
|-------|-------------|
| `power-bi` | Data modeling, DAX mastery, Power Query, star schema, RLS, deployment |
| `power-apps` | Canvas/Model-driven apps, Power Fx, delegation, components, ALM |
| `power-automate` | Cloud flows, desktop RPA, expressions, error handling, approvals |
| `sharepoint` | Site architecture, lists, PnP PowerShell, search, permissions, migration |
| `copilot-studio` | Bot design, topics, generative AI, plugin actions, adaptive cards |
| `power-platform-admin` | Environments, DLP, CoE Starter Kit, governance, licensing |
| `microsoft-dataverse` | Table design, security model, Web API, FetchXML, plugins |
| `m365-integration` | Microsoft Graph API, Teams dev, MSAL auth, webhooks |

## Repository Structure

```
aaron-skill-library/
|-- CLAUDE.md                      # Master project instructions
|-- README.md                      # This file
|-- .gitignore
|
|-- skills/                        # All 17 skills, organized by category
|   |-- core/                      # Orchestration & meta-skills
|   |-- strategy/                  # Business & market advisory
|   |-- product/                   # Product-specific domain skills
|   |-- microsoft/                 # MS Power Platform (8 skills)
|
|-- platform-configs/              # Per-tool instruction file templates
|   |-- shared/                    # Shared content fragments (DRY source)
|   |-- claude/                    # Claude Code templates
|   |-- codex/                     # Codex CLI templates
|   |-- gemini/                    # Antigravity/Gemini CLI templates
|   |-- cursor/                    # Cursor IDE templates
|   |-- chatgpt/                   # ChatGPT custom instructions & GPTs
|
|-- scripts/                       # Tooling
|   |-- register-commands.sh       # Register skills as Claude Code commands
|   |-- deploy.sh                  # Deploy configs & skills to projects
|
|-- evals/                         # Skill evaluation test cases
|-- .claude/commands/              # Project-level slash commands
```

## Platform Support

| Platform | Instruction File | Skill System | Template Location |
|----------|-----------------|--------------|-------------------|
| Claude Code | `CLAUDE.md` at project root | Slash commands via `~/.claude/commands/` | `platform-configs/claude/` |
| Antigravity (Gemini CLI) | `GEMINI.md` at project root | N/A (inline in GEMINI.md) | `platform-configs/gemini/` |
| Codex | `AGENTS.md` at project root | N/A (inline in AGENTS.md) | `platform-configs/codex/` |
| Cursor | `.cursorrules` at project root | N/A | `platform-configs/cursor/` |
| ChatGPT | Custom Instructions in settings | Custom GPTs | `platform-configs/chatgpt/` |

## Deploying to Projects

### Deploy platform config files to a new project

```bash
# Deploy all platform configs at once
./scripts/deploy.sh --target /path/to/project --platforms claude,codex,gemini,cursor

# Deploy just Claude Code config
./scripts/deploy.sh --target /path/to/project --platforms claude
```

### Register skills as project-level commands

```bash
# Register specific skills
./scripts/deploy.sh --target /path/to/project --skills polychronos-team,biohacking-data-pipeline

# Register all Microsoft skills for a consulting project
./scripts/deploy.sh --target /path/to/project --category microsoft
```

### Register skills globally for Claude Code

```bash
# All skills
./scripts/register-commands.sh

# Only one category
./scripts/register-commands.sh --category core

# List registered commands
./scripts/register-commands.sh --list

# Remove all registered commands
./scripts/register-commands.sh --clean
```

## How Skills Work

Each skill is a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: skill-name
description: |
  What the skill does and when to activate it.
---

# Skill Content
Deep domain expertise, frameworks, and instructions...
```

Skills are activated as Claude Code slash commands. When registered, typing `/skill-name` in any Claude Code conversation loads the skill's full content as context.

## Adding New Skills

1. Create a directory under the appropriate category:
   ```bash
   mkdir -p skills/strategy/new-skill-name
   ```

2. Create `SKILL.md` with YAML frontmatter (`name` and `description` fields)

3. Optionally add a `references/` subdirectory for supporting materials

4. Re-run registration:
   ```bash
   ./scripts/register-commands.sh
   ```

## Cross-Conversation Usage

- **This repo is the single source of truth.** Edit skills here, not in project repos.
- **Claude Code commands are symlinked.** Changes in this repo are immediately available everywhere.
- **Gemini/Codex configs are copied.** Re-run `deploy.sh` after changes to update project copies.

## Shared Content Fragments

The `platform-configs/shared/` directory contains the DRY source of truth for content that repeats across platforms:

| Fragment | Content |
|----------|---------|
| `identity.md` | Who Aaron is, current projects |
| `tech-stack.md` | Python/FastAPI/PostgreSQL/GCP stack details |
| `conventions.md` | Coding conventions, operating principles, constraints |
| `blast-protocol.md` | B.L.A.S.T. workflow and task tier classification |

Edit these fragments to update content across all platform templates.
