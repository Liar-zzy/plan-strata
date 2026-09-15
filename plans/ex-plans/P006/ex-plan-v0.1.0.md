---
{"schema":1,"kind":"plan","id":"P006","revision":"v0.1.0","core":"plans/core/core-v0.3.0.md","core_sha256":"5690f47e59e9d79b222a9e191f24a078583b2b86f5f45368edfd60dc43d7cc8f","ready":true,"tasks":[{"id":"T01","type":"development","depends_on":[]}],"integration_required":false}
---

# P006 — 同步 main hotfix 到 dev

2026-09-07 用户已同意主分支小范围修复和 dev 同步。起始 dev 为 197885c，
来源 main hotfix 为 86ef43e2a87fef734e427910f651be3ddbfffce7。允许完成验证后
提交、推送 dev；不修改 GitHub 设置、创建 Release/tag、安装全局技能或运行新 Agent。

## T01 — 公共修复同步与全量兼容性

将 scripts/strata.py、references/protocol.md 与 tests/test_workflow.py 三份
公共文件与 main hotfix 对齐；已有保留标识和范围说明保持原样，只补缺少的
循环路径异常处理及测试。不把 main 的 CURRENT/P005 记录覆盖到 dev。

保持 alpha.2、默认关闭、并行任务单、演示驱动和已有试用产物不变。Python 3.10
和 3.14 分别运行 dev 的完整测试，核对最新源码指纹及三份公共文件与 main 的字节
一致性。新增接受记录，保留 P003/P004 的历史检查；明确此前 49 项为旧源码结果。
文档更新只说明本次同步及最新测试，不把确定性回归当成新的 Agent 行为试用。

本任务包含公共补丁与现有并行流程的联合验证，无需增加重复终验任务。核对本地
记录后推送并检查对应提交的 GitHub CI；不合并实验性并行功能到 main。
