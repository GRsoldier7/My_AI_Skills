---
name: app-security-architect
description: |
  Bleeding-edge application and web security expert. Use whenever building, reviewing, or
  auditing apps, APIs, websites, or cloud infrastructure for security. Applies OWASP,
  zero-trust, defense-in-depth, and AI/LLM-specific threat models.

  AUTO-TRIGGER on: any new API endpoint, auth flow, database schema, file upload, user input
  handling, third-party integration, secrets/credentials question, or deployment to production.

  EXPLICIT TRIGGER on: "secure this", "security review", "is this safe", "auth/authz",
  "protect against", "OWASP", "penetration test", "threat model", "security audit",
  "encrypt", "JWT", "API keys", "CORS", "CSP headers", "SQL injection", "XSS", "CSRF",
  "secrets management", "zero trust", "vulnerability", "CVE", "rate limiting",
  "input validation", "LLM security", "prompt injection", "AI security", "Power Platform
  security", "GCP security", "Docker security", "Cloud Run security", "FastAPI security".

  Also trigger proactively when writing code that handles: user authentication, file uploads,
  external API calls, database queries, environment variables, or any data from untrusted sources.

  Covers: OWASP Top 10 (2021+), LLM security (OWASP LLM Top 10), cloud-native security,
  secrets management, secure SDLC, threat modeling, and emerging AI agent security threats.
metadata:
  author: aaron-deyoung
  version: "1.0"
  domain-category: engineering
  adjacent-skills: code-review, database-design, cloud-migration-playbook, testing-strategy
  last-reviewed: "2026-03-21"
  review-trigger: "New OWASP Top 10 release, major CVE affecting stack, new Claude/AI security research"
  stack-context: "Python/FastAPI, Next.js/React, PostgreSQL, GCP (Cloud Run/Cloud SQL), Docker, Microsoft Power Platform"
  capability-assumptions:
    - "No external tools required — all guidance is text-based"
    - "Code examples target Python 3.12+, FastAPI 0.100+, SQLAlchemy 2.0+"
    - "GCP patterns assume Cloud Run + Cloud SQL + Secret Manager setup"
  fallback-patterns:
    - "If stack differs from defaults: ask user to confirm their stack before generating code"
    - "If no GCP: substitute equivalent patterns for AWS (Secrets Manager) or Azure (Key Vault)"
  degradation-mode: "graceful"
---

## Composability Contract
- Input expects: code, architecture description, feature request, or security question
- Output produces: threat model, secure code, hardened config, remediation list, or security checklist
- Can chain from: code-review (security layer on top of general review)
- Can chain into: testing-strategy (security tests), cloud-migration-playbook (hardening)
- Orchestrator notes: always flag Critical and High severity findings before Medium/Low

## Security Posture
Operate from these principles in all security guidance:
1. **Defense in depth** — multiple independent controls, not one strong wall
2. **Zero trust** — never trust, always verify. No implicit trust based on network location
3. **Least privilege** — minimum permissions needed, at every layer
4. **Secure by default** — the default configuration must be the secure one
5. **Fail securely** — errors and failures must not expose data or grant access
6. **Attack surface minimization** — fewer exposed surfaces = fewer vulnerabilities

---

## OWASP Top 10 (2021) — Applied to Your Stack

### A01 — Broken Access Control (Most Critical)
**Your stack risks:** FastAPI route protection, PostgreSQL RLS, GCP IAM, Power Platform sharing

**Patterns to enforce:**
```python
# FastAPI — always use dependency injection for auth, never manual header checks
from fastapi import Depends, HTTPException, status
from app.auth import get_current_user, require_role

@router.get("/patients/{patient_id}/data")
async def get_patient_data(
    patient_id: int,
    current_user: User = Depends(get_current_user)
):
    # Verify ownership — don't trust the path param alone
    if not await user_can_access_patient(current_user.id, patient_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
```

**PostgreSQL Row-Level Security:**
```sql
-- Enable RLS on every table with user-owned data
ALTER TABLE health_data ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_isolation ON health_data
    USING (user_id = current_setting('app.current_user_id')::int);
```

**GCP IAM rules:**
- Cloud Run service account: only the permissions it needs, nothing else
- Cloud SQL: use IAM database authentication, not password auth
- Secret Manager: one service account per service, scoped to exactly its secrets

### A02 — Cryptographic Failures
**Your stack risks:** Health/biometric data (PII+PHI), API keys, tokens, PostgreSQL at rest

