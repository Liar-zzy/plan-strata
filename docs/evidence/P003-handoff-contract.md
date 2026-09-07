# P003 — 交接契约审阅

日期：2026-09-07。检查者：root。候选技能版本：0.1.0-alpha.2。

入口新增 5 行条件指针，按需进入 parallel-handoff.md；默认流程、protocol v1、
状态字段、任务类型和只读校验器未更改。新增 Worker 与 Integrator 两份普通 Markdown
模板，由人或 Agent 填写，不宣称这些占位字段受到现有 JSON 校验器验证。

逐项审阅：并行选择与交接渠道独立；任务输入、共享接口、写入范围、资源预算先明确；
只覆盖一份已确认 ex-plan；任务绑定、代码或输入指纹、报告位置可从任务单恢复。
Manager 独自维护进度和派发回执；Worker 返回可保留的产物和实际证据；重复结果需要
核对，替换运行中的尝试需要先停止或隔离旧写入。集成使用既有关卡，不增加 review 类型。
科研共同预算、有效负结果与外部操作授权在对应分支说明，不作为默认工作的新步骤。

实际格式命令：

```sh
uv run --offline --no-project --with pyyaml python /Users/liar/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/plan-strata
```

输出：`Skill is valid!`，退出 0。直接使用默认 Python 首次运行因校验器自身缺少
PyYAML 退出 1；随后使用已有缓存的临时环境完成，不为技能增加依赖或改全局配置。

本检查接受交接契约的首版结构，未把文字审阅当成行为验证。后续 T02 在隔离目录
进行实际接手、结果收集与终验；若试用改变规则，保留本记录并更新适用检查。
