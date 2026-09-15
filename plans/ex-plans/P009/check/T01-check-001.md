---
{
  "schema": 2,
  "kind": "check",
  "id": "T01-check-001",
  "task": "T01",
  "plan": "plans/ex-plans/P009/ex-plan-v0.1.0.md",
  "verdict": "pass",
  "subjects": [
    "skills/plan-strata/SKILL.md",
    "skills/plan-strata/LICENSE",
    "skills/plan-strata/agents/openai.yaml",
    "skills/plan-strata/scripts/strata.py",
    "skills/plan-strata/references/protocol.md",
    "skills/plan-strata/references/development.md",
    "skills/plan-strata/references/research.md",
    "skills/plan-strata/references/repair-loop.md",
    "skills/plan-strata/references/parallel-handoff.md",
    "skills/plan-strata/assets/core.md",
    "skills/plan-strata/assets/ex-plan.md",
    "skills/plan-strata/assets/CURRENT.md",
    "skills/plan-strata/assets/progress.md",
    "skills/plan-strata/assets/check.md",
    "skills/plan-strata/assets/task-handoff.md",
    "skills/plan-strata/assets/integration-handoff.md",
    "tests/test_workflow.py",
    "tests/test_repair_workflow.py",
    "tests/test_parallel_trial.py",
    "tests/test_issue_trial.py",
    "evals/prepare.py",
    "evals/parallel_trial.py",
    "evals/issue_trial.py",
    "evals/run_checks.py",
    "evals/install_smoke.py",
    "evals/capture.py",
    "evals/README.md",
    "README.md",
    "README.zh-CN.md",
    "docs/FIRST_USE.md",
    "docs/PUBLISHING.md",
    "docs/dev-readiness.md",
    "docs/v0.2.0-alpha.1.md"
  ],
  "evidence": [
    "evals/results/no-hash-py310-002.json",
    "evals/results/no-hash-py314-002.json",
    "evals/results/no-hash-install-002.json",
    "evals/results/no-hash-github-install-001.json",
    "evals/results/no-hash-first-use-001.json",
    "evals/results/no-hash-review-red-001.json"
  ]
}
---

# P009/T01 — 无哈希默认流程验收

检查者 root，2026-09-10。同一 Agent 实现、审查并检查；没有独立审核 Agent，
不把脚本化合成场景称为真实多 Agent 行为评测。

## 实际执行与观察

- Python 3.10.9 与 3.14.7 分别运行 `evals/run_checks.py`：各 77 项通过，exit 0。
  涵盖路径/绑定/依赖/旧 schema 拒绝、无 Git 单任务与修复闭环、负科研结果、可选
  隔离交接、集成和历史保留。测试实际运行小项目命令，不仅匹配说明措辞。
- 新增边界测试先运行失败，复现非字符串/空字符路径异常，以及软链接/硬链接将
  检查文件自身当证据的问题；补入口检查和文件别名判断后重跑通过，red 报告保留。
- 安装冒烟测试先用本地源，再用 GitHub dev URL：Codex/Claude Code 两种项目级
  安装各 16 个包文件直接比较一致，安装后的 validator 返回 schema 2 /
  structure_only / consistent / open，已有项目文件不变；没有全局安装变更。
- 首次使用生成器与 capture 实际运行：隔离目录的求和测试通过，示例输出 6 / 0；
  文档任务仍待完成，因此 consistent/open 为正确结果，不宣称演示整轮完成。
- `quick_validate.py skills/plan-strata`：Skill is valid，exit 0。两份 README
  与当前协议/模板版本一致；20 份 Markdown 本地链接目标检查无缺失；变更无空白错误。
  新补的远端安装命令与实际冒烟测试所用来源/参数一致。
- 当前脚本和安装包不计算内容哈希；保留的 digest 字段名仅用于拒绝旧元数据，
  文档中旧指令仅用于迁移说明/明确标记的历史记录。路径不证明内容未变这一限制
  已在入口、协议、README 和测试中明示。

## 远端核对

实现提交 [10779b6](https://github.com/Liar-zzy/plan-strata/commit/10779b6138e7402552f1528604a585b625de4324)
已向 origin/dev 正常 push。`git ls-remote` 核对到该提交；main 保持原提交
86ef43e2a87fef734e427910f651be3ddbfffce7。
[GitHub Checks 34437294166](https://github.com/Liar-zzy/plan-strata/actions/runs/34437294166)
两版 Python 的测试与当前记录校验均成功。远端安装的技能包与该本地包一致。
发布结果/快捷安装文案的后续记录提交不修改技能或测试代码。

## 判定与限制

接受 0.2.0-alpha.1 作为 dev 预览版。未合入 main、未创建 tag/GitHub Release、未发布
外部 Issue、未上传原始反馈。用户的 .gitignore 改动保持本地，未纳入提交。
正式复核使用一轮成组返修，未扩展原任务范围。

此记录不认证文件内容、覆盖充分性或长期运行效果。相关输入改变时由 Manager
显式重新打开受影响验收并实际复测；校验器不会自动检测。历史 schema 1 需要明确
迁移，不可只改数字。并行默认关闭，预算、认领和取消仍依赖宿主与单一协调者。
下一步为用户按需要试用已发布的 dev 副本并记录实际反馈；本轮不自动升级安装。
