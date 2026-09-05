#!/usr/bin/env python3
"""Run the local contract suite and preserve its output and source fingerprints."""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="new JSON report file")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    output = Path(args.output)
    if output.exists():
        parser.exit(2, f"Refusing to overwrite {output}\n")
    command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    result = subprocess.run(command, cwd=repo, text=True, capture_output=True, check=False)
    files = sorted({p for base in (repo / "skills", repo / "tests") for p in base.rglob("*")
                    if p.is_file() and "__pycache__" not in p.parts}
                   | set((repo / "evals").glob("*.py")))
    report = {
        "kind": "automated-contract-tests", "created_at": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version, "command": ["python3", *command[1:]], "cwd": ".",
        "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
        "subjects": [{"path": p.relative_to(repo).as_posix(),
                      "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
        "limits": "Contract tests use synthetic fixtures. They do not establish long-term agent behavior or research validity.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(f"exit_code={result.returncode}; report={output}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
