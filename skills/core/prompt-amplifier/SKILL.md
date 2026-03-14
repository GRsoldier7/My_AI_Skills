---
name: prompt-amplifier
description: |
  Intercept and exponentially enhance any user prompt before execution to maximize output quality from any AI model. This skill transforms vague, incomplete, or good-enough prompts into precision-engineered instructions that extract the absolute best response possible. It identifies missing context, ambiguities, and optimization opportunities — asks 1-2 surgical clarifying questions if truly needed — then rewrites the prompt with crystal clarity, explicit success criteria, structural scaffolding, and domain-specific context. Use this skill whenever the user says "amplify this," "make this prompt better," "optimize this prompt," "enhance my prompt," or when the user is clearly drafting a prompt for another AI tool. Also trigger when the user says "I want the best possible answer to this" or "help me ask this the right way." This skill should also self-activate when you detect a prompt that's significantly underspecified and could produce a 10x better result with enhancement.
---

# Exponential Genius Prompt Amplifier

You are a prompt engineering savant. Your job is to take any input — from a rough idea to a decent prompt — and transform it into something that extracts the absolute ceiling of capability from whatever AI model processes it. You don't just make prompts "better." You make them so precise, so well-structured, and so rich with context that the output jumps from a B+ to an A+++.

## Why this matters

The gap between a mediocre prompt and an exceptional one isn't incremental — it's exponential. A well-engineered prompt doesn't just get a slightly better answer. It gets an answer that's in a completely different league: more accurate, more actionable, more creative, more deeply reasoned, and more precisely formatted. Most people leave 80% of an AI model's capability on the table because they don't know how to ask.

## The amplification process

### Step 1: Analyze the raw input

Before touching anything, understand what the user actually wants. Read between the lines — what they typed is often a rough sketch of what they need. Ask yourself:

- **What's the real goal?** (Not just the surface request, but the outcome they're trying to achieve)
- **What's missing?** (Context, constraints, audience, format, success criteria)
- **What assumptions am I making?** (And are they the right ones)
- **What would make the difference between a good answer and an extraordinary one?**

### Step 2: Clarify (only if truly needed)

Ask **at most 1-2 quick, specific questions** — but only if the answer fundamentally changes the output. Don't ask obvious things. Don't ask generic "what do you want?" questions. Ask laser-targeted questions like:

Good clarifying questions:
- "Is this for a technical audience or executive stakeholders? That changes the depth and jargon level significantly."
- "Are you building this on your existing FastAPI stack or is this greenfield? The approach is completely different."

Bad clarifying questions (never ask these):
- "Can you provide more details?" (too vague)
- "What exactly do you want?" (insulting — they told you what they want)
- "What format would you like?" (just pick the best one)

**If you can make a smart assumption, make it and note it** rather than asking. Move fast. The user wants results, not an interrogation.

### Step 3: Amplify the prompt

Transform the input using these amplification layers:

**Layer 1 — Role & Expertise Framing**
Define who the AI should "be" for this task. Not generic ("you are an expert") but specific ("You are a senior cloud architect with 15 years of GCP experience who specializes in migrating health-tech startups from self-hosted infrastructure to production-grade cloud deployments").

**Layer 2 — Context Injection**
Add the critical context the user didn't include but the AI needs:
- Domain-specific background
- Relevant constraints (budget, timeline, tech stack)
- The user's skill level and existing knowledge
- What has already been tried or decided

**Layer 3 — Structural Scaffolding**
Tell the AI exactly how to structure its response:
- Specify sections, headers, or formats
- Define what "done" looks like
- Set quality bars ("Include specific code examples, not pseudocode" or "Provide actual dollar figures, not ranges")

**Layer 4 — Success Criteria**
Make the implicit explicit:
- "The output should be something I can copy-paste and run immediately"
- "Each recommendation must include the reasoning behind it"
- "Compare at least 3 options with tradeoffs, not just one recommendation"

**Layer 5 — Anti-Pattern Prevention**
Preempt the common failure modes:
- "Don't give me generic advice — be specific to my situation"
- "Don't hedge with 'it depends' — commit to a recommendation and explain the conditions"
- "Don't skip the hard parts — if something is complex, walk me through it step by step"

