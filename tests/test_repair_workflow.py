"""Scripted evidence transitions, not a scheduler or an agent-behavior evaluation."""

import runpy
import sys
import tempfile
import unittest
from pathlib import Path

from evals.prepare import CORE, PLAN, PROGRESS, check_record, observe, record, sha, write


REPO = Path(__file__).resolve().parents[1]
Validator = runpy.run_path(str(REPO / "skills/plan-strata/scripts/strata.py"))["Validator"]
SOURCE = "src/entry.py"
TEST = "tests/check_entry.py"
PARTIAL = ("def start(config):\n    return 'ready'\n\n"
           "def turn(config):\n    if not config.get('enabled'):\n"
           "        raise ValueError('disabled')\n    return 'ready'\n")
REPAIRED = ("def require_enabled(config):\n    if not config.get('enabled'):\n"
            "        raise ValueError('disabled')\n\n"
            "def start(config):\n    require_enabled(config)\n    return 'ready'\n\n"
            "def turn(config):\n    require_enabled(config)\n    return 'ready'\n")


class RepairWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="plan-strata-repair-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        record(self.root, CORE, {"schema": 1, "kind": "core", "revision": "v0.1.0"},
               "# Synthetic fixture\n\nLocal checks only; no external actions.\n")
        record(self.root, PLAN, {
            "schema": 1, "kind": "plan", "id": "P001", "revision": "v0.1.0",
            "core": CORE, "core_sha256": sha(self.root, CORE), "ready": True,
            "tasks": [{"id": "T01", "type": "development", "depends_on": []}],
            "integration_required": False,
        }, "# Entry validation\n\nT01: startup and turn entry both reject missing/false\n"
           "enabled configuration with ValueError; enabled inputs return ready.\n"
           "Acceptance: run tests/check_entry.py. Allow implementation/self-checks\n"
           "and up to two grouped review/repair rounds, at most four test runs.\n")
        record(self.root, "plans/CURRENT.md", {
            "schema": 1, "kind": "current", "plan": PLAN,
            "plan_sha256": sha(self.root, PLAN), "progress": PROGRESS,
        }, "# Current\n\nSelected synthetic task.\n")
        self.progress("in_progress")
        write(self.root, SOURCE, PARTIAL)
        write(self.root, TEST,
              "import sys\nfrom pathlib import Path\n"
              "sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))\n"
              "from entry import start, turn\n\n"
              "for entry in (start, turn):\n"
              "    assert entry({'enabled': True}) == 'ready'\n"
              "    for config in ({}, {'enabled': False}):\n"
              "        try:\n            entry(config)\n"
              "        except ValueError:\n            pass\n"
              "        else:\n            raise AssertionError(entry.__name__ + ' accepted disabled config')\n"
              "print('startup and turn enabled/disabled checks passed')\n")
        self.bound = self.snapshot([CORE, PLAN, "plans/CURRENT.md"])

    def snapshot(self, paths):
        return {path: (self.root / path).read_bytes() for path in paths}

    def progress(self, state, check=None):
        record(self.root, PROGRESS, {
            "schema": 1, "kind": "progress", "plan_id": "P001", "integration_check": None,
            "tasks": [{"id": "T01", "state": state, "owner": "fixture-manager",
                       "next": "Inspect the current result within the existing task budget",
                       "check": check, "plan": PLAN, "plan_sha256": sha(self.root, PLAN)}],
        }, "# Scripted fixture\n\nOne writer; no agents or background jobs.\n")

    def verify(self, name, expected_exit):
        log = f"observations/{name}.log"
        self.assertFalse((self.root / log).exists())
        self.assertEqual(observe(self.root, [sys.executable, "-B", TEST], log), expected_exit)
        return log

    def freeze(self, name, log, verdict):
        # Retain actual inspected bytes, not just their old hashes.
        inputs = [f"deliveries/{name}/{path}" for path in (SOURCE, TEST)]
        for path, retained in zip((SOURCE, TEST), inputs):
            write(self.root, retained, (self.root / path).read_text(encoding="utf-8"))
        path = f"plans/ex-plans/P001/check/T01-{name}.md"
        self.assertFalse((self.root / path).exists())
        check_record(self.root, path, "T01", [SOURCE, TEST], [log, *inputs], verdict)
        return path, self.snapshot([path, log, *inputs])

    def assert_accepted_without_replanning(self):
        result = Validator(self.root).validate()
        self.assertEqual((result["status"], result["overall"]), ("consistent", "verified"))
        self.assertEqual(result["tasks"][0]["id"], "T01")
        self.assertEqual(result["tasks"][0]["plan"], PLAN)
        self.assertEqual(self.snapshot(self.bound), self.bound)

    def test_internal_self_check_repair_needs_only_one_acceptance_check(self):
        failed = self.verify("self-check-fail", 1)
        failed_bytes = self.snapshot([failed])
        self.assertFalse((self.root / "plans/ex-plans/P001/check").exists())
        write(self.root, SOURCE, REPAIRED)
        passed = self.verify("self-check-pass", 0)
        check, _ = self.freeze("check-001", passed, "pass")
        self.progress("done", check)
        self.assert_accepted_without_replanning()
        self.assertEqual(self.snapshot(failed_bytes), failed_bytes)
        self.assertEqual(len(list((self.root / "plans/ex-plans/P001/check").glob("*.md"))), 1)

    def test_formal_failure_then_repair_keeps_frozen_failed_inputs_and_check(self):
        log = self.verify("delivery-001", 1)
        failed, history = self.freeze("check-001", log, "fail")
        self.progress("needs_review", failed)
        self.assertEqual(Validator(self.root).validate()["overall"], "open")
        self.progress("in_progress", failed)
        write(self.root, SOURCE, REPAIRED)
        log = self.verify("delivery-002", 0)
        passed, _ = self.freeze("check-002", log, "pass")
        self.progress("done", passed)
        self.assert_accepted_without_replanning()
        self.assertEqual(self.snapshot(history), history)

    def test_changed_passing_inputs_need_fresh_verification_and_check(self):
        write(self.root, SOURCE, REPAIRED)
        log = self.verify("delivery-001", 0)
        first, history = self.freeze("check-001", log, "pass")
        self.progress("done", first)
        self.assert_accepted_without_replanning()
        write(self.root, SOURCE, REPAIRED.replace("config.get('enabled')", "config.get('enabled', False)"))
        result = Validator(self.root).validate()
        self.assertEqual((result["status"], result["overall"]), ("invalid", "open"))
        self.assertEqual(result["tasks"][0]["effective_state"], "needs_review")
        self.assertIn("STALE_SUBJECTS", {error["code"] for error in result["errors"]})
        self.progress("needs_review", first)
        log = self.verify("delivery-002", 0)
        second, _ = self.freeze("check-002", log, "pass")
        self.progress("done", second)
        self.assert_accepted_without_replanning()
        self.assertEqual(self.snapshot(history), history)

    def test_exhausted_scripted_repair_budget_cannot_accept_remaining_failure(self):
        # This test chooses a finite schedule; the validator does not enforce budgets.
        history = {}
        for delivery in range(1, 4):  # Initial delivery plus two failed repair rounds.
            write(self.root, SOURCE, PARTIAL + f"\n# Incomplete repair {delivery - 1}\n")
            log = self.verify(f"delivery-{delivery:03}", 1)
            failed, frozen = self.freeze(f"check-{delivery:03}", log, "fail")
            history.update(frozen)
            self.progress("needs_review", failed)
        self.progress("blocked", failed)
        result = Validator(self.root).validate()
        self.assertEqual((result["status"], result["overall"]), ("consistent", "open"))
        self.progress("done", failed)
        result = Validator(self.root).validate()
        self.assertIn("CHECK_NOT_PASSING", {error["code"] for error in result["errors"]})
        self.assertEqual(result["overall"], "open")
        self.assertEqual(self.snapshot(history), history)
        self.assertEqual(self.snapshot(self.bound), self.bound)


if __name__ == "__main__":
    unittest.main()