**Mandatory for biohacking platform:**
```python
# Never store raw health data fields that identify individuals in plaintext
# Use field-level encryption for: bloodwork values linked to identity, supplement protocols
from cryptography.fernet import Fernet

# Key rotation: store key version alongside ciphertext
ENCRYPTION_KEY = settings.FIELD_ENCRYPTION_KEY  # from Secret Manager, never hardcoded

def encrypt_sensitive_field(value: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()
```

**TLS everywhere:**
- Cloud Run: TLS termination handled automatically — never disable it
- Cloud SQL: `require_ssl = true` in connection config
- Internal service-to-service: use GCP's internal load balancer with mTLS

**Password hashing (if you ever store passwords):**
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# argon2 > bcrypt > scrypt. Never MD5/SHA1/SHA256 for passwords.
```

### A03 — Injection (SQL, Command, LDAP, XSS)
**Your stack risks:** FastAPI + SQLAlchemy + PostgreSQL, n8n webhook payloads, Power Automate inputs

**SQLAlchemy — always parameterized, never f-string SQL:**
```python
# NEVER do this:
query = f"SELECT * FROM users WHERE email = '{email}'"

# Always do this (SQLAlchemy ORM):
user = await db.execute(select(User).where(User.email == email))

# Or if raw SQL is necessary, use text() with bound params:
from sqlalchemy import text
result = await db.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {"email": email}
)
```

**FastAPI input validation — use Pydantic v2 strictly:**
```python
from pydantic import BaseModel, field_validator, EmailStr
import re

class UserInput(BaseModel):
    email: EmailStr  # validated format
    name: str

    @field_validator('name')
    @classmethod
    def name_must_be_safe(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z\s\-\']+$', v):
            raise ValueError('Name contains invalid characters')
        return v.strip()
```

**Next.js XSS prevention:**
```tsx
// Never use dangerouslySetInnerHTML with user content
// Use DOMPurify if HTML rendering is genuinely needed:
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userHtml);

// Content Security Policy headers in next.config.js:
const ContentSecurityPolicy = `
  default-src 'self';
  script-src 'self' 'nonce-${nonce}';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: blob:;
  connect-src 'self' https://api.yourdomain.com;
  frame-ancestors 'none';
`;
```

### A04 — Insecure Design
Apply threat modeling BEFORE writing code for any new feature.

**Threat model framework (STRIDE) — quick version:**
For each new feature, ask:
- **S**poofing: Can an attacker impersonate another user?
- **T**ampering: Can they modify data in transit or at rest?
- **R**epudiation: Can they deny having performed an action?
- **I**nformation disclosure: What data could leak if this fails?
- **D**enial of service: Can this be abused to degrade availability?
- **E**levation of privilege: Can this be used to gain higher access?

Document answers before implementation. Any "yes" triggers a control requirement.

### A05 — Security Misconfiguration
**Your stack — hardening checklist:**

```yaml
# Docker: never run as root
FROM python:3.12-slim
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Don't expose unnecessary ports
EXPOSE 8080  # Only the port Cloud Run needs

# No secrets in Dockerfile or docker-compose
# Use GCP Secret Manager + mount as env at runtime
```

```python
# FastAPI — disable docs in production
from fastapi import FastAPI
import os

app = FastAPI(
    docs_url="/docs" if os.getenv("ENVIRONMENT") == "development" else None,
    redoc_url=None,
    openapi_url="/openapi.json" if os.getenv("ENVIRONMENT") == "development" else None,
)

# CORS — never use wildcard in production
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # explicit list, not ["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### A06 — Vulnerable and Outdated Components
**Toolchain:**
```bash
# Python — weekly dependency audit
pip-audit  # checks against PyPI advisory database
safety check

# Add to GitHub Actions CI:
- name: Security audit
  run: pip-audit --requirement requirements.txt

# Node/Next.js
npm audit --audit-level=high
```

Set up **Dependabot** in GitHub for automatic PRs on vulnerable dependencies.

### A07 — Identification and Authentication Failures
**JWT best practices:**
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Use RS256 (asymmetric) for JWTs in production, not HS256
# RS256: private key signs, public key verifies — compromised service can't forge tokens
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # short-lived — use refresh tokens for longer sessions
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {**data, "exp": expire, "iat": datetime.utcnow(), "jti": str(uuid4())}
    return jwt.encode(to_encode, settings.PRIVATE_KEY, algorithm=ALGORITHM)
```

**Rate limiting — protect auth endpoints:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute per IP
async def login(request: Request, credentials: LoginCredentials):
    ...
```

