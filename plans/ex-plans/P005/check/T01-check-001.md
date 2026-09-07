---
{
  "schema": 1,
  "kind": "check",
  "id": "T01-check-001",
  "task": "T01",
  "plan": "plans/ex-plans/P005/ex-plan-v0.1.0.md",
  "plan_sha256": "0d7b7fdf25a385c1180de636b90bb4f78d3822364980b7120eb1642f105353b1",
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
      "sha256": "e2fa62e3a3d97d3682de5c2ac649af08afed050ad09cce6633db6d94ae528650"
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
      "path": "skills/plan-strata/assets/progress.md",
      "sha256": "00c2414b00f0394103f8133278bc8bfc255ebcfb8728d81aac09b24317d529fa"
    },
    {
      "path": "skills/plan-strata/references/development.md",
      "sha256": "d91ec715e6f1f837f4f68ef5851c61acc3e6557cd77095f4d459f59e752713f2"
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
      "path": "tests/test_workflow.py",
      "sha256": "a6bfe6e183454a4301beebf85370b3ceb85940014a58117a4c6123a6229173c0"
    },
    {
      "path": "README.md",
      "sha256": "359c5f14a8b9015809bbcf13f0772a69598450a5754c70c04e3ea67677eeae3c"
    },
    {
      "path": "README.zh-CN.md",
      "sha256": "10284f5e0e198a2df365564a2d0f55a7b1118618ec4b637cf506ec04ada55d6a"
    },
    {
      "path": "docs/validation-main-hotfix.md",
      "sha256": "b1f89e5526224aa4f98096ef3c27bc9695668d11641a17738b562c6e964280c2"
    }
  ],
  "evidence": [
    {
      "path": "evals/results/main-hotfix-red-001.json",
      "sha256": "0c3d820e7e599e3ff40a9bdf59450171658dfb3703cbcd8e74f9f3f53bfa4c76"
    },
    {
      "path": "evals/results/main-hotfix-py310-001.json",
      "sha256": "5f9088ae70665216c73eeff3cb128e9c126d0545cc4bf46a84325dc993fb19fb"
    },
    {
      "path": "evals/results/main-hotfix-py314-001.json",
      "sha256": "5197a761eab2742a5ec97837658ee8ed041e8c61974f6a43e7d8a5ebde25e2d7"
    },
    {
      "path": "evals/results/main-hotfix-replay-001.json",
      "sha256": "dfb6f20438a29a471bf53a470da7a67305bf7b0715a4252794fcd82569b6d2f4"
    }
  ]
}
---

# P005 T01 — main hotfix 本地验收

检查者：root（实现作者），2026-09-07。接受范围是主分支基础修复与本地验证，
不是尚未观察到的远端 CI、客户端行为或科研真实性。

## 观察

先锁定红色回归：Python 3.10.9 下 26 项出现 6 次失败，退出 1。修复保留任务 ID
和路径解析边界，另加合法内部链接对照后，Python 3.10.9 与 3.14.7 各 27 项通过，
退出 0。两份绿色输出的 17 项源码指纹都匹配当前文件。没有删除或弱化原有 20 项。

原审查脚本复跑：普通 integration 科研任务返回 RESERVED_TASK_ID / invalid / open；
循环链接返回 JSON 错误，不再输出 traceback。清单单独哈希仍只约束清单本身；
明确列入数据成员后，数据变化正确撤销验收。新增说明没有改变此范围边界。

共享实现只改路径解析的 RuntimeError 转换、保留标识检查及协议说明；验证和
fingerprint 保持只读。合法内部链接、外部路径隔离和科研负结果已由回归覆盖。
技能格式校验返回 Skill is valid!，标准库运行依赖、12 文件包和自动发现策略不变。
两种 README 仅新增本轮验证入口；没有引入 dev 的并行模板、参考或演示驱动。

## 决定与限制

接受本地 hotfix，允许按用户授权提交并推送 main。推送后须核对确切提交的 CI，
不能拿本地测试代替 GitHub 结果；最终远端结果由该提交的 Checks 运行记录承载。
同步 dev 时另跑其完整回归并使用单独记录，保留默认关闭和已有并行功能。

P001/P002 检查保持原字节，旧验收不被改写。没有新 Agent 行为试用、真实科研、
全局安装、Release/tag 或仓库设置变更。循环路径在不同 Python 版本的诊断细节
可以不同，但均有非零退出码及 JSON 错误，不宣称生产安全或完整依赖推断。
