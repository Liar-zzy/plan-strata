# 0.1.0-alpha.2 — 交接验收修复复验

> 后续更新：dev 已同步 main hotfix 的路径异常处理及测试；最新源码的全量复验见
> [P006 检查](../plans/ex-plans/P006/check/T01-check-001.md)。下文的 49 项结果保留为
> P004 当时的历史记录，不作为这次同步后版本的新验证。

日期：2026-09-07。这是本地未发布候选的后续修复，不是新版本发布。
用户要求先修复已确认漏洞，保持并行默认关闭；本轮未创建分支、Issue、commit、
push、Release 或全局安装。项目记录见 [P004](../plans/ex-plans/P004/ex-plan-v0.1.0.md)。

## 问题与修复

1. **接收端基线漂移。** 旧演示驱动检查 Worker 的变更及目标文件冲突，却没有
   核对 Manager 的其他固定输入。弱化 Manager 的测试可让错误实现通过；终验后
   修改 Manager 的管线代码，再收集漏列该文件的 check，甚至会得到 verified。
   现在 collect/finish 在写入前核对接收端完整文件快照，拒绝新增、删除及修改；
   重复收集也必须核对。只允许 Manager 改进度正文和非空 next 文本，身份、执行
   绑定、负责人、状态和 check 引用仍固定。进度使用协议的严格解析器，损坏格式
   不能绕过接收检查。该驱动仍只用于小型合成样例，不随技能安装。
2. **终验输入漏列。** 新试用的 INTEGRATION-INPUTS.json 排除动态 progress，
   其余受检输入及清单本身必须逐项成为终验 subjects，漏项会在复制前被拒绝。
   完成后修改其中某个固定输入，只读校验器也会撤销整体 verified。
   没有新增协议字段或通用清单解析器：校验器仍只核对显式 subjects/evidence。
3. **保留标识冲突。** 普通计划任务使用 integration，可使同一 check 同时充当
   普通任务与终验，并绕过 research 解释字段。现在计划解析明确报
   RESERVED_TASK_ID；合法 T01 科研任务及负结果完成规则保持不变。

旧试用收据没有接收端检查点，当前驱动会明确要求保留旧试用并新建目录。
不自动迁移或重写 [P003 的首次 Agent 试用](validation-parallel.md)及其捕获证据。
技能的 protocol v1 记录保持兼容，唯一收紧是禁止普通任务占用保留标识。

## 红色回归、修复与绿色复验

沿用上一轮已经重复复现的最小反例，跳过重新扩张假设和临时日志，直接锁定真实
collect/finish/Validator 调用。先添加失败测试，再修复；未加入调试日志。

| 运行 | 实际结果 | 保留输出与源码指纹 |
|---|---|---|
| 首次红色回归 | 46 项，14 次失败断言（含子场景），退出 1 | [red-001](../evals/results/handoff-fix-red-001.json) |
| 进度格式边界复查 | 49 项，1 次失败断言，退出 1 | [red-002](../evals/results/handoff-fix-red-002.json) |
| Python 3.10.9 最终复验 | 49/49 通过，退出 0 | [py310](../evals/results/handoff-fix-py310-001.json) |
| Python 3.14.7 最终复验 | 49/49 通过，退出 0 | [py314](../evals/results/handoff-fix-py314-001.json) |

最终命令为 `python3 evals/run_checks.py --output <new-file.json>`，分别使用上述
两个 Python 解释器运行。结果文件保留完整 unittest 输出及技能、测试和评测源码
指纹；先前红色运行的源码指纹是历史状态，不要求匹配最终源码。

额外将原审查脚本的三个反例分段原样重跑，接收端两例在接受前拒绝，标识冲突例
返回 invalid/open 和 RESERVED_TASK_ID，见[原反例复跑](../evals/results/handoff-fix-replay-001.json)。
测试仓库保留了对应反例。新增 14 项测试之外，原有 35 项全部保留并通过，覆盖
原样重试、真实任务测试失败、终验 fail/open、失败历史保留、合法科研负结果，
以及无 Git 的普通流程。技能格式校验输出为 `Skill is valid!`，文档、链接和
安装片段检查见[本轮审计](../evals/results/handoff-fix-audit-001.json)。

## 默认关闭与启用边界

[技能入口](../skills/plan-strata/SKILL.md)和[按需交接说明](../skills/plan-strata/references/parallel-handoff.md)
规定当前迭代/批次的明确 opt-in；[英文](../README.md#optional-parallel-handoffs)与
[中文 README](../README.zh-CN.md#可选的并行交接)分别提供启用和仅提案示例。
文案路径审查覆盖：普通继续工作、只发现 Git、只请求提案均不派发；明确启用的
当前批次及其合法接手可以执行；缺少能力时提供手工交接/串行方案；新的批次重新
确认是否已授权。未改动技能自动发现策略或宿主的全局配置。

自然语言请求、技能显式/隐式加载和宿主权限边界参照
[官方技能说明](https://learn.chatgpt.com/docs/build-skills)、
[子 Agent 说明](https://learn.chatgpt.com/docs/agent-configuration/subagents)及
[权限说明](https://learn.chatgpt.com/docs/agent-approvals-security)。
这次是指令路径审查和确定性回归，没有重新派发 Agent 检验修改后的行为。
默认关闭是技能的工作约定，不是独立于宿主的运行时安全开关。

## 仍然存在的边界

- 接收检查假设命令执行期间没有其他写入者，不提供锁、事务回滚、沙箱或防伪签名。
  Python 缓存不纳入试用输入快照；试用代码及宿主环境须可信。
- 接受后新增未列入范围的文件，或隐含依赖变化，不能靠只读校验器自动发现。
  重用验收前仍需审查范围；清单覆盖也不能证明测试充分、报告真实或科研结论正确。
- 未验证真实多 Agent 取消/重启、Git 合并冲突、Issue 派发、生产并发、科研预算执行
  或长期协作收益。P003 的旧 Agent 快照及旧 CI 不是本次实现的验证证据。

本地修复可以进入受控试用；对外推送、发布或主分支合并仍需用户另行授权。
