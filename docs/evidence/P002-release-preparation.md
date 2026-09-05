# P002 — Release preparation checks

Date: 2026-09-05. Reviewer: root. Scope: local preparation for the first public
alpha at [Liar-zzy/plan-strata](https://github.com/Liar-zzy/plan-strata).
The installed skill remains `0.1.0-alpha.1`; this round changes repository-level
documentation and release checks, not the skill's workflow or runtime helper.

## Observed results

| Check | Result | Evidence |
|---|---|---|
| Project-local Codex installation | Pass: all 12 package files match; installed validation and fingerprint commands exit 0; existing project files unchanged | [Installation log](../../evals/results/install-local-001.json) |
| Project-local Claude Code installation | Pass: all 12 package files match through its installation path; the same installed commands exit 0; existing files unchanged | Same installation log |
| Python 3.10 contract suite | 20 tests pass, exit 0 | [Python 3.10](../../evals/results/release-py310-001.json) |
| Python 3.14 contract suite | 20 tests pass, exit 0 | [Python 3.14](../../evals/results/release-py314-001.json) |
| Skill packaging | Bundled skill-creator validator reports `Skill is valid!`, exit 0 | Local format check; temporary PyYAML environment, no added runtime dependency |
| README example | English and Chinese shell blocks match; extracted demo commands run successfully and return `consistent / open` as documented | [Documentation checks](../../evals/results/release-docs-001.json) |
| GitHub Actions configuration | YAML parses; matrix, triggers, read-only permissions, disabled credential persistence, and pinned action commits checked | Static review only; GitHub has not run this workflow |

The installation check used Node.js v26.7.0 and Skills CLI 1.5.23 with telemetry
disabled. Its source was this local checkout, not GitHub. Each target was a new
temporary synthetic project. The report keeps command results and package hashes;
temporary directories are cleaned up. Known source, temporary, and interpreter
paths are replaced by labels in the report.

The optional checker is reproducible with `python3 evals/install_smoke.py`.
The exact package files plus the smoke-check implementation and fixture generator
are fingerprinted in its report. The test reports likewise identify their source
files. These hashes were compared to the final files during preparation.

## Documentation and publication boundary

The English and Chinese READMEs describe the same installation choices, development
and research examples, record responsibilities, validator semantics, and alpha
limits. Installation instructions distinguish a full development checkout from
the standalone skill and explain that installing a skill does not initialize a
target project's plans. A copy-ready About description, topics, and release draft
are in [Publishing](../PUBLISHING.md).

Publishable files were checked for recognizable private-key, GitHub-token,
OpenAI-style API-key, and AWS access-key patterns; none were found. The original
conversation export and temporary trial directories are excluded by Git. This is
a limited pattern scan and file review, not a comprehensive security audit.
Historical evaluation captures contain synthetic work, agent labels, and local
paths; they are intentionally retained as evidence, not installed with the skill.

P001's plan and checks are unchanged. Its original README remains available in
Git commit `409f31d`. P002 supplies acceptance for the new release-facing documents
without rewriting the old pass or claiming it still covers changed bytes.

## Still unverified

- Public GitHub download and installation after the first push.
- Actual execution of GitHub Actions on its hosted runners.
- Skill discovery and invocation in either client, and behavior across clients.
- User-global installation and the Codex built-in installer route; these are
  documented alternatives, not executed checks in this round.
- Long-term production workflows or real scientific experiments.

The remote repository was empty when inspected. No push, remote configuration,
About change, tag, or release was performed. Local packaging is ready for an alpha
publication handoff; follow the post-push checks before treating distribution as
verified. Permission to push or create a release remains a separate user decision.