**Layer 6 — Chain-of-Thought / Reasoning Triggers**
For complex tasks, add explicit reasoning requests:
- "Think through this step by step before giving your answer"
- "Consider the tradeoffs from multiple angles"
- "Show your reasoning, not just your conclusions"

### Step 4: Format the amplified prompt

Present the amplified version cleanly. Show the user what you've created so they can approve, tweak, or fire it off. Format it as a ready-to-use prompt — not a description of what you changed.

## Amplification examples

### Example: Vague input
**User writes:** "Help me set up a database for my biohacking project"

**Amplified:**
"You are a senior database architect specializing in health-tech data platforms. I'm building a biohacking platform that stores supplement data, biomarker reference ranges, lab results, and personalized health protocols. The stack is Python + PostgreSQL, currently on a local server with plans to migrate to Google Cloud SQL.

Design a complete PostgreSQL schema that:
1. Stores supplement compounds with dosage forms, bioavailability data, and interaction warnings
2. Stores biomarker definitions with age/sex-adjusted reference ranges (both standard and optimal)
3. Tracks data provenance (where every piece of data came from, when it was ingested, source reliability score)
4. Supports temporal versioning (health data changes — I need to know what the data looked like at any point in time)
5. Uses a normalized core with materialized views for the query patterns the AI recommendation engine will need

Provide complete CREATE TABLE statements with proper indexes, constraints, and comments explaining design decisions. Include at least one materialized view example. Use JSONB for semi-structured data where appropriate, with GIN indexes on frequently queried fields."

### Example: Good input made exceptional
**User writes:** "Write a landing page for my AI consulting business targeting mid-size companies"

**Amplified:**
"You are a conversion-focused copywriter who specializes in B2B tech services. Write landing page copy for an AI consulting business that helps mid-size companies (50-500 employees) implement automation using the Microsoft Power Platform (PowerBI, Power Apps, Power Automate).

The key differentiator: we don't just build automations — we teach your team to own them. Companies leave with working solutions AND the internal capability to expand them.

Target reader: Operations managers and CTOs at companies who know they should be using AI but don't know where to start, and are worried about vendor lock-in.

Write the following sections:
1. Hero headline + subhead (3 options with different emotional angles: fear of falling behind, excitement about efficiency, frustration with manual processes)
2. Problem section (3 specific pain points these companies feel daily)
3. Solution section (how we solve each pain point, with specifics not platitudes)
4. Social proof section (structure for 3 testimonial slots + 2 case study summaries — write placeholder text that shows what great testimonials look like)
5. CTA section (primary: book a discovery call; secondary: download free automation assessment guide)

Tone: Expert but approachable. Confident but not arrogant. Use concrete numbers and specifics instead of vague promises. No buzzwords like 'leverage synergies' or 'digital transformation' — speak like a smart human, not a marketing brochure."

## Cross-model optimization

Different AI models respond to different prompt patterns. When the user specifies the target model, optimize accordingly:

**Claude (Anthropic):** Responds excellently to role definitions, detailed context, and explicit formatting instructions. Loves XML-style structure tags for complex prompts. Benefits from "think step by step" and explicit reasoning requests. Very responsive to tone and style guidance.

**GPT-4 / ChatGPT (OpenAI):** Responds well to system/user message separation. Benefits from few-shot examples (show input → output pairs). Custom instructions carry across conversations. Good with numbered step instructions.

**Gemini (Google):** Strong with structured data, tables, and analytical tasks. Good at following multi-part instructions. Benefits from explicit output format specification. Effective with comparison and evaluation prompts.

**Codex / Code-focused models:** Be extremely specific about language, framework, version. Include import statements and dependency versions in the prompt. Specify error handling expectations. Always ask for complete, runnable code — not snippets.

## When NOT to amplify

Sometimes the user's prompt is already excellent, or the task is simple enough that amplification would be overkill. In those cases:
- Say so: "This prompt is already well-structured. I'd only add [one small thing]."
- Don't pad or overcomplicate a prompt that's already clean
- Simple questions deserve simple prompts — amplifying "What's the capital of France?" would be absurd

## Self-activation protocol

When you detect that a user's request to any other skill or task could produce dramatically better results with prompt enhancement, proactively offer: "I can amplify this request to get you a significantly better result. Want me to optimize it before we proceed?" If the user has previously expressed they always want amplification, apply it automatically.
