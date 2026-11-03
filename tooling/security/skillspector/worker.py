"""Sandbox entrypoint. It never executes candidate skill content."""
import errno
import json
import os
from pathlib import Path
import socket
import subprocess
import sys

unreachable = False
try:
    with socket.socket() as connection:
        connection.settimeout(1)
        connection.connect(("192.0.2.1", 9))
except OSError as error:
    unreachable = error.errno in (errno.ENETUNREACH, errno.EHOSTUNREACH)
evidence = {
    "network_namespace": os.readlink("/proc/self/ns/net"),
    "network_unreachable": unreachable,
    "input_read_only": bool(os.statvfs("/input").f_flag & os.ST_RDONLY),
    "home_empty": not any(Path("/home").iterdir()),
    "credential_environment_empty": not any(
        token in name.upper() for name in os.environ for token in ["KEY", "TOKEN", "SECRET", "COOKIE", "CREDENTIAL"]
    ),
    "tracing_disabled": all(os.environ.get(name) == "false" for name in ["LANGSMITH_TRACING", "LANGCHAIN_TRACING_V2"]),
}
Path("/output/isolation.json").write_text(json.dumps(evidence))
if "--probe" in sys.argv:
    raise SystemExit(0 if all(value for key, value in evidence.items() if key != "network_namespace") else 1)
with Path("/output/scanner.log").open("wb") as log:
    result = subprocess.run([
        "/opt/venv/bin/python", "/opt/venv/bin/skillspector", "scan", "/input",
        "--no-llm", "--format", "json", "--output", "/output/report.json",
        "--fail-on-findings", "--fail-on-incomplete",
    ], stdout=log, stderr=subprocess.STDOUT, check=False)
raise SystemExit(result.returncode)
