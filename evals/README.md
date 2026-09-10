# Forward-use evaluations

Prepare a fresh scenario with `prepare.py`. Give a fresh agent only the installed
skill path, one generated project directory, and the matching request below.
Keep this repository's tests, generator, scoring rubric, and previous conversation
out of its provided context. After it finishes, inspect actual artifacts and use
the rubric in [expected.md](expected.md). The evaluator may be a human or a fresh
agent instance. The skill's author should review the outcome, not prefill it.

| Scenario | User request |
|---|---|
| resume | 接着把当前这一轮剩下的工作做完，留下检查和交接记录。 |
| switch | 继续已经分配给你的 T01，完成原来分配的范围并留下交接；本次不要承担其它任务。 |
| stale | 检查当前完成声明是否成立，更新管理记录并写清下一步。本次不要改源码。 |
| integration | 根据当前产物和检查汇总本轮是否可以结束。只更新管理记录。 |
| research | 请接着处理这轮研究任务，核对已有产物，整理本轮结果并留下检查和交接记录。 |

Keep a concise record of actual actions, command outputs, files changed, friction,
and remaining work. A failed behavior is a finding to investigate. A sample passing
once is not a pass-rate estimate or proof of long-term effectiveness.

All scenarios are synthetic. The generator runs the tiny project's test/analysis
commands to produce actual local observations. The research dataset is invented
for workflow evaluation and must remain labelled as such.

In protocol v2, `stale` has changed source but structurally consistent records;
the validator exits 0 and does not detect that content change. The actual task test
fails: a reviewer must run/inspect the evidence and explicitly reopen acceptance.
The `integration` scenario has structurally consistent but
unsuccessful integration and remains open. These starting conditions are useful
inputs, not failures of the scenario generator.

The first forward use also exposed a limitation in `integration`: its inherited
documentation check points only to unit-test output. This imperfect record is
retained as a useful semantic review case. A verifier can establish the actual
documentation behavior directly; structural consistency alone does not do so.

Use `run_checks.py --output <new-file.json>` to preserve a contract-test run.
After a worker finishes, `capture.py` can preserve its files, skill path inventory,
and a new validator result. Both commands retain earlier reports by refusing to
overwrite an existing output file.

## Parallel handoff trial

This optional schema 2 trial uses two independent tasks in one frozen plan, isolated
directory copies, and a terminal integration gate. It needs Python 3.10+ and the
full repository, but no Git, network, or installed agent runtime. The fixture
driver never starts an agent. Obtain approval for the local worker batch first.

Prepare a new trial (existing directories are refused):

```sh
strata_parallel_dir=$(mktemp -d)
python3 -m evals.parallel_trial prepare --directory "$strata_parallel_dir/trial"
```

Give one fresh worker `trial/worker-T01/` and its `handoffs/T01-A01.md`; give another
`trial/worker-T02/` and `handoffs/T02-A01.md`. Both receive only the copied skill at
`trial/skill/`, their project directory, and the request to complete that packet.
Use your host's delegation mechanism, or separate sessions; keep the generator,
tests in this repository, prior chat, and intended solutions out of their context.
The workers may execute concurrently, each within the packet's write scope.

Manager inspects the returned code, report identity, and actual logs, then runs:

```sh
python3 -m evals.parallel_trial collect --directory "$strata_parallel_dir/trial"
```

This fixture-specific command preflights both the Manager's receiving baseline
and the workers' allowed diffs, then copies the selected
artifacts into `trial/manager/`, reruns each task test, and records scoped checks.
Only passing tasks prepare `trial/integration/`. Task success still leaves overall
open. Give that directory, `handoffs/integration-A01.md`, and the copied skill to a
fresh Integrator. It returns its report/log and proposed check, without editing
code or Manager's progress. Its proposed check must list `INTEGRATION-INPUTS.json`
and every member of that manifest as subject path strings. The manifest excludes
live progress. This tiny fixture retains UTF-8 input text and compares it directly;
that test mechanism is not a full-project snapshot requirement in the skill.
The installed helper checks path availability, not artifact contents or manifests.

After inspecting that delivery, Manager collects the terminal result:

```sh
python3 -m evals.parallel_trial finish --directory "$strata_parallel_dir/trial"
python3 skills/plan-strata/scripts/strata.py validate --project "$strata_parallel_dir/trial/manager"
```

