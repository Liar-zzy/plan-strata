---
{
  "schema": 1,
  "kind": "check",
  "id": "T02-check-001",
  "task": "T02",
  "plan": "plans/ex-plans/P003/ex-plan-v0.1.0.md",
  "plan_sha256": "6093a244c1f1129976d12d010dffcb6dcc951256c591de46f399221de7c03ffb",
  "verdict": "pass",
  "subjects": [
    {
      "path": "README.md",
      "sha256": "204a563698fc0401195b53c620af5122ce32c11b2c0bae7149429d8568b6d157"
    },
    {
      "path": "README.zh-CN.md",
      "sha256": "73a1debe03d54dfd2b687d48fd2e8019ff68a8fb11b41647c6b21c01ca09eb1a"
    },
    {
      "path": "evals/README.md",
      "sha256": "8b85e1c807d9045ddfe35da891aa93ce10a84a20d206c8ac981ed9c3775ad2f0"
    },
    {
      "path": "docs/validation-parallel.md",
      "sha256": "f7c93e568c5556e404b68d1873c8336c92221291c270a419e43aa2c32ce94615"
    },
    {
      "path": "evals/parallel_trial.py",
      "sha256": "6654e293d132ef1fe950c41d84f8266660fd9bf7fc3e39ff08f640a4914d14bd"
    },
    {
      "path": "tests/test_parallel_trial.py",
      "sha256": "516ed3f7175d6b36cd3620544e91739767d8b193c9bda8b1015eba725eb10f20"
    },
    {
      "path": "tests/test_workflow.py",
      "sha256": "32156431a1799252ccf83395fd5ebdf77918232d6e67a31093e4e3867867432a"
    }
  ],
  "evidence": [
    {
      "path": "evals/results/parallel-py310-001.json",
      "sha256": "a3e0057f34b12fa350f288a57839017224aae70933da0ded3948c3be037f9780"
    },
    {
      "path": "evals/results/parallel-py314-001.json",
      "sha256": "7775eae363353ab5b7683647c15526048e51469ca016461101628a2ab54b4e24"
    },
    {
      "path": "evals/results/parallel-worker-T01-001.json",
      "sha256": "5d1ec8b52909f155c8564d4723ec2b72a4fa2a0c65913b4a9a7c4b885e2d9871"
    },
    {
      "path": "evals/results/parallel-worker-T02-001.json",
      "sha256": "ef9514b129e80364ef0cc208e71bd2b4425e6f19878b31cc3f33a1568fd91fab"
    },
    {
      "path": "evals/results/parallel-integration-001.json",
      "sha256": "25507fe71753a5885fa84070dbc702bd209f1bb4de447d7c35bf67c806573174"
    },
    {
      "path": "evals/results/parallel-manager-001.json",
      "sha256": "55be3c6f292facdc17c451630dad90b5e0a051999b0e052b8ec8c0b5b92510f0"
    },
    {
      "path": "evals/results/parallel-audit-001.json",
      "sha256": "4e530cab64f09b5296706610190697e72947ac28d5b79718eb3c6f1fae56196f"
    }
  ]
}
---

# T02 — 本地闭环与双语入口

检查者 root，2026-09-07。方法：读取两份 Worker 交付、源码、独立 Integrator 的
报告及实际测试日志；核对允许写入范围、绑定与预算；通过本地试用驱动收集证据。

两个 Worker 分别完成清洗和渲染任务，各自指定测试运行一次通过。Manager 重跑任务
测试并接受后整体仍 open；新 Integrator 对组合后的产物完成 3/3 测试，未改源码或
进度；Manager 收集并挂接其检查后得到 consistent/verified，所有引用可从归档恢复。
这是本地文件复制组合，不是 Git merge 或远端任务执行验证。

35 项检查在 Python 3.10.9/3.14.7 上均通过。独立核对两个测试报告的全部 22 个
source 指纹、四份捕获的技能指纹与文字字节、终验和 Manager 捕获中的各 23 个
检查引用。所选用户文档和技能文档的 51 个本地链接、5 个片段锚点有效；中英文
README 的 5 个 shell 块与原版一致。双语新增段落均说明可选模式、单计划范围、
宿主执行、唯一进度维护者和外部操作权限，不声称内置调度或机器验证任务单。

失败/过期/越界/重试路径由确定性测试覆盖，不能当作独立 Agent 试用。没有测量
效率优势或真实科研效果；跨计划、GitHub 同步、分支冲突及生产并发未验证。
结论：接受该最小本地试用与文档，等待 P003 最终集成验收，不授权 push 或安装升级。