### A08 — Software and Data Integrity Failures
- Verify checksums for downloaded dependencies in CI pipelines
- Use GitHub Actions with pinned action SHA hashes, not floating tags
- For n8n and Power Automate: validate webhook payloads with HMAC signatures
- Sign Docker images with cosign before pushing to Artifact Registry

### A09 — Security Logging and Monitoring Failures
Log security events with structlog — never log sensitive values (passwords, tokens, raw PII).
Always log: who, what, when, from where. Never log: the secret itself.
GCP Cloud Logging alerts to configure: 5+ auth failures/IP/minute, admin endpoint access,
unusual query volume spikes (exfiltration signal), unexpected geographic patterns.

### A10 — Server-Side Request Forgery (SSRF)
Critical for biohacking platform (external API integrations):
```python
import ipaddress
from urllib.parse import urlparse

ALLOWED_DOMAINS = {"api.labcorp.com", "api.questdiagnostics.com", "api.oura.com"}

def validate_external_url(url: str) -> bool:
    parsed = urlparse(url)
    # Block private IP ranges
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except ValueError:
        pass  # hostname, not IP — check allowlist
    return parsed.hostname in ALLOWED_DOMAINS
```

---

## OWASP LLM Top 10 — AI/Agent Security

Read `references/owasp-llm-top10.md` when working on AI features, agentic systems, Copilot Studio, or any LLM integration.

**Critical summary (apply immediately without reading reference):**
- **LLM01 Prompt Injection:** Separate instruction and data channels. Validate all tool call arguments against JSON schema before execution. Sanitize external content (emails, docs, web pages) before passing to LLM.
- **LLM06 Data Disclosure:** Scrub PHI/PII before sending to external APIs. Never send raw patient data to Claude/OpenAI.
- **LLM08 Excessive Agency:** Gate all irreversible agent actions (delete, send, deploy, pay) behind explicit human confirmation.

---

## Secrets Management

Read `references/secrets-and-platform-security.md` for full GCP Secret Manager patterns, rotation schedules, and git hygiene templates.

**Zero-tolerance rules (memorize these):**
- No secrets in code, git history, Docker layers, or logs — ever
- Use GCP Secret Manager + Cloud Run env injection in production
- `.env` in `.gitignore` always; `.env.example` with placeholders is the only committed env file
- Add `gitleaks` pre-commit hook to every repo before first commit

---

## Microsoft Power Platform Security

Read `references/secrets-and-platform-security.md` (Power Platform section) for full DLP, Copilot Studio, Power Automate, and Dataverse security guidance.

**Critical rules (apply immediately):**
- Entra ID auth on all apps and agents — no anonymous access to business data
- DLP policies: separate Business/Non-Business/Blocked connector tiers in Admin Center
- Managed identities for all Azure connections — no stored credentials in flows
- Audit all active flows monthly

---

## Security Code Review Checklist

When reviewing any new code, run through this list mentally before approving:

**Input handling:**
- [ ] All user inputs validated with Pydantic schema (types, lengths, patterns)
- [ ] No raw string concatenation in SQL queries
- [ ] File uploads: type validated server-side (not just client-side), size limited, stored outside webroot
- [ ] URL parameters decoded and validated before use

**Authentication & authorization:**
- [ ] Every endpoint has explicit auth dependency
- [ ] Resource ownership verified (not just "is logged in" but "owns this resource")
- [ ] Sensitive operations require re-authentication or 2FA

**Data handling:**
- [ ] PHI/PII not logged in plaintext
- [ ] Sensitive fields encrypted at rest
- [ ] API responses don't leak internal IDs, stack traces, or system info

**Infrastructure:**
- [ ] No hardcoded secrets
- [ ] No wildcard CORS in production
- [ ] Swagger/docs disabled in production
- [ ] Health check endpoint doesn't expose version or config info

**Dependencies:**
- [ ] No known CVEs in pip-audit / npm audit
- [ ] Pinned versions in requirements.txt / package.json

---

## Self-Evaluation (run before presenting security guidance)

Before presenting any security output, silently check:
[ ] Does the guidance apply defense-in-depth — not just one control?
[ ] Is every code example production-safe, not pseudocode?
[ ] Are the most critical findings presented first (Critical → High → Medium → Low)?
[ ] Are recommendations specific to the actual stack (FastAPI/GCP/PostgreSQL/Next.js)?
[ ] Has the threat model been considered, not just the symptom?
If any check fails, revise before presenting.

---

## Read references/ for:
- Full OWASP LLM Top 10 guidance (coming in next version)
- GCP security hardening runbook
- Power Platform DLP policy templates
- Penetration testing checklist for pre-launch audits
- Incident response playbook
