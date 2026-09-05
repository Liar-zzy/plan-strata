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

In a fresh project directory, the `stale` scenario is intentionally inconsistent;
the validator exits 1. The `integration` scenario has structurally consistent but
unsuccessful integration and remains open. These starting conditions are useful
inputs, not failures of the scenario generator.

The first forward use also exposed a limitation in `integration`: its inherited
documentation check points only to unit-test output. This imperfect record is
retained as a useful semantic review case. A verifier can establish the actual
documentation behavior directly; structural consistency alone does not do so.

Use `run_checks.py --output <new-file.json>` to preserve a contract-test run.
After a worker finishes, `capture.py` can preserve its files, skill fingerprints,
and a new validator result. Both commands retain earlier reports by refusing to
overwrite an existing output file.
