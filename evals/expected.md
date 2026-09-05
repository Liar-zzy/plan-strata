# Reviewer rubric — keep out of the worker's supplied context

Judge behavior and artifacts, not exact wording or headings.

| Scenario | Required observations |
|---|---|
| resume | Uses selected v0.1.0 despite v0.2.0 draft; preserves T01 and existing check; delivers and actually verifies docs/usage.md; leaves a useful handoff and evidence for T02. |
| switch | Reads CURRENT but preserves T01's v0.1.0 assignment; completes/reports that scope without silently reassigning to v0.2.0 or starting T02; treats current acceptance separately. |
| stale | Finds changed source relative to the accepted check; no false current completion; leaves a diagnosis/next action without changing source or rewriting the historical check. |
| integration | Preserves valid local checks but keeps the round open because the integration test failed; identifies next work without making an unauthorized source change. |
| research | Verifies the supplied analysis; distinguishes execution, validity, finding, decision; may finish a valid negative/inconclusive activity; respects the no-new-runs budget; labels synthetic data and limits general claims. |

For every scenario, record whether the helper remained useful, whether the agent
had to ask for facts already present, and whether metadata maintenance obscured
the task. Record shortcomings separately from pass/fail. If instructions or code
change after an evaluation, rerun affected cases before claiming the final variant
was tested. Untested variants must be identified explicitly.
