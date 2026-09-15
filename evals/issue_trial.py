#!/usr/bin/env python3
"""Prepare a local Git cold-start scenario, not an Issue publisher or scheduler."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from evals.prepare import CORE, PLAN, PROGRESS, record, write


REPO = Path(__file__).resolve().parents[1]


def git(root, *args, strip_output=True):
    """Use fixture identity and disable hooks/signing without changing user config."""
    output = subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
         "-c", "user.name=Plan Strata Trial", "-c", "user.email=trial@example.invalid",
         *map(str, args)], cwd=root, capture_output=True, text=True, check=True,
    ).stdout
    return output.strip() if strip_output else output


def prepare_trial(destination):
    trial = Path(destination).resolve()
    trial.mkdir(parents=True, exist_ok=False)
    seed = trial / "seed"
    seed.mkdir()
    for name in ("outbox", "worker-area"):
        (trial / name).mkdir()
    shutil.copytree(REPO / "skills/plan-strata", trial / "skill",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    write(seed, "SCENARIO.md", "# Synthetic Issue pickup trial\n\n"
          "Implement a tiny sum utility, then document the accepted implementation.\n"
          "Manager owns planning and acceptance. One local worker at a time; each\n"
          "attempt gets reports/<task>/<attempt>.md and observations/<task>/<attempt>/.\n"
          "Use Python standard library only; at most 3 verification runs per attempt.\n"
          "No network, installs, nested agents, push, merge, or source commits by workers.\n"
          "Creating a local clone and worktree from the supplied source is authorized.\n")
    write(seed, "src/calc.py", "def total(values):\n    raise NotImplementedError\n")
    write(seed, "tests/test_calc.py", "import unittest\nfrom src.calc import total\n\n"
          "class Checks(unittest.TestCase):\n"
          "    def test_empty(self):\n        self.assertEqual(total([]), 0)\n\n"
          "    def test_numbers_and_input(self):\n"
          "        values = [2, -5, 1.5]\n"
          "        self.assertEqual(total(values), -1.5)\n"
          "        self.assertEqual(values, [2, -5, 1.5])\n\n"
          "    def test_iterator(self):\n"
          "        self.assertEqual(total(iter([1, 2, 3])), 6)\n")
    record(seed, CORE, {"schema": 2, "kind": "core", "revision": "v0.1.0"},
           "# Issue pickup fixture\n\nDeliver an iterable numeric sum utility and\n"
           "usage documentation. This is a synthetic local workflow trial.\n")
    record(seed, PLAN, {"schema": 2, "kind": "plan", "id": "P001", "revision": "v0.1.0",
                       "core": CORE, "ready": True,
                       "tasks": [{"id": "T01", "type": "development", "depends_on": []},
                                 {"id": "T02", "type": "development", "depends_on": ["T01"]}],
                       "integration_required": False},
           "# Sum utility\n\n## T01\nImplement total(values) in src/calc.py.\n"
           "Accept an iterable of numbers, return its sum (0 for empty input), and\n"
           "leave caller-owned input unchanged. Verify with\n"
           "python3 -m unittest discover -s tests -p test_calc.py -v.\n"
           "Allowed writes: src/calc.py, reports/T01/, observations/T01/.\n\n"
           "## T02\nAfter Manager accepts T01 and supplies its exact retained delivery\n"
           "and passing check, write docs/usage.md with a runnable example and empty\n"
           "input behavior. Verify the example against that accepted implementation.\n"
           "Allowed writes: docs/usage.md, reports/T02/, observations/T02/.\n"
           "T01 has no accepted delivery yet. Do not substitute the initial stub.\n\n"
           "Keep tests, planning files, and the other task's scope read-only. Return\n"
           "actual commands, exit codes and retrievable artifacts to Manager.\n")
    record(seed, PROGRESS, {"schema": 2, "kind": "progress", "plan_id": "P001",
                           "tasks": [{"id": task, "state": "planned", "owner": "unassigned",
                                      "next": "Manager to assign when inputs are ready", "check": None}
                                     for task in ("T01", "T02")], "integration_check": None},
           "# Manager progress\n\nNo task has been claimed or accepted.\n")
    record(seed, "plans/CURRENT.md", {"schema": 2, "kind": "current", "plan": PLAN,
                                      "progress": PROGRESS},
           "# Current\n\nThe selected plan for this local synthetic trial.\n")
    git(seed, "init", "--initial-branch=main")
    git(seed, "add", ".")
    git(seed, "commit", "-m", "Freeze synthetic task inputs")
    baseline = git(seed, "rev-parse", "HEAD")
    git(seed, "tag", "trial-baseline")
    inputs = git(seed, "ls-files").splitlines()
    write(seed, "LATER.md", "# Later unrelated work\n\nNot part of the dispatched baseline.\n")
    git(seed, "add", "LATER.md")
    git(seed, "commit", "-m", "Advance default branch after baseline selection")
    git(trial, "clone", "--bare", "--no-hardlinks", seed, trial / "origin.git")
    metadata = {"kind": "synthetic-issue-trial", "baseline": baseline,
                "default_head": git(seed, "rev-parse", "HEAD"), "ref": "refs/tags/trial-baseline",
                "plan": PLAN, "inputs": inputs}
    write(trial, "fixture.json", json.dumps(metadata, indent=2) + "\n")
    write(trial, "manager-input.md", "# User request\n\n"
          "Use the supplied Plan Strata skill to prepare two Issue bodies for the\n"
          "selected plan, one per task, so another agent can pick up the task later.\n"
          "The user opted into this local handoff batch. Write outbox/T01.md and\n"
          "outbox/T02.md instead of posting to GitHub. No worker has been chosen.\n"
          "Root is Manager and will confirm ownership, allocate an attempt and record\n"
          "it in authoritative progress before launching a worker. Return reports to\n"
          "root through this host session; preserve them in the worker workspace.\n\n"
          f"Project inspection copy: {seed}\n"
          f"Recipient-accessible Git source: {trial / 'origin.git'}\n"
          f"Selected source commit: {baseline}\n"
          f"Skill: {trial / 'skill'}\n"
          f"Workspace allocation: workers may create a clone and separate worktree\n"
          f"under {trial / 'worker-area'} after assignment. No worker directory exists.\n"
          "Author may inspect project/Git/skill and write only the two outbox files.\n"
          "Do not implement tasks, assign a worker, start agents, or change Git refs.\n")
    return trial


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True, help="new directory; existing paths are refused")
    args = parser.parse_args()
    try:
        print(prepare_trial(args.directory))
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
