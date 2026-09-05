# Plan Strata

Versioned plans, recoverable progress, and scoped evidence for development and research.

状态：`0.1.0-alpha.1`，本地实验版。一个执行计划可以包含开发和科研任务，
并由多个 Agent 共用。当前版本采用文件记录和显式交接，适合个人与小团队。

## 它管理什么

| 文件 | 负责的信息 |
|---|---|
| `core` | 项目目的、范围、关键约束和停止边界 |
| `ex-plan` | 一轮工作的任务定义、依赖、方法和验收要求 |
| `progress` | 当前负责人、状态、执行绑定、下一步和检查引用 |
| `check/` | 检查对象、实际证据、结论和适用范围 |
| `CURRENT.md` | 新工作的默认入口 |

执行开始时绑定确切计划；当前入口切换后，运行中的任务保留原绑定。
开发验收和科研判断分别定义。有效负结果可以完成一轮科研任务。

## 试用

可直接从[第一次使用说明](docs/FIRST_USE.md)开始，复制其中的命令建立一个小型试用项目。

先让支持本地技能的 Agent 读取本仓库的
[SKILL.md](skills/plan-strata/SKILL.md)，并给出一个范围明确的任务，例如：

> 使用这个 plan-strata skill，恢复本项目的计划，继续下一项已授权的工作。

也可以把整个 `skills/plan-strata/` 目录放入客户端支持的 skills 目录。
Codex 的项目级发现位置可使用 `.agents/skills/plan-strata/`；其它客户端按照其
本地技能安装方式配置。只安装这个技能目录即可，评测材料不用一起安装。
具体安装和发现行为以[客户端官方说明](https://learn.chatgpt.com/docs/build-skills)为准。

技能指导 Agent 在目标项目生成计划文件。默认使用 Markdown 和模板中的 JSON
frontmatter，辅助工具只需要 Python 3.10+ 标准库。JSON 是 YAML 的子集；工具
明确只解析这个受限格式。已有不同格式的计划可以手动检查，不必迁移。

```sh
python3 skills/plan-strata/scripts/strata.py validate --project /path/to/project
python3 skills/plan-strata/scripts/strata.py fingerprint --project /path/to/project src/example.py
```

`validate` 是只读操作。`status: consistent` 表示记录一致，`overall: verified`
才表示当前记录满足本轮验收结构；两者均不能代替检查真实证据。
命令不会执行 Markdown 中的命令、修改计划、启动实验或上传内容。

## 小场景验证

不需要完整项目。以下命令在临时目录生成一个待接手的小项目：

```sh
trial_root=$(mktemp -d)
python3 evals/prepare.py --scenario resume --destination "$trial_root/project"
python3 skills/plan-strata/scripts/strata.py validate --project "$trial_root/project"
```

把该项目和技能交给新会话，让它继续工作。可选场景为 `resume`、`switch`、
`stale`、`integration`、`research`。场景均明确标记为模拟材料；其中本地测试
命令实际执行，科研数据为合成数据。生成器拒绝覆盖已有目录。

[评测说明](evals/README.md)将执行请求与评分标准分开放置。
[验证记录](docs/validation.md)记录实际执行过的检查及限制。

运行自动检查：

```sh
python3 -m unittest discover -s tests -v
```

## 当前边界

- 辅助工具仅检查显式列出的本地文件及声明的依赖。遗漏的依赖、证据的真实性
  和研究结论，需要执行者或评审者判断。
- 大型数据、外部存储和运行环境可以通过本地清单引用；工具不会自动核验外部对象。
- 协作采用单一进度维护者，工作目录和计算资源的并发隔离由实际环境承担。
- 计划和检查的快照保留依赖工作约定与版本控制；内容哈希不是防篡改签名。
- 本轮试用尚不能证明长期生产项目或不同客户端中的稳定效果。

本仓库的 `plans/` 是开发本技能的实际工作记录；`skills/` 是可安装的技能包；
`evals/` 和 `tests/` 用于复现实验。原始私人会话导出保留在本地，并被 Git 忽略。

## 参考与贡献

技能封装遵循 [Agent Skills](https://agentskills.io/specification)。设计讨论参考了
[Planning with Files](https://github.com/OthmanAdi/planning-with-files) 的文件化记忆、
[Superpowers](https://github.com/obra/superpowers) 的完成前验证，以及
[COS](https://www.cos.io/initiatives/prereg) 对探索和验证性研究的区分。
本仓库的规则与代码为本次实现，没有复制这些项目的工作流代码。

反馈请附可复现的起始文件、实际请求、观察到的行为和预期差异；涉及私人数据时
先用最小模拟材料重现。授权见 [MIT License](LICENSE)。
