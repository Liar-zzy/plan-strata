---
{
  "schema": 1,
  "kind": "check",
  "id": "T01-check-001",
  "task": "T01",
  "plan": "plans/ex-plans/P006/ex-plan-v0.1.0.md",
  "plan_sha256": "2156b181b9d8c4197c2d8fcb5550ea69d815c4fb05609e5c01308b0d84a1c31b",
  "verdict": "pass",
  "subjects": [
    {
      "path": "evals/capture.py",
      "sha256": "fb366d649d0d210e6096279c927d938f0b6f50be6307a7c4d2b35635f28ffbb0"
    },
    {
      "path": "evals/install_smoke.py",
      "sha256": "f36ff49e0437ee20c1c3653068f0863aa3434bd97de72b5cba6c39e173b31980"
    },
    {
      "path": "evals/parallel_trial.py",
      "sha256": "75f86c395eef51780184f75094667079145bc9c2673bb50f1f5f564027975d96"
    },
    {
      "path": "evals/prepare.py",
      "sha256": "7fe8badb85362b10dc87d7eb9ef84fb88419366904a0e250a48ff1148c1a739e"
    },
    {
      "path": "evals/run_checks.py",
      "sha256": "fea1edd5c57d2f6aa629204ac6809b3c874cf2f9edcc8445455126ffe50e5278"
    },
    {
      "path": "skills/plan-strata/LICENSE",
      "sha256": "7b5a822173a1122da41fe373b929cf386c04b9347ac08e127401514c79005679"
    },
    {
      "path": "skills/plan-strata/SKILL.md",
      "sha256": "b1e6a5c98b98152a03de58e03fed5e816bb496a3fede5e538a3be0711f5efa9f"
    },
    {
      "path": "skills/plan-strata/agents/openai.yaml",
      "sha256": "0f8a379169d45cfd2750d7a8a23b8a863aacf27384742002113ba9a9e99d5876"
    },
    {
      "path": "skills/plan-strata/assets/CURRENT.md",
      "sha256": "407be11482609337686361b339d2cc255437deaa3f15d69fcd8fdc9c97fc8c6f"
    },
    {
      "path": "skills/plan-strata/assets/check.md",
      "sha256": "bde0fa9ac14f67ec9eaa5e7d710206b28049d2271c63838272fdba3a1f85a5d0"
    },
    {
      "path": "skills/plan-strata/assets/core.md",
      "sha256": "cee2c0aba4bf6dfe7e886881c6ee69614387aa9acb61f6a97da5b3dcb58748a7"
    },
    {
      "path": "skills/plan-strata/assets/ex-plan.md",
      "sha256": "2f89e8bc085609844a56ef4da2815a7ee8a1e14b3ace69d18764f4d4d51ec3f6"
    },
    {
      "path": "skills/plan-strata/assets/integration-handoff.md",
      "sha256": "23529de0dcf1bc8e314eebea103be53b7347cd53a1d4eaeaf2f423d805aa4694"
    },
    {
      "path": "skills/plan-strata/assets/progress.md",
      "sha256": "00c2414b00f0394103f8133278bc8bfc255ebcfb8728d81aac09b24317d529fa"
    },
    {
      "path": "skills/plan-strata/assets/task-handoff.md",
      "sha256": "dc939e4a2bb3f69e508e53f241328822d38c260f1fff6fa5e17d460535792cb2"
    },
    {
      "path": "skills/plan-strata/references/development.md",
      "sha256": "d91ec715e6f1f837f4f68ef5851c61acc3e6557cd77095f4d459f59e752713f2"
    },
    {
      "path": "skills/plan-strata/references/parallel-handoff.md",
      "sha256": "b3f72f0efab21dd26bb24da0b33668481bf3ee919cb67701363e6f6b68fe84bc"
    },
    {
      "path": "skills/plan-strata/references/protocol.md",
      "sha256": "063bd61071831121b6ce9559db553721fbfec9b42a7c82afd76b4b9e6e2bbcd2"
    },
    {
      "path": "skills/plan-strata/references/research.md",
      "sha256": "688c4e57e1e19509fa433a0568afec4d462d5328cf3f4abe6f84415b2a1ec805"
    },
    {
      "path": "skills/plan-strata/scripts/strata.py",
      "sha256": "c8126230964accea0ed774cc653aa88ee5dc4b303fce1af3ff3f58cdb3263c31"
    },
    {
      "path": "tests/test_parallel_trial.py",
      "sha256": "a3309213a899f4f9b759de47f2493e34cb6439ab498a02119814a859aea9d90f"
    },
    {
      "path": "tests/test_workflow.py",
      "sha256": "a6bfe6e183454a4301beebf85370b3ceb85940014a58117a4c6123a6229173c0"
    },
    {
      "path": "docs/validation-handoff-fixes.md",
      "sha256": "c2fc5e0c469a08dd3daa6a56fd9bbb66eab52892fcb11f92bb5f2a62adcf6719"
    },
    {
      "path": "README.md",
      "sha256": "e272e2cc3b6344296b4e9d6bea0fdadad15c9244f0ef5deb4c76c6eb413c4989"
    },
    {
      "path": "README.zh-CN.md",
      "sha256": "c3bde2f60a12798d89cfb4d123eb2d04ee4aa1f7c8534d17e358a84c0263df7d"
    }
  ],
  "evidence": [
    {
      "path": "evals/results/dev-hotfix-py310-001.json",
      "sha256": "474b0209a97b16b201bc22eddcb0b1381b5c255d7d14f2126495a2eab50237fc"
    },
    {
      "path": "evals/results/dev-hotfix-py314-001.json",
      "sha256": "d8dd538d7cfd10c307a8f4046c56d9617981e2694b1957146ceb6c3db8a67554"
    }
  ]
}
---

