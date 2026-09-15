import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evals.prepare import CORE, PLAN, PROGRESS, check_record, make_case, read_record, record


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "skills/plan-strata/scripts/strata.py"
Validator = runpy.run_path(str(SCRIPT))["Validator"]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="plan-strata-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = make_case(Path(self.temp.name) / "project", "resume")

    def validate(self):
        return Validator(self.root).validate()

    def update(self, path, edit):
        data, body = read_record(self.root, path)
        edit(data)
        record(self.root, path, data, body)

    def select(self, path):
        self.update("plans/CURRENT.md", lambda d: d.update(plan=path))

    def codes(self, output):
        return {entry["code"] for entry in output["errors"]}

    def test_resume_selects_pointer_and_does_not_treat_consistency_as_completion(self):
        result = self.validate()
        self.assertEqual(result["status"], "consistent")
        self.assertEqual(result["overall"], "open")
        self.assertEqual(result["current_plan"], PLAN)

    def test_selected_draft_is_rejected(self):
        self.select("plans/ex-plans/P001/ex-plan-v0.2.0.md")
        self.assertIn("UNREADY_PLAN", self.codes(self.validate()))

    def test_plan_and_core_prose_changes_require_agent_review_not_automatic_detection(self):
        with (self.root / PLAN).open("a") as stream:
            stream.write("Changed acceptance.\n")
        with (self.root / CORE).open("a") as stream:
            stream.write("Changed scope.\n")
        result = self.validate()
        self.assertEqual(result["status"], "consistent")
        self.assertEqual(result["validation_scope"], "structure_only")

    def test_running_task_retains_old_binding_after_switch(self):
        self.root = make_case(Path(self.temp.name) / "switch", "switch")
        result = self.validate()
        self.assertEqual(result["status"], "consistent")
        self.assertEqual(result["tasks"][0]["plan"], PLAN)
        self.assertIn("OLDER_BASIS", {w["code"] for w in result["warnings"]})

    def test_old_acceptance_cannot_silently_carry_into_new_revision(self):
        new = "plans/ex-plans/P001/ex-plan-v0.2.0.md"
        self.update(new, lambda d: d.update(ready=True))
        self.select(new)
        self.assertIn("OLD_ACCEPTANCE", self.codes(self.validate()))

    def test_done_requires_check(self):
        self.update(PROGRESS, lambda d: d["tasks"][0].update(check=None))
        self.assertIn("MISSING_CHECK", self.codes(self.validate()))

    def test_changed_subject_needs_actual_test_and_explicit_reopening(self):
        self.root = make_case(Path(self.temp.name) / "stale", "stale")
        check = self.root / "plans/ex-plans/P001/check/T01-check-001.md"
        before = check.read_bytes()
        result = self.validate()
        self.assertEqual(result["status"], "consistent")
        self.assertEqual(result["tasks"][0]["effective_state"], "done")
        tested = subprocess.run([sys.executable, "-B", "tests/check_total.py"], cwd=self.root,
                                capture_output=True, text=True, check=False)
        self.assertNotEqual(tested.returncode, 0)
        self.update(PROGRESS, lambda d: d["tasks"][0].update(state="needs_review"))
        self.assertEqual(self.validate()["tasks"][0]["effective_state"], "needs_review")
        self.assertEqual(check.read_bytes(), before)

    def test_changed_evidence_contents_are_not_authenticated(self):
        (self.root / "observations/total.log").write_text("passed", encoding="utf-8")
        self.assertEqual(self.validate()["status"], "consistent")

    def test_missing_evidence_prevents_acceptance(self):
        (self.root / "observations/total.log").unlink()
        result = self.validate()
        self.assertIn("MISSING_FILE", self.codes(result))
        self.assertEqual(result["tasks"][0]["effective_state"], "needs_review")

    def test_validator_does_not_read_subject_or_evidence_contents(self):
        original = Path.open
        artifacts = {self.root / p for p in ("src/calc.py", "tests/check_total.py", "observations/total.log")}

        def record_only(path, *args, **kwargs):
            if path in artifacts:
                raise AssertionError(f"Artifact contents must not be read by structural validation: {path}")
            return original(path, *args, **kwargs)

        with patch.object(Path, "open", record_only):
            self.assertEqual(self.validate()["status"], "consistent")

    def test_legacy_and_mixed_schema_records_are_rejected_without_rewriting(self):
        for path in ("plans/CURRENT.md", PLAN, CORE, PROGRESS,
                     "plans/ex-plans/P001/check/T01-check-001.md"):
            with self.subTest(path=path):
                self.update(path, lambda d: d.update(schema=1))
                before = (self.root / path).read_bytes()
                result = self.validate()
                self.assertIn("UNSUPPORTED_SCHEMA", self.codes(result))
                self.assertEqual((self.root / path).read_bytes(), before)
                self.update(path, lambda d: d.update(schema=2))

    def test_renumbering_legacy_fields_does_not_silently_migrate_them(self):
        self.update(PLAN, lambda d: d.update(core_sha256="legacy"))
        self.assertIn("INVALID_RECORD", self.codes(self.validate()))

    def test_check_paths_are_nonempty_strings_not_legacy_digest_objects(self):
        path = "plans/ex-plans/P001/check/T01-check-001.md"
        for subjects in ([], [{"path": "src/calc.py", "sha256": "legacy"}],
                         ["src/calc.py", "src/calc.py"], [path]):
            with self.subTest(subjects=subjects):
                self.update(path, lambda d: d.update(subjects=subjects))
                self.assertIn("INVALID_RECORD", self.codes(self.validate()))

    def test_malformed_plan_paths_return_diagnostics_instead_of_tracebacks(self):
        for path in (None, [], {}, 7, "bad\u0000path"):
            with self.subTest(path=path):
                self.update("plans/CURRENT.md", lambda d: d.update(plan=path))
                result = self.cli("validate", "--project", str(self.root))
                self.assertEqual(result.returncode, 1)
                self.assertIn("INVALID_PATH", self.codes(json.loads(result.stdout)))
        self.select(PLAN)
        self.update(PROGRESS, lambda d: d["tasks"][0].update(plan=[]))
        result = self.cli("validate", "--project", str(self.root))
        self.assertEqual(result.returncode, 1)
        self.assertIn("INVALID_PATH", self.codes(json.loads(result.stdout)))

    def test_null_byte_in_subject_path_returns_diagnostic(self):
        self.update("plans/ex-plans/P001/check/T01-check-001.md",
                    lambda d: d.update(subjects=["bad\u0000path"]))
        result = self.cli("validate", "--project", str(self.root))
        self.assertEqual(result.returncode, 1)
        self.assertIn("INVALID_PATH", self.codes(json.loads(result.stdout)))

    def test_check_cannot_use_symlink_or_hardlink_to_itself_as_evidence(self):
        check = "plans/ex-plans/P001/check/T01-check-001.md"
        for link_type in ("symlink", "hardlink"):
            with self.subTest(link_type=link_type):
                alias = self.root / f"{link_type}.md"
                if link_type == "symlink":
                    alias.symlink_to(check)
                else:
                    alias.hardlink_to(self.root / check)
                self.update(check, lambda d: d.update(evidence=[alias.name]))
                result = self.validate()
                self.assertIn("INVALID_RECORD", self.codes(result))
                self.assertEqual(result["tasks"][0]["effective_state"], "needs_review")

    def test_unrelated_file_does_not_invalidate_a_scoped_check(self):
        (self.root / "unrelated.txt").write_text("notes", encoding="utf-8")
        self.assertEqual(self.validate()["status"], "consistent")

    def test_missing_evidence_on_open_task_is_a_warning(self):
        (self.root / "observations/total.log").unlink()
        self.update(PROGRESS, lambda d: d["tasks"][0].update(state="needs_review"))
        result = self.validate()
        self.assertEqual(result["status"], "consistent")
        self.assertIn("MISSING_FILE", {w["code"] for w in result["warnings"]})

    def test_local_success_with_failed_integration_stays_open(self):
        self.root = make_case(Path(self.temp.name) / "integration", "integration")
        result = self.validate()
        self.assertEqual(result["status"], "consistent")
        self.assertEqual(result["overall"], "open")
        self.assertTrue(all(t["state"] == "done" for t in result["tasks"]))

    def test_valid_negative_research_can_complete(self):
        self.root = make_case(Path(self.temp.name) / "research", "research")
        path = "plans/ex-plans/P001/check/T01-check-001.md"
        check_record(self.root, path, "T01", ["analysis.py", "results.csv"],
                     ["observations/analysis.log"], research={"mode": "exploratory",
                     "finding": "not_supported", "decision": "stop"})
        self.update(PROGRESS, lambda d: d["tasks"][0].update(state="done", check=path))
        self.assertEqual(self.validate()["overall"], "accepted")

    def test_research_check_requires_separate_interpretation(self):
        self.root = make_case(Path(self.temp.name) / "research", "research")
        path = "plans/ex-plans/P001/check/T01-check-001.md"
        check_record(self.root, path, "T01", ["results.csv"], ["observations/analysis.log"])
        self.update(PROGRESS, lambda d: d["tasks"][0].update(state="done", check=path))
        self.assertEqual(self.validate()["overall"], "open")
        self.assertTrue(self.validate()["errors"])

    def test_integration_is_reserved_and_cannot_bypass_research_acceptance(self):
        self.root = make_case(Path(self.temp.name) / "reserved", "research")
        self.update(PLAN, lambda d: d.update(
            tasks=[{"id": "integration", "type": "research", "depends_on": []}],
            integration_required=True))
        self.select(PLAN)
        path = "plans/ex-plans/P001/check/integration-check-001.md"
        check_record(self.root, path, "integration", ["analysis.py", "results.csv"],
                     ["observations/analysis.log"])
        self.update(PROGRESS, lambda d: d.update(
            tasks=[{"id": "integration", "state": "done", "owner": "root", "next": "Review",
                    "plan": PLAN, "check": path}],
            integration_check=path))
        result = self.validate()
        self.assertIn("RESERVED_TASK_ID", self.codes(result))
        self.assertEqual(result["overall"], "open")

    def test_integration_is_also_reserved_for_development_tasks(self):
        self.update(PLAN, lambda d: d["tasks"][0].update(id="integration"))
        self.select(PLAN)
        self.assertIn("RESERVED_TASK_ID", self.codes(self.validate()))

    def test_acceptance_propagates_through_dependencies(self):
        self.root = make_case(Path(self.temp.name) / "integration", "integration")
        self.update(PROGRESS, lambda d: d["tasks"][0].update(state="needs_review"))
        self.assertIn("OPEN_DEPENDENCY", self.codes(self.validate()))

    def test_dependency_cycle_is_rejected(self):
        self.update(PLAN, lambda d: d["tasks"][0].update(depends_on=["T02"]))
        self.select(PLAN)
        self.assertIn("DEPENDENCY_CYCLE", self.codes(self.validate()))

    def test_wrong_check_cannot_satisfy_another_task(self):
        self.root = make_case(Path(self.temp.name) / "integration", "integration")
        self.update(PROGRESS, lambda d: d["tasks"][1].update(check=d["tasks"][0]["check"]))
        self.assertIn("WRONG_CHECK_SCOPE", self.codes(self.validate()))

    def test_path_escape_and_external_symlink_are_rejected(self):
        self.update("plans/CURRENT.md", lambda d: d.update(plan="../outside.md"))
        self.assertIn("INVALID_PATH", self.codes(self.validate()))
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("outside", encoding="utf-8")
        (self.root / "link.md").symlink_to(outside)
        self.update("plans/CURRENT.md", lambda d: d.update(plan="link.md"))
        self.assertIn("INVALID_PATH", self.codes(self.validate()))

    def test_malformed_metadata_returns_a_diagnostic(self):
        (self.root / "plans/CURRENT.md").write_text("---\nplan: ordinary-yaml\n---\n", encoding="utf-8")
        self.assertIn("INVALID_RECORD", self.codes(self.validate()))

    def loop_path(self):
        path = self.root / "cycle.md"
        path.symlink_to("cycle.md")
        return path

    def cli(self, *args):
        result = subprocess.run([sys.executable, str(SCRIPT), *args],
                                capture_output=True, text=True, check=False)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def test_invalid_or_missing_current_is_a_validation_finding(self):
        for path, code in (("/plans/CURRENT.md", "INVALID_PATH"),
                           ("../CURRENT.md", "INVALID_PATH"),
                           ("", "INVALID_PATH"),
                           ("plans/absent.md", "MISSING_FILE"),
                           ("plans", "MISSING_FILE")):
            with self.subTest(path=path):
                result = self.cli("validate", "--project", str(self.root), "--current", path)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stderr, "")
                data = json.loads(result.stdout)
                self.assertEqual((data["status"], data["overall"]), ("invalid", "open"))
                self.assertIn(code, self.codes(data))

    def test_invalid_record_reference_is_also_a_validation_finding(self):
        for path, code in (("/plans/plan.md", "INVALID_PATH"),
                           ("plans/absent.md", "MISSING_FILE")):
            with self.subTest(path=path):
                self.update("plans/CURRENT.md", lambda d: d.update(plan=path))
                result = self.cli("validate", "--project", str(self.root))
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stderr, "")
                self.assertIn(code, self.codes(json.loads(result.stdout)))

    def test_project_initialization_failure_is_a_command_error(self):
        for project in (self.root / "absent", self.root / CORE):
            with self.subTest(project=project):
                result = self.cli("validate", "--project", str(project))
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertTrue(json.loads(result.stderr)["error"])

    def test_argument_errors_use_stderr_without_validation_json(self):
        for args in (("validate", "--current"), ("fingerprint",),
                     ("validate", "--unknown-flag")):
            with self.subTest(args=args):
                result = self.cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr)
                with self.assertRaises(json.JSONDecodeError):
                    json.loads(result.stderr)

    def test_zero_exit_with_warnings_does_not_mean_completion(self):
        self.root = make_case(Path(self.temp.name) / "open-integration", "integration")
        result = self.cli("validate", "--project", str(self.root))
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        data = json.loads(result.stdout)
        self.assertEqual((data["status"], data["overall"]), ("consistent", "open"))
        self.assertTrue(data["warnings"])

    def test_help_returns_text_without_running_validation(self):
        result = self.cli("validate", "--project", str(self.root / "absent"), "--help")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertTrue(result.stdout)
        with self.assertRaises(json.JSONDecodeError):
            json.loads(result.stdout)

    def test_looping_plan_reference_returns_json_diagnostic(self):
        self.loop_path()
        self.update("plans/CURRENT.md", lambda d: d.update(plan="cycle.md"))
        result = self.cli("validate", "--project", str(self.root))
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        self.assertEqual((data["status"], data["overall"]), ("invalid", "open"))
        self.assertTrue(data["errors"])

    def test_looping_check_subject_revokes_acceptance_with_json_diagnostic(self):
        self.loop_path()
        data, _ = read_record(self.root, PROGRESS)
        self.update(data["tasks"][0]["check"], lambda d: d.update(subjects=["cycle.md"]))
        result = self.cli("validate", "--project", str(self.root))
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        self.assertEqual((data["status"], data["overall"]), ("invalid", "open"))
        self.assertEqual(data["tasks"][0]["effective_state"], "needs_review")

    def test_looping_project_root_returns_json_error(self):
        result = self.cli("validate", "--project", str(self.loop_path()))
        self.assertEqual(result.returncode, 2)
        self.assertTrue(json.loads(result.stderr)["error"])

    def test_internal_symlink_can_still_reference_a_record(self):
        path = self.root / "core-link.md"
        path.symlink_to(CORE)
        self.update(PLAN, lambda d: d.update(core=path.name))
        result = self.cli("validate", "--project", str(self.root))
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["status"], "consistent")
        self.assertTrue(path.is_symlink())

    def test_validator_is_read_only_and_cli_returns_json(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = subprocess.run([sys.executable, str(SCRIPT), "validate", "--project", str(self.root)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["status"], "consistent")
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_fixture_preparation_refuses_overwrite(self):
        with self.assertRaises(FileExistsError):
            make_case(self.root, "resume")


if __name__ == "__main__":
    unittest.main()
