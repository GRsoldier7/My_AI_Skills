#!/usr/bin/env python3
"""Run the library's portable release checks from any directory."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

def lint_library():
    proc = subprocess.run([sys.executable, "-B", str(SCRIPTS / "lint-skills.py"), "--json"],
                          cwd=ROOT, stdout=subprocess.PIPE)
    if proc.returncode not in (0, 1):
        return False
    report = json.loads(proc.stdout)
    registry = json.loads((ROOT / "registry/skills.json").read_bytes())
    problems = []
    for finding in report["findings"]:
        if finding["severity"] != "FAIL":
            continue
        problems.append(f'{finding["skill"]} line {finding["line"]}: {finding["rule"]}')
    print(f'Full audit: {report["scanned"]} skills, {report["fail_count"]} failures, '
          f'{report["warn_count"]} warnings.')
    for item in problems:
        print(item)
    if report["scanned"] != registry["totals"]["skills"]:
        print("Audit and registry disagree on the number of skills.")
        return False
    return not problems

def main():
    checks = [
        ("generate-skill-registry.py", "--check"), ("test-registry-portability.py",),
        ("project-guidance.py", "check"), ("test-project-guidance.py",),
        ("test-phantom-refs.py",), ("test-project-router.py",),
        ("test-skill-picks.py",), ("test-work-skills.py",), ("test-solution-preflight.py",), ("lint-skills.py", "--category", "faith"),
    ]
    failed = []
    for args in checks:
        print(f'\n$ {Path(sys.executable).name} scripts/{" ".join(args)}', flush=True)
        result = subprocess.run([sys.executable, "-B", str(SCRIPTS / args[0]), *args[1:]], cwd=ROOT)
        if result.returncode:
            failed.append(args[0])
    if not lint_library():
        failed.append("full library audit")
    if failed:
        print("Failed checks: " + ", ".join(failed), file=sys.stderr)
    return int(bool(failed))

if __name__ == "__main__":
    sys.exit(main())
