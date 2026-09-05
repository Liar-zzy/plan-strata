---
{
  "schema": 1,
  "kind": "check",
  "id": "T03-check-001",
  "task": "T03",
  "plan": "plans/ex-plans/P001/ex-plan-v0.1.0.md",
  "plan_sha256": "67d145264016c002c49bb450d6075c7011b697d846c60e38d12c4383b2516f0f",
  "verdict": "pass",
  "subjects": [
    {
      "path": "docs/validation.md",
      "sha256": "0ed440ece0bf68f5d0e607681892b4cb0cf361589d4812d69cdd1b9832dc4667"
    },
    {
      "path": "evals/README.md",
      "sha256": "1937740274e8f75cbffda11b2143485336545b893755a436e18e46486a9585d5"
    },
    {
      "path": "evals/expected.md",
      "sha256": "bc339a61324376def867fe526f61ff2ea6efbfbfb07801ac7b9e550bc101b86e"
    },
    {
      "path": "evals/run_checks.py",
      "sha256": "fea1edd5c57d2f6aa629204ac6809b3c874cf2f9edcc8445455126ffe50e5278"
    },
    {
      "path": "evals/capture.py",
      "sha256": "fb366d649d0d210e6096279c927d938f0b6f50be6307a7c4d2b35635f28ffbb0"
    }
  ],
  "evidence": [
    {
      "path": "evals/results/resume-001.json",
      "sha256": "827ad7e316801e8ce7581f6655e1145535dc07f3bade17409ee424b396728f2b"
    },
    {
      "path": "evals/results/switch-001.json",
      "sha256": "4ea8d681fbf5d7147d48d729ab15ef74ab737b618544044cd2d6d37a577140ea"
    },
    {
      "path": "evals/results/stale-001.json",
      "sha256": "6fb5a05ba7298c6ff2aec46827b255ddc1dce82c886a1fff920c826b3a6952a2"
    },
    {
      "path": "evals/results/integration-001.json",
      "sha256": "3e502f29f95eabe709b4eb3b1ab242cad45c547bb256352cc5bf5fd12e57dc1a"
    },
    {
      "path": "evals/results/research-001.json",
      "sha256": "a1b690d03384499aea63615488f6e08ea4e50d67218d91780c597de17b06ad74"
    },
    {
      "path": "evals/results/research-002.json",
      "sha256": "b97686b940e4633407c9c51aaef77dff4c3c98d7ebd14f48abd66362f42e3ea4"
    },
    {
      "path": "evals/results/handoff-001.json",
      "sha256": "2314daeb2a3acadb661e322f5a82c714e7fa84ead9f7b60690a5641aaace277b"
    },
    {
      "path": "evals/results/package-check-001.json",
      "sha256": "10b379c36a155ae25ee44d23e80b8c181909f6f0a5dacbee6e0a57476a81cbce"
    }
  ]
}
---

# T03 — 场景验证与结论记录

检查者：root。日期：2026-09-05。

阅读各次 EVALUATION、检查和交接，并对完成后的各个隔离项目重新运行校验。
四个开发情景与科研负结果情景表现符合事先定义的行为要求；open 结果与该情景
待处理的集成、修复或基线接受一致。科研预算歧义已修正文案，由另一新会话复测。

已检查七份前向试用快照的 129 个文字产物，其文本与记录 SHA-256 一致。
报告准确区分一个开发评测会话中的四场景、独立科研会话及真实文档交接，
没有把这些样本转化为通过率、长期效果或真实科研证据。

接受本轮可复现记录与局限说明。下一轮关注实际恢复成本和信息缺口，当前任务
无需继续增加场景即可结束。

