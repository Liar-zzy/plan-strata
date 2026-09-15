---
{
  "schema": 2,
  "kind": "check",
  "id": "T01-check-001",
  "task": "T01",
  "plan": "plans/ex-plans/P011/ex-plan-v0.1.0.md",
  "verdict": "pass",
  "subjects": [
    "skills/plan-strata/SKILL.md",
    "skills/plan-strata/agents/openai.yaml",
    "skills/plan-strata/references/protocol.md",
    "skills/plan-strata/references/parallel-handoff.md",
    "skills/plan-strata/references/repair-loop.md",
    "skills/plan-strata/references/research.md",
    "skills/plan-strata/assets/ex-plan.md",
    "skills/plan-strata/assets/task-handoff.md",
    "skills/plan-strata/assets/integration-handoff.md",
    "skills/plan-strata/assets/progress.md",
    "skills/plan-strata/assets/core.md",
    "skills/plan-strata/assets/check.md",
    "skills/plan-strata/assets/CURRENT.md",
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
    "evals/README.md"
  ],
  "evidence": ["evals/results/production-simplification-001.json"]
}
---

# P011/T01 — 生产流程精简验收

2026-09-15，root 实现、自检并依据本轮授权接受；root 为唯一 progress writer。
检查对象为 dev 本地工作区，本轮开始时已包含未提交的 P010 修订，不以 HEAD
冒充本次被检内容版本。沿用 core v0.5、schema 2 和原校验器；无运行代码修改。

## 精简结果

以本轮开始时的文件为基线，使用 `wc -l -w` 统计：SKILL.md 从 133 行 / 1112 词
降至 78 行 / 607 词；入口、references 与 assets 从 788 行 / 6250 词降至
516 行 / 3695 词，总词数减少 40.9%。这是空白分词统计，不是模型 token 或成本测量。
删除 `references/development.md`，必要验收内容并入协议，现行文档链接已更新；
删除文件可从 Git 历史恢复，不改写旧验收记录中的历史路径。

## 静态场景核对

以下是对最终指令及模板的人工推演，不是独立 Agent 执行结果。

| 场景 | 核对结论 |
|---|---|
| 普通本地返修，用户未给次数额度 | 沿用现有范围及宿主限制，不自设返修/测试配额或台账；停滞时调查原因，不无限重复失败方法。 |
| 明确限额、科研或付费计算 | 实际资源边界仍有效，跨重试/Worker 累计使用，不把未知消耗当零；负结果不是额外实验授权。 |
| 同一 Worker 交付后继续修复 | 沿用派工，产生新交付版本和报告，保留旧产物/证据；同版本内容改变须调查，重派须隔离旧执行。 |
| 项目已有 CI/集成环境 | 复用它检查最终组合状态，不强制独立 Agent、目录或 packet；相关冲突修复须更新受影响检查，接收状态须匹配被检状态。 |
| 恢复时已有可靠上下文，CURRENT 已切换 | 只补齐缺失/过时及下一步所需内容，原任务保持绑定；不按版本号或文件时间猜入口。 |
| 实现或测试策略调整；固定科研方法调整 | 承诺内实现细节不修计划；约定范围、验收、接口依赖、资源边界或固定科研方法变化才建修订，已用版本保持不变。 |
| 已有任务卡、PR/CI 和进度记录 | 优先复用，替代格式手工核对；bundled schema 2 仍需要真实本地记录及路径，不把远端链接伪装成可校验文件。 |
| 只读 Reviewer 发现记录错误 | 返回范围内结论或建议，不自动写 check、progress 或修复记录；获准 Manager 接受，指定 writer 记 done。 |
| 未绑定小改，或请求仅要求建议 | 不自动纳入管理，不因 CURRENT/ready/工具可用而实施或派工；已批准批次可复用宿主派工与绑定任务卡。 |
| 某动作缺输入、冲突或需新权限 | 只暂停受影响动作，继续独立授权工作；验收关键路径无法继续才整体阻塞，明确停止和共享限额除外。 |

## 实际验证

- `python3 evals/run_checks.py --output evals/results/production-simplification-001.json`：
  Python 3.14.7，77 项现有测试通过，5.627 秒，exit 0；见
  [原始报告](../../../../evals/results/production-simplification-001.json)。
  覆盖结构校验、模板生成和既有交接/返修 fixture；未增写文本匹配测试。
- skill-creator 的 `quick_validate.py skills/plan-strata`：`Skill is valid!`，exit 0。
  复用 P010 临时 venv 的 PyYAML；openai.yaml 实际解析及界面字段检查通过。
  未新增项目或技能依赖。
- 本地链接检查读取两份 README、FIRST_USE、evals/README、CURRENT、core v0.5、
  技能包与当时的 P011 文件，解析 Markdown 目标及标题锚点：20 文件、74 引用、
  0 错误，exit 0。
- `git diff --check` 通过；校验器、测试及 evals Python 文件均无差异。
- 接受前运行 `strata.py validate --project .` 得到 `consistent / open`，无错误或
  警告，T01 为 in_progress；未用结构一致替代上述验收。

## 决定与限制

接受这轮本地精简。测试 fixture 自选的固定次数、独立目录和单 attempt 单交付
规则已在 evals/README 限定为场景配置，不作为新版技能的通用要求。
未验证同一派工多版本传输的宿主实现、独立 Agent 行为、真实 CI 派发或生产并发；
现有 77 项测试不能证明这些新增指导会被模型稳定执行，也不能证明成本下降。
保留 P010 及更早历史，未提交、推送、发布或升级安装。
