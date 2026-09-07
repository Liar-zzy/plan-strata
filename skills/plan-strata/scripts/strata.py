#!/usr/bin/env python3
"""Read-only checks for Plan Strata protocol v1. Python 3.10+, standard library."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


STATES = {"planned", "in_progress", "blocked", "needs_review", "done", "cancelled"}
HASH = re.compile(r"[0-9a-f]{64}\Z")


class RecordError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def require(condition, message, code="INVALID_RECORD"):
    if not condition:
        raise RecordError(code, message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def hash_value(value):
    return isinstance(value, str) and HASH.fullmatch(value) is not None


class Validator:
    def __init__(self, project):
        self.project = Path(project).resolve(strict=True)
        require(self.project.is_dir(), "Project must be a directory", "INVALID_PATH")
        self.errors = []
        self.warnings = []
        self.plans = {}

    def issue(self, code, message, warning=False):
        (self.warnings if warning else self.errors).append(
            {"code": code, "message": message}
        )

    def file(self, ref):
        require(nonempty(ref), "Expected a project-relative file path", "INVALID_PATH")
        require(
            not ref.startswith("/") and "\\" not in ref
            and all(p not in {"", ".", ".."} for p in ref.split("/")),
            f"Not a project-relative POSIX path: {ref}", "INVALID_PATH",
        )
        path = (self.project / ref).resolve()
        require(path.is_relative_to(self.project), f"Path escapes project: {ref}", "INVALID_PATH")
        require(path.is_file(), f"Missing regular file: {ref}", "MISSING_FILE")
        return path

    def record(self, ref, kind):
        try:
            content = self.file(ref).read_text(encoding="utf-8")
            lines = content.splitlines()
            require(lines and lines[0] == "---", f"{ref}: missing frontmatter")
            end = lines.index("---", 1)
            data = json.loads("\n".join(lines[1:end]), object_pairs_hook=unique_object)
            require(isinstance(data, dict), f"{ref}: metadata must be a JSON object")
            require(type(data.get("schema")) is int and data["schema"] == 1,
                    f"{ref}: expected schema 1")
            require(data.get("kind") == kind, f"{ref}: expected kind {kind}")
            return data
        except RecordError:
            raise
        except (ValueError, OSError, UnicodeError) as exc:
            raise RecordError("INVALID_RECORD", f"{ref}: {exc}") from exc

    def matches(self, ref, expected):
        require(hash_value(expected), f"{ref}: expected a lowercase SHA-256 digest")
        return digest(self.file(ref)) == expected

    def plan(self, ref):
        if ref in self.plans:
            return self.plans[ref]
        data = self.record(ref, "plan")
        require(nonempty(data.get("id")) and nonempty(data.get("revision")),
                f"{ref}: plan id and revision are required")
        require(data.get("ready") is True, f"{ref}: plan is not ready", "UNREADY_PLAN")
        require(type(data.get("integration_required")) is bool,
                f"{ref}: integration_required must be boolean")
        core_ref = data.get("core")
        core = self.record(core_ref, "core")
        require(nonempty(core.get("revision")), f"{core_ref}: revision is required")
        require(self.matches(core_ref, data.get("core_sha256")),
                f"{ref}: core snapshot changed", "CORE_CHANGED")
        tasks = self.index(data.get("tasks"), f"{ref}: tasks")
        require(tasks, f"{ref}: define at least one bounded task")
        require("integration" not in tasks, f"{ref}: integration is reserved for the terminal check",
                "RESERVED_TASK_ID")
        for task in tasks.values():
            require(isinstance(task.get("type"), str) and task["type"] in {"development", "research"},
                    f"{ref}: invalid task type for {task['id']}")
            deps = task.get("depends_on")
            require(isinstance(deps, list) and all(nonempty(d) for d in deps),
                    f"{ref}: dependencies must be a list of task IDs")
            require(len(deps) == len(set(deps)), f"{ref}: duplicate dependency")
            require(all(d in tasks for d in deps), f"{ref}: unknown dependency")
        visiting, visited = set(), set()

        def visit(task_id):
            require(task_id not in visiting, f"{ref}: dependency cycle", "DEPENDENCY_CYCLE")
            if task_id in visited:
                return
            visiting.add(task_id)
            for dep in tasks[task_id]["depends_on"]:
                visit(dep)
            visiting.remove(task_id)
            visited.add(task_id)

        for task_id in tasks:
            visit(task_id)
        self.plans[ref] = (data, tasks)
        return data, tasks

    @staticmethod
    def index(rows, label):
        require(isinstance(rows, list), f"{label} must be a list")
        result = {}
        for row in rows:
            require(isinstance(row, dict) and nonempty(row.get("id")),
                    f"{label}: every row requires a nonempty id")
            require(row["id"] not in result, f"{label}: duplicate id {row['id']}")
            result[row["id"]] = row
        return result

    def check(self, ref, task_id, plan_ref, plan_hash, accepting):
        data = self.record(ref, "check")
        require(nonempty(data.get("id")), f"{ref}: check id required")
        require(data.get("task") == task_id, f"{ref}: wrong task", "WRONG_CHECK_SCOPE")
        require(data.get("plan") == plan_ref and data.get("plan_sha256") == plan_hash,
                f"{ref}: wrong execution baseline", "WRONG_CHECK_BASIS")
        require(self.matches(plan_ref, plan_hash), f"{ref}: plan changed", "PLAN_CHANGED")
        _, definitions = self.plan(plan_ref)
        require(task_id == "integration" or task_id in definitions,
                f"{ref}: task absent from bound plan", "WRONG_CHECK_SCOPE")
        verdict = data.get("verdict")
        require(isinstance(verdict, str) and verdict in {"pass", "fail", "inconclusive"}, f"{ref}: invalid verdict")
        fresh = True
        for field in ("subjects", "evidence"):
            records = data.get(field)
            require(isinstance(records, list) and records, f"{ref}: {field} must be nonempty")
            seen = set()
            for item in records:
                require(isinstance(item, dict), f"{ref}: invalid {field} entry")
                path = item.get("path")
                require(nonempty(path) and path != ref, f"{ref}: invalid/self-referencing evidence")
                require(path not in seen, f"{ref}: duplicate {field} path")
                seen.add(path)
                try:
                    same = self.matches(path, item.get("sha256"))
                    if not same:
                        fresh = False
                        self.issue("STALE_" + field.upper(), f"{ref}: changed {path}", not accepting)
                except RecordError as exc:
                    fresh = False
                    self.issue(exc.code, str(exc), not accepting)
        if task_id != "integration" and definitions[task_id]["type"] == "research":
            research = data.get("research")
            require(isinstance(research, dict), f"{ref}: research interpretation required")
            require(isinstance(research.get("mode"), str) and research["mode"] in {"exploratory", "confirmatory"},
                    f"{ref}: invalid research mode")
            require(isinstance(research.get("finding"), str) and research["finding"] in {"supported", "not_supported", "inconclusive"},
                    f"{ref}: invalid research finding")
            require(isinstance(research.get("decision"), str) and research["decision"] in {"continue", "diagnose", "revise", "stop"},
                    f"{ref}: invalid research decision")
        if accepting:
            require(verdict == "pass", f"{ref}: completion requires a passing check", "CHECK_NOT_PASSING")
        return verdict == "pass" and fresh

    def validate(self, current_ref="plans/CURRENT.md"):
        output = {"schema": 1, "status": "invalid", "overall": "open", "tasks": []}
        try:
            current = self.record(current_ref, "current")
            plan_ref = current.get("plan")
            plan_hash = current.get("plan_sha256")
            require(self.matches(plan_ref, plan_hash), "CURRENT's selected plan changed", "PLAN_CHANGED")
            plan, definitions = self.plan(plan_ref)
            progress = self.record(current.get("progress"), "progress")
            require(progress.get("plan_id") == plan["id"], "Progress belongs to another iteration")
            require("integration_check" in progress, "Progress requires integration_check (path or null)")
            rows = self.index(progress.get("tasks"), "progress tasks")
            output["current_plan"] = plan_ref
            missing = set(definitions) - set(rows)
            require(not missing, f"Missing progress tasks: {', '.join(sorted(missing))}", "MISSING_TASK")
            effective = {}
            for task_id, row in rows.items():
                before = len(self.errors)
                state = row.get("state")
                try:
                    require(isinstance(state, str) and state in STATES, f"{task_id}: invalid state")
                    require(nonempty(row.get("owner")) and nonempty(row.get("next")),
                            f"{task_id}: owner and next action/reason required")
                    require("check" in row, f"{task_id}: check must be a path or null")
                    if task_id not in definitions:
                        self.issue("HISTORICAL_TASK", f"{task_id}: absent from current plan", True)
                    bound = row.get("plan")
                    bound_hash = row.get("plan_sha256")
                    if state != "planned" or bound is not None or row["check"] is not None:
                        require(self.matches(bound, bound_hash), f"{task_id}: bound plan changed", "PLAN_CHANGED")
                        old_plan, old_tasks = self.plan(bound)
                        require(old_plan["id"] == plan["id"] and task_id in old_tasks,
                                f"{task_id}: invalid task binding", "WRONG_TASK_BASIS")
                        if bound != plan_ref or bound_hash != plan_hash:
                            self.issue("OLDER_BASIS", f"{task_id}: bound to {bound}; CURRENT selects {plan_ref}", True)
                            if state == "done" and task_id in definitions:
                                self.issue("OLD_ACCEPTANCE", f"{task_id}: assess reuse under the current plan")
                    if row["check"] is not None:
                        self.check(row["check"], task_id, bound, bound_hash,
                                   state == "done" and task_id in definitions)
                    elif state == "done":
                        self.issue("MISSING_CHECK", f"{task_id}: done requires evidence")
                except (RecordError, OSError) as exc:
                    self.issue(getattr(exc, "code", "IO_ERROR"), str(exc))
                effective[task_id] = "needs_review" if state == "done" and len(self.errors) > before else state

            # Propagate revoked acceptance through declared dependencies.
            changed = True
            while changed:
                changed = False
                for task_id, task in definitions.items():
                    if effective.get(task_id) == "done" and any(
                        effective.get(dep) != "done" for dep in task["depends_on"]
                    ):
                        self.issue("OPEN_DEPENDENCY", f"{task_id}: a dependency is not accepted")
                        effective[task_id] = "needs_review"
                        changed = True
            output["tasks"] = [
                {"id": tid, "state": row.get("state"), "effective_state": effective.get(tid),
                 "plan": row.get("plan"), "owner": row.get("owner"), "next": row.get("next")}
                for tid, row in rows.items()
            ]
            integrated = not plan["integration_required"]
            integration = progress["integration_check"]
            if integration is not None:
                integrated = self.check(integration, "integration", plan_ref, plan_hash, False)
                if not integrated:
                    self.issue("INTEGRATION_OPEN", "Integration is not currently verified", True)
            elif plan["integration_required"]:
                self.issue("INTEGRATION_OPEN", "An integration check is still required", True)
            if integrated and all(effective.get(tid) == "done" for tid in definitions) and not self.errors:
                output["overall"] = "verified"
        except (RecordError, OSError) as exc:
            self.issue(getattr(exc, "code", "IO_ERROR"), str(exc))
        output.update(status="invalid" if self.errors else "consistent",
                      errors=self.errors, warnings=self.warnings)
        return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="check active records without changing them")
    validate.add_argument("--project", default=".")
    validate.add_argument("--current", default="plans/CURRENT.md")
    fingerprint = commands.add_parser("fingerprint", help="print SHA-256 identities of local files")
    fingerprint.add_argument("--project", default=".")
    fingerprint.add_argument("files", nargs="+")
    args = parser.parse_args(argv)
    try:
        validator = Validator(args.project)
        if args.command == "validate":
            result = validator.validate(args.current)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1 if result["errors"] else 0
        print(json.dumps([{"path": ref, "sha256": digest(validator.file(ref))}
                          for ref in args.files], ensure_ascii=False, indent=2))
        return 0
    except (RecordError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
