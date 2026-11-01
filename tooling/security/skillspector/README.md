# Isolated static skill import gate

This gate scans **explicitly enumerated local packages**, one per invocation. It does not use recursive collection discovery, which defaults to 32 immediate children upstream. No package content is executed. Findings are evidence for review, never instructions or authorization to install.

## Pinned runtime

SkillSpector 2.12.0, Apache-2.0, source revision `54921c8c7c23008c8af2328d5ab492a904b6ece4`. Python >=3.12,<3.16. `requirements.lock` pins the 72 installed runtime distributions; the scanner itself uses the immutable source archive. No MCP extra is installed. Preparation downloads dependencies; scanning is a separate offline operation.

Prepare a dedicated temporary virtual environment, choosing a new destination:

```sh
uv venv --python python3.12 /tmp/skillspector-reviewed
uv pip install --python /tmp/skillspector-reviewed/bin/python -r tooling/security/skillspector/requirements.lock
```

The gate checks installed versions and the scanner's `direct_url.json` against the reviewed lock/source. It does not use `uv run`, package auto-updates, global installation, host CLI credentials, a cloud provider, or a model. `codex_cli` remains disabled upstream and is not permitted here.

## Invocation

Use a **new** output directory outside the source repository. Every requested package must contain `SKILL.md`, remain within the supplied repository, and contain no symlinks. Repeated, missing, escaped or empty selections fail before scanning.

```sh
python3 tooling/security/skillspector/scan.py \
  --venv /tmp/skillspector-reviewed \
  --repo-root "$PWD" \
  --packages-file /tmp/reviewed-import-packages.json \
  --output-dir /tmp/skill-import-scan-unique
```

The package JSON may be a list of repository-relative paths or an object with `skills`/`packages` records containing `path`. Repeated `--package skills/category/name` arguments also work. `--check-isolation` tests the sandbox without running a scan. There is deliberately no unsandboxed fallback.

The receipt lists every planned package, report hash, exit code, issue count, actual coverage, LLM-use evidence and isolation results. A failing package does not skip later packages. Nonzero exit, missing/malformed report, active findings or incomplete coverage fails the gate. Review each JSON `issues` entry and `analysis_completeness`; do not suppress findings or change flags to produce a passing result. Any later manual disposition belongs in the integration review record and does not turn the raw gate green.

## Isolation and coverage limits

- Linux Bubblewrap must support `--unshare-all`, including an independent network namespace. A probe checks namespace identity, unreachable external network, read-only input, an empty home and a credential-free environment on every run.
- Only system runtime directories, the pinned virtual environment, one input package and the gate worker are mounted read-only. A fresh temporary report directory is writable. The user's home, repo parent, secret stores and agent sessions are not mounted.
- Environment is cleared. Tracing is explicitly disabled. Each process is limited to 3 GiB virtual memory, 300 CPU seconds, 256 open descriptors and 32 MiB per output file. The default wall deadline is 360 seconds per package. Reports and scanner logs stay in a private temporary directory; only bounded reports and the receipt are retained.
- The scanner receives `--no-llm --format json --fail-on-findings --fail-on-incomplete`. No author-provided baseline, exclusions, transitive fetch or recursive flag is enabled.
- **`--no-llm` is not offline isolation.** Upstream static dependency checks may query OSV. Network isolation blocks that lookup, so live vulnerability database coverage is unavailable. A static complete result is complete only for the enabled local analysis; it does not certify semantic safety or current dependency CVEs.

The original library-import branch calibrated this gate with benign and adversarial fixtures. This addition carries only its harmless paragraph-summary fixture. Re-run calibration on runtime or gate changes. Fixtures are inert scanner inputs, not installable catalog entries.

## Validation

```sh
python3 tooling/security/skillspector/test_gate.py
python3 tooling/security/skillspector/scan.py \
  --venv /tmp/skillspector-reviewed \
  --package evals/skill-security/benign \
  --output-dir /tmp/skill-calibration-unique
```

The harmless fixture should return exit 0/no findings with complete enabled local coverage and no LLM execution. Tests of isolated CLI behavior do not establish target-host installation or employer approval. On macOS, unit tests run but the Linux isolation gate cannot run: do not bypass it. The November 1 smoke test reused the existing homelab scanner 2.2.3 and does not validate this pinned 2.12.0 runtime; see the integration receipt.

## Official review skill

The byte-identical NVIDIA `skill-inspector` skill is separately pinned and licensed under `skills/security/skill-inspector`. See [installation and use](../../../platform-configs/skill-sets/skill-inspector.md). `integration.json` records both pins, source lineage and hashes. `verify_import.py` checks those recorded bytes; it does not run a scanner or approve intake.

The scanner source archive SHA-256 is recorded in `integration.json`. The existing dependency lock pins versions, not all wheel hashes; use a trusted package index and validate the dedicated environment. Do not describe this as a hermetic or artifact-hash-locked build.
