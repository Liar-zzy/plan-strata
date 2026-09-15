---
{"schema":1,"kind":"progress","plan_id":"P008","tasks":[{"id":"T01","state":"done","owner":"root","next":"文档续检已验收，剩余风险见 docs/dev-readiness.md；行为试用及提交/push 等待另行授权","check":"plans/ex-plans/P008/check/T01-check-002.md","plan":"plans/ex-plans/P008/ex-plan-v0.1.0.md","plan_sha256":"5ecb704ff8cc25754e40dddb84b19053de9d3bbaf43ce524e2d1ead65f2d8f56"}],"integration_check":null}
---

# P008 — 本地修复

root 是唯一写入者；不启用并行，不修改用户的 .gitignore 或原始反馈。当前使用
skill-creator 与 writing-for-agents 将规则写为简短的可执行指引。普通自检返修
保留在本任务内，最终统一检查；真实失败证据与已冻结文件保持不变。

已完成：有限闭环规则与示例、分配/登记边界、保持现有 CLI 行为的退出码契约、
中英文说明、7 项 CLI 与 4 项修复回归。最终 Python 3.10.9 / 3.14.7 各 70 项
通过，指纹逐项匹配；技能格式与差异空白检查通过。默认 Python 缺少 yaml 的
格式检查失败通过现有 Python 3.10 解决，无需安装依赖。详情见
docs/validation-repair-loop.md；证据保留在 evals/results/repair-loop-*.json。

测试由脚本安排动作，不代表自主 Agent 闭环或人工中转成本已验证；没有新增子
Agent、后台任务或外部操作。P001–P007 和 core 快照保留原样。本次尚未提交或
推送，也未修改 main、全局安装或用户的反馈文件。

## 2026-09-10 — 剩余风险与文档续检

用户要求评估剩余问题并更新 Markdown。沿用 T01 的范围和冻结绑定，不另建任务
或改计划；本次是首次正式验收后的一轮文档返修（两轮限额内）。root 单人完成。
检查预算交接、安装来源以及声明边界；只读核对远端 HEAD/main/dev，不作外部写入。
将修改的五个旧 subject 已按 check-001 的指纹验证并保存在
evals/results/repair-loop-pre-followup-001.json，旧检查、测试报告和验证文档不覆盖。
尚无后台作业；本轮不改变代码/测试、技能版本或并行默认值。

本轮文档返修完成：预算恢复进入现有 progress/返回契约，README 显示安装来源
区别并链接 docs/dev-readiness.md。旧检查与五个旧输入的归档指纹逐项匹配；
新的 check-002 接受当前文档。003 报告在 Python 3.10/3.14 各通过 70 项测试，
格式、链接与差异检查通过。消耗：一次正式验收后的文档返修、两次完整回归；
该两轮返修限额尚余一轮，无未结束作业或资源预留。若后续需超出该额度/范围，
先明确新的边界，不凭新会话重置额度。
