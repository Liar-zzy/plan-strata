---
{
  "schema": 1,
  "kind": "progress",
  "plan_id": "P002",
  "tasks": [{
    "id": "T01", "state": "done", "owner": "root",
    "next": "双语参与说明已验收；后续按真实使用反馈维护，发布状态以 GitHub 对应提交为准",
    "check": "plans/ex-plans/P002/check/T01-check-002.md",
    "plan": "plans/ex-plans/P002/ex-plan-v0.1.0.md",
    "plan_sha256": "aa04df317c01a9a609d674123c6321721a0895f67d7454d808b3b0fd942cbecb"
  }],
  "integration_check": null
}
---

# 交接

英文入口 README.md，中文入口 README.zh-CN.md；英文 About、Topics、Release 草稿
与后续清单在 docs/PUBLISHING.md；本轮证据在 docs/evidence/P002-release-preparation.md。
双语说明、隔离安装与回归检查已完成。技能仍为 0.1.0-alpha.1，包内文件未修改。

准备阶段交付时尚未 commit 或 push，也未配置 remote、创建 tag/release 或修改
GitHub About。P002 检查只接受本地材料，不从本地安装通过推断远端或客户端结果。

## 后续发布授权

2026-09-05，用户提供 git@github.com:Liar-zzy/plan-strata.git 并明确要求 push。
只读检查确认目标为公开空仓库，本地分支 main；按此新授权提交准备材料并首次推送，
随后核验 GitHub CI 和远端安装。不创建 tag/release，不修改 GitHub About 或全局技能。

## 首次发布观察

首次推送提交：0250878d072041aa45d3ad624e774c26139cffd7，分支 main，远端已与本地
该提交一致。GitHub 返回英文 README 与中文 README 的公开文件地址。

[首次 GitHub CI](https://github.com/Liar-zzy/plan-strata/actions/runs/33970907435)
已完成并成功，Python 3.10 与 3.14 两个任务均通过；对应提交和步骤元数据保存在
[CI 观察](../../../evals/results/github-ci-001.json)。

使用公开仓库源 Liar-zzy/plan-strata 运行安装冒烟检查，Codex 和 Claude Code
安装位置均包含与源目录相同的 12 个包文件；安装后的 validate、fingerprint 退出 0，
临时目标项目原有文件不变。见[GitHub 安装记录](../../../evals/results/install-github-001.json)。
此次检查验证远端获取和安装文件，不代表两个客户端的发现或 Agent 行为已验证。

本节和两份新证据作为后续记录另行提交，不改变已验收的技能包。CI 观察只对应上面
列出的首次推送提交；后续提交的运行应另查 GitHub，不将旧结果当作新运行。

P001 与其历史证据保持不变；私人会话继续 Git-ignored。没有后台作业或全局安装。

## README 参与入口维护

2026-09-06，按用户要求在两个 README 顶部加入 Join us 提示，在正文提供可复制的
可选 AGENTS.md 使用反馈约定和 issue 入口。只修改发布说明，不改变技能内容、
安装方式或原验收标准。旧文档检查保留，新检查重新接受当前 README；详见
[本次复验](check/T01-check-002.md)。

反馈采取“使用中观察、交接时归档”，不自动修改技能或向外上传；未在本仓库实际
创建 AGENTS.md 或反馈文件。本次 20 项测试、文档链接和锚点检查通过。
以上是提交前的本地复验记录。随后用户明确要求“完成后帮我 push”，授权将这轮
文档和验收记录推送到 origin/main；对应推送及 CI 状态以 GitHub 提交和运行记录
为准。先前 GitHub 成功结果只对应先前已推送提交，不代替本次 CI。
