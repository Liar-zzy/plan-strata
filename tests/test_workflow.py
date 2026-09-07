import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from evals.prepare import CORE, PLAN, PROGRESS, check_record, make_case, read_record, record, sha


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
        self.update("plans/CURRENT.md", lambda d: d.update(plan=path, plan_sha256=sha(self.root, path)))

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

    def test_changed_plan_and_core_are_detected(self):
        with (self.root / PLAN).open("a") as stream:
            stream.write("Changed acceptance.\n")
        self.assertIn("PLAN_CHANGED", self.codes(self.validate()))
        self.select(PLAN)
        with (self.root / CORE).open("a") as stream:
            stream.write("Changed scope.\n")
        self.assertIn("CORE_CHANGED", self.codes(self.validate()))

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

    def test_changed_subject_revokes_current_acceptance_without_rewriting_history(self):
        self.root = make_case(Path(self.temp.name) / "stale", "stale")
        check = self.root / "plans/ex-plans/P001/check/T01-check-001.md"
        before = check.read_bytes()
        result = self.validate()
        self.assertIn("STALE_SUBJECTS", self.codes(result))
        self.assertEqual(result["tasks"][0]["effective_state"], "needs_review")
        self.assertEqual(check.read_bytes(), before)

    def test_changed_evidence_is_detected(self):
        (self.root / "observations/total.log").write_text("passed", encoding="utf-8")
        self.assertIn("STALE_EVIDENCE", self.codes(self.validate()))

    def test_unrelated_file_does_not_invalidate_a_scoped_check(self):
        (self.root / "unrelated.txt").write_text("notes", encoding="utf-8")
        self.assertEqual(self.validate()["status"], "consistent")

    def test_stale_check_on_open_task_is_a_warning(self):
        self.root = make_case(Path(self.temp.name) / "stale", "stale")
        self.update(PROGRESS, lambda d: d["tasks"][0].update(state="needs_review"))
        result = self.validate()
        self.assertEqual(result["status"], "consistent")
        self.assertIn("STALE_SUBJECTS", {w["code"] for w in result["warnings"]})

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
        self.assertEqual(self.validate()["overall"], "verified")

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
                    "plan": PLAN, "plan_sha256": sha(self.root, PLAN), "check": path}],
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
