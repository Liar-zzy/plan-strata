---
{"schema":2,"kind":"plan","id":"P010","revision":"v0.1.0","core":"plans/core/core-v0.5.0.md","ready":true,"tasks":[{"id":"T01","type":"development","depends_on":[]}],"integration_required":false}
---

# P010 — 触发、授权与宿主交接边界

依据 2026-09-15 用户在逐项审阅反馈后要求“先 update”，更新本地技能与相关文档。
前身 P009 已交付 dev 预览；其计划、检查及发布证据保留，不复用为本次改动的验收。

## T01 — 统一指令、模板和使用说明

范围：skills/plan-strata 的入口、引用文档、相关模板与默认提示，中英文 README，
本轮计划和验证记录。收窄触发，定义已有授权，支持宿主 assignment message 与
绑定任务卡交接，允许宿主返回 Agent ID 后记回执，区分局部阻塞与整任务阻塞，
明确角色完成条件和指定 progress writer，限制校验后修复及其他管理记录写入。
保持 schema 2 无哈希协议、现有状态与校验器，不修改运行代码。

root 单 Agent 兼任执行、审阅、Manager 和唯一 progress writer。只更新本地，
不 commit/push、发布、升级安装或启用子 Agent；过去发布批次的授权不延用。
预算为实现、自检及最多两轮成组审阅修正，不增加独立 Agent 行为试验。

验收：逐项核对八条反馈与相关引用/模板的一致性；静态检查未绑定问答/诊断、
已授权宿主派工、局部缺失输入、只读 Reviewer、非 writer Worker、替代绑定格式
及单 Agent 验收场景。运行技能格式检查、已有合约测试、本地链接与空白检查，
最后验证本轮记录。静态推演和合约测试不冒充独立 Agent 行为验证。
