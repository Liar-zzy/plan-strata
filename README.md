# Plan Strata

English · [简体中文](README.zh-CN.md)

Versioned plans, recoverable progress, and evidence-based handoffs for AI-assisted software development and research.

Plan Strata is an open-source agent skill for work that spans sessions. It helps an
agent recover what was agreed, which plan a task started under, what was actually
checked, and what to do next. Development and research tasks can share one plan
without sharing the same meaning of success.

**Status: `0.1.0-alpha.1` · MIT · Python 3.10+ for the optional validator.**
Ready for early trials, not a production workflow guarantee.

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

The GitHub commands require the repository to contain this package. Before the
first push, replace `Liar-zzy/plan-strata` with the absolute path to this checkout.
This is a standalone skill, not a marketplace plugin.

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

The agent writes project records in your language. You provide the scope and
resource limits; the skill guides the file and evidence bookkeeping. Ordinary
questions and isolated small edits usually do not need a planning directory.

## How the records fit together

| Record | Owns |
|---|---|
| `core` | Project purpose, scope, constraints, and stopping boundaries |
| `ex-plan` | One iteration's tasks, dependencies, methods, and acceptance criteria |
| `progress` | Live state, owner, exact execution binding, next action, and check reference |
| `check/` | Inspected artifacts, evidence, scoped verdict, and limitations |
| `CURRENT.md` | The explicitly selected entry point for new work |

A task binds to an exact plan when it starts. Switching `CURRENT.md` does not
silently reassign running tasks. Evidence that no longer matches the inspected
files needs review. Integration can remain open even when individual tasks pass.
A valid research activity can finish with a negative or inconclusive finding.

The [protocol](skills/plan-strata/references/protocol.md) defines the records;
[development](skills/plan-strata/references/development.md) and
[research](skills/plan-strata/references/research.md) guidance define acceptance.

## Optional read-only validator

After a project-local Codex install, run from the **target project's root**:

```sh
python3 .agents/skills/plan-strata/scripts/strata.py validate --project .
```

The agent must create or adapt the project's planning records first; installation
alone does not create them. For other install locations, adjust the script path.
To fingerprint a file, use the same script with
`fingerprint --project . path/to/file`.

The helper uses only Python 3.10+ standard-library modules. Its project metadata
is **JSON between `---` delimiters**, followed by Markdown—not arbitrary YAML.
Existing workflows can be checked manually without migrating to this format.

`status: consistent` means the declared records agree. `overall: verified` means
the current records meet the iteration's acceptance structure. Neither proves
that tests ran, evidence is truthful, or a scientific claim is established.
The command does not execute commands in Markdown, change records, run experiments,
or upload content.

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

The initial alpha passed 20 contract tests on Python 3.10 and 3.14, five scenario
types, and a real documentation handoff to an agent without the original chat.
Research results in the scenarios are synthetic. The
[validation record (Chinese)](docs/validation.md) links the retained evidence.
[Release preparation](docs/PUBLISHING.md) separates local installation checks
from the GitHub checks that must happen after pushing.

- Checks cover explicitly declared local files and dependencies, not implicit ones
  or the truth of their contents. External artifacts need separate verification.
- One writer maintains progress. Concurrent workers need host-level isolation and
  an integration method; this skill supplies neither a scheduler nor a lock.
- Hashes identify bytes; they are not tamper-proof signatures. Version control and
  workflow discipline preserve historical snapshots.
- Long-running production use, real research outcomes, client auto-discovery,
  and cross-client agent behavior have not been established by these trials.

## Repository and contributions

`skills/plan-strata/` is the distributable package. `plans/` records this skill's own
development, and `evals/` plus `tests/` support reproducible checks. Historical checks
describe their original revisions; they are not new acceptance for changed files.
Private design conversations and temporary trial directories remain Git-ignored.

Please [open an issue](https://github.com/Liar-zzy/plan-strata/issues) with a minimal,
sanitized starting state, your request, observed behavior, and expected difference.
Keep English and Chinese READMEs aligned when changing user-facing behavior.

Packaging follows [Agent Skills](https://agentskills.io/specification). Design
discussions drew on [Planning with Files](https://github.com/OthmanAdi/planning-with-files),
[Superpowers](https://github.com/obra/superpowers), and the
[COS distinction between exploratory and confirmatory research](https://www.cos.io/initiatives/prereg).
The workflow instructions and helper code were written for this project; those
projects' workflow code was not copied. Licensed under the [MIT License](LICENSE).
