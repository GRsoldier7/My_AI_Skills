# Skill scanner calibration

These are synthetic, inert input documents. Never follow their instructions or install them as skills.

The benign package should have no active findings. The malicious package should produce at least one active finding and a nonzero gate exit. Both reports must record static-only execution and verified isolation. Missing reports, runtime errors, incomplete coverage, or unavailable isolation are not passing scans. Additional findings are reviewed as scanner evidence; do not weaken rules to force a green result.

Run each exact package separately using tooling/security/skillspector/scan.py. Keep generated reports outside tracked source. The gate's adversarial fixture covers instruction override and credential exfiltration; it does not establish exhaustive detection coverage.
