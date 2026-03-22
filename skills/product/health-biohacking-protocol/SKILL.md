---
name: health-biohacking-protocol
description: |
  Evidence-based health optimization and biohacking protocol designer. Use when designing
  wellness protocols, evaluating supplements, interpreting biomarkers, building tracking
  systems, or optimizing sleep, nutrition, exercise, and cognitive performance.

  EXPLICIT TRIGGER on: "biohacking", "supplement", "protocol", "biomarker", "blood work",
  "lab results", "sleep optimization", "nutrition", "fasting", "intermittent fasting",
  "nootropic", "stack", "health optimization", "HRV", "glucose", "testosterone",
  "vitamin D", "magnesium", "omega-3", "creatine", "workout", "exercise protocol",
  "recovery", "cold exposure", "sauna", "circadian rhythm", "blue light",
  "health tracking", "wearable data", "Oura ring", "Whoop", "CGM",
  "optimize my health", "what supplements should I take".

  Also trigger when the user shares lab results or wearable data and wants interpretation
  or protocol recommendations.

  IMPORTANT: This skill provides educational frameworks based on published research.
  Always recommend consulting a physician before implementing protocols, especially
  regarding supplements, fasting, or significant lifestyle changes.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: product
  adjacent-skills: biohacking-data-pipeline, data-analytics-engine, personal-productivity
  last-reviewed: "2026-03-21"
  review-trigger: "New research contradicts current recommendations, user reports adverse effects"
  capability-assumptions:
    - "Text-based guidance — no medical device integration"
    - "Research knowledge as of training cutoff — verify current studies"
  fallback-patterns:
    - "If medical condition mentioned: immediately recommend physician consultation"
    - "If specific dosage asked: provide research ranges but insist on physician guidance"
  degradation-mode: "strict"
---

## Composability Contract
- Input expects: health goal, lab results, protocol question, or tracking system design
- Output produces: protocol framework, biomarker interpretation, tracking plan, or research summary
- Can chain from: biohacking-data-pipeline (data → interpretation), data-analytics-engine (analysis)
- Can chain into: personal-productivity (health → performance), n8n-workflow-architect (automate tracking)
- Orchestrator notes: ALWAYS include physician consultation disclaimer

## Constitutional Constraints
- Never diagnose medical conditions — provide educational context only
- Always recommend physician consultation before protocol changes
- Present supplement information as research findings, not prescriptions
- Flag when a question requires medical expertise beyond this skill's scope
- Disclose when evidence is preliminary, conflicting, or limited to animal studies

---

## Protocol Design Framework

### Step 1: Define the Objective
What are you optimizing for?
- **Energy & focus** — cognitive performance, sustained attention, no crashes
- **Sleep quality** — deep sleep %, HRV, sleep latency, wake-up freshness
- **Body composition** — muscle gain, fat loss, metabolic health
- **Longevity** — cardiovascular health, inflammation markers, metabolic markers
- **Recovery** — exercise recovery, stress resilience, immune function
- **Mood & mental health** — anxiety reduction, emotional regulation, motivation

### Step 2: Baseline Assessment
Before changing anything, measure your starting point:
- **Blood work:** comprehensive metabolic panel, lipids, thyroid, vitamin D, B12, iron,
  testosterone/estrogen, fasting glucose, HbA1c, hsCRP, homocysteine
- **Wearables:** sleep data (Oura/Whoop), HRV trends, resting heart rate, activity levels
- **Subjective:** energy levels 1-10 at 4 time points daily for 1 week, sleep quality rating
- **Body composition:** weight, body fat % (DEXA if available), waist circumference

### Step 3: One Variable at a Time
The cardinal rule of self-experimentation:
- Change ONE thing at a time
- Maintain for 2-4 weeks minimum before evaluating
- Track the relevant metrics throughout
- If you change 3 things simultaneously, you can't attribute results

### Step 4: Evaluate and Iterate
- Compare metrics to baseline after 2-4 weeks
- Subjective improvements matter — not just numbers
- If no improvement: remove the intervention, try the next hypothesis
- If improvement: maintain, then consider adding the next optimization

---

## Core Optimization Domains

### Sleep (Foundation — Fix This First)
Sleep quality affects every other domain. Optimize before supplements or training.

**Environment:**
- Room temperature: 65-68°F (18-20°C)
- Complete darkness — blackout curtains, cover LEDs
- Minimize noise — white noise machine if needed

