import json
import runpy
import tempfile
import unittest
from pathlib import Path

from evals.issue_trial import REPO, git, prepare_trial
from evals.prepare import PROGRESS, read_record, write


Validator = runpy.run_path(str(REPO / "skills/plan-strata/scripts/strata.py"))["Validator"]


class IssueTrialTests(unittest.TestCase):
    """Fixture mechanics only; these tests do not simulate agent decisions."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="plan-strata-issue-test-")
        self.addCleanup(self.temp.cleanup)
        self.trial = prepare_trial(Path(self.temp.name) / "trial")
        self.metadata = json.loads((self.trial / "fixture.json").read_text())

    def test_ref_retains_baseline_after_default_branch_moves(self):
        origin = self.trial / "origin.git"
        self.assertEqual(git(origin, "rev-parse", "trial-baseline"), self.metadata["baseline"])
        self.assertEqual(git(origin, "rev-parse", "HEAD"), self.metadata["default_head"])
        self.assertNotEqual(self.metadata["baseline"], self.metadata["default_head"])

    def test_context_is_retrievable_from_pinned_commit(self):
        for path in self.metadata["inputs"]:
            content = git(self.trial / "origin.git", "show", f"{self.metadata['baseline']}:{path}",
                          strip_output=False)
            self.assertEqual(content, (self.trial / "seed" / path).read_text(), path)

    def test_tasks_are_unclaimed_and_worker_workspace_is_not_prepared(self):
        result = Validator(self.trial / "seed").validate()
        self.assertEqual((result["status"], result["overall"]), ("consistent", "open"))
        progress, _ = read_record(self.trial / "seed", PROGRESS)
        self.assertTrue(all(row["state"] == "planned" and row["owner"] == "unassigned"
                            for row in progress["tasks"]))
        self.assertEqual(list((self.trial / "worker-area").iterdir()), [])
        self.assertEqual(list((self.trial / "outbox").iterdir()), [])

    def test_recipient_can_clone_and_create_worktree_at_old_baseline(self):
        clone = self.trial / "worker-area" / "clone"
        worktree = self.trial / "worker-area" / "task"
        git(self.trial, "clone", "--no-hardlinks", self.trial / "origin.git", clone)
        git(clone, "worktree", "add", "--detach", worktree, self.metadata["baseline"])
        self.assertTrue((worktree / ".git").is_file())
        self.assertEqual(git(worktree, "rev-parse", "HEAD"), self.metadata["baseline"])
        self.assertFalse((worktree / "LATER.md").exists())

    def test_existing_trial_is_preserved(self):
        write(self.trial, "outbox/keep.md", "Retained observation\n")
        with self.assertRaises(FileExistsError):
            prepare_trial(self.trial)
        self.assertEqual((self.trial / "outbox/keep.md").read_text(), "Retained observation\n")
