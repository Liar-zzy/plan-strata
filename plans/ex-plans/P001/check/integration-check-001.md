---
{
  "schema": 1,
  "kind": "check",
  "id": "integration-check-001",
  "task": "integration",
  "plan": "plans/ex-plans/P001/ex-plan-v0.1.0.md",
  "plan_sha256": "67d145264016c002c49bb450d6075c7011b697d846c60e38d12c4383b2516f0f",
  "verdict": "pass",
  "subjects": [
    {
      "path": "README.md",
      "sha256": "f565b7669ae509ba1bc9094508d9f1545863c1b9eaf575a975c82c191c93ddb7"
    },
    {
      "path": "docs/FIRST_USE.md",
      "sha256": "7e62244d54b887726ef678bcb2645d132006259716665898866b4cfec2024773"
    },
    {
      "path": "docs/validation.md",
      "sha256": "0ed440ece0bf68f5d0e607681892b4cb0cf361589d4812d69cdd1b9832dc4667"
    },
    {
      "path": "skills/plan-strata/SKILL.md",
      "sha256": "e2fa62e3a3d97d3682de5c2ac649af08afed050ad09cce6633db6d94ae528650"
    },
    {
      "path": "skills/plan-strata/scripts/strata.py",
      "sha256": "4e4d12a0578ea2cf4fd986a84d24020565243ceb47c9dec8253f2231e909f382"
    },
    {
      "path": "evals/prepare.py",
      "sha256": "7fe8badb85362b10dc87d7eb9ef84fb88419366904a0e250a48ff1148c1a739e"
    }
  ],
  "evidence": [
    {
      "path": "evals/results/first-use-root-001.json",
      "sha256": "e4d3340ef2a76e311c8d24264b004a49cb7b12c48d25ea556abfe97f03df50c1"
    },
    {
      "path": "evals/results/package-check-001.json",
      "sha256": "10b379c36a155ae25ee44d23e80b8c181909f6f0a5dacbee6e0a57476a81cbce"
    },
    {
      "path": "evals/results/automated-py314-001.json",
      "sha256": "76d9d9d6f1fd8437837a4792155b1c40af64ce59c17c52691c689c7d5882133c"
    }
  ]
}
---

# 本地实验版集成验收

检查者：root。日期：2026-09-05。

在最终根目录实际执行首次使用说明的完整命令块，验证模板化情景生成、只读
校验、指纹命令、小项目执行和测试套件能够一同工作，全部退出 0。
另核对技能格式、内部链接、归档产物字节以及自动测试绑定的源码与当前文件一致。
三个任务各有独立检查；本记录覆盖当前可使用包与说明的组合。

接受 0.1.0-alpha.1 本地实验版。原始私人会话与临时工作目录被 Git 忽略。
未测试跨客户端自动触发、并发写入或长期生产效果；未发布到 GitHub。

