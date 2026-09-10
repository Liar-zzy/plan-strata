import json
import runpy
import sys
import tempfile
import unittest
from pathlib import Path

from evals.parallel_trial import REPO, collect_trial, collect_worker, files, finish_trial, prepare_trial
from evals.prepare import PLAN, PROGRESS, check_record, observe, read_record, record, write


Validator = runpy.run_path(str(REPO / "skills/plan-strata/scripts/strata.py"))["Validator"]


class ParallelTrialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="plan-strata-parallel-test-")
        self.addCleanup(self.temp.cleanup)
        self.trial = prepare_trial(Path(self.temp.name) / "trial")
        self.base, self.manager = self.trial / "baseline", self.trial / "manager"

    def finish_workers(self):
        # Deterministic fixture solutions, not an agent-behavior evaluation.
        for task, name, code in (
            ("T01", "normalize", "return [v.strip().lower() for v in values if v.strip()]"),
            ("T02", "render", "return ', '.join(values) if values else '(empty)'"),
        ):
            worker = self.trial / ("worker-" + task)
            write(worker, f"src/{name}.py", f"def {name}_labels(values):\n    {code}\n")
            write(worker, f"reports/{task}/A01.md", f"# {task}/A01\n\nSynthetic test delivery.\n")

    def test_prepared_trial_is_open_without_git_and_has_pinned_inputs(self):
        result = Validator(self.manager).validate()
        self.assertEqual((result["status"], result["overall"]), ("consistent", "open"))
        self.assertFalse((self.manager / ".git").exists())
        baseline = json.loads((self.base / "BASELINE.json").read_text())
        self.assertTrue(all((self.base / path).read_text() == content for path, content in baseline.items()))
        with self.assertRaises(FileExistsError):
            prepare_trial(self.trial)

    def test_collection_accepts_tasks_but_waits_for_real_integration(self):
        self.finish_workers()
        self.assertTrue(collect_trial(self.trial)["workers_accepted"])
        result = Validator(self.manager).validate()
        self.assertTrue(all(row["state"] == "done" for row in result["tasks"]))
        self.assertEqual(result["overall"], "open")

    def test_unchanged_collection_is_a_no_op(self):
        self.finish_workers()
        first = collect_trial(self.trial)
        before = files(self.trial)
        self.assertEqual(collect_trial(self.trial), first)
        self.assertEqual(files(self.trial), before)

    def test_changed_attempt_is_rejected_before_writing(self):
        self.finish_workers()
        collect_trial(self.trial)
        before = files(self.manager)
        write(self.trial / "worker-T01", "reports/T01/late.md", "New result under old identity\n")
        with self.assertRaises(ValueError):
            collect_trial(self.trial)
        self.assertEqual(files(self.manager), before)

    def test_forbidden_plan_or_shared_file_write_stops_collection(self):
        self.finish_workers()
        before = files(self.manager)
        write(self.trial / "worker-T02", PLAN, "Changed plan\n")
        with self.assertRaises(ValueError):
            collect_trial(self.trial)
        self.assertEqual(files(self.manager), before)

    def test_worker_cannot_replace_manager_progress(self):
        self.finish_workers()
        write(self.trial / "worker-T01", PROGRESS, "Everything done\n")
        with self.assertRaises(ValueError):
            collect_trial(self.trial)

    def test_stale_destination_is_not_overwritten(self):
        self.finish_workers()
        write(self.manager, "src/normalize.py", "# Manager changed this input\n")
        before = files(self.manager)
        with self.assertRaises(ValueError):
            collect_worker(self.base, self.trial / "worker-T01", self.manager, "T01")
        self.assertEqual(files(self.manager), before)

    def test_collection_rejects_weakened_manager_test_before_any_write(self):
        self.finish_workers()
        worker = self.trial / "worker-T01"
        write(worker, "src/normalize.py", "def normalize_labels(values):\n    return []\n")
        self.assertNotEqual(observe(worker, [sys.executable, "-m", "unittest", "discover",
                                            "-s", "tests", "-p", "test_normalize.py", "-v"],
                                    "observations/T01/original-test.log"), 0)
        write(self.manager, "tests/test_normalize.py", "import unittest\n"
              "from src.normalize import normalize_labels\n\nclass Checks(unittest.TestCase):\n"
              "    def test_returns_list(self):\n"
              "        self.assertIsInstance(normalize_labels(['Alpha']), list)\n")
        before = files(self.trial)
        with self.assertRaisesRegex(ValueError, "Manager.*baseline"):
            collect_trial(self.trial)
        self.assertEqual(files(self.trial), before)

    def change_manager_input(self, mutation):
        if mutation == "add":
            write(self.manager, "src/__init__.py", "# New import-time input\n")
        elif mutation == "delete":
            (self.manager / "tests/test_integration.py").unlink()
        else:
            write(self.manager, "src/pipeline.py", "def summarize_labels(values):\n    return 'wrong'\n")

    def test_initial_collection_rejects_added_deleted_or_changed_manager_inputs(self):
        for mutation in ("add", "delete", "modify"):
            with self.subTest(mutation=mutation):
                self.setUp()
                self.finish_workers()
                self.change_manager_input(mutation)
                before = files(self.trial)
                with self.assertRaisesRegex(ValueError, "Manager.*baseline"):
                    collect_trial(self.trial)
                self.assertEqual(files(self.trial), before)

    def test_repeated_collection_rechecks_manager_inputs(self):
        self.finish_workers()
        collect_trial(self.trial)
        self.change_manager_input("modify")
        before = files(self.trial)
        with self.assertRaisesRegex(ValueError, "Manager.*baseline"):
            collect_trial(self.trial)
        self.assertEqual(files(self.trial), before)

    def update_manager_next(self):
        data, body = read_record(self.manager, PROGRESS)
        data["tasks"][0]["next"] = "Manager will review the retained results"
        record(self.manager, PROGRESS, data, body + "\nManager handoff note.\n")

    def test_manager_can_update_next_action_and_prose_without_changing_binding(self):
        self.finish_workers()
        self.update_manager_next()
        first = collect_trial(self.trial)
        self.update_manager_next()
        before = files(self.trial)
        self.assertEqual(collect_trial(self.trial), first)
        self.assertEqual(files(self.trial), before)

    def test_manager_progress_binding_is_not_a_blanket_baseline_exception(self):
        self.finish_workers()
        data, body = read_record(self.manager, PROGRESS)
        data["tasks"][0]["plan"] = "plans/ex-plans/P001/ex-plan-v0.2.0.md"
        record(self.manager, PROGRESS, data, body)
        before = files(self.trial)
        with self.assertRaisesRegex(ValueError, "Manager.*baseline"):
            collect_trial(self.trial)
        self.assertEqual(files(self.trial), before)

    def test_malformed_manager_progress_is_rejected_before_collection(self):
        self.finish_workers()
        write(self.manager, PROGRESS, "Invalid prefix\n" + (self.manager / PROGRESS).read_text())
        before = files(self.trial)
        with self.assertRaisesRegex(ValueError, "Manager.*baseline"):
            collect_trial(self.trial)
        self.assertEqual(files(self.trial), before)

    def test_legacy_collection_without_receiver_checkpoint_requires_new_trial(self):
        self.finish_workers()
        collect_trial(self.trial)
        receipt = json.loads((self.trial / "collection.json").read_text())
        del receipt["manager"]
        write(self.trial, "collection.json", json.dumps(receipt))
        before = files(self.trial)
        with self.assertRaisesRegex(ValueError, "Manager baseline checkpoint missing"):
            collect_trial(self.trial)
        self.assertEqual(files(self.trial), before)

    def test_deleted_or_symlinked_worker_input_is_rejected(self):
        self.finish_workers()
        worker = self.trial / "worker-T01"
        (worker / "src/normalize.py").unlink()
        with self.assertRaises(ValueError):
            collect_trial(self.trial)
        (worker / "src/normalize.py").symlink_to(self.base / "src/normalize.py")
        with self.assertRaises(ValueError):
            collect_trial(self.trial)

    def test_missing_report_cannot_be_collected(self):
        with self.assertRaises(ValueError):
            collect_trial(self.trial)

    def test_failed_worker_is_retained_without_starting_integration(self):
        self.finish_workers()
        write(self.trial / "worker-T01", "src/normalize.py", "def normalize_labels(values):\n    return []\n")
        self.assertFalse(collect_trial(self.trial)["workers_accepted"])
        self.assertFalse((self.trial / "integration").exists())
        result = Validator(self.manager).validate()
        self.assertEqual((result["status"], result["overall"]), ("consistent", "open"))
        self.assertEqual(result["tasks"][0]["state"], "needs_review")

    def test_integration_failure_then_fresh_pass_preserves_history(self):
        self.finish_workers()
        collect_trial(self.trial)
        root = self.trial / "integration"
        write(root, "src/pipeline.py", "def summarize_labels(values):\n    return 'wrong'\n")
        command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
        self.assertNotEqual(observe(root, command, "observations/fail.log"), 0)
        failed = "plans/ex-plans/P001/check/integration-check-001.md"
        subjects = ["src/normalize.py", "src/render.py", "src/pipeline.py", "tests/test_integration.py"]
        check_record(root, failed, "integration", subjects, ["observations/fail.log"], "fail")
        data, body = read_record(root, PROGRESS)
        data["integration_check"] = failed
        record(root, PROGRESS, data, body)
        old = (root / failed).read_bytes()
        self.assertEqual(Validator(root).validate()["overall"], "open")
        # A separately authorized synthetic repair, not an integrator changing scope.
        write(root, "src/pipeline.py", (self.base / "src/pipeline.py").read_text())
        self.assertEqual(observe(root, command, "observations/pass.log"), 0)
        passed = "plans/ex-plans/P001/check/integration-check-002.md"
        check_record(root, passed, "integration", subjects, ["observations/pass.log"])
        data["integration_check"] = passed
        record(root, PROGRESS, data, body)
        self.assertEqual(Validator(root).validate()["overall"], "accepted")
        self.assertEqual((root / failed).read_bytes(), old)
        write(root, "src/render.py", "def render_labels(values):\n    return 'changed'\n")
        self.assertEqual(Validator(root).validate()["overall"], "accepted")
        self.assertNotEqual(observe(root, command, "observations/changed.log"), 0)
        data["integration_check"] = None  # Manager explicitly reopens affected acceptance.
        record(root, PROGRESS, data, body + "\nRelevant input changed; integration requires review.\n")
        self.assertEqual(Validator(root).validate()["overall"], "open")

    def propose_integration(self, verdict="pass"):
        self.finish_workers()
        collect_trial(self.trial)
        root = self.trial / "integration"
        log = "observations/integration/A01.log"
        self.assertEqual(observe(root, [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], log), 0)
        write(root, "reports/integration/A01.md", "# Synthetic integration review\n")
        check_record(root, "plans/ex-plans/P001/check/integration-check-001.md", "integration",
                     [p for p in json.loads((root / "INTEGRATION-INPUTS.json").read_text()) if p != PROGRESS]
                     + ["INTEGRATION-INPUTS.json"],
                     [log, "reports/integration/A01.md"], verdict)
        return root

    def test_finish_rejects_added_deleted_or_changed_manager_inputs_before_any_write(self):
        for mutation in ("add", "delete", "modify"):
            with self.subTest(mutation=mutation):
                self.setUp()
                root = self.propose_integration()
                # Reproduce an integrator whose declared subjects omit the pipeline.
                check_record(root, "plans/ex-plans/P001/check/integration-check-001.md", "integration",
                             ["src/normalize.py", "src/render.py", "CONTRACT.md"],
                             ["observations/integration/A01.log", "reports/integration/A01.md"])
                self.change_manager_input(mutation)
                before = files(self.trial)
                with self.assertRaisesRegex(ValueError, "Manager.*baseline"):
                    finish_trial(self.trial)
                self.assertEqual(files(self.trial), before)

    def test_finish_rejects_incomplete_input_coverage_even_when_manager_is_unchanged(self):
        root = self.propose_integration()
        path = "plans/ex-plans/P001/check/integration-check-001.md"
        data, body = read_record(root, path)
        data["subjects"] = [path for path in data["subjects"] if path != "src/pipeline.py"]
        record(root, path, data, body)
        before = files(self.trial)
        with self.assertRaisesRegex(ValueError, "input.*coverage"):
            finish_trial(self.trial)
        self.assertEqual(files(self.trial), before)

    def test_input_manifest_excludes_live_progress_but_not_frozen_inputs(self):
        root = self.propose_integration()
        inputs = json.loads((root / "INTEGRATION-INPUTS.json").read_text())
        self.assertNotIn(PROGRESS, inputs)
        self.assertIn("tests/test_normalize.py", inputs)
        self.assertIn("src/pipeline.py", inputs)

    def test_final_acceptance_checks_manifest_members_and_allows_progress_notes(self):
        self.propose_integration()
        self.update_manager_next()
        self.assertEqual(finish_trial(self.trial)["overall"], "accepted")
        self.update_manager_next()
        before = files(self.trial)
        self.assertEqual(finish_trial(self.trial)["overall"], "accepted")
        self.assertEqual(files(self.trial), before)
        collect_trial(self.trial)
        self.assertEqual(files(self.trial), before)
        self.change_manager_input("modify")
        result = Validator(self.manager).validate()
        self.assertEqual(result["overall"], "accepted")
        self.assertEqual(result["validation_scope"], "structure_only")
        # Fixture-only retained-text comparison catches this; the installed helper cannot.
        before = files(self.trial)
        with self.assertRaisesRegex(ValueError, "Manager.*baseline"):
            finish_trial(self.trial)
        self.assertEqual(files(self.trial), before)

    def test_finish_detects_drift_with_complete_proposal_coverage(self):
        self.propose_integration()
        self.change_manager_input("modify")
        before = files(self.trial)
        with self.assertRaisesRegex(ValueError, "Manager.*baseline"):
            finish_trial(self.trial)
        self.assertEqual(files(self.trial), before)

    def test_manager_finishes_once_without_replacing_progress_from_integrator(self):
        root = self.propose_integration()
        before = (root / PROGRESS).read_bytes()
        self.assertEqual(finish_trial(self.trial)["overall"], "accepted")
        snapshot = files(self.trial)
        self.assertEqual(finish_trial(self.trial)["overall"], "accepted")
        self.assertEqual(files(self.trial), snapshot)
        self.assertEqual((root / PROGRESS).read_bytes(), before)

    def test_failed_terminal_verdict_is_retained_and_stays_open(self):
        # Passing commands need not imply that a review accepted the whole delivery.
        self.propose_integration("fail")
        result = finish_trial(self.trial)
        self.assertEqual((result["status"], result["overall"]), ("consistent", "open"))
        self.assertTrue((self.manager / "plans/ex-plans/P001/check/integration-check-001.md").exists())

    def test_integrator_source_repair_is_outside_read_only_review_scope(self):
        root = self.propose_integration()
        before = files(self.manager)
        write(root, "src/pipeline.py", "# Unapproved repair\n")
        with self.assertRaises(ValueError):
            finish_trial(self.trial)
        self.assertEqual(files(self.manager), before)

    def test_missing_passing_terminal_evidence_is_rejected(self):
        root = self.propose_integration()
        (root / "observations/integration/A01.log").unlink()
        with self.assertRaises(ValueError):
            finish_trial(self.trial)

    def test_changed_log_contents_require_review_not_structural_authentication(self):
        root = self.propose_integration()
        write(root, "observations/integration/A01.log", "Changed after check\n")
        result = finish_trial(self.trial)
        self.assertEqual((result["overall"], result["validation_scope"]), ("accepted", "structure_only"))


if __name__ == "__main__":
    unittest.main()
