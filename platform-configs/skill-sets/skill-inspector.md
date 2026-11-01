# NVIDIA SkillSpector and Skill Inspector

SkillSpector is NVIDIA's scanner. **Skill Inspector** is NVIDIA's official agent skill that combines scanner evidence with source review. The skill here is unchanged upstream text, not a locally authored replacement. The Linux isolation launcher is locally authored repository tooling reused from the existing library-import branch.

## Use and optional skill installation

```sh
python3 tooling/security/skillspector/verify_import.py
bash scripts/install-skills.sh --set platform-configs/skill-sets/skill-inspector.txt
# Apply only on the host where the skill should be available:
bash scripts/install-skills.sh --set platform-configs/skill-sets/skill-inspector.txt --apply
```

Preview exit 3 means changes are pending. This links the official skill into Claude and Codex using the existing installer; it does not install a scanner, modify host configuration or enable hooks. Keep the checkout persistent. Do not use `--prune`. Reload the host catalog and invoke `$skill-inspector` in Codex or `/skill-inspector` in Claude. This addition was published to GitHub; these optional global install commands were not applied in this task.

For this repository's import gate, use the [pinned isolated scanner setup](../../tooling/security/skillspector/README.md), selecting only the explicitly requested package. Keep `--no-llm`. The gate requires Linux and Bubblewrap and has no unsandboxed fallback. A missing scanner or unsupported host permits manual source review, but must be reported as an incomplete automated check; it does not waive intake approval. The official skill's generic CLI example is not a replacement for the repository gate.

## Data and authorization boundaries

- Do not execute target skill scripts. Scan exact local input paths; do not sweep unrelated directories, follow remote dependencies or enable hooks/MCP automatically.
- No paid semantic scans, external model uploads or new credentials are enabled. Agent source review occurs in the current authorized session, separately from scanner LLM analysis.
- `--no-llm` alone is **not offline mode**. Upstream's OSV client sends dependency ecosystem/name/version records to `api.osv.dev/v1/querybatch` and fetches advisory details. The isolated gate blocks all network traffic, so live dependency vulnerability coverage is unavailable. Any separately authorized online check must contain public dependency metadata only.
- Preserve raw findings. Read the cited code and verify current primary advisory status (including rejected/withdrawn CVEs); never infer safety from a score or suppress findings to make the gate green.
- Existing ALLOW/NOTIFY/BLOCK intake rules still apply. The official skill's APPROVE/CAUTION/REJECT wording is review advice, not permission to install, execute, publish or bypass a failed gate.

## Pins and validation

Official skill: NVIDIA/SkillSpector commit `6d0b7c849949cab9181e57798247f89e48ce5d6a`, `skills/skill-inspector/SKILL.md`, Apache-2.0. Scanner setup: existing SkillSpector 2.12.0 at `54921c8c7c23008c8af2328d5ab492a904b6ece4`, Python >=3.12,<3.16. The separate pins are intentional: the existing reproducible gate is retained while importing the current official review skill. All source hashes and local adaptations are in [integration.json](../../tooling/security/skillspector/integration.json).

The existing homelab runtime 2.2.3 scanned only the exact official skill package and harmless fixture with `--no-llm`, an empty HOME, cleared credentials and tracing disabled. Skill score: 2/100, SAFE; four LOW EA3 matches in Apache license wording at lines 27, 32, 55 and 160, reviewed as non-executable legal text. Fixture: 0/100, no findings. The older scanner has no analysis-completeness field; this is not proof of full modern coverage. Raw reports are preserved under `tooling/security/skillspector/reviews/20261101/`.

No Linux/Bubblewrap runtime was available for this task, so the imported 2.12.0 isolation gate was unit-tested but not run end to end. No scanner/runtime/global configuration was installed or upgraded. The existing other checkout remains untouched.
