# Quarantine Manifest — {{AUDIT_DATE}}

Each entry below is a quarantine action. To restore a file, copy the
`restore` command and run it.

---

## {{ISO_TIMESTAMP}} — {{REL_PATH}}

- original: `{{ORIGINAL_PATH}}`
- archived: `{{ARCHIVE_PATH}}`
- mtime: {{MTIME}}
- size: {{SIZE}} bytes
- hash: {{HASH}}
- reason: {{REASON}}
- restore: `mkdir -p "{{ORIGINAL_PARENT}}" && mv "{{ARCHIVE_PATH}}" "{{ORIGINAL_PATH}}"`

---
