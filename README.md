# Plan Strata

English · [简体中文](README.zh-CN.md)

Versioned plans, recoverable progress, and evidence-based handoffs for AI-assisted software development and research.

Plan Strata is an open-source agent skill for work that spans sessions. It helps an
agent recover what was agreed, which plan a task started under, what was actually
checked, and what to do next. Development and research tasks can share one plan
without sharing the same meaning of success.

**Status: `0.2.0-alpha.1` · MIT · Python 3.10+ for the optional validator.**
Ready for early trials, not a production workflow guarantee.

> **Schema 2 — no-hash workflow:** this version removes mandatory digests and the
> `fingerprint` command. The validator checks structure, not unchanged contents or
> test quality. Existing schema 1 projects need a deliberate transition; see
> [migration and release notes](docs/v0.2.0-alpha.1.md). The default install below
> uses `main`, which carries this workflow.

> **🙌 Join us! Help improve Plan Strata through real use.**
> Using AI for development or research? [Copy the optional AGENTS.md feedback snippet](#join-us)
> and [share one sanitized case](https://github.com/Liar-zzy/plan-strata/issues/new).

## Quick install

Run this in the project where you want to use the skill:

```sh
npx skills add Liar-zzy/plan-strata --skill plan-strata
```

The [Skills CLI](https://github.com/vercel-labs/skills) prompts for your agent and
installation scope. Choose **Project** for a repo-local install. It requires Git
and Node.js; the tested CLI version is `1.5.23` (Node.js 22.20+).
Only `skills/plan-strata/` is installed, not this repository's plans or evaluations.

For a non-interactive, project-local Codex install:

```sh
npx --yes skills@1.5.23 add Liar-zzy/plan-strata --skill plan-strata --agent codex --yes
```

Use `--agent claude-code` for Claude Code, or add `--global` for a user-wide install.
The pinned version is the **installer version**, not the Plan Strata version.
Reinstalling can replace an existing skill of the same name; back up local edits
and omit the final `--yes` to review prompts. Skills run with the host agent's
permissions, so review the [skill instructions](skills/plan-strata/SKILL.md) first.
The third-party CLI has telemetry; set `DISABLE_TELEMETRY=1` to opt out.

### Codex without Node.js

If your Codex setup includes `$skill-installer`, send this in **Codex chat**, not
your terminal:

```text
$skill-installer install plan-strata from https://github.com/Liar-zzy/plan-strata, path skills/plan-strata.
```

For a manual install, copy the entire `skills/plan-strata/` directory into your
project's `.agents/skills/plan-strata/`, preserving its subdirectories. Review any
existing installation before replacing it. Codex discovers that project-local
location; restart it if the skill does not appear. See the
[official installation and discovery guidance](https://learn.chatgpt.com/docs/build-skills).

### Choose the source

The repository shorthand above uses `main`, including the schema 2 workflow and
simplified instructions. `dev` is a separate development branch, not a required
installation source or a guarantee of the same snapshot.

Review/back up an existing installation first. For source review or unpublished
changes, inspect the intended checkout and copy its entire `skills/plan-strata/`
directory using the manual method above. A remote checkout contains only pushed
changes. Updating the repository does not automatically update an installation.

Record the source branch/commit and any local edits when known. The same alpha
version label can cover different snapshots; if the installed package's source
is unknown, record that uncertainty and the installed location/version. No file
digests or extra commits are required for this bookkeeping. A separate
repository's HEAD is not proof of what was installed. This is a standalone skill,
not a marketplace plugin.

## Start using it

In Codex, invoke `$plan-strata`; in other agents, use their skill selector or ask
the agent to load `plan-strata`. For example:

**Development**

> Use $plan-strata to plan a bounded iteration for adding CSV export. Record the
> scope, dependencies, and acceptance checks. Do not implement it yet.

**Research**

> Use $plan-strata to compare the existing baseline and candidate results. Allow
> one fixed comparison and deterministic verification, but no new experiments.
> Record the finding and whether to continue, revise, or stop.

**Resume**

> Use $plan-strata to recover this project's current iteration from its files,
> then continue the next authorized task and leave a checked handoff.

The agent writes project records in your language. Use the skill when explicitly
establishing Plan Strata planning or executing, resuming, revising, or accepting work it
already manages. Unbound questions, diagnosis, and small edits do not trigger it.
The current request or an assignment traceable to an approved batch supplies
authority within its scope; CURRENT, `ready`, and tool availability do not.

Implementation and in-scope repair can remain one task:

> Complete the agreed capability, self-check it, and fix defects against its
> existing acceptance criteria. Continue within the current scope and resource
> limits; report the result or a blocker needing my decision. Keep new requirements
> separate; do not push or publish.

Ordinary local repair needs no invented round/test quota or budget ledger; explicit
limits and material resource use still have boundaries. The same worker can continue
under the same assignment, returning new delivery versions without redispatch.
Preserve earlier deliveries/checks and reverify changed inputs. See
[repair and delivery](skills/plan-strata/references/repair-loop.md).

## How the records fit together

Prefer existing project task cards, PR/CI evidence, and progress records. The table
describes the optional bundled format; it is not a second tracking system to add
alongside them. Alternative formats are checked manually, not by the bundled parser.

| Record | Owns |
|---|---|
| `core` | Project purpose, scope, constraints, and stopping boundaries |
| `ex-plan` | One iteration's tasks, dependencies, methods, and acceptance criteria |
| `progress` | Live state, owner, exact execution binding, next action, and check reference |
| `check/` | Inspected artifacts, evidence, scoped verdict, and limitations |
| `CURRENT.md` | The explicitly selected entry point for new Plan-Strata-managed work |

A task retains its declared plan binding when it starts: a versioned plan path
in bundled schema 2, or the project's explicit alternative. No hashes are required
by schema 2. Switching `CURRENT.md` does not silently reassign running tasks.
After relevant inputs change, the designated writer reopens affected acceptance;
authorized reviewers rerun checks. The validator cannot detect those changes.
Integration can remain open even when individual tasks pass.
A valid research activity can finish with a negative or inconclusive finding.

Recover missing or stale context, not the entire record set on every turn.
Implementation, debugging, and test choices can evolve within committed scope,
acceptance, interfaces/dependencies, and resource boundaries. Revise the plan only
when those commitments or fixed research methods change; reuse an unchanged core.

See the [protocol](skills/plan-strata/references/protocol.md) for records and
[acceptance](skills/plan-strata/references/protocol.md#acceptance) for reviews;
[research guidance](skills/plan-strata/references/research.md) adds research-specific rules.

## Optional parallel handoffs

Parallel execution is off unless explicitly authorized for the iteration/batch.
An approved assignment reuses that authority; a proposal request does not authorize
dispatch. No extra skill switch is needed. For example:

> Use $plan-strata and enable parallel handoffs for this iteration. Delegate ready,
> independent tasks to at most two local workers. You are the Manager: inspect
> deliveries and verify the final combined state. Keep work local; do not create
> Issues, push, or merge the default branch.

Use the host's available tools and allocation adapter. A host assignment message
plus its bound task card can be the complete handoff, without another packet.
When an existing adapter guarantees exclusive allocation, the designated writer
records the receipt after the host returns the Agent ID; otherwise record allocation
before execution. Shared interfaces, conflicting writes, and actual resource limits
still need coordination. If delegation is unavailable, use an authorized manual
handoff or sequential execution.

Workers return artifacts, self-checks, and reports ready for review; Reviewers
complete scoped checks. Only an authorized Manager accepts; only the designated
writer updates progress (Manager by default). One agent may fill authorized roles.
Existing CI or a suitable environment can verify the final combined state without
a separate Integrator agent or workspace; actual write conflicts still need isolation.

This mode covers one ex-plan and does not require Git/GitHub. An Issue can carry
the executable task contract with fixed, accessible references. Completeness,
dependency readiness, and allocation are distinct; a packet or Issue does not
launch an agent. External posting, paid jobs, and merges require their own authority.

Pause only actions affected by missing inputs, scope conflicts, or new authority;
continue independent authorized work. Block the task only when its acceptance-critical
path cannot proceed. Explicit stops and shared resource limits still apply.

See [handoff guidance](skills/plan-strata/references/parallel-handoff.md) and the
optional [worker](skills/plan-strata/assets/task-handoff.md) /
[integration](skills/plan-strata/assets/integration-handoff.md) templates.
Contributors can [rebuild the local two-worker trial](evals/README.md#parallel-handoff-trial).
These Markdown contracts are guidance, not machine-validated records or a scheduler.

## Optional read-only validator

After a project-local Codex install, run from the **target project's root**:

```sh
python3 .agents/skills/plan-strata/scripts/strata.py validate --project .
```

The agent must create or adapt the project's planning records first; installation
alone does not create them. For other install locations, adjust the script path.
No hash calculation is part of this workflow.

The helper uses only Python 3.10+ standard-library modules. Its project metadata
is **JSON between `---` delimiters**, followed by Markdown—not arbitrary YAML.
Existing workflows can be checked manually without migrating to this format.

The result explicitly reports `validation_scope: structure_only`.
`status: consistent` means the declared records agree. `overall: accepted` means
the current records meet the iteration's acceptance structure. Neither proves
that inputs are unchanged, tests ran or cover enough cases, evidence is truthful,
or a scientific claim is established. Relevant changes require explicit review;
keep earlier checks and add a new check after affected verification.
The command does not execute commands in Markdown, change records, run experiments,
or upload content. Report inconsistencies first; repair records only when the
current role and write scope authorize it. Other roles return findings to the
responsible writer.

For automation, consult the [exit-code contract](skills/plan-strata/references/protocol.md#reading-validation-output):
validation findings, including an invalid `--current` path, use exit `1`; argument
or project-root startup failures use `2`. Exit `0` alone does not mean completion.

## Try a small example

From a **full clone of this repository**, not an installed skill alone:

```sh
strata_trial_dir=$(mktemp -d)
python3 evals/prepare.py --scenario resume --destination "$strata_trial_dir/project"
python3 skills/plan-strata/scripts/strata.py validate --project "$strata_trial_dir/project"
```

Expected: `consistent / open`—one documentation task is deliberately unfinished.
Give that directory and the skill to a fresh session to continue it. Other synthetic
scenarios cover `switch`, `stale`, `integration`, and `research`.
The [step-by-step walkthrough](docs/FIRST_USE.md) is currently in Chinese.

For contributors:

```sh
python3 -m unittest discover -s tests -v
python3 skills/plan-strata/scripts/strata.py validate --project .
```

## Validation and limits

The [0.2.0-alpha.1 notes](docs/v0.2.0-alpha.1.md) describe the no-hash migration,
current verification, and remaining limitations. Previous validation records below
are historical, not new acceptance of this version.

The initial alpha passed 20 contract tests on Python 3.10 and 3.14, five scenario
types, and a real documentation handoff to an agent without the original chat.
Research results in the scenarios are synthetic. The
[validation record (Chinese)](docs/validation.md) links the retained evidence.
[Release preparation](docs/PUBLISHING.md) separates local installation checks
from the GitHub checks that must happen after pushing.

The [main-branch hotfix record (Chinese)](docs/validation-main-hotfix.md) covers
reserved task IDs, symlink-loop diagnostics, and explicit input-manifest scope.

The initial alpha.2 [parallel-handoff trial (Chinese)](docs/validation-parallel.md)
is historical evidence. Subsequent receiver-baseline and reserved-ID repairs have
[their own regression record (Chinese)](docs/validation-handoff-fixes.md).
The [Issue cold-start record (Chinese)](docs/validation-issue-handoff.md) separately
tracks the local Issue-body → fresh-worktree evaluation and its observed failures.
The [bounded-repair regression record (Chinese)](docs/validation-repair-loop.md)
covers evidence preservation and CLI classifications, not autonomous-agent behavior
or a measured reduction in human handoffs.
These checks do not establish live GitHub dispatch, runtime orchestration, or production concurrency.

- Checks cover explicitly declared local files and dependencies, not implicit ones
  or the truth of their contents. External artifacts need separate verification.
- One writer maintains progress. Concurrent workers need host-level isolation and
  an integration method; this skill supplies neither a scheduler nor a lock.
- No hashes are required. The helper does not read artifact contents, detect drift,
  or assess test coverage. Review relevant changes and retain useful versions with
  existing version control or delivery records; Git itself is optional.
- Long-running production use, real research outcomes, client auto-discovery,
  and cross-client agent behavior have not been established by these trials.

## Join us!

You don't need to write code to contribute. Tell us where a handoff gets stuck,
instructions are unclear, or maintaining records costs more effort than it saves.

Append this **optional** block to your target project's `AGENTS.md`, preserving
its existing instructions. If your agent uses a different project-instruction
file, adapt the location. This collects local observations; nothing is sent
automatically.

```markdown
## Plan Strata usage feedback

While using plan-strata, note observed ambiguity, blocked workflows,
state/evidence mismatches, and unnecessary bookkeeping. Keep the current
project task as the priority.

- At a milestone or handoff, record issues in docs/plan-strata-feedback.md.
  Create the file only when needed, and merge repeated observations.
- Record the available skill version or source, development/research context,
  expected and actual behavior, task impact, workaround, and local evidence
  references or a sanitized minimal example.
  Include the source commit and local edits when known; otherwise mark the source
  unknown and identify the actual installed files, rather than assuming a checkout matches.
- Separate observations from suspected causes. Mark uncertain attribution
  as "needs confirmation"; environment or usage issues may also be responsible.
- Keep task state in the project's existing progress records. The feedback
  file records skill issues, not a second task tracker.
- If an issue compromises data safety or valid acceptance, explain it and
  pause the affected action; otherwise record a justified workaround and continue.
- Changes or upgrades to the installed skill and GitHub submissions require
  separate authorization. Keep private data and credentials out of feedback
  notes, and review/redact any material before sharing it externally.
- No observed issue means no feedback note. Do not launch extra experiments
  solely to look for skill defects.
```

Review your local notes, then [open an issue](https://github.com/Liar-zzy/plan-strata/issues/new)
with one sanitized case. There is no need to upload your full project, chat
history, or unpublished research. Confirmed cases can guide clearer instructions,
regression checks, and simpler workflows.

## Repository and contributions

`skills/plan-strata/` is the distributable package. `plans/` records this skill's own
development, and `evals/` plus `tests/` support reproducible checks. Historical checks
describe their original revisions; they are not new acceptance for changed files.
Private design conversations and temporary trial directories remain Git-ignored.

Keep English and Chinese READMEs aligned when changing user-facing behavior.

Packaging follows [Agent Skills](https://agentskills.io/specification). Design
discussions drew on [Planning with Files](https://github.com/OthmanAdi/planning-with-files),
[Superpowers](https://github.com/obra/superpowers), and the
[COS distinction between exploratory and confirmatory research](https://www.cos.io/initiatives/prereg).
The workflow instructions and helper code were written for this project; those
projects' workflow code was not copied. Licensed under the [MIT License](LICENSE).