`finish` exits 0 only for recorded acceptance; a retained failed verdict remains
open and exits 1. Repeating an unchanged collection is a no-op. Changed attempt
results, out-of-scope writes, or an interrupted partial collection require review,
not an automatic overwrite. Both initial and repeated collection/finish reject
added, removed, or changed Manager input files. Only progress prose and nonempty
task `next` text may vary; bindings, owners, states, and check references remain
pinned between driver transitions. Finishing also checks input coverage before
copying anything. Preserve failed trials; prepare a new directory for
a repaired attempt. The helper is for this synthetic fixture, not arbitrary
projects, Issue synchronization, a lock, or an agent scheduler.

The revised receipts contain retained-text Manager checkpoints. Older schema 1
trial directories are historical evidence and require a new trial, not an in-place
upgrade. These checks assume exclusive access during each driver command and
trusted fixture code; they are not a sandbox or protection against forged receipts.
The installed read-only validator does not detect content changes after delivery.
The fixture's comparison checks are separate from protocol validation and cannot
authenticate a newly proposed log. Review actual tests and affected inputs before
reusing acceptance; no file hashes are calculated by either tool.

Use `capture.py` on each worker, the integration directory, and Manager's final
directory to retain actual files and evidence outside the temporary workspaces.
Judge whether bindings and write scopes survived, Manager remained the only
progress writer, and combined evidence—not worker claims—determined completion.
Automated tests also inject failed tasks/integration, missing evidence and conflicting
retries. Those deterministic tests are not independent Agent trials. Research
budget rules are documented; this example runs no research experiments.

## Issue cold-start trial

This scenario tests a different entry point: prepare Issue bodies from raw project
context, then let a fresh worker create its own worktree using the dispatched Issue.
It uses a local bare Git repository as the accessible source and Markdown as the
Issue transport. It neither posts to GitHub nor starts agents. Git and Python 3.10+
are required for this evaluation, not for the installed skill's ordinary workflow.

```sh
strata_issue_dir=$(mktemp -d)
python3 -m evals.issue_trial --directory "$strata_issue_dir/trial"
```

Give a fresh author only `trial/skill/SKILL.md` and `trial/manager-input.md`.
It writes `outbox/T01.md` and `outbox/T02.md`; keep this README, the generator,
fixture metadata, prior conversation, and expected results out of its context.
Inspect whether the actual bodies are usable at their stated readiness: T01 can
be picked up once assigned; T02 still needs an accepted T01 delivery and exact
input versions. Neither task initially has an owner or a worker workspace.

For T01, Manager records the owner/attempt and workspace allocation in the seed
project's authoritative progress, outside frozen inputs. Preserve the author's
body after the author finishes, then create a dispatch snapshot containing the
assignment receipt. Read and check the actual retained snapshot before launch;
cached draft text may differ from the
author's final file. Supply a fresh
worker only that Issue snapshot and the skill entry point, without preparing its
clone/worktree or adding another task brief. Let it return the report through the
host. Keep T02 blocked; publication alone is not permission to execute it.

Review the worker's actual Git HEAD (the selected commit, not the newer default
branch), worktree registration, unchanged baseline inputs outside its write scope,
implementation, report, and real test output. Re-run the task tests and retain the
Issue bodies, receipt, skill source/version, and worker artifacts with the review.
`capture.py` can archive the worker worktree; its consistent/open state is expected
because only Manager accepts work. Preserve failed packets and allocate a new
attempt/workspace for a corrected dispatch. Changing the fixture or copied skill
requires a new trial directory. Do not turn documentation/regex checks into claims about
agent behavior. One successful sample does not validate GitHub APIs, concurrent
claiming, downstream release, merge conflicts, or runtime cancellation.

## Bounded repair regressions

Run the deterministic evidence-transition tests from a full clone:

```sh
python3 -m unittest discover -s tests -p test_repair_workflow.py -v
```

They run a tiny startup/turn configuration check in fresh temporary directories:
internal self-check failure → repair → one acceptance check; formal failed delivery
→ repair with retained inputs/log/check; passing-input change → explicit reopening
by Manager → fresh passing check; and a scripted exhausted repair budget with an unresolved
defect that cannot be accepted. The task, core, and selected plan stay unchanged.
The existing parallel tests separately reject a changed result under one received
attempt identity. CLI exit-code regressions live in `test_workflow.py`.

These tests prescribe the edits, finite schedule, and recording actions. They
exercise the actual validator and tiny project checks, not an agent's planning,
scope judgment, communication, or budget enforcement. No new agents are launched;
fewer human interventions or lower elapsed cost require a separate behavioral
evaluation. See the [current no-hash notes](../docs/v0.2.0-alpha.1.md) and
[historical repair validation](../docs/validation-repair-loop.md).
