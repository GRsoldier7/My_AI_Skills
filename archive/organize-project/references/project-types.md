# Project Type Best-Practice Structures

## Python Package / Library
```
project/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── pyproject.toml          # or setup.cfg / setup.py
├── requirements.txt
├── requirements-dev.txt
├── src/
│   └── package_name/
│       ├── __init__.py
│       └── ...
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── docs/
├── scripts/                # one-off utility scripts
└── .github/workflows/
```
**Key skills:** `superpowers:test-driven-development`, `health`, `review`, `testing-strategy`

---

## Python Scripts / Automation
```
project/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── scripts/                # main scripts organized by function
│   ├── setup/
│   ├── maintenance/
│   └── analysis/
├── lib/                    # shared utility modules
├── config/                 # config files, templates
├── runbooks/               # step-by-step procedures for recurring tasks
├── reports/                # generated output and analysis
├── references/             # external docs, research notes
└── archive/                # old/superseded scripts
```
**Key skills:** `investigate`, `health`, `learn`, `knowledge-management`

---

## Node / TypeScript Web App
```
project/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── package.json
├── tsconfig.json
├── .env.example
├── src/
│   ├── components/
│   ├── pages/             # or app/ for Next.js App Router
│   ├── hooks/
│   ├── utils/
│   ├── types/
│   └── styles/
├── public/
├── tests/
│   ├── unit/
│   └── e2e/
├── scripts/               # build/deploy scripts
└── docs/
```
**Key skills:** `superpowers:test-driven-development`, `health`, `review`, `qa`, `design-review`

---

## API / Backend Service
```
project/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── src/
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   ├── models/
│   ├── middleware/
│   └── utils/
├── tests/
├── migrations/
├── config/
├── scripts/
└── docs/
    ├── api/               # OpenAPI spec, endpoint docs
    └── architecture/
```
**Key skills:** `superpowers:test-driven-development`, `database-design`, `app-security-architect`, `health`, `review`

---

## Network / Infrastructure / Automation
```
project/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── diagnostics/           # runnable diagnostic tools
│   ├── powershell/
│   ├── python/
│   └── bash/
├── runbooks/              # step-by-step operational procedures
├── scripts/               # automation scripts
├── config/                # configuration templates and examples
├── monitoring/            # dashboards, alert configs
├── reports/               # RCA documents, health reports
├── references/            # research notes, vendor docs, specs
├── skills/                # custom Claude skills for this domain
└── archive/               # superseded procedures and old reports
```
**Key skills:** `investigate`, `superpowers:systematic-debugging`, `learn`, `cso`, `knowledge-management`

---

## Data / ML Project
```
project/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── data/
│   ├── raw/               # never modified, source of truth
│   ├── processed/
│   └── outputs/
├── notebooks/             # exploration; don't put production logic here
├── src/
│   └── package_name/      # production pipeline code
├── models/                # saved model artifacts
├── configs/               # experiment configs (YAML/JSON)
├── tests/
├── scripts/               # training, evaluation, deployment scripts
└── reports/               # figures, analysis, paper drafts
```
**Key skills:** `health`, `superpowers:writing-plans`, `review`, `knowledge-management`

---

## Documentation / Knowledge Base
```
project/
├── CLAUDE.md
├── README.md
├── CHANGELOG.md
├── docs/
│   ├── guides/
│   ├── reference/
│   ├── tutorials/
│   └── architecture/
├── runbooks/
├── decisions/             # architecture decision records (ADRs)
├── research/              # notes, investigations, raw findings
└── archive/
```
**Key skills:** `knowledge-management`, `document-release`, `learn`

---

## Multi-type / Monorepo
Identify the primary type and secondary type, then apply a hybrid:
- Use the primary type's structure at root
- Add sub-directories for each secondary concern
- CLAUDE.md should explicitly name the multi-type nature and map each area
**Key skills:** Combine recommendations from each type. Start with `superpowers:writing-plans` to establish clear boundaries.