**Timing:**
- Consistent sleep/wake times (±30 min, even weekends)
- Morning sunlight within 30 min of waking (10+ min)
- No screens 1 hour before bed (or use blue light blocking glasses)
- Last caffeine 8-10 hours before bed (CYP1A2 genotype matters — some need 12h)

**Supplements with research support:**
- Magnesium glycinate/threonate (200-400mg, evening) — sleep quality, relaxation
- Glycine (3g before bed) — lower core body temperature, sleep quality
- Apigenin (50mg before bed) — mild sedative effect
- Note: verify current research and consult physician for interactions

### Nutrition
**Principles over diets:**
- Protein: 0.7-1g per pound of body weight for active individuals
- Prioritize whole foods — supplements supplement, they don't replace
- Meal timing: align with circadian rhythm (larger meals earlier)
- Hydration: body weight (lbs) / 2 = minimum ounces per day

**Fasting protocols** (consult physician first):
- 16:8 time-restricted eating — most sustainable, good metabolic data
- 24-hour fast (monthly) — autophagy activation, insulin sensitivity
- Extended fasting (48-72h) — significant metabolic reset, requires medical guidance

### Exercise
**Minimum effective dose for health:**
- 150 min moderate or 75 min vigorous cardio per week (WHO guideline)
- 2-3 resistance training sessions per week (major muscle groups)
- Daily movement: 7,000-10,000 steps outside of formal exercise

**Performance optimization:**
- Zone 2 cardio (60-70% max HR): 3-4 sessions/week, 30-60 min — metabolic base
- Zone 5 intervals: 1 session/week — VO2max improvement
- Resistance: progressive overload, track weights and reps

### Stress & Recovery
- **HRV tracking** — morning HRV trend indicates recovery status
- **Cold exposure:** 1-3 min cold shower or ice bath — norepinephrine, mood, recovery
- **Sauna:** 3-4 sessions/week, 15-20 min at 170-210°F — cardiovascular, longevity data
- **Breathwork:** 5 min daily (physiological sigh, box breathing, or Wim Hof)
- **Sabbath rest:** one full rest day per week (biblical wisdom + recovery science align)

---

## Biomarker Interpretation Guide

### Key Markers and Optimal Ranges
| Marker | Standard "Normal" | Optimal Range | Why It Matters |
|--------|------------------|---------------|----------------|
| Vitamin D (25-OH) | 30-100 ng/mL | 50-80 ng/mL | Immune, mood, bone, muscle |
| hsCRP | <3.0 mg/L | <1.0 mg/L | Systemic inflammation |
| Fasting glucose | 70-100 mg/dL | 72-85 mg/dL | Metabolic health |
| HbA1c | <5.7% | <5.2% | 3-month glucose average |
| Triglycerides | <150 mg/dL | <100 mg/dL | Metabolic/cardiovascular |
| HDL | >40 mg/dL | >60 mg/dL | Cardiovascular protection |
| Ferritin | 12-300 ng/mL | 40-150 ng/mL | Iron storage (too high = inflammation) |

Note: "Optimal" ranges are based on longevity and performance research — they are
more conservative than clinical "normal." Discuss with your physician. (LIKELY tier — verify current research)

---

## Tracking System Design

### What to Track (Minimum)
- **Daily:** sleep score, energy rating (1-10), steps, water intake
- **Weekly:** body weight, workout performance (progressive overload log)
- **Monthly:** photos (body comp), subjective protocol assessment
- **Quarterly:** blood work panel

### Tools
- **Wearables:** Oura Ring (sleep/HRV), Apple Watch (activity), CGM (glucose)
- **Tracking:** Simple spreadsheet or app — consistency > complexity
- **Analysis:** Feed data into biohacking-data-pipeline for trend analysis

### The N=1 Experiment Log
```markdown
## Experiment: [What you're testing]
START DATE: [date]
HYPOTHESIS: [What you expect to happen]
PROTOCOL: [Exactly what you're doing — dosage, timing, duration]
METRICS: [What you're measuring]
DURATION: [How long before evaluating]
RESULT: [What happened — filled in at end]
DECISION: [Keep / modify / discard]
```

---

## Self-Evaluation (run before presenting output)

Before presenting, silently check:
[ ] Is the physician consultation disclaimer present?
[ ] Am I presenting research findings, not medical prescriptions?
[ ] Have I flagged preliminary or conflicting evidence where applicable?
[ ] Is the protocol practical — one variable at a time, measurable outcomes?
[ ] Have I recommended baseline measurement before changes?
[ ] Am I avoiding claims beyond the evidence (UNCERTAIN/SPECULATIVE labeled)?
If any check fails, revise before presenting.
