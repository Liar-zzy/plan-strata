# T02 首次使用验证证据

执行与记录者：handoff-agent；日期：2026-09-05（Asia/Shanghai）。本记录保留
本次工具实际返回的命令输出，由执行者转录；未把初始交接文字中的通过声明作为证据。
检查范围是根项目 P001/T02 的首次使用说明。实际执行代码与配套样例可在本副本
复查，没有启动背景作业，也没有开展发布或其它任务验收。

## 环境与起点

工作目录：`/tmp/plan-strata-eval.61HMhi/handoff`。macOS 在子 shell 中解析为
`/private/tmp/plan-strata-eval.61HMhi/handoff`，两者指向同一隔离副本。

执行 `date -u '+%Y-%m-%dT%H:%M:%SZ'`、`uname -sr`、`python3 --version`、
`command -v python3`；均 exit 0，输出依次为：

```text
2026-09-05T13:07:38Z
Darwin 25.4.0
Python 3.14.7
/opt/homebrew/bin/python3
```

执行 `python3 skills/plan-strata/scripts/strata.py --help`，exit 0；显示两个子命令
`validate` 与 `fingerprint`，帮助文字为 Python 3.10+、标准库、只读检查。
本机仅实测 Python 3.14.7 和 zsh；Python 3.10 是项目声明的最低要求，未逐版本验证。

接手前执行 `python3 skills/plan-strata/scripts/strata.py validate --project .`，
exit 0，实际结果为 `status: consistent`、`overall: open`、`errors: []`；
T01 `needs_review`、T02 `planned`、T03 `planned`。唯一 warning 是
`INTEGRATION_OPEN: An integration check is still required`。选中计划为
`plans/ex-plans/P001/ex-plan-v0.1.0.md`，哈希
`67d145264016c002c49bb450d6075c7011b697d846c60e38d12c4383b2516f0f`。

## 直接执行说明中的命令

完整命令块保存在 `docs/FIRST_USE.md`，没有另抄一份脚本。实际从文档提取唯一
`sh` 代码块交给干净 zsh 执行：

```sh
sed -n '/^```sh$/,/^```$/p' docs/FIRST_USE.md | sed '1d;$d' | /bin/zsh -f
```

工具返回 exit 0。代码块启用了 `set -eu`，生成、校验、指纹、小项目测试、数值
示例与仓库测试均实际执行完成；末尾 `OK` 对应 20 项自动测试。stdout 与 stderr
合并记录如下：

