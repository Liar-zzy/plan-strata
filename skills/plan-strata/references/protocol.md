# Protocol v1

## Files and authority

Default layout: `plans/CURRENT.md`, `plans/core/core-v0.1.0.md`, and
`plans/ex-plans/P001/{ex-plan-v0.1.0.md,progress.md,check/}`. Create checks and worker
reports when used. One P-number identifies a bounded iteration, with as many tasks
and agents as that iteration needs. Another iteration gets another identity.
Plan revisions, iteration identities, software releases, and skill releases differ.

CURRENT selects the default plan for new work and its progress file. The plan
references its core and defines tasks. Progress owns task state, owner, next
action, execution binding, and applicable check. A check owns its evidence and
verdict. Prose explains these records without maintaining a second status table.

## Portable metadata

The templates have **JSON between `---` delimiters**, followed by ordinary Markdown.
JSON is a YAML subset; this deliberately restricted frontmatter allows the helper
to use Python's standard library. Regular YAML is fine for a user's existing
workflow, but is outside this helper's parser. The installed SKILL.md itself uses
ordinary Agent Skills YAML and is not a project record.

All records have `schema: 1` and `kind`. All path fields are project-relative POSIX
file paths, without `..`. The helper checks local regular files inside the project,
including symlink containment; it neither follows network references nor executes
commands in records. Large/external artifacts can be represented by a local
manifest listing durable locations, versions, and known hashes. The helper only
validates the local manifest; a reviewer verifies the external artifacts separately.

Use `python3 <skill>/scripts/strata.py fingerprint --project <project> <files...>`
to calculate file fingerprints. Hash the complete bytes. Hashes identify files;
they are not signatures or evidence of when/how a file was produced.

| Kind | Required metadata beyond schema and kind |
|---|---|
| `core` | `revision` |
| `plan` | `id`, `revision`, `core`, `core_sha256`, `ready`, `tasks`, `integration_required` |
| `current` | `plan`, `plan_sha256`, `progress` |
| `progress` | `plan_id`, `tasks`, `integration_check` (path or null) |
| `check` | `id`, `task`, `plan`, `plan_sha256`, `verdict`, `subjects`, `evidence` |

A plan task has `id`, `type` (`development` or `research`), and `depends_on` (task
IDs). Its prose defines inputs, outputs, scope, and acceptance. A progress task has
`id`, `state`, `owner`, `next`, and `check` (path or null). Once started, it also has
`plan` and `plan_sha256`, binding this task's attempt to an exact revision. The
bound plan in turn pins core. Completed/cancelled tasks retain this provenance.

Check `task` is a task ID or `integration`. `verdict` is `pass`, `fail`, or
`inconclusive` **about the stated acceptance method**. `subjects` and `evidence`
are nonempty lists of `{ "path": "...", "sha256": "..." }`: subjects identify
what was inspected; evidence identifies logs, review notes, or other actual
observations. A check file cannot be its own subject or evidence.

Check prose records the reviewer, date, method/command, actual results (including
exit code when applicable), limitations, and next decision. A research task check
also has `research` with `mode` (`exploratory` or `confirmatory`), `finding`
(`supported`, `not_supported`, or `inconclusive`), and `decision` (`continue`,
`diagnose`, `revise`, or `stop`). These labels do not replace a scientific argument.

## State and recovery

States: `planned`, `in_progress`, `blocked`, `needs_review`, `done`, `cancelled`.
Typical path: planned → in_progress → needs_review → done. A block retains the
binding and reason. Resuming or fixing returns to in_progress. Changed evidence
moves acceptance to needs_review. Cancellation has a reason and leaves the round
open if its required delivery was not replaced through a plan revision.

All tasks in the current plan need a progress row. Historical rows can remain.
A running task may legitimately bind an older plan; the validator warns and
preserves that binding. Before new work, resolve whether to finish under that
basis or explicitly reassign it. An older accepted result does not automatically
satisfy a new revision: record a new, reasoned reuse check under the new baseline,
or set the task to needs_review. A reuse check cites the old check in its prose,
uses the new baseline, and fingerprints the applicable subjects and evidence.

`done` requires a current-baseline passing check, matching subject and evidence
hashes, and completed dependencies. A declared scope may omit dependencies;
the human/agent reviewer must assess its adequacy. The helper cannot infer a full
dependency graph from source code. Unrelated file changes do not stale a check.

CURRENT's selected hash detects accidental in-place edits. The selected plan must
have `ready: true`; higher numbered drafts stay inactive. `ready` means the plan
is sufficiently specified for authorized work, not a substitute for user authority.

## Revisions and selection

Once used, keep core and plan snapshots byte-stable. A substantive change creates
a new revision with the predecessor, reason, affected tasks, and reuse decisions in
prose. Even a cosmetic correction to a started snapshot must preserve the old
bytes (a new file or a retrievable Git object); this alpha's path-based validator
uses new files. Ordinary progress and reruns do not revise the plan.

Prepare the new files first. Select a ready plan by replacing CURRENT's complete
metadata in one edit, including its hash. Selection changes the entry point for
new work; it does not rebind running tasks. Retarget pending tasks deliberately.
Reconcile existing acceptance separately. Single-writer coordination is assumed;
for concurrent writers, use host/workspace isolation and an explicit coordinator.

## Reading validation output

`validate` returns JSON and makes no changes. Exit 0 means the records are
consistent, exit 1 means discrepancies, and exit 2 means invocation/path failure.
`overall: verified` requires all current tasks done, plus an applicable passing
integration check if integration is required or an integration check was recorded.
Otherwise overall is `open`. Invalid records always yield overall open.

Only selected/bound records and referenced checks are inspected. Unreferenced
historical checks are preserved, including failures and once-valid old hashes.
Stale evidence supporting done is an error; stale evidence attached to an open
task is a warning. A failed integration check remains an open outcome, not a
malformed record. No validator output establishes research truth or artifact
reproducibility beyond the explicitly checked local bytes.
