---
{
  "schema": 2,
  "kind": "check",
  "id": "T01-check-002",
  "task": "T01",
  "plan": "plans/ex-plans/P011/ex-plan-v0.1.0.md",
  "verdict": "pass",
  "subjects": [
    "skills/plan-strata/SKILL.md",
    "skills/plan-strata/references/protocol.md",
    "skills/plan-strata/scripts/strata.py",
    "tests/test_workflow.py",
    "tests/test_issue_trial.py",
    "tests/test_parallel_trial.py",
    "tests/test_repair_workflow.py",
    "evals/prepare.py",
    "evals/parallel_trial.py",
    "evals/issue_trial.py",
    "evals/run_checks.py",
    "README.md",
    "README.zh-CN.md",
    "docs/FIRST_USE.md",
    "docs/PUBLISHING.md",
    "docs/v0.2.0-alpha.1.md",
    "docs/validation-main-hotfix.md",
    "plans/ex-plans/P005/ex-plan-v0.1.0.md",
    "plans/ex-plans/P005/progress.md",
    "plans/ex-plans/P005/check/T01-check-001.md"
  ],
  "evidence": [
    "evals/results/main-merge-001.json",
    "evals/results/main-merge-002.json",
    "plans/ex-plans/P011/check/T01-check-001.md"
  ]
}
---

# P011/T01 — main 合并复核

2026-09-15，root 完成合并、审阅并按当前用户授权接受，仍为唯一 progress writer。
原 main 为 86ef43e，dev 的精简交付为 ba8e509；用户已明确批准整体合入并正常
推送 main，不强推、不创建发布/标签、不升级安装。这是 P011 的后续交付复核，
不改写原计划、check-001 或此前历史。

## 合并决策

- README 保留双方的历史验证链接，安装来源改为 main；旧 dev 发布说明标明
  历史日期，不把旧安装/CI 结果当作本次远端验证。
- CURRENT 沿用 schema 2 / P011，保留 main 的 P005 历史，不继续选择 schema 1。
- 协议与测试采用已批准的 schema 2。旧版的 SHA/指纹用例不重新引入；保留任务
  标识与路径诊断修复已在 dev 中，main 的原修复并未丢失。
- Git 自动合并重复加入了 resolve_path，去重后技能包、测试及 evals Python 代码
  与 dev 相同。主分支独有的 8 个验收/日志/说明文件逐字节核对，均完整保留。

## 实际检查

- 合并后的两轮 `evals/run_checks.py` 均通过现有 77 项测试，Python 3.14.7，exit 0。
  第一轮后仅恢复测试文件的一个空行；最终报告为
  [main-merge-002.json](../../../../evals/results/main-merge-002.json)。
- 技能格式检查输出 `Skill is valid!`，exit 0；包内容与 ba8e509 一致，沿用
  [check-001](T01-check-001.md) 的指令审阅，仅对本次组合及说明变化重新验收。
- 本地链接检查覆盖两份 README、FIRST_USE、PUBLISHING、版本说明、evals/README、
  当前 core/入口、技能包及当时 P011 文件：23 个 Markdown 文件、87 引用、0 错误。
- 本次修改的差异通过 `git diff --check`。相对旧 main 的全量 staged 检查报告
  P003/check/T01-check-001.md 与 P008/check/T01-check-001.md 的既有 EOF 空行；
  已确认两份冻结记录与 dev 原文一致，保留历史，不做无关格式清理。
- 接受前 validator 为 `consistent / open`，T01 为 needs_review，无错误或警告。
  相关工作区差异及主分支历史已实际核对，不以结构输出代替合并审阅。

## 决定与限制

接受本地最终合并状态，允许依据用户请求提交并推送 main。远端推送和本次 GitHub
CI 尚待执行，应以最终 merge commit 的远端 ref/Checks 为准，不在此预先宣称成功。
未运行新的客户端发现、安装冒烟或独立 Agent 行为测试；未发布标签或更改安装副本。
