#!/usr/bin/env python3
"""Prepare/collect one synthetic local handoff trial; never launches agents."""

import argparse
import json
import runpy
import shutil
import sys
from pathlib import Path

from evals.prepare import CORE, PLAN, PROGRESS, check_record, observe, read_record, record, sha, write


REPO = Path(__file__).resolve().parents[1]
TASKS = {"T01": "normalize", "T02": "render"}


def files(root):
    result = {}
    for path in sorted(root.rglob("*")):
        if "__pycache__" in path.parts:
            continue
        if path.is_symlink():
            raise ValueError(f"Symlink outside the trial contract: {path}")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = sha(root, path.relative_to(root))
    return result


def manager_snapshot(root):
    """Fixture checkpoint; only next-action text and progress prose may drift."""
    inputs = files(root)
    inputs.pop(PROGRESS, None)
    try:
        validator_class = runpy.run_path(str(REPO / "skills/plan-strata/scripts/strata.py"))["Validator"]
        progress = validator_class(root).record(PROGRESS, "progress")
        for row in progress["tasks"]:
            if not isinstance(row["next"], str) or not row["next"].strip():
                raise ValueError("Next action must remain nonempty")
            del row["next"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ValueError("Manager progress baseline is missing or malformed") from exc
    return {"inputs": inputs, "progress": progress}


def verify_manager(expected, manager):
    if expected is None:
        raise ValueError("Manager baseline checkpoint missing; preserve this legacy trial and prepare a new one")
    if manager_snapshot(manager) != expected:
        raise ValueError("Manager baseline changed; preserve this trial and review the receiving inputs/progress")


def packet(skill, template, values):
    text = (skill / "assets" / template).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    if "{{" in text:
        raise ValueError(f"Unfilled packet: {template}")
    return text


def prepare_trial(destination):
    trial = Path(destination).resolve()
    trial.mkdir(parents=True, exist_ok=False)
    skill = trial / "skill"
    shutil.copytree(REPO / "skills/plan-strata", skill,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    base = trial / "baseline"
    base.mkdir()
    write(base, "SCENARIO.md", "# Synthetic parallel trial\n\n"
          "A tiny label formatter, not a production project or scientific result.\n"
          "The user authorized two isolated local workers and a final integrator.\n"
          "No Git, network, package installation, nested agents, or paid jobs are needed.\n")
    write(base, "CONTRACT.md", "# Frozen interface\n\n"
          "normalize_labels(values) returns a new list of stripped, lowercase, nonempty\n"
          "strings, preserving order and duplicates. Input contains strings only.\n"
          "render_labels(values) joins the supplied strings with ', ', or returns\n"
          "'(empty)' for empty input. It does not normalize or sort.\n"
          "summarize_labels(values) composes normalization then rendering.\n"
          "Use Python standard library only. Tests and this interface are read-only.\n")
    write(base, "src/normalize.py", "def normalize_labels(values):\n    raise NotImplementedError\n")
    write(base, "src/render.py", "def render_labels(values):\n    raise NotImplementedError\n")
    write(base, "src/pipeline.py", "from src.normalize import normalize_labels\n"
          "from src.render import render_labels\n\n"
          "def summarize_labels(values):\n    return render_labels(normalize_labels(values))\n")
    for name, imports, assertions in (
        ("normalize", "from src.normalize import normalize_labels",
         "values = [' A ', '', '  ', 'B', ' A ']\n"
         "        self.assertEqual(normalize_labels(values), ['a', 'b', 'a'])\n"
         "        self.assertEqual(values, [' A ', '', '  ', 'B', ' A '])\n"
         "        self.assertEqual(normalize_labels([]), [])"),
        ("render", "from src.render import render_labels",
         "self.assertEqual(render_labels([' A ', 'B', 'B']), ' A , B, B')\n"
         "        self.assertEqual(render_labels([]), '(empty)')"),
        ("integration", "from src.pipeline import summarize_labels",
         "self.assertEqual(summarize_labels([' Alpha ', '', 'BETA']), 'alpha, beta')\n"
         "        self.assertEqual(summarize_labels([' ', '']), '(empty)')"),
    ):
        write(base, f"tests/test_{name}.py", f"import unittest\n{imports}\n\n"
              f"class Checks(unittest.TestCase):\n    def test_contract(self):\n        {assertions}\n")
    record(base, CORE, {"schema": 1, "kind": "core", "revision": "v0.1.0"},
           "# Local handoff trial\n\nDeliver the frozen label formatter contract.\n"
           "Two isolated workers, one terminal integrator, no external effects.\n")
    record(base, PLAN, {"schema": 1, "kind": "plan", "id": "P001", "revision": "v0.1.0",
                       "core": CORE, "core_sha256": sha(base, CORE), "ready": True,
                       "tasks": [{"id": t, "type": "development", "depends_on": []} for t in TASKS],
                       "integration_required": True},
           "# Parallel label formatter\n\n"
           "## T01\nImplement src/normalize.py against CONTRACT.md. Verify with\n"
           "python3 -m unittest discover -s tests -p test_normalize.py -v.\n\n"
           "## T02\nImplement src/render.py against CONTRACT.md. Verify with\n"
           "python3 -m unittest discover -s tests -p test_render.py -v.\n\n"
           "Workers share read-only inputs but have distinct write scopes and no dependencies.\n"
           "Manager alone updates progress; workers return reports and real logs.\n\n"
           "## Integration\nAfter Manager accepts both task deliveries, combine the exact\n"
           "files in an isolated directory and run python3 -m unittest discover -s tests -v.\n"
           "Integrator may only add its report, log, and proposed integration check.\n"
           "A failure goes back to Manager; no source repair or external merge is authorized.\n")
    record(base, PROGRESS, {"schema": 1, "kind": "progress", "plan_id": "P001",
                           "tasks": [{"id": t, "state": "in_progress", "owner": f"worker-{t}",
                                      "next": f"Return reports/{t}/A01.md for Manager review", "check": None,
                                      "plan": PLAN, "plan_sha256": sha(base, PLAN)} for t in TASKS],
                           "integration_check": None},
           "# Manager handoff\n\nAuthorized batch: T01 and T02, one local attempt A01 each.\n"
           "Dispatch receipts: T01/A01 -> handoffs/T01-A01.md, worker-T01/;\n"
           "T02/A01 -> handoffs/T02-A01.md, worker-T02/. No background jobs yet.\n"
           "These workspace names are relative to the trial directory. Manager owns progress.\n")
    record(base, "plans/CURRENT.md", {"schema": 1, "kind": "current", "plan": PLAN,
                                      "plan_sha256": sha(base, PLAN), "progress": PROGRESS},
           "# Current\n\nSelected local trial.\n")
    for task, name in TASKS.items():
        write(base, f"handoffs/{task}-A01.md", packet(skill, "task-handoff.md", {
            "task_key": f"label-trial/P001/{task}", "attempt": "A01", "worker": f"worker-{task}",
            "project": f"label-trial at {trial / ('worker-' + task)}", "plan": PLAN,
            "plan_sha256": sha(base, PLAN), "baseline": "BASELINE.json pins the initial files; verify before writing",
            "skill": f"{skill} (0.1.0-alpha.2 snapshot)", "manager": f"root; {trial / 'manager' / PROGRESS}",
            "context": f"SCENARIO.md, CONTRACT.md, {CORE}, {PLAN} section {task}; relevant source and tests",
            "objective": f"Implement {name}_labels in src/{name}.py to satisfy the frozen contract.",
            "dependencies": "None; shared contract and tests are frozen and supplied",
            "write_scope": f"src/{name}.py, reports/{task}/, observations/{task}/ only",
            "constraints": "Read-only tests, other worker's source, and planning files; no shared mutable services",
            "acceptance": f"python3 -m unittest discover -s tests -p test_{name}.py -v; preserve actual output",
            "budget": "One task/attempt, at most 3 task-test runs; no nested agents, network, installs, or other effects; report blocks",
            "report": f"reports/{task}/A01.md",
        }))
    write(base, "BASELINE.json", json.dumps(files(base), indent=2) + "\n")
    for name in ("manager", "worker-T01", "worker-T02"):
        shutil.copytree(base, trial / name)
    return trial


def collect_artifacts(original, source, destination, allowed, required, *, apply=True):
    """Preflight the entire declared diff before applying an allowlisted copy."""
    result = files(source)
    if original.keys() - result.keys():
        raise ValueError("Worker deleted baseline files")
    changed = {p: h for p, h in result.items() if original.get(p) != h}
    if any(not allowed(p) for p in changed):
        raise ValueError("Worker changed a path outside its assignment")
    if not set(required).issubset(changed):
        raise ValueError("Worker report is missing")
    pending = []
    for path, fingerprint in changed.items():
        target = destination / path
        if target.is_symlink() or not target.resolve().is_relative_to(destination.resolve()):
            raise ValueError("Unsafe collection destination")
        existing = sha(destination, path) if target.is_file() else None
        if existing == fingerprint:
            continue
        if existing != original.get(path):
            raise ValueError("Conflicting result: preserve the old attempt and investigate")
        pending.append(path)
    if apply:
        for path in pending:
            write(destination, path, (source / path).read_text(encoding="utf-8"))
    return {"artifacts": changed, "copied": pending}


def collect_worker(base, worker, destination, task, *, apply=True):
    """Fixture-only allowlist collection; a repeat is a no-op, a changed attempt fails."""
    return collect_artifacts(files(base), worker, destination,
                             lambda p: p == f"src/{TASKS[task]}.py" or
                             p.startswith((f"reports/{task}/", f"observations/{task}/")),
                             [f"reports/{task}/A01.md"], apply=apply)


def collect_trial(trial):
    trial = Path(trial).resolve()
    base, manager = trial / "baseline", trial / "manager"
    receipt_path = trial / "collection.json"
    previous = None
    if receipt_path.exists():
        previous = json.loads(receipt_path.read_text(encoding="utf-8"))
        terminal = trial / "integration-collection.json"
        checkpoint = json.loads(terminal.read_text(encoding="utf-8")) if terminal.exists() else previous
        verify_manager(checkpoint.get("manager"), manager)
    else:
        verify_manager(manager_snapshot(base), manager)
    receipts = [collect_worker(base, trial / ("worker-" + task), manager, task, apply=False) for task in TASKS]
    if previous is not None:
        if any(r["copied"] for r in receipts) or [r["artifacts"] for r in receipts] != previous["artifacts"]:
            raise ValueError("Collection changed; preserve this trial and investigate")
        return previous
    if (manager / "plans/ex-plans/P001/check").exists() or (trial / "integration").exists():
        raise ValueError("Interrupted collection: inspect retained artifacts before retrying")
    for task in TASKS:
        collect_worker(base, trial / ("worker-" + task), manager, task)
    progress, body = read_record(manager, PROGRESS)
    for row in progress["tasks"]:
        task, name = row["id"], TASKS[row["id"]]
        log, check = f"observations/manager-{task}.log", f"plans/ex-plans/P001/check/{task}-check-001.md"
        code = observe(manager, [sys.executable, "-m", "unittest", "discover", "-s", "tests",
                                 "-p", f"test_{name}.py", "-v"], log)
        check_record(manager, check, task, [f"src/{name}.py", f"tests/test_{name}.py", "CONTRACT.md"],
                     [log, f"reports/{task}/A01.md"], "pass" if code == 0 else "fail")
        row.update(state="done" if code == 0 else "needs_review", check=check,
                   next="Await final integration" if code == 0 else "Manager must review failed task")
    record(manager, PROGRESS, progress, body + "\n\nCollection reviewed by the local fixture driver.\n")
    accepted = all(row["state"] == "done" for row in progress["tasks"])
    if accepted:
        integration = trial / "integration"
        shutil.copytree(manager, integration)
        write(integration, "INTEGRATION-INPUTS.json", json.dumps(
            {p: h for p, h in files(integration).items() if p != PROGRESS}, indent=2) + "\n")
        write(integration, "handoffs/integration-A01.md", packet(trial / "skill", "integration-handoff.md", {
            "plan_id": "P001", "attempt": "A01", "project": integration, "plan": PLAN,
            "plan_sha256": sha(manager, PLAN), "skill": f"{trial / 'skill'} (0.1.0-alpha.2 snapshot)",
            "manager": f"root; {manager / PROGRESS}",
            "deliveries": "T01/A01 and T02/A01; task checks in plans/ex-plans/P001/check/; hashes in INTEGRATION-INPUTS.json",
            "baseline": "INTEGRATION-INPUTS.json pins the collected files; verify before checking",
            "context": f"SCENARIO.md, CONTRACT.md, {CORE}, {PLAN}, worker reports and task checks",
            "write_scope": "Files already combined by allowlisted copy. Only reports/integration/A01.md, observations/integration/, and plans/ex-plans/P001/check/integration-check-001.md may be added",
            "acceptance": "Inspect both deliveries and run python3 -m unittest discover -s tests -v on this directory. "
                          "The proposed check subjects must include INTEGRATION-INPUTS.json and every file listed in it, "
                          "with their current hashes. The driver requires this explicit input coverage; live progress is excluded",
            "budget": "At most 2 full-suite runs; no source fixes, progress edits, nested agents, network, installs, or merges; return failure to Manager",
            "report": "reports/integration/A01.md",
        }))
        for context in ("INTEGRATION-INPUTS.json", "handoffs/integration-A01.md"):
            write(manager, context, (integration / context).read_text(encoding="utf-8"))
        write(trial, "integration-baseline.json", json.dumps(files(integration), indent=2) + "\n")
    result = {"kind": "synthetic-local-collection", "artifacts": [r["artifacts"] for r in receipts],
              "manager": manager_snapshot(manager),
              "workers_accepted": accepted, "integration_prepared": accepted,
              "limits": "Fixture driver validates declared file scopes and runs task tests, not report semantics or agent scheduling."}
    write(trial, "collection.json", json.dumps(result, indent=2) + "\n")
    return result


def finish_trial(trial):
    """Manager-side collection after reviewing the integrator's real report."""
    trial = Path(trial).resolve()
    integration, manager = trial / "integration", trial / "manager"
    baseline = json.loads((trial / "integration-baseline.json").read_text(encoding="utf-8"))
    receipt = trial / "integration-collection.json"
    previous = json.loads(receipt.read_text(encoding="utf-8")) if receipt.exists() else None
    checkpoint = previous if previous is not None else json.loads(
        (trial / "collection.json").read_text(encoding="utf-8"))
    verify_manager(checkpoint.get("manager"), manager)
    check = "plans/ex-plans/P001/check/integration-check-001.md"
    report = "reports/integration/A01.md"
    allowed = lambda p: p in {check, report} or p.startswith("observations/integration/")
    incoming = collect_artifacts(baseline, integration, manager, allowed, [check, report], apply=False)
    if previous is not None and previous["artifacts"] != incoming["artifacts"]:
        raise ValueError("Integrator changed an already collected attempt")
    validator_class = runpy.run_path(str(trial / "skill/scripts/strata.py"))["Validator"]
    validator = validator_class(integration)
    if validator.validate()["errors"]:
        raise ValueError("Integration input records need review")
    validator.check(check, "integration", PLAN, sha(manager, PLAN), False)
    proposed, _ = read_record(integration, check)
    inputs = json.loads((integration / "INTEGRATION-INPUTS.json").read_text(encoding="utf-8"))
    covered = {item["path"] for item in proposed["subjects"]}
    if not (set(inputs) | {"INTEGRATION-INPUTS.json"}).issubset(covered):
        raise ValueError("Integration input coverage is incomplete; list the manifest and every member as subjects")
    if proposed["verdict"] == "pass" and (validator.errors or any(
            w["code"].startswith("STALE_") or w["code"] in {"MISSING_FILE", "INVALID_PATH"}
            for w in validator.warnings)):
        raise ValueError("Passing integration proposal has stale or missing evidence")
    collect_artifacts(baseline, integration, manager, allowed, [check, report])
    data, body = read_record(manager, PROGRESS)
    if data["integration_check"] != check:
        data["integration_check"] = check
        for row in data["tasks"]:
            row["next"] = ("Task accepted; Manager reviews final delivery" if proposed["verdict"] == "pass"
                           else "Task accepted; Manager addresses the open integration verdict")
        record(manager, PROGRESS, data, body + "\n\nManager collected the terminal review; inspect overall separately.\n")
    if not receipt.exists():
        write(trial, receipt.name, json.dumps(
            {"artifacts": incoming["artifacts"], "manager": manager_snapshot(manager)}, indent=2) + "\n")
    return validator_class(manager).validate()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "collect", "finish"))
    parser.add_argument("--directory", required=True, help="new trial directory for prepare; existing trial for collect")
    args = parser.parse_args()
    try:
        result = {"prepare": prepare_trial, "collect": collect_trial, "finish": finish_trial}[args.action](args.directory)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print(json.dumps(result, indent=2) if isinstance(result, dict) else str(result))
    if args.action == "finish":
        return 0 if result["overall"] == "verified" else 1
    return 1 if isinstance(result, dict) and not result["workers_accepted"] else 0


if __name__ == "__main__":
    sys.exit(main())
