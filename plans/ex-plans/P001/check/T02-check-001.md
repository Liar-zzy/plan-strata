---
{
  "schema": 1,
  "kind": "check",
  "id": "T02-check-001",
  "task": "T02",
  "plan": "plans/ex-plans/P001/ex-plan-v0.1.0.md",
  "plan_sha256": "67d145264016c002c49bb450d6075c7011b697d846c60e38d12c4383b2516f0f",
  "verdict": "pass",
  "subjects": [
    {
      "path": "docs/FIRST_USE.md",
      "sha256": "7e62244d54b887726ef678bcb2645d132006259716665898866b4cfec2024773"
    },
    {
      "path": "README.md",
      "sha256": "f565b7669ae509ba1bc9094508d9f1545863c1b9eaf575a975c82c191c93ddb7"
    },
    {
      "path": "evals/prepare.py",
      "sha256": "7fe8badb85362b10dc87d7eb9ef84fb88419366904a0e250a48ff1148c1a739e"
    },
    {
      "path": "skills/plan-strata/scripts/strata.py",
      "sha256": "4e4d12a0578ea2cf4fd986a84d24020565243ceb47c9dec8253f2231e909f382"
    }
  ],
  "evidence": [
    {
      "path": "evals/results/handoff-001.json",
      "sha256": "2314daeb2a3acadb661e322f5a82c714e7fa84ead9f7b60690a5641aaace277b"
    },
    {
      "path": "evals/results/first-use-root-001.json",
      "sha256": "e4d3340ef2a76e311c8d24264b004a49cb7b12c48d25ea556abfe97f03df50c1"
    },
    {
      "path": "docs/evidence/T02-first-use-commands.md",
      "sha256": "fe8fa2b5db13ccdea185db5dda39306a170167235e1403d415e1e3ffd10ce3d3"
    }
  ]
}
---

# T02 — 接收独立文档交接后的根目录验收

检查者：root；文档执行者：real_handoff。日期：2026-09-05。

新会话仅依据本项目文件完成说明并在隔离副本中运行命令，20 个测试通过。
root 阅读其说明与实际证据，将文档原字节接收至当前项目，并从说明提取完整
命令块在最终根目录运行：退出 0，示例输出 6 与 0，20 个测试通过。

原隔离检查及其临时目录证据全文保留在 handoff-001.json 的 artifacts 中。
本记录是根目录的接受判断，不直接沿用原临时路径。首次说明给出的包与仓库
区别、入口恢复、证据处理与已知限制已核对；Python 3.10 支持另有 T01 测试依据。

接受当前文档。它证明一次真实文档接手与本地命令可执行，未验证自动安装发现
或长周期项目效果。没有为了集成本交付而修改原隔离检查或原计划。

