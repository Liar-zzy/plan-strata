---
{
  "schema": 1,
  "kind": "plan",
  "id": "P001",
  "revision": "v0.1.0",
  "core": "plans/core/core-v0.1.0.md",
  "core_sha256": "eab8d72b274f75b243b7a2f40af6ba17323b5b32f2eba1b57ef8664b89d1cfb3",
  "ready": true,
  "tasks": [
    {
      "id": "T01",
      "type": "development",
      "depends_on": []
    },
    {
      "id": "T02",
      "type": "development",
      "depends_on": []
    },
    {
      "id": "T03",
      "type": "development",
      "depends_on": [
        "T01",
        "T02"
      ]
    }
  ],
  "integration_required": true
}
---

# P001 — 本地实验版与首次试用

## T01 — 可安装技能和机械校验

产物：skills/plan-strata/、tests/、evals/prepare.py。
验收：技能格式检查通过；自动测试覆盖基线、完成证据、依赖和科研结果语义；
只读校验不修改用户记录。保持辅助工具为 Python 3.10+ 标准库。

## T02 — 独立使用说明与真实交接

产物：docs/FIRST_USE.md。由没有本会话上下文的接手者读取技能和现有实现，
在隔离副本中编写可直接执行的首次使用说明并验证命令。已有核心代码可读取，
该任务不要求改动技能或源码。接手者记录实际检查和遇到的问题。

## T03 — 场景验证与发布准备

产物：docs/validation.md 和可追溯的检查记录。
覆盖恢复、运行中切换、过期证据、集成失败、有效科研负结果。记录实际结果，
区分自动检查、模拟工作流和真实仓库文档交接；不推断长期效果。

## 集成与结束

上述产物能一同使用；README 所述命令可运行；技能引用存在；根项目记录通过
校验且具有对应证据。保留本地实验版，报告试用发现和下一步。

