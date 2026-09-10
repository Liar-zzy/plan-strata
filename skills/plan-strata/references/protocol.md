# Protocol v2 — no-hash records

## Files and authority

Default layout: `plans/CURRENT.md`, `plans/core/core-v0.1.0.md`, and
`plans/ex-plans/P001/{ex-plan-v0.1.0.md,progress.md,check/}`. Create checks and
worker reports when needed. One P-number identifies a bounded iteration;
iteration IDs, plan revisions, software releases, and skill releases differ.

CURRENT selects the default plan and progress for new work. The plan references
core and defines tasks. Progress owns task state, owner, next action, bound plan,
and applicable check. A check records evidence and verdict. Prose explains these
records without a second status table. One Manager writes authoritative progress.

## Portable metadata

Templates use **JSON between `---` delimiters**, followed by Markdown. This YAML
subset needs only Python's standard library. Ordinary YAML in existing project
records is outside this parser; SKILL.md uses ordinary Agent Skills YAML.

All records have integer `schema: 2` and `kind`. Paths are project-relative POSIX
file paths without `..`. The helper checks existing regular files and symlink
containment; it does not execute commands or follow network references. For large
or external artifacts, a local note may list durable locations and versions.
A reviewer must inspect those artifacts separately.

| Kind | Required metadata beyond schema and kind |
|---|---|
| `core` | `revision` |
| `plan` | `id`, `revision`, `core`, `ready`, `tasks`, `integration_required` |
| `current` | `plan`, `progress` |
| `progress` | `plan_id`, `tasks`, `integration_check` (path or null) |
| `check` | `id`, `task`, `plan`, `verdict`, `subjects`, `evidence` |

A plan task has `id`, `type` (`development` or `research`), and `depends_on`
(task IDs). The exact ID `integration` is reserved for terminal checks, not plan
tasks. Task prose defines inputs, outputs, scope, budget, and acceptance.

A progress task has `id`, `state`, `owner`, `next`, and `check` (path or null).
Once started, it also has `plan`, identifying the versioned plan file. Keep this
binding for completed/cancelled tasks and across later CURRENT changes. The bound
plan references its versioned core. Paths identify the intended revision; the
helper cannot detect in-place edits to its contents.

Check `task` is a task ID or `integration`. `verdict` is `pass`, `fail`, or
`inconclusive` about the stated acceptance method. `subjects` and `evidence`
are nonempty lists of path strings, for example:

```json
{"subjects":["src/calc.py","tests/check_total.py"],"evidence":["observations/total-001.log"]}
```

Subjects identify what was inspected; evidence identifies actual logs, review
notes, or observations. No duplicate paths within a list or self-reference to the
check file. List relevant inputs explicitly; the helper does not expand manifests
or discover omitted code, tests, configuration, or dependencies. Live progress is
not a frozen input. Check prose records reviewer, date, method/command, actual
results (including exit codes when applicable), limitations, and next decision.

Research checks also have `research`: `mode` (`exploratory` or `confirmatory`),
`finding` (`supported`, `not_supported`, `inconclusive`), and `decision`
(`continue`, `diagnose`, `revise`, `stop`). A valid negative finding can pass
acceptance; these labels do not replace a scientific argument.

## State, change, and recovery

States: `planned`, `in_progress`, `blocked`, `needs_review`, `done`, `cancelled`.
A block retains the binding and reason; a repair can return to in_progress.
All current plan tasks need progress rows. Historical rows can remain.
An older running binding produces a warning; decide whether to finish it or
explicitly reassign it. An older accepted result does not satisfy a new revision:
assess reuse in a new check bound to that revision, citing the old check in prose.

`done` requires a current-plan passing check, available subject/evidence paths,
and completed dependencies. These are recorded conditions, not proof of execution.

After relevant code, tests, data, configuration, or acceptance changes, Manager
explicitly reopens affected tasks as `needs_review`. Clear an affected
`integration_check` to null and retain its previous reference in progress prose.
Preserve old checks/logs; rerun affected verification and add a new check before
accepting again. Unrelated edits need not reopen acceptance. The helper cannot
detect content changes, determine relevance, or enforce this review step.

Use existing Git versions/diffs when useful. Git is optional: normal single-agent
work needs no extra commit, full-workspace snapshot, or content digest for record
bookkeeping. Retain retrievable versions of important deliveries in proportion to
risk; concurrent handoffs additionally follow the isolation/collection guidance.

## Revisions and selection

Keep used core/plan revisions unchanged and available. For changed scope,
dependencies, methods, or acceptance, add a new versioned file with the reason,
predecessor, affected tasks, and reuse decisions. Ordinary execution updates
progress. Cosmetic notes can go in progress without rewriting the bound plan.

Prepare new files first, then select the ready plan by replacing CURRENT metadata
in one edit. Higher-numbered drafts remain inactive. `ready: true` means the plan
is specified, not that new authority has been granted. Selection does not rebind
running work. Reconcile pending work and previous acceptance deliberately.

## Reading validation output

`validate` is read-only. Every validation result reports
`schema: 2` and `validation_scope: structure_only`.

| Exit | Meaning | Output |
|---|---|---|
| `0` | No record errors; warnings or unfinished work may remain | JSON stdout, `status: consistent` |
| `1` | Invalid records/references, including missing/invalid CURRENT | JSON stdout, `status: invalid`, `overall: open` |
| `2` | Invalid CLI arguments or unusable project root | stderr diagnostic; no validation JSON |

Project-root failures emit an error JSON; argument errors use argparse text.
Help exits 0 with text. Missing subject/evidence paths supporting a done task are
errors; on an open task they are warnings. A failed or incomplete integration
check keeps overall open without treating a valid failure record as malformed.

`overall: accepted` means all current tasks are recorded done with eligible
checks, plus a passing integration check when required or supplied. Otherwise
overall is `open`; invalid records always stay open. Only selected/bound records
and referenced checks are inspected, not every historical file.

Neither `consistent` nor `accepted` proves that tests ran, inputs are unchanged,
evidence is truthful, test coverage is adequate, or research claims are valid.
The helper reads planning/check records, not artifact contents, and computes no
hashes. Review actual results before declaring completion.

## Migration from v1

Skill 0.2.0-alpha.1 introduces this breaking schema. The `fingerprint` command and
digest fields are removed; `overall: verified` becomes `overall: accepted`.
Schema 1 and mixed active records are rejected with `UNSUPPORTED_SCHEMA`, rather
than silently interpreting old acceptance under weaker rules.

Preserve old plans, checks, and evidence. Finish an active legacy iteration with
its matching skill/validator, or deliberately close/hand it off and start a new
schema 2 iteration from the templates. Reconcile running jobs/ownership first.
Use a new versioned core, select the new plan explicitly, and recheck any reused
delivery under it. Do not simply change old schema numbers or rewrite old verdicts.
Unreferenced legacy history can remain in the project without blocking v2.
