---
{
  "schema": 1,
  "kind": "check",
  "id": "T01-check-001",
  "task": "T01",
  "plan": "plans/ex-plans/P004/ex-plan-v0.1.0.md",
  "plan_sha256": "a7baee06182095ad1472cb06bda4198cc4e5e3b42c6b4eaa2f82db1936307bab",
  "verdict": "pass",
  "subjects": [
    {
      "path": "README.md",
      "sha256": "e272e2cc3b6344296b4e9d6bea0fdadad15c9244f0ef5deb4c76c6eb413c4989"
    },
    {
      "path": "README.zh-CN.md",
      "sha256": "c3bde2f60a12798d89cfb4d123eb2d04ee4aa1f7c8534d17e358a84c0263df7d"
    },
    {
      "path": "docs/validation-handoff-fixes.md",
      "sha256": "d779d0d3e3d73b381a20e54d33ff259def9377507fd155745e61fc3e39807026"
    },
    {
      "path": "docs/validation-parallel.md",
      "sha256": "f060036e3d8507c18d8d4a72c40575e3146016ec72d6f9c5815fb548ae037f43"
    },
    {
      "path": "evals/README.md",
      "sha256": "d2192a9773e5257d3d8047b31494bdbdabedf5c29ca8c0aa88b6565195513565"
    },
    {
      "path": "evals/parallel_trial.py",
      "sha256": "75f86c395eef51780184f75094667079145bc9c2673bb50f1f5f564027975d96"
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
      "sha256": "d0c35081c22f2da0a588dd357ce92b3f7a1e2274bb28d13184b6829609cf3b6d"
    },
    {
      "path": "tests/test_parallel_trial.py",
      "sha256": "a3309213a899f4f9b759de47f2493e34cb6439ab498a02119814a859aea9d90f"
    },
    {
      "path": "tests/test_workflow.py",
      "sha256": "f8a20522d7e91f9317d0bae4fbd917ca79f7ca8178d7245fbfb48fbb04021d96"
    }
  ],
  "evidence": [
    {
      "path": "evals/results/handoff-fix-red-001.json",
      "sha256": "a365dd90c379483d1dee803115d8f983b679e2815a6ce4c03a5f105db3bc113b"
    },
    {
      "path": "evals/results/handoff-fix-red-002.json",
      "sha256": "d71c2a5a99a2655b0f684bf30cfbeb97d407c3790c049c50e5a8a12254b0b518"
    },
    {
      "path": "evals/results/handoff-fix-py310-001.json",
      "sha256": "20d11fcc8352c6c2879d182355010a54deecabfbd7a44f800a82a764a13e202b"
    },
    {
      "path": "evals/results/handoff-fix-py314-001.json",
      "sha256": "2b0dce2c97b6cb82abe49e8e60f2e5fb39b65d1ca181092535763042a6251571"
    },
    {
      "path": "evals/results/handoff-fix-replay-001.json",
      "sha256": "a98dfd92939f452f1c6e93efc509152dcf7c525f80ee5ff3afded83b3926aadd"
    },
    {
      "path": "evals/results/handoff-fix-audit-001.json",
      "sha256": "91f1b3f84e88c519f46cfde0e99954c5c746bb93dafc610fe48a779f3d3f0f1e"
    }
  ]
}
---

# P004 T01 — 局部修复与交付检查

Reviewer：root（实现作者）。日期：2026-09-07。本轮没有新的 Agent 行为试用，
也没有 Git 提交、push、远端修改、客户端安装或真实科研实验。

## 方法与实际结果

先将上轮已重复复现的接收端漂移和保留标识反例加入回归。red-001 运行 46 项，
出现 14 次失败断言（含子场景），退出 1；补查严格进度解析后 red-002 运行 49 项，
出现 1 次失败断言，退出 1。历史红色结果保留原源码指纹，不替换成最终指纹。

修复后分别用 Python 3.10.9 和 3.14.7 运行
python3 evals/run_checks.py --output <new-file.json>，49 项全部通过，退出 0。
两份绿色记录中的 22 项源码指纹均匹配最终文件。原审查脚本的三个反例分段原样
复跑，两例在接受前拒绝，一例返回 RESERVED_TASK_ID / invalid / open。

检查代码：collect/finish 在副作用前核对 Manager 输入和受保护进度；同一结果
重复收集仍先检查基线，再返回 no-op；终验要求清单成员逐项成为 subjects，动态
progress 不在其中。常规任务禁止 integration 标识，合法科研负结果仍可完成。
修复没有增加协议字段、通用清单解析、Git 适配器或调度器。

审阅默认关闭、用户明确选择当前迭代/批次、仅提案不派发、收到已授权任务单、
工具不可用时回退及外部行为授权边界。技能发现策略未改。中英文 README 各
5 段 sh 安装/试用命令与 HEAD 相同，shell 语法通过；66 个本地链接/锚点有效。
15 文件技能包格式校验退出 0，输出 Skill is valid!。git diff --check 通过。

## 范围与决定

接受 P004 T01 的本地代码与文档修复。旧 P003 计划、check 和捕获文件未改写，
首次 Agent 试用文档已显式标注历史适用范围。当前验证说明记录了红/绿证据与限制。

这不是指令遵从率、生产并发、完整依赖推断、测试充分性或科研真实性的证明。
接收检查依赖独占执行和可信本地环境，不提供锁、事务回滚或防伪收据；接受后新增
未列出文件仍需人工/Agent 审查。默认关闭是技能工作约定，不是宿主权限开关。
下一步由用户选择受控试用或授权推送到 dev；本轮不自行发布。