# P006 T01 — dev hotfix 同步验收

检查者：root（同步作者），2026-09-07。本记录接受公共修复在 dev 上的本地兼容性。
来源 main 为 86ef43e2a87fef734e427910f651be3ddbfffce7，起始 dev 为 197885c。

## 方法与观察

分别使用 Python 3.10.9 和 3.14.7 运行
python3 evals/run_checks.py --output <new-file.json>。两次各 54 项全部通过、退出 0，
两份报告的 22 项源码指纹均匹配当前文件。54 项包括 27 项基础协议检查与 27 项
本地并行试用驱动检查；不是 54 次独立 Agent 实验。

git diff --exit-code main -- skills/plan-strata/scripts/strata.py
skills/plan-strata/references/protocol.md tests/test_workflow.py 比对退出 0，
三份公共文件与 main hotfix 字节相同。main 对应提交的两版 Python CI 已成功：
https://github.com/Liar-zzy/plan-strata/actions/runs/34111560137
该运行验证 main 的 27 项，不用于替代上面 dev 的独立回归。

与 197885c 比对，SKILL.md、agents/openai.yaml、两份交接模板、parallel-handoff.md、
evals/parallel_trial.py 和 tests/test_parallel_trial.py 七份文件保持原字节。
因此本次没有新增并行权限、改变默认关闭规则或替换已验证的试用驱动。
技能格式校验输出 Skill is valid!，退出 0。

文档仅在历史 P004 记录开头增加当前检查入口，不改写旧 49 项输出或旧验收文件。
保留 alpha.2 和独立的 CURRENT/P006，不复制 main 的 P005 管理记录。

## 决定与限制

本地公共修复及完整回归通过，可以按用户授权推送 dev；发布后核对该提交的
GitHub Checks，不提前把本地通过声明成远端 CI 通过。

没有新 Agent 行为试用、客户端安装、真实科研或仓库设置变更。协议仍只核对显式
对象，不自动展开输入清单。保持历史 P003/P004 产物作为对应版本的证据，不用旧
源码指纹接受这次新实现。main 只接收基础 hotfix，实验性并行功能继续留在 dev。
