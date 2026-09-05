#!/usr/bin/env python3
"""Preserve a forward-use workspace and a fresh validator result as one JSON artifact."""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def inventory(root, include_text):
    records = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(p in {".git", "__pycache__"} for p in path.relative_to(root).parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Evaluation artifacts must be regular files: {path}")
        content = path.read_bytes()
        item = {"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(content).hexdigest()}
        if include_text:
            item["text"] = content.decode("utf-8")
        records.append(item)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--worker", required=True)
    parser.add_argument("--output", required=True, help="new file outside the evaluated project")
    args = parser.parse_args()
    project, skill, output = Path(args.project).resolve(), Path(args.skill).resolve(), Path(args.output).resolve()
    if output.exists() or output.is_relative_to(project):
        parser.exit(2, "Output must be a new file outside the evaluated project\n")
    result = subprocess.run([sys.executable, str(skill / "scripts/strata.py"), "validate",
                             "--project", str(project)], capture_output=True, text=True, check=False)
    try:
        report = {
            "kind": "forward-use-capture", "scenario": args.scenario, "worker": args.worker,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "skill_files": inventory(skill, False), "artifacts": inventory(project, True),
            "validation_exit_code": result.returncode, "validation": json.loads(result.stdout),
            "validation_stderr": result.stderr,
            "limits": "A record of one observed workspace, not a success-rate estimate. Artifact prose is worker-authored; inspect the evidence itself.",
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    except (OSError, ValueError) as exc:
        parser.exit(2, f"{exc}\n")
    print(f"scenario={args.scenario}; validator_exit={result.returncode}; report={output}")


if __name__ == "__main__":
    main()