```text
Python 3.14.7
技能路径：/private/tmp/plan-strata-eval.61HMhi/handoff/skills/plan-strata/SKILL.md
试用项目：/private/tmp/plan-strata-eval.61HMhi/handoff/.first-use.FboYry/project
/private/tmp/plan-strata-eval.61HMhi/handoff/.first-use.FboYry/project
{
  "schema": 1,
  "status": "consistent",
  "overall": "open",
  "tasks": [
    {
      "id": "T01",
      "state": "done",
      "effective_state": "done",
      "plan": "plans/ex-plans/P001/ex-plan-v0.1.0.md",
      "owner": "fixture-worker",
      "next": "Accepted; continue the dependent documentation"
    },
    {
      "id": "T02",
      "state": "planned",
      "effective_state": "planned",
      "plan": null,
      "owner": "fixture-worker",
      "next": "Write and verify docs/usage.md"
    }
  ],
  "current_plan": "plans/ex-plans/P001/ex-plan-v0.1.0.md",
  "errors": [],
  "warnings": []
}
[
  {
    "path": "plans/ex-plans/P001/ex-plan-v0.1.0.md",
    "sha256": "04486175d73174db58508bad9c3b2034b979b37a83a353d25c3b80afdf22e9f8"
  },
  {
    "path": "src/calc.py",
    "sha256": "3251dbf18617cd67c47707cb9bd1611dbac212ff0ee9814a75b8ce1f34b85aad"
  },
  {
    "path": "tests/check_total.py",
    "sha256": "103b39641f71cf4d1206a265b4298ab32940c5e7a238b4cca9147db49d7222cc"
  },
  {
    "path": "observations/total.log",
    "sha256": "e64e4370447eb3c0e52e27deb52ce7bc24ee926baea16026fc46ba31cc308da0"
  }
]
empty input and numeric sum passed
6
0
test_acceptance_propagates_through_dependencies (test_workflow.WorkflowTests.test_acceptance_propagates_through_dependencies) ... ok
test_changed_evidence_is_detected (test_workflow.WorkflowTests.test_changed_evidence_is_detected) ... ok
test_changed_plan_and_core_are_detected (test_workflow.WorkflowTests.test_changed_plan_and_core_are_detected) ... ok
test_changed_subject_revokes_current_acceptance_without_rewriting_history (test_workflow.WorkflowTests.test_changed_subject_revokes_current_acceptance_without_rewriting_history) ... ok
test_dependency_cycle_is_rejected (test_workflow.WorkflowTests.test_dependency_cycle_is_rejected) ... ok
test_done_requires_check (test_workflow.WorkflowTests.test_done_requires_check) ... ok
test_fixture_preparation_refuses_overwrite (test_workflow.WorkflowTests.test_fixture_preparation_refuses_overwrite) ... ok
test_local_success_with_failed_integration_stays_open (test_workflow.WorkflowTests.test_local_success_with_failed_integration_stays_open) ... ok
test_malformed_metadata_returns_a_diagnostic (test_workflow.WorkflowTests.test_malformed_metadata_returns_a_diagnostic) ... ok
test_old_acceptance_cannot_silently_carry_into_new_revision (test_workflow.WorkflowTests.test_old_acceptance_cannot_silently_carry_into_new_revision) ... ok
test_path_escape_and_external_symlink_are_rejected (test_workflow.WorkflowTests.test_path_escape_and_external_symlink_are_rejected) ... ok
test_research_check_requires_separate_interpretation (test_workflow.WorkflowTests.test_research_check_requires_separate_interpretation) ... ok
test_resume_selects_pointer_and_does_not_treat_consistency_as_completion (test_workflow.WorkflowTests.test_resume_selects_pointer_and_does_not_treat_consistency_as_completion) ... ok
test_running_task_retains_old_binding_after_switch (test_workflow.WorkflowTests.test_running_task_retains_old_binding_after_switch) ... ok
test_selected_draft_is_rejected (test_workflow.WorkflowTests.test_selected_draft_is_rejected) ... ok
test_stale_check_on_open_task_is_a_warning (test_workflow.WorkflowTests.test_stale_check_on_open_task_is_a_warning) ... ok
test_unrelated_file_does_not_invalidate_a_scoped_check (test_workflow.WorkflowTests.test_unrelated_file_does_not_invalidate_a_scoped_check) ... ok
test_valid_negative_research_can_complete (test_workflow.WorkflowTests.test_valid_negative_research_can_complete) ... ok
test_validator_is_read_only_and_cli_returns_json (test_workflow.WorkflowTests.test_validator_is_read_only_and_cli_returns_json) ... ok
test_wrong_check_cannot_satisfy_another_task (test_workflow.WorkflowTests.test_wrong_check_cannot_satisfy_another_task) ... ok

----------------------------------------------------------------------
Ran 20 tests in 0.680s

OK
```

生成器保留的原始日志 `.first-use.FboYry/project/observations/total.log` 已读取核对：

```text
$ /opt/homebrew/opt/python@3.14/bin/python3.14 tests/check_total.py
empty input and numeric sum passed

exit_code: 0
```

`.first-use.FboYry/project/SCENARIO.md` 明确标注合成演示。该项目仅用于验证说明，
没有作为另一项任务被继续执行；它的 T02 保持 planned，不能混入根项目验收。

## 文档审阅与实现边界

执行后逐段读取 FIRST_USE，对照实际实现、模板与协议检查：入口与工作目录明确；
命令中的项目路径正确；声明了完整仓库与独立技能包的区别；期望结果与输出一致；
能给新会话提供具体技能路径、项目路径和接手请求；说明了开始时的计划绑定、
检查证据、完成与集成条件、修订保留以及开发和科研检查的区别。

运行前后分别执行 `shasum -a 256` 检查了
`docs/evidence/T02-source-baseline.sha256` 中的 18 个文件，返回值均为 0，
逐项输出相同。该清单包括技能全部文本文件、生成器、自动测试、README、选中
计划、core 与 CURRENT。它记录实际本地文件字节，用于复核未改动实现与执行基线。

本次限于本地文档和命令验证，不代表 T01 整体验收、T03 的独立场景试用、安装
客户端兼容性、跨 Python 版本行为、长期使用效果或发布完成。根项目最终记录
校验输出另存于 `docs/evidence/T02-final-validation.md`，避免混淆演示与实际任务。
