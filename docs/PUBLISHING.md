# Publishing Plan Strata

> The first-release draft and P002 evidence below are historical. For the current
> dev prerelease, source selection, and schema migration, see
> [0.2.0-alpha.1](v0.2.0-alpha.1.md). Do not use the old release title or assume
> the default-branch install fetches dev.

Target: [Liar-zzy/plan-strata](https://github.com/Liar-zzy/plan-strata).
First release: `v0.1.0-alpha.1`, marked as a **pre-release**.
This is a standalone Agent Skills package, not a marketplace submission.

## GitHub About

Description (copy as one line):

```text
An agent skill for versioned plans, recoverable progress, and evidence-based handoffs in software development and research.
```

Suggested topics:

```text
agent-skills codex claude-code project-planning research-workflow reproducibility markdown
```

Leave Website empty unless there is a separate documentation site. The README is
the main entry point. English and Chinese versions link to each other.

## English introduction

Plan Strata is an open-source agent skill for software development and research
that spans multiple sessions. It separates project intent, execution plans, live
progress, and verification evidence so an agent can recover the agreed scope,
continue authorized work, and leave a useful handoff. Tasks stay bound to the plan
they started under, and research can conclude with a valid negative result rather
than an endless search for a positive one.

## Release title and notes

Title: **Plan Strata v0.1.0-alpha.1 — First public alpha**

Draft release body:

> Plan Strata brings versioned plans and evidence-based handoffs to AI-assisted
> software development and research. This first alpha includes a standalone agent
> skill, Markdown record templates, development and research guidance, and an
> optional read-only validator using Python's standard library.
>
> The workflow preserves task-to-plan bindings across revisions, keeps live state
> in one progress record, and distinguishes task completion from integrated
> acceptance. Research checks separate activity validity, findings, and the next
> decision—including stopping after a negative result.
>
> Initial validation includes 20 contract tests on Python 3.10 and 3.14, synthetic
> recovery and evidence scenarios, and a real documentation handoff without the
> original chat history. These trials do not establish long-term production
> reliability, real scientific validity, or cross-client agent behavior.
>
> Install with `npx skills add Liar-zzy/plan-strata --skill plan-strata`.
> See the bilingual README for installation scope, usage, evidence, and limitations.
> Feedback with small, sanitized reproductions is welcome. Licensed under MIT.

## Local checks before pushing

From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 skills/plan-strata/scripts/strata.py validate --project .
python3 evals/install_smoke.py
```

The optional installation check uses `skills@1.5.23`, needs Git, Node.js 22.20+,
and npm access, and installs only into new temporary projects. It compares the
complete installed payload for Codex and Claude Code against the local package,
runs the installed structural validator, and checks that existing
project files remain unchanged. It neither launches either client nor installs
skills globally. Telemetry is disabled for this check.

Review the Git diff and the actual files to be committed. The installable package
must include its own LICENSE, references, assets, and helper, not just SKILL.md.
Keep `agent-plan-session-export/`, trial directories, caches, credentials, and
private research data out of the commit. Historical evaluation records retain
synthetic artifacts and local path labels; review any new captures before sharing.

The [CI workflow](../.github/workflows/check.yml) runs the contract suite and current
record validation on Python 3.10 and 3.14. Actions have read-only repository
permissions, no persisted checkout credential, and pinned action commits. The
network-dependent installation check is a release check, not part of every PR.

Local evidence for this preparation round is recorded in
[P002 release checks](evidence/P002-release-preparation.md). Old P001 checks refer
to their original bytes (Git commit `409f31d`); they do not accept the new README.

## After the first authorized push

1. Confirm both README pages render and their links work on GitHub.
2. Wait for the Checks workflow to pass. Local results are not GitHub CI results.
3. From a checkout of the pushed revision, run:

   ```sh
   python3 evals/install_smoke.py --source Liar-zzy/plan-strata
   ```

   This additionally checks the public GitHub retrieval path and compares it with
   that checkout. A local-source pass cannot establish this remote result.
4. Check skill discovery and one explicit invocation in the intended client before
   advertising that client's behavior as verified.
5. Set the About text and topics. After approval to create a release, tag the
   reviewed commit as `v0.1.0-alpha.1` and publish the notes above as a pre-release.

These are follow-up actions, not a claim that the repository has already been
pushed, CI has run, a tag exists, or a release has been published. Remote writes
remain deferred until the maintainer requests them.

For a reproducible skill revision after a tag exists, use the full skill directory
URL with that tag (or an immutable commit), rather than an unpinned default branch.
See the [Skills CLI source formats](https://github.com/vercel-labs/skills#source-formats)
and [Codex skill discovery guidance](https://learn.chatgpt.com/docs/build-skills).
