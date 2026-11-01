#!/usr/bin/env python3
"""Enumerate exact local packages and run the pinned static scanner in Bubblewrap."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import resource
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
REVISION = "54921c8c7c23008c8af2328d5ab492a904b6ece4"
SOURCE = f"https://github.com/NVIDIA/SkillSpector/archive/{REVISION}.zip"
LIMIT_BYTES = 32 * 1024 * 1024


def canonical_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def validate_runtime(venv: Path) -> dict:
    """Read distribution metadata without importing scanner/provider code."""
    sites = list((venv / "lib").glob("python*/site-packages"))
    if len(sites) != 1 or not (venv / "bin/python").exists():
        raise ValueError("Expected a dedicated Python virtual environment")
    expected = {}
    for line in (HERE / "requirements.lock").read_text().splitlines():
        if "==" in line and not line.startswith("#"):
            name, version = line.split("==", 1)
            expected[canonical_name(name)] = version
    expected["skillspector"] = "2.12.0"
    distributions = list(importlib.metadata.distributions(path=[str(sites[0])]))
    actual = {canonical_name(d.metadata["Name"]): d.version for d in distributions}
    if actual != expected:
        raise ValueError("Runtime distributions differ from requirements.lock; prepare the pinned environment")
    scanner = next(d for d in distributions if canonical_name(d.metadata["Name"]) == "skillspector")
    direct = json.loads(scanner.read_text("direct_url.json") or "{}")
    if direct.get("url") != SOURCE:
        raise ValueError("Scanner source does not match the reviewed immutable archive")
    for path in sites[0].rglob("*"):
        if path.is_symlink() and not path.resolve().is_relative_to(venv):
            raise ValueError("Runtime package links outside its isolated environment")
    return {"version": scanner.version, "revision": REVISION,
            "dependency_count": len(actual),
            "lock_sha256": hashlib.sha256((HERE / "requirements.lock").read_bytes()).hexdigest()}


def limits() -> None:
    resource.setrlimit(resource.RLIMIT_FSIZE, (LIMIT_BYTES, LIMIT_BYTES))
    resource.setrlimit(resource.RLIMIT_AS, (3 * 1024**3, 3 * 1024**3))
    resource.setrlimit(resource.RLIMIT_CPU, (300, 300))
    resource.setrlimit(resource.RLIMIT_NOFILE, (256, 256))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def sandbox_command(venv: Path, package: Path, output: Path, probe: bool) -> list[str]:
    bwrap = shutil.which("bwrap")
    if not bwrap:
        raise ValueError("Bubblewrap unavailable; no unsandboxed fallback is permitted")
    command = [bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv"]
    for directory in ["/usr", "/lib", "/lib64"]:
        if Path(directory).exists():
            command += ["--ro-bind", directory, directory]
    command += ["--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
                "--dir", "/home", "--dir", "/opt", "--dir", "/gate",
                "--ro-bind", str(venv), "/opt/venv",
                "--ro-bind", str(HERE / "worker.py"), "/gate/worker.py",
                "--ro-bind", str(package), "/input", "--bind", str(output), "/output",
                "--setenv", "HOME", "/tmp", "--setenv", "PATH", "/opt/venv/bin:/usr/bin",
                "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
                "--setenv", "LANGSMITH_TRACING", "false",
                "--setenv", "LANGCHAIN_TRACING_V2", "false",
                "--setenv", "OTEL_SDK_DISABLED", "true",
                "--setenv", "AWS_EC2_METADATA_DISABLED", "true",
                "--chdir", "/tmp", "/opt/venv/bin/python", "/gate/worker.py"]
    if probe:
        command.append("--probe")
    return command


def enumerate_packages(args: argparse.Namespace) -> list[Path]:
    values = list(args.package)
    if args.packages_file:
        supplied = json.loads(args.packages_file.read_text())
        if isinstance(supplied, dict):
            supplied = supplied.get("skills", supplied.get("packages"))
        if not isinstance(supplied, list):
            raise ValueError("Package manifest must be a list, or contain skills/packages list")
        values += [v["path"] if isinstance(v, dict) else v for v in supplied]
    paths = []
    for value in values:
        path = args.repo_root / value
        if path.is_symlink() or not path.resolve().is_relative_to(args.repo_root):
            raise ValueError(f"Package must stay within the supplied repository: {value}")
        path = path.resolve()
        if not path.is_dir() or not (path / "SKILL.md").is_file():
            raise ValueError(f"Missing exact skill package: {value}")
        if any(p.is_symlink() for p in path.rglob("*")):
            raise ValueError(f"Symlink inside package is not admitted: {value}")
        if path in paths:
            raise ValueError(f"Duplicate package: {value}")
        paths.append(path)
    if not paths:
        raise ValueError("Supply at least one exact --package or --packages-file entry")
    return paths


def run_one(venv: Path, package: Path, destination: Path, timeout: int, probe=False) -> dict:
    parent_net = os.readlink("/proc/self/ns/net")
    with tempfile.TemporaryDirectory(prefix="skillspector-output-") as directory:
        temporary = Path(directory)
        with (temporary / "launcher.log").open("wb") as log:
            process = subprocess.run(sandbox_command(venv, package, temporary, probe),
                                     stdout=log, stderr=subprocess.STDOUT, timeout=timeout,
                                     env={"PATH": "/usr/bin:/bin"}, preexec_fn=limits)
        isolation = temporary / "isolation.json"
        if not isolation.is_file():
            raise ValueError("Sandbox failed before proving isolation: " +
                             (temporary / "launcher.log").read_text(errors="replace")[:1000])
        evidence = json.loads(isolation.read_text())
        if evidence["network_namespace"] == parent_net or not all(
            evidence[k] for k in ["input_read_only", "home_empty", "network_unreachable", "credential_environment_empty"]
        ):
            raise ValueError("Isolation probe failed; scanner result rejected")
        result = {"isolation": evidence, "exit_code": process.returncode}
        if not probe:
            report_path = temporary / "report.json"
            if not report_path.is_file() or report_path.stat().st_size > LIMIT_BYTES:
                raise ValueError("Scanner report missing or exceeded output bound")
            report = json.loads(report_path.read_text())
            shutil.copyfile(report_path, destination)
            metadata = report.get("metadata", {})
            completeness = report.get("analysis_completeness", {})
            issues = report.get("issues")
            if not isinstance(issues, list) or metadata.get("llm_requested") is not False or metadata.get("inference_usage") != []:
                raise ValueError("Unexpected report schema or LLM use; result rejected")
            result.update({"report": str(destination), "report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
                           "finding_count": len(issues), "coverage": completeness,
                           "scan_mode": "static-only", "llm_used": False,
                           "recommendation": report.get("risk_assessment", {}).get("recommendation")})
            if issues or completeness.get("is_complete") is not True or report.get("execution_successful") is not True:
                result["exit_code"] = 1
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--venv", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--package", action="append", default=[])
    parser.add_argument("--packages-file", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=360)
    parser.add_argument("--check-isolation", action="store_true")
    args = parser.parse_args()
    args.repo_root = args.repo_root.resolve()
    args.venv = args.venv.resolve()
    args.output_dir = args.output_dir.resolve()
    if args.output_dir.is_relative_to(args.repo_root):
        parser.error("Retained reports must be outside the source repository")
    receipt = {"mode": "static-only", "network": "isolated; OSV live lookup unavailable",
               "llm": False, "package_results": [], "gate_passed": False,
               "limitations": ["Static analysis is not semantic safety certification", "No live dependency vulnerability lookup"],
               "started_at_unix": time.time()}
    args.output_dir.mkdir(parents=True, exist_ok=False)
    try:
        if not 10 <= args.timeout <= 900:
            raise ValueError("Timeout must be between 10 and 900 seconds")
        receipt["runtime"] = validate_runtime(args.venv)
        packages = [HERE] if args.check_isolation else enumerate_packages(args)
        receipt["package_count"] = len(packages)
        receipt["planned_packages"] = [str(p.relative_to(args.repo_root)) if p.is_relative_to(args.repo_root) else str(p) for p in packages]
        for index, package in enumerate(packages):
            try:
                result = run_one(args.venv, package, args.output_dir / f"{index:04d}-{package.name}.json",
                                 args.timeout, probe=args.check_isolation)
            except (ValueError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
                result = {"exit_code": 1, "error": str(error)}
            result["package"] = receipt["planned_packages"][index]
            receipt["package_results"].append(result)
            print(json.dumps({"package": result["package"], "exit_code": result["exit_code"],
                              "finding_count": result.get("finding_count")} ), flush=True)
        receipt["gate_passed"] = all(r["exit_code"] == 0 for r in receipt["package_results"])
    except (ValueError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        receipt["error"] = str(error)
        print(f"Gate blocked: {error}", file=sys.stderr)
    receipt["completed_at_unix"] = time.time()
    (args.output_dir / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return 0 if receipt["gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
