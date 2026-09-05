# Development tasks

Define observable behavior and a proportionate acceptance method. Include changed
interfaces, compatibility constraints, outputs, and dependencies where they matter.
Implementation details can evolve inside that scope without revising the plan.

Record the actual tested source/configuration and the observed output. A commit
alone is insufficient when the worktree is dirty: preserve the relevant patch and
untracked inputs, or fingerprint and retain the actual files. Use the project's
existing test/build tools. A documentation task can use a documented review with
specific observations; it need not invent a runtime test.

Set `integration_required` when separate deliveries must work together. Task
checks do not establish integration. A successful unit test also does not prove
an unrelated compatibility, usability, or performance claim. State the limits.

Before accepting work, inspect evidence rather than simply copying a worker's
completion statement. The same agent may implement and verify low-impact work;
independent review can add confidence for important interfaces or risky changes.
Both forms need explicit methods and provenance.

When a source, configuration, or relevant dependency changes, reconsider checks
that used it. Preserve the historical result and revise current acceptance.
