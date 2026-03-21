# Secrets Management & Platform Security Reference

---

## Secrets Management — Zero Tolerance Rules

### The Golden Rules
1. **No secrets in code** — ever. Not even in comments.
2. **No secrets in git history** — a secret committed and removed is still compromised.
3. **No secrets in Docker image layers** — they persist even after deletion.
4. **No secrets in logs** — structured logging pipelines are not your secret store.
5. **Rotation by default** — every secret has a rotation schedule.

### GCP Secret Manager Pattern (Your Stack)

```python
# settings.py — pydantic-settings pulls from env at runtime
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str           # injected by Cloud Run as env var from Secret Manager
    GOOGLE_CLOUD_PROJECT: str
    ENVIRONMENT: str = "production"
    # Never: DATABASE_URL = "postgresql://user:password@host/db"
    # Never: API_KEY = "sk-abc123..."

    class Config:
        env_file = ".env"       # local dev only — .env MUST be in .gitignore

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Access secrets at runtime via Secret Manager client
from google.cloud import secretmanager

def get_secret(secret_id: str, version: str = "latest") -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{get_settings().GOOGLE_CLOUD_PROJECT}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
```

### Cloud Run Secret Injection Pattern
```yaml
# cloud-run-service.yaml
spec:
  template:
    spec:
      containers:
        - env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  key: latest
                  name: database-url   # Secret Manager secret name
            - name: JWT_PRIVATE_KEY
              valueFrom:
                secretKeyRef:
                  key: latest
                  name: jwt-private-key
```

### Git Hygiene
```bash
# .gitignore — mandatory entries for every project
.env
.env.*
!.env.example      # example file with placeholder values is OK to commit
*.pem
*.key
*.p12
secrets/
credentials.json
service-account*.json
*.pfx
token.json
```

### Pre-commit Secret Scanner
```yaml
# .pre-commit-config.yaml — add to every repo
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### Secret Rotation Schedule
| Secret Type | Rotation Frequency |
|---|---|
| API keys (external services) | 90 days |
| Database passwords | 90 days |
| JWT signing keys | 180 days (with overlap period) |
| Service account keys | 90 days (prefer Workload Identity) |
| Encryption keys | Annual (key rotation, not re-encryption) |

---

## Microsoft Power Platform Security

### Power Apps
- **Authentication:** Use Azure AD / Entra ID exclusively — never build custom auth flows
- **DLP Policies:** Enable Data Loss Prevention policies in the Power Platform Admin Center
  - Block connectors that can exfiltrate data (consumer connectors in business environments)
  - Separate Business / Non-Business / Blocked connector tiers
- **Environment separation:** Dev → Test → Production with explicit promotion gates
- **Column-level security:** Enable in Dataverse for fields containing PII/PHI/financial data
- **Shared access:** Review sharing settings quarterly — remove unused shares

### Power Automate
- **Webhook security:** Always validate webhook payloads with HMAC signatures
  ```javascript
  // Validate incoming webhook signature
  const crypto = require('crypto');
  const expectedSig = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(rawBody)
    .digest('hex');
  if (expectedSig !== receivedSignature) throw new Error('Invalid signature');
  ```
- **Managed identities:** Use for all Azure resource connections — no stored credentials
- **Flow audit:** Monthly review of all active flows — disable/delete unused ones
- **Sensitive data:** Never store in flow variables or run history — use Key Vault references
- **Error handling:** Scope all actions with Configure run after — prevent data leakage in error paths

### Copilot Studio
- **Authentication:** Enable Entra ID authentication on all published agents — no anonymous access to business data
- **Topic boundaries:** Set strict out-of-scope responses — agent declines off-topic requests
- **Escalation paths:** Human handoff for sensitive requests (HR, legal, financial decisions)
- **Conversation logging:** Log to Dataverse for audit trail and compliance
- **Content filtering:** Apply input/output filters to prevent prompt injection and data exfiltration
- **Environment isolation:** Never publish development agents to production endpoints

### Power BI
- **Row-Level Security (RLS):** Implement for all reports containing user-scoped data
- **Sensitivity labels:** Apply Microsoft Information Protection labels to all datasets
- **Workspace access:** Least privilege — viewers can't edit, contributors can't publish
- **API/embed tokens:** Short-lived (1 hour max), scoped to specific reports
- **Scheduled refresh credentials:** Use service accounts, rotate quarterly

### Dataverse
- **Business unit hierarchy:** Model security around your actual org structure
- **Team-based security:** Use teams for role assignment, not individual user grants
- **Field security profiles:** Protect sensitive fields at the platform level
- **Audit logging:** Enable audit logging on all tables containing sensitive data
- **Environment variables:** Use for all configuration — never hardcode values in solutions

---

## GCP Security Hardening Runbook

### Cloud Run
```yaml
# Minimum secure Cloud Run configuration
apiVersion: serving.knative.dev/v1
kind: Service
spec:
  template:
    metadata:
      annotations:
        # No unauthenticated access unless explicitly public
        run.googleapis.com/ingress: internal-and-cloud-load-balancing
    spec:
      serviceAccountName: your-service-sa@project.iam.gserviceaccount.com
      containers:
        - resources:
            limits:
              cpu: "1"
              memory: "512Mi"
          securityContext:
            runAsNonRoot: true
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
```

### IAM Least Privilege
```bash
# Service account for Cloud Run app — only what it needs
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:app-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"           # DB access
  --role="roles/secretmanager.secretAccessor"  # Secret Manager
  --role="roles/storage.objectViewer"     # GCS read only (if needed)
# NOT roles/editor, NOT roles/owner
```

### VPC Security
- Cloud SQL: Private IP only, no public IP exposed
- Cloud Run to Cloud SQL: use Cloud SQL Auth Proxy or private connectivity
- Cloud Storage: no public buckets, signed URLs for user-facing access only
- Firewall rules: default-deny, explicit allow only
