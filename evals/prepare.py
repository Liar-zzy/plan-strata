#!/usr/bin/env python3
"""Generate small isolated workflow scenarios. Fixtures are explicitly synthetic."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


CASES = ("resume", "switch", "stale", "integration", "research")
PLAN = "plans/ex-plans/P001/ex-plan-v0.1.0.md"
PROGRESS = "plans/ex-plans/P001/progress.md"
CORE = "plans/core/core-v0.1.0.md"


def write(root, path, content):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def record(root, path, metadata, body):
    write(root, path, "---\n" + json.dumps(metadata, ensure_ascii=False, indent=2)
          + "\n---\n\n" + body.rstrip() + "\n")


def read_record(root, path):
    text = (root / path).read_text(encoding="utf-8")
    _, metadata, body = text.split("---", 2)
    return json.loads(metadata), body.strip()


def observe(root, command, log):
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
    write(root, log, "$ " + " ".join(command) + "\n" + result.stdout + result.stderr
          + f"\nexit_code: {result.returncode}\n")
    return result.returncode


def task_row(root, task_id, state, next_action, check=None):
    row = {"id": task_id, "state": state, "owner": "fixture-worker", "next": next_action, "check": check}
    if state != "planned":
        row.update(plan=PLAN)
    return row


def check_record(root, path, task_id, subjects, evidence, verdict="pass", research=None):
    data = {"schema": 2, "kind": "check", "id": Path(path).stem, "task": task_id,
            "plan": PLAN, "verdict": verdict,
            "subjects": list(subjects), "evidence": list(evidence)}
    if research is not None:
        data["research"] = research
    record(root, path, data,
           "# Fixture check\n\nReviewer: scenario preparation script.\n\n"
           "The linked evidence records the actual local command result. This is a\n"
           "synthetic demonstration project; no real research result is claimed.\n")


def make_case(destination, case):
    if case not in CASES:
        raise ValueError(f"Unknown scenario: {case}")
    root = Path(destination)
    root.mkdir(parents=True, exist_ok=False)
    write(root, "SCENARIO.md", "# Synthetic workflow fixture\n\n"
          "Files describe a deliberately small demonstration project. Any research\n"
          "data are synthetic. Commands and logs can be verified locally.\n")
    record(root, CORE, {"schema": 2, "kind": "core", "revision": "v0.1.0"},
           "# Core\n\nComplete a bounded demonstration and retain accurate evidence.\n"
           "Use local files only. No new dependencies, external services, or real experiments.\n")
    research_case = case == "research"
    tasks = ([{"id": "T01", "type": "research", "depends_on": []}] if research_case else
             [{"id": "T01", "type": "development", "depends_on": []},
              {"id": "T02", "type": "development", "depends_on": ["T01"]}])
    body = ("# P001 — Synthetic exploratory comparison\n\n"
            "## T01\nCompare the supplied method scores using analysis.py. This is an\n"
            "exploratory demonstration. Budget: one fixed comparison, zero new experiments,\n"
            "datasets, or candidate methods. Verification may recompute this same analysis.\n"
            "A difference of +0.02 is the preselected practical improvement target.\n"
            "Acceptance requires a correct analysis of supplied data, a bounded\n"
            "interpretation, and a justified next decision. It does not require improvement.\n"
            "Evidence: results.csv and observations/analysis.log. Verify as needed.\n"
            if research_case else
            "# P001 — Sum utility and usage documentation\n\n"
            "## T01\nImplement total(values), including empty input, in src/calc.py.\n"
            "Validate with python3 tests/check_total.py.\n\n"
            "## T02\nWrite docs/usage.md with an actual import/run command, empty-input\n"
            "behavior, and a numeric example. Verify the example and record evidence.\n"
            "Keep the existing arithmetic behavior.\n\n"
            "## Integration\nWhen integration is required, verify the public wrapper\n"
            "using python3 tests/check_integration.py. Local task success alone is insufficient.\n")
    record(root, PLAN, {"schema": 2, "kind": "plan", "id": "P001", "revision": "v0.1.0",
                       "core": CORE, "ready": True,
                       "tasks": tasks, "integration_required": case == "integration"}, body)
    integration_check = None
    if research_case:
        write(root, "results.csv", "method,score\nbaseline,0.80\nbaseline,0.81\nbaseline,0.79\n"
              "candidate,0.79\ncandidate,0.80\ncandidate,0.78\n")
        write(root, "analysis.py", "import csv\nfrom statistics import mean\n\n"
              "groups = {}\nwith open('results.csv', newline='') as stream:\n"
              "    for row in csv.DictReader(stream):\n"
              "        groups.setdefault(row['method'], []).append(float(row['score']))\n"
              "delta = mean(groups['candidate']) - mean(groups['baseline'])\n"
              "print('Synthetic demonstration only')\n"
              "print(f'candidate_minus_baseline: {delta:.6f}')\n"
              "print('practical_improvement_target: 0.020000')\n")
        observe(root, [sys.executable, "analysis.py"], "observations/analysis.log")
        rows = [task_row(root, "T01", "needs_review", "Inspect the analysis and complete its scoped check")]
    else:
        write(root, "src/calc.py", "def total(values):\n    return sum(values)\n")
        write(root, "tests/check_total.py", "import sys\nfrom pathlib import Path\n"
              "sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))\n"
              "from calc import total\nassert total([]) == 0\nassert total([1, 2, 3]) == 6\n"
              "print('empty input and numeric sum passed')\n")
        observe(root, [sys.executable, "tests/check_total.py"], "observations/total.log")
        c1 = "plans/ex-plans/P001/check/T01-check-001.md"
        check_record(root, c1, "T01", ["src/calc.py", "tests/check_total.py"], ["observations/total.log"])
        rows = [task_row(root, "T01", "done", "Accepted; continue the dependent documentation", c1),
                task_row(root, "T02", "planned", "Write and verify docs/usage.md")]
        draft, _ = read_record(root, PLAN)
        draft.update(revision="v0.2.0", ready=False)
        record(root, "plans/ex-plans/P001/ex-plan-v0.2.0.md", draft,
               "# Unselected proposal\n\nExplore replacing the sum utility with multiplication.\n"
               "This draft has not been selected for execution.\n")
        if case == "switch":
            draft.update(ready=True)
            record(root, "plans/ex-plans/P001/ex-plan-v0.2.0.md", draft,
                   body + "\n## Revision\nNew documentation should additionally include negative values.\n"
                   "The already-running T01 remains assigned to v0.1.0; reconcile acceptance later.\n")
            rows[0] = task_row(root, "T01", "in_progress", "Finish the original T01 scope and hand it off")
        if case == "stale":
            write(root, "src/calc.py", "def total(values):\n    return sum(values) + 1\n")
        if case == "integration":
            write(root, "docs/usage.md", "# Usage\n\nRun from project root:\n\n"
                  "```sh\nPYTHONPATH=src python3 -c 'from calc import total; print(total([1, 2, 3]))'\n"
                  "```\n\nThe result is 6. Empty input returns 0.\n")
            observe(root, [sys.executable, "tests/check_total.py"], "observations/docs.log")
            c2 = "plans/ex-plans/P001/check/T02-check-001.md"
            check_record(root, c2, "T02", ["docs/usage.md", "src/calc.py"], ["observations/docs.log"])
            rows[1] = task_row(root, "T02", "done", "Review integration outcome", c2)
            write(root, "src/public.py", "from calc import total\ndef public_total(values):\n    return total(values) * 2\n")
            write(root, "tests/check_integration.py", "import sys\nfrom pathlib import Path\n"
                  "sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))\n"
                  "from public import public_total\nassert public_total([1, 2, 3]) == 6\n")
            observe(root, [sys.executable, "tests/check_integration.py"], "observations/integration.log")
            integration_check = "plans/ex-plans/P001/check/integration-check-001.md"
            check_record(root, integration_check, "integration", ["src/calc.py", "src/public.py",
                         "tests/check_integration.py"], ["observations/integration.log"], "fail")
    record(root, PROGRESS, {"schema": 2, "kind": "progress", "plan_id": "P001",
                           "tasks": rows, "integration_check": integration_check},
           "# Handoff\n\nRead the task metadata and relevant observation files.\n"
           "There are no background jobs. Synthetic fixture preparation produced the existing files.\n")
    selected = "plans/ex-plans/P001/ex-plan-v0.2.0.md" if case == "switch" else PLAN
    record(root, "plans/CURRENT.md", {"schema": 2, "kind": "current", "plan": selected,
                                      "progress": PROGRESS},
           "# Current\n\nSelected for this bounded synthetic demonstration.\n")
    return root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, help="new directory; never overwrites existing files")
    parser.add_argument("--scenario", choices=CASES, required=True)
    args = parser.parse_args()
    try:
        result = make_case(args.destination, args.scenario)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print(result.resolve())


if __name__ == "__main__":
    main()
