# Protocol v2 — no-hash records

## Files and authority

Prefer the project's existing task cards, PR/CI evidence, and progress records.
Use their declared bindings and acceptance conventions; do not migrate or duplicate
status merely to adopt this skill. The bundled format below is an optional adapter,
not a claim that the validator understands alternative formats.

Bundled layout: `plans/CURRENT.md`, `plans/core/core-v0.1.0.md`, and
`plans/ex-plans/P001/{ex-plan-v0.1.0.md,progress.md,check/}`. Templates:
[core](../assets/core.md), [plan](../assets/ex-plan.md), [progress](../assets/progress.md),
[pointer](../assets/CURRENT.md), [check](../assets/check.md). Reuse an unchanged core.
CURRENT selects new managed work; plan defines tasks; progress alone owns live
state; checks record scoped evidence. P-numbers identify iterations, not plan or
software revisions. All writes follow [role authority](../SKILL.md#scope-and-authority).

## Portable metadata

Bundled records use **JSON between `---` delimiters**, followed by Markdown.
This YAML subset needs only Python's standard library; arbitrary project YAML is
outside the parser. SKILL.md itself uses ordinary Agent Skills YAML.

All records have integer `schema: 2` and `kind`. Paths are project-relative POSIX
file paths without `..`. The helper checks existing regular files and symlink
containment, not network references. For external artifacts, a local note may
identify durable locations/versions; reviewers still inspect those artifacts.
Using existing remote evidence does not remove bundled local record requirements.

| Kind | Required metadata beyond schema and kind |
|---|---|
| `core` | `revision` |
| `plan` | `id`, `revision`, `core`, `ready`, `tasks`, `integration_required` |
| `current` | `plan`, `progress` |
| `progress` | `plan_id`, `tasks`, `integration_check` (path or null) |
| `check` | `id`, `task`, `plan`, `verdict`, `subjects`, `evidence` |

A plan task has `id`, `type` (`development` or `research`), and `depends_on`
(task IDs). Reserve `integration` for check.task, not plan tasks. Prose specifies
inputs, outcome, scope, acceptance, and applicable resource limits.
A progress task has `id`, `state`, `owner`, `next`, `check` (path or null), and,
once started, `plan` identifying the versioned plan file.

Check `task` is a task ID or `integration`; `verdict` is `pass`, `fail`, or
`inconclusive` about acceptance. `subjects` and `evidence` are nonempty path lists:

```json
{"subjects":["src/calc.py","tests/check_total.py"],"evidence":["observations/total-001.log"]}
```

Subjects identify inspected inputs; evidence identifies actual logs/observations.
No duplicate paths within a list or self-reference to the check, including aliases.
List relevant inputs explicitly: the helper neither expands manifests nor discovers
omissions. Mutable progress is not a frozen subject. Check prose records reviewer,
date, method/command, actual results/exit codes, limitations, and next decision.

Research checks additionally have `research.mode` (`exploratory` or `confirmatory`),
`finding` (`supported`, `not_supported`, `inconclusive`), and `decision`
(`continue`, `diagnose`, `revise`, `stop`) in the `research` object.
A valid negative/inconclusive finding can pass; labels do not replace an argument.

## Acceptance

Use the project's proportionate test/build/review method and inspect actual evidence.
Documentation can use a documented review; no artificial runtime test is needed.
Identify the tested state, including relevant dirty/untracked inputs—a commit alone
may not identify it. Git, extra commits, full-workspace snapshots, and hashes are
not required. Preserve retrievable delivery versions appropriate to the risk.

An authorized Manager accepts; the designated writer records `done` with a
current-plan passing check and completed dependencies. Worker delivery or a
Reviewer verdict alone is not acceptance. Overall acceptance additionally needs a
passing integration check when required or supplied; existing CI can verify the
final combined state. The validator checks records, not authority or execution.

## State and recovery

States: `planned`, `in_progress`, `blocked`, `needs_review`, `done`, `cancelled`.
All current tasks need progress rows; historical rows can remain. A block retains
binding/reason and affects the whole task only when its acceptance-critical path
cannot proceed. Repair can return it to `in_progress`.

An older running binding warns; decide whether to finish or explicitly reassign.
An older accepted result does not satisfy a new revision without a new reuse check
bound to that revision, citing the old check. After relevant code, tests, data,
configuration, or criteria changes, the writer sets affected tasks to `needs_review`,
clears an affected `integration_check` to null, and retains the old reference in
progress prose. Preserve checks/logs; rerun affected verification and add a new
check before accepting again. Unrelated changes need not reopen acceptance.

## Revisions and selection

Keep used core/plan revisions unchanged and available. Revise committed scope,
acceptance, key interfaces/dependencies, resource boundaries, or fixed research
methods in a new file with reason, predecessor, affected tasks, and reuse decisions.
Implementation choices, debug order, and test strategy can evolve within those
commitments without a revision; record useful execution notes in progress.
Change core only for changed project intent or key constraints.

Prepare new records, then select a ready plan by replacing CURRENT metadata in one
edit. Higher-numbered drafts stay inactive. `ready` means specified, not authorized.
Selection does not rebind running work; reconcile affected work/acceptance explicitly.

## Plan bindings

Retain each started task's declared immutable binding, including completed/cancelled
tasks and across CURRENT changes. Bundled schema 2 uses the versioned plan path and
referenced core; keep both unchanged and available. Paths do not prove immutability.
An alternative format can use its retained task-card revision or fixed repository
reference. Disclose missing bindings; do not invent hashes or silently migrate.

## Reading validation output

```text
python3 <skill-directory>/scripts/strata.py validate --project <project-directory>
```

This optional command is read-only. Report inconsistencies first; repair only within
the current role/write scope. Check alternative formats manually and disclose that
the bundled validator was not used on them. Results include `schema: 2` and
`validation_scope: structure_only`.

| Exit | Meaning | Output |
|---|---|---|
| `0` | No record errors; warnings/unfinished work may remain | JSON stdout, `status: consistent` |
| `1` | Invalid records/references, including invalid CURRENT | JSON stdout, `status: invalid`, `overall: open` |
| `2` | Invalid arguments or unusable project root | stderr diagnostic; no validation result |

Root failures emit error JSON on stderr; argument errors use argparse text.
Help exits 0 with text. Missing subject/evidence paths are errors for done tasks,
warnings for open tasks. A valid failed/incomplete integration check keeps overall
open without being malformed. Only selected/bound records and referenced checks
are inspected, not all historical files.

`overall: accepted` means all current tasks have eligible recorded acceptance and
any required/supplied integration check passes; otherwise overall is `open`.
Neither `consistent` nor `accepted` proves unchanged inputs, actual/sufficient tests,
truthful evidence, or valid research claims. The helper reads records, not artifact
contents, and computes no hashes. Review actual results before declaring completion.

## Migration from v1

Skill 0.2.0-alpha.1 removes `fingerprint` and digest fields; `overall: verified`
becomes `overall: accepted`. Schema 1/mixed active records fail with
`UNSUPPORTED_SCHEMA`; no silent migration.

Preserve history. Finish legacy work with its matching skill/validator, or
deliberately close/hand it off and start schema 2 with a new versioned core and
explicit plan selection. Reconcile running jobs/ownership and recheck reused
deliveries. Do not relabel old schemas or verdicts. Unreferenced legacy history
does not block v2.
