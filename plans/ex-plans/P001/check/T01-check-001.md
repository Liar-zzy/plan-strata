---
{
  "schema": 1,
  "kind": "check",
  "id": "T01-check-001",
  "task": "T01",
  "plan": "plans/ex-plans/P001/ex-plan-v0.1.0.md",
  "plan_sha256": "67d145264016c002c49bb450d6075c7011b697d846c60e38d12c4383b2516f0f",
  "verdict": "pass",
  "subjects": [
    {
      "path": "skills/plan-strata/SKILL.md",
      "sha256": "e2fa62e3a3d97d3682de5c2ac649af08afed050ad09cce6633db6d94ae528650"
    },
    {
      "path": "skills/plan-strata/scripts/strata.py",
      "sha256": "4e4d12a0578ea2cf4fd986a84d24020565243ceb47c9dec8253f2231e909f382"
    },
    {
      "path": "skills/plan-strata/references/protocol.md",
      "sha256": "f9f00ee951f31c88d512fc15b86db49fcab1f7d1ec8662d92d461da8b3d6855b"
    },
    {
      "path": "skills/plan-strata/references/development.md",
      "sha256": "d91ec715e6f1f837f4f68ef5851c61acc3e6557cd77095f4d459f59e752713f2"
    },
    {
      "path": "skills/plan-strata/references/research.md",
      "sha256": "688c4e57e1e19509fa433a0568afec4d462d5328cf3f4abe6f84415b2a1ec805"
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
      "path": "skills/plan-strata/assets/CURRENT.md",
      "sha256": "407be11482609337686361b339d2cc255437deaa3f15d69fcd8fdc9c97fc8c6f"
    },
    {
      "path": "skills/plan-strata/assets/check.md",
      "sha256": "bde0fa9ac14f67ec9eaa5e7d710206b28049d2271c63838272fdba3a1f85a5d0"
    },
    {
      "path": "skills/plan-strata/agents/openai.yaml",
      "sha256": "0f8a379169d45cfd2750d7a8a23b8a863aacf27384742002113ba9a9e99d5876"
    },
    {
      "path": "skills/plan-strata/LICENSE",
      "sha256": "7b5a822173a1122da41fe373b929cf386c04b9347ac08e127401514c79005679"
    },
    {
      "path": "tests/test_workflow.py",
      "sha256": "32156431a1799252ccf83395fd5ebdf77918232d6e67a31093e4e3867867432a"
    },
    {
      "path": "evals/prepare.py",
      "sha256": "7fe8badb85362b10dc87d7eb9ef84fb88419366904a0e250a48ff1148c1a739e"
    }
  ],
  "evidence": [
    {
      "path": "evals/results/automated-py314-001.json",
      "sha256": "76d9d9d6f1fd8437837a4792155b1c40af64ce59c17c52691c689c7d5882133c"
    },
    {
      "path": "evals/results/automated-py310-001.json",
      "sha256": "b4296f9f6166637bc1da4d242088dfa4dfd8fa3875658d218df2a73ece4bbf93"
    },
    {
      "path": "evals/results/package-check-001.json",
      "sha256": "10b379c36a155ae25ee44d23e80b8c181909f6f0a5dacbee6e0a57476a81cbce"
    }
  ]
}
---

# T01 — 技能与校验工具验收

检查者：root。日期：2026-09-05。

实际在 Python 3.14.7 与 Python 3.10 环境运行 20 个自动检查，均退出 0；
内置 skill-creator 格式检查器返回 Skill is valid!。包内 8 个本地链接存在。
检查记录包含源码指纹，集成复核确认它们与当前文件一致。工具无需第三方包。

接受技能、模板、只读工具和测试实现。自动检查覆盖声明的状态与文件关系，
不证明所有隐含依赖、证据真实性或任意客户端的技能发现行为。

