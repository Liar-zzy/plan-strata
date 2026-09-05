---
{
  "schema": 1,
  "kind": "check",
  "id": "T01-check-001",
  "task": "T01",
  "plan": "plans/ex-plans/P002/ex-plan-v0.1.0.md",
  "plan_sha256": "aa04df317c01a9a609d674123c6321721a0895f67d7454d808b3b0fd942cbecb",
  "verdict": "pass",
  "subjects": [
    {
      "path": "README.md",
      "sha256": "2c3fa48dfc98c7de746dbf58aec8dff39ef0ecf266f1622e1b0cca83bc7ec405"
    },
    {
      "path": "README.zh-CN.md",
      "sha256": "bf891d3a8843076e5a3c5212aad535f76a185c4215030e92fc81255a08a19ffe"
    },
    {
      "path": "docs/PUBLISHING.md",
      "sha256": "3c50edeb9a604542db0e10882c6d9059e228e088c2e4b122186356fae7e0fd3d"
    },
    {
      "path": "docs/evidence/P002-release-preparation.md",
      "sha256": "9c59c7de649a9a62103c8d8ab8efc91c9591fb13597fecef4113bb054be91bc7"
    },
    {
      "path": ".github/workflows/check.yml",
      "sha256": "25013dc0c9c4c5074e40711228b7a8598e3bfeb5a97afb608082d989d82003cb"
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
      "path": "tests/test_workflow.py",
      "sha256": "32156431a1799252ccf83395fd5ebdf77918232d6e67a31093e4e3867867432a"
    },
    {
      "path": ".gitignore",
      "sha256": "b84b218bbb0239c7388fe1f87e805306e2fd0088e5ca6fa0f02f202e4bc6ab68"
    },
    {
      "path": "LICENSE",
      "sha256": "7b5a822173a1122da41fe373b929cf386c04b9347ac08e127401514c79005679"
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
      "sha256": "f9f00ee951f31c88d512fc15b86db49fcab1f7d1ec8662d92d461da8b3d6855b"
    },
    {
      "path": "skills/plan-strata/references/research.md",
      "sha256": "688c4e57e1e19509fa433a0568afec4d462d5328cf3f4abe6f84415b2a1ec805"
    },
    {
      "path": "skills/plan-strata/scripts/strata.py",
      "sha256": "4e4d12a0578ea2cf4fd986a84d24020565243ceb47c9dec8253f2231e909f382"
    }
  ],
  "evidence": [
    {
      "path": "evals/results/install-local-001.json",
      "sha256": "ccaf993b03d940776e713da043eba9638c5bf7fd65ac0abc57402ee441deb6c1"
    },
    {
      "path": "evals/results/release-py310-001.json",
      "sha256": "6bdb4b9d3becc990943daa6b9cca2af55931e84ee4885219530365a577d1e807"
    },
    {
      "path": "evals/results/release-py314-001.json",
      "sha256": "96e1221f701f5a7fd916aee7da1173b398e79e0d02132f88e138983a6f72f242"
    },
    {
      "path": "evals/results/release-docs-001.json",
      "sha256": "5fe486a5cf126fb7cfca71b64528c60fd8a59e17979dea9ae0ad865b46914cb3"
    }
  ]
}
---

# P002 — 双语发布材料与安装验收

检查者：root。日期：2026-09-05。范围：本地 GitHub alpha 发布准备。

实际执行安装冒烟检查：Skills CLI 1.5.23 在两个新临时项目中分别安装到 Codex
和 Claude Code 的技能位置；每种安装包含与源目录完全一致的 12 个文件。安装后的
validate 和 fingerprint 均退出 0，演示记录 consistent / open，已有项目文件未变。
另核对检查脚本拒绝覆盖已有证据（退出 2，原字节不变），空源目录返回 fail / 退出 1。

实际执行 Python 3.10 与 3.14 的 20 项合约测试，均退出 0。技能格式校验通过；
工作流 YAML 已解析，事件、只读权限、Python 矩阵及固定 action 提交通过静态核对。
中英文说明的 5 个 shell 块一致，抽取的演示命令退出 0；53 个本地 Markdown 链接
存在。所有证据报告中的 subject 哈希与本轮最终源文件一致。

人工审阅确认两种语言保留相同使用范围和 alpha 边界，发布草稿包含英文简介、
Topics、Release 文案、安装覆盖风险及 push 后核验步骤。有限密钥模式扫描无命中，
私人会话与临时目录未进入可发布文件集合；不将此声明扩大为完整安全审计。

接受本轮本地交付，不承诺首次远端下载、GitHub CI、客户端自动发现、全局安装或
跨客户端行为已经验证。P001 冻结记录保留，旧 README 在提交 409f31d 中可找回；
本检查重新接受当前发布材料，不修改或复用旧 README 的通过结论。

下一步：交用户审阅；仅在收到后续指示后 push，并验证实际远端安装和 GitHub CI。
没有创建远端配置、About、tag 或 release。本轮技能包内容和版本保持不变。
