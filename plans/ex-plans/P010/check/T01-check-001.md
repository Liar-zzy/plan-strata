---
{
  "schema": 2,
  "kind": "check",
  "id": "T01-check-001",
  "task": "T01",
  "plan": "plans/ex-plans/P010/ex-plan-v0.1.0.md",
  "verdict": "pass",
  "subjects": [
    "skills/plan-strata/SKILL.md",
    "skills/plan-strata/agents/openai.yaml",
    "skills/plan-strata/references/protocol.md",
    "skills/plan-strata/references/parallel-handoff.md",
    "skills/plan-strata/references/repair-loop.md",
    "skills/plan-strata/assets/task-handoff.md",
    "skills/plan-strata/assets/integration-handoff.md",
    "skills/plan-strata/assets/progress.md",
    "README.md",
    "README.zh-CN.md"
  ],
  "evidence": ["evals/results/authority-boundaries-001.json"]
}
---

# P010/T01 — 指令边界与宿主交接验收

审阅者 root，2026-09-15；同一 Agent 实现、自检并以本轮 Manager 身份接受，
root 为唯一 progress writer。依据当前用户批准的本地更新范围，检查相对
2ae6e07 的相关差异。八条反馈已按既定结论落实，第六条保留 schema 2 无哈希协议。

## 静态场景核对

以下为最终指令的逐项推演，不是新 Agent 的实际执行记录。

| 场景 | 核对到的规则 |
|---|---|
| 未绑定的问答、诊断、小改，即使仓库有 CURRENT | 入口描述不自动触发；明确要求建立计划和已管理任务的执行仍有入口。 |
| 已批准批次通过宿主消息和绑定任务卡直接派工 | 组合内容满足交接契约即可，沿用已有宿主独占分配；不增加 packet 或开工前 owner 登记门槛。Agent ID 返回后由 writer 记回执。 |
| CURRENT/ready 存在，但当前请求仅要求检查或建议 | 只执行已请求的检查/建议；计划和工具不能授权实施、派工或新的外部动作。 |
| 某分支输入缺失或需要新外部授权，另有独立工作 | 暂停受影响动作，继续独立的授权工作；验收关键路径无法继续时才整任务阻塞，显式停止和共享预算仍有效。 |
| Worker 完成交付，或 Reviewer 得到通过结论 | Worker 返回产物、自检和报告；Reviewer 完成 scoped check；由获准 Manager 决定接受，不新增状态。 |
| Manager 与 progress writer 是不同角色 | Manager 给出接受决定，只有指定 writer 写入 done；默认 Manager 兼任 writer。 |
| 只读 Reviewer 发现 validator 不一致或证据失效 | 在回复或获准报告中返回结论，不强制创建 check 文件；未经相应写入授权不修记录、不重开状态、不清 integration_check。 |
| 项目已有 task-card revision 等替代绑定 | 使用项目明示绑定；bundled schema 2 仍使用版本化路径，不伪造哈希、不强制迁移；路径不能证明内容未变。 |
| 单 Agent 获准完成并验收任务 | 可以兼任执行、审阅、Manager/writer，使用实际检查完成验收，不新增人类确认节点。 |

核对范围包含入口、协议、并行交接、有限返修、三个相关模板及中英文 README。
默认提示现在仅在当前请求或派工授权时执行下一项动作。

## 实际验证

- `python3 evals/run_checks.py --output evals/results/authority-boundaries-001.json`：
  Python 3.14.7，77 项现有合约测试通过，exit 0。日志见
  [合约测试报告](../../../../evals/results/authority-boundaries-001.json)。
  覆盖现有结构校验、模板生成、隔离交接和返修 fixture 的兼容性。
- skill-creator 的 `quick_validate.py skills/plan-strata`：`Skill is valid!`，exit 0。
  系统 Python 首次缺少 yaml；使用临时 venv 的 Python 3.14.7 / PyYAML 6.0.3 完成，
  未为技能加入运行依赖。openai.yaml 实际解析成功，界面字段及技能调用名检查通过。
- 本地 Markdown 链接检查：对技能包、两份 README 和本轮当时已有的计划文件逐一
  解析链接，检查本地文件及标题锚点；19 个文件、70 处引用，无缺失目标，exit 0。
- `git diff --check`：exit 0。Python 运行代码与现有测试文件均无改动。
- 写入验收前，本轮 validator 返回 `consistent / open`，无错误或警告；当时任务
  为 in_progress，符合预期。结构一致性不作为上述语义核对或实际测试的替代。

## 接受与限制

接受本地指令修订。保留版本标记 0.2.0-alpha.1、schema 2、原有任务状态和校验器。
未开展独立 Agent 行为试验、宿主运行时派工或跨客户端验证；单一作者的静态场景
核对不证明模型会稳定遵守规则。77 项测试只支持既有合约与模板兼容性结论。
P009 及更早证据保留，不用于本次改动的验收。

本轮交付为本地工作区修改；未提交、推送、发布或更新已安装副本。
