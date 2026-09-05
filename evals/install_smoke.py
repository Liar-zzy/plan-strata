#!/usr/bin/env python3
"""Check Skills CLI installation in temporary projects; never install globally."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from prepare import make_case


REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "skills/plan-strata"
INSTALLER = "skills@1.5.23"


def snapshot(directory):
    return {
        path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(REPO),
                        help="Skills CLI source; default: this local checkout")
    parser.add_argument("--output", help="new JSON report file; default: stdout")
    args = parser.parse_args()
    output = Path(args.output) if args.output else None
    if output and (output.exists() or output.is_symlink()):
        parser.exit(2, f"Refusing to overwrite {output}\n")
    npx = shutil.which("npx")
    if not npx:
        parser.exit(2, "This optional check needs Node.js 22.20+ and npx.\n")
    env = {**os.environ, "DISABLE_TELEMETRY": "1", "DO_NOT_TRACK": "1",
           "PYTHONDONTWRITEBYTECODE": "1", "NO_COLOR": "1"}
    expected = snapshot(PACKAGE)
    report = {
        "kind": "release-install-smoke", "created_at": datetime.now(timezone.utc).isoformat(),
        "installer": INSTALLER, "source": args.source, "status": "fail",
        "commands": [], "installations": [],
        "subjects": [
            {"path": f"skills/plan-strata/{path}", "sha256": digest}
            for path, digest in expected.items()
        ] + [
            {"path": path, "sha256": hashlib.sha256((REPO / path).read_bytes()).hexdigest()}
            for path in ("evals/install_smoke.py", "evals/prepare.py")
        ],
        "limits": "Checks package bytes and installed CLI behavior, not client discovery or agent behavior. "
                  "Temporary/source/interpreter paths in output are replaced with labels. "
                  "A local source does not test GitHub transport. No global skills are installed.",
    }
    with tempfile.TemporaryDirectory(prefix="plan-strata-install-") as temporary:
        def run(command, cwd):
            result = subprocess.run(command, cwd=cwd, env=env, text=True,
                                    capture_output=True, timeout=120, check=False)
            report["commands"].append({"command": command, "cwd": str(cwd),
                                       "exit_code": result.returncode,
                                       "stdout": result.stdout, "stderr": result.stderr})
            if result.returncode:
                raise RuntimeError(f"Command exited {result.returncode}: {command[0]}")
            return result.stdout

        try:
            run(["node", "--version"], temporary)
            run([npx, "--yes", INSTALLER, "--version"], temporary)
            for agent, relative in (("codex", ".agents/skills/plan-strata"),
                                    ("claude-code", ".claude/skills/plan-strata")):
                project = make_case(Path(temporary) / agent, "resume")
                before = snapshot(project)
                run([npx, "--yes", INSTALLER, "add", args.source, "--skill", "plan-strata",
                     "--agent", agent, "--yes"], project)
                installed = project / relative
                actual = snapshot(installed)
                if actual != expected:
                    raise RuntimeError(f"{agent}: installed files differ from this checkout's package")
                script = str(installed / "scripts/strata.py")
                validation = json.loads(run([sys.executable, script, "validate", "--project", "."], project))
                if (validation["status"], validation["overall"]) != ("consistent", "open"):
                    raise RuntimeError(f"{agent}: unexpected validation result")
                fingerprints = json.loads(run([sys.executable, script, "fingerprint", "--project",
                                              str(installed), "SKILL.md"], project))
                if fingerprints != [{"path": "SKILL.md", "sha256": expected["SKILL.md"]}]:
                    raise RuntimeError(f"{agent}: installed fingerprint command differs")
                after = snapshot(project)
                if any(after.get(path) != digest for path, digest in before.items()):
                    raise RuntimeError(f"{agent}: existing project files changed")
                report["installations"].append({"agent": agent, "path": relative,
                                                "files": actual, "validation": validation,
                                                "existing_project_unchanged": True})
            report["status"] = "pass"
        except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
            report["error"] = str(error)

    encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    for path, label in ((temporary, "<temporary-workspace>"), (str(REPO), "<source-repository>"),
                        (sys.executable, "python3")):
        encoded = encoded.replace(path, label)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8") as stream:
            stream.write(encoded)
        print(f"status={report['status']}; report={output}")
    else:
        print(encoded, end="")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
