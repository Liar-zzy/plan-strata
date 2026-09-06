# Plan Strata

[English](README.md) · 简体中文

面向 AI 辅助开发与科研的版本化计划、可恢复进度与基于证据的交接。

Plan Strata 是一个用于跨会话工作的开源 Agent skill。它帮助 Agent 从文件恢复：
之前约定了什么、任务开始时依据哪个计划、实际检查过什么，以及下一步该做什么。
开发与科研任务可以共用一份计划，同时保留各自的验收含义。

**状态：`0.1.0-alpha.1` · MIT · 可选校验器需要 Python 3.10+。**
适合早期试用，尚不承诺生产级工作流可靠性。

> **🙌 Join us! 一起把 Plan Strata 用顺。**
> 欢迎用 AI 做项目、做科研的小伙伴参与试用！[复制可选的 AGENTS.md 反馈约定](#join-us)，
> 记录实际遇到的问题，再[提交一个脱敏案例](https://github.com/Liar-zzy/plan-strata/issues/new)。

## 快捷安装

在你希望使用此技能的目标项目目录运行：

```sh
npx skills add Liar-zzy/plan-strata --skill plan-strata
```

[Skills CLI](https://github.com/vercel-labs/skills) 会提示选择 Agent 和安装范围。
选择 **Project** 即安装到当前项目。需要 Git 和 Node.js；本轮验证的安装器版本
为 `1.5.23`，要求 Node.js 22.20+。只会安装 `skills/plan-strata/` 技能目录，
不会把本仓库的开发计划和评测材料装进你的项目。

Codex 项目级免交互安装：

```sh
npx --yes skills@1.5.23 add Liar-zzy/plan-strata --skill plan-strata --agent codex --yes
```

Claude Code 将参数改成 `--agent claude-code`；需要用户级安装时加 `--global`。
这里固定的是**安装器版本**，不是 Plan Strata 版本。重复安装可能替换同名技能，
请先备份本地修改；去掉末尾的 `--yes` 可以查看交互确认。技能在宿主 Agent 的
权限范围内运行，使用前请阅读[技能说明](skills/plan-strata/SKILL.md)。第三方安装器
包含遥测，可设置环境变量 `DISABLE_TELEMETRY=1` 关闭。

### Codex 无需 Node.js 的安装方式

如果你的 Codex 配置中包含 `$skill-installer`，在 **Codex 对话框**而非终端发送：

```text
$skill-installer 从 https://github.com/Liar-zzy/plan-strata 安装 plan-strata，技能路径是 skills/plan-strata。
```

也可以手动把整个 `skills/plan-strata/` 复制到目标项目的
`.agents/skills/plan-strata/`，保留全部子目录；替换已有安装前先检查本地修改。
Codex 支持从这个项目级位置发现技能；如果未显示，重启客户端。安装和发现规则见
[官方说明](https://learn.chatgpt.com/docs/build-skills)。

GitHub 安装命令需要远端已经包含技能文件。首次 push 前，可将命令中的
`Liar-zzy/plan-strata` 替换为本地仓库的绝对路径。本项目是独立 skill，
不是已经上架的插件市场包。

## 开始使用

在 Codex 中使用 `$plan-strata`；其他 Agent 使用其技能选择器，或明确要求加载
`plan-strata`。例如：

**项目开发**

> 使用 $plan-strata，为 CSV 导出功能规划一轮范围明确的迭代。记录范围、依赖和
> 验收方法，暂时不要实施。

**科研管理**

> 使用 $plan-strata，比较现有 baseline 和候选方法的结果。预算为一个固定比较，
> 允许确定性复算，但不允许新增实验。记录研究发现，以及继续、修订还是停止。

**断点恢复**

> 使用 $plan-strata，从本项目的文件恢复当前迭代，继续下一项已授权任务，
> 并留下经过检查的交接记录。

Agent 使用你的语言撰写项目记录。你提供工作范围和资源边界，技能指导文件与证据
维护。普通问答和孤立的小修改通常不需要建立计划目录。

## 文件如何分工

| 文件 | 负责的信息 |
|---|---|
| `core` | 项目目的、范围、关键约束和停止边界 |
| `ex-plan` | 一轮工作的任务定义、依赖、方法和验收要求 |
| `progress` | 当前状态、负责人、确切执行绑定、下一步和检查引用 |
| `check/` | 实际检查对象、证据、适用范围内的结论及限制 |
| `CURRENT.md` | 为新工作显式选定的入口 |

任务开始时绑定确切计划；切换 `CURRENT.md` 不会静默重分配运行中的任务。
证据与被检查文件不再匹配时，需要重新审查。单项任务通过，集成仍可能未完成。
有效的科研活动可以以负结果或不确定发现结束。

完整记录定义见[协议](skills/plan-strata/references/protocol.md)；验收分别遵循
[开发说明](skills/plan-strata/references/development.md)与
[科研说明](skills/plan-strata/references/research.md)。

## 可选的只读校验器

完成 Codex 项目级安装后，从**目标项目根目录**运行：

```sh
python3 .agents/skills/plan-strata/scripts/strata.py validate --project .
```

需要先让 Agent 创建或适配项目计划；安装技能本身不会自动生成计划文件。
其他安装位置请相应调整脚本路径。计算文件指纹时，使用同一脚本的
`fingerprint --project . path/to/file` 子命令。

工具只依赖 Python 3.10+ 标准库。项目 metadata 使用两个 `---` 之间的 **JSON**，
之后是 Markdown 正文，而非任意 YAML。已有不同格式的工作流可手工检查，无需迁移。

`status: consistent` 表示声明的记录一致；`overall: verified` 表示当前记录满足
本轮验收结构。两者都不能证明测试实际运行过、证据真实或科学结论成立。
工具不会执行 Markdown 中的命令、修改记录、启动实验或上传内容。

## 小场景试用

以下命令在**本仓库的完整克隆**中运行；只安装技能包不包含演示生成器：

```sh
strata_trial_dir=$(mktemp -d)
python3 evals/prepare.py --scenario resume --destination "$strata_trial_dir/project"
python3 skills/plan-strata/scripts/strata.py validate --project "$strata_trial_dir/project"
```

预期输出为 `consistent / open`：其中一个文档任务刻意保留为未完成。
把新目录与技能交给新会话继续工作即可。其他合成场景包括 `switch`、`stale`、
`integration` 和 `research`。详细步骤见[第一次使用说明](docs/FIRST_USE.md)。

贡献者可运行：

```sh
python3 -m unittest discover -s tests -v
python3 skills/plan-strata/scripts/strata.py validate --project .
```

## 验证与当前边界

首轮 alpha 在 Python 3.10 与 3.14 上通过 20 个合约检查，完成五类场景试用，以及
一次无原会话上下文 Agent 接手的真实文档任务。科研场景数据为合成数据。
[验证记录](docs/validation.md)链接了保留的证据；[发布准备说明](docs/PUBLISHING.md)
区分本地安装检查和 push 后仍需进行的 GitHub 检查。

- 工具检查显式列出的本地文件与依赖，不推断隐含依赖或内容真实性；外部对象需另行核验。
- 使用单一进度维护者。并行执行依赖实际环境的隔离和集成方式，技能不提供调度器或锁。
- 哈希标识文件字节，不是防篡改签名；历史快照通过版本控制和工作约定保留。
- 尚未建立长期生产使用、真实科研效果、客户端自动发现或跨客户端 Agent 行为的验证结论。

## Join us!

不写代码也能参与。哪一步交接卡住了、哪条说明看不懂、哪些记录操作比实际工作
还费劲，都欢迎告诉我们。

将下面这段**可选约定追加**到你实际使用技能的目标项目 `AGENTS.md` 中，保留原有
指令；如果你的 Agent 使用其他项目指令文件，可相应调整位置。它只收集本地观察，
不会自动向外发送反馈。

```markdown
## Plan Strata 使用反馈

使用 plan-strata 时，留意实际遇到的规则歧义、流程阻塞、状态与证据
不一致，以及明显多余的记录成本。保持当前项目任务优先。

- 在阶段结束或交接时，将问题记录到 docs/plan-strata-feedback.md。
  首次发现问题再创建文件，同类问题合并。
- 记录可获得的技能版本或来源、开发/科研场景、预期与实际行为、
  任务影响、临时处理方式，以及本地证据引用或脱敏后的最小复现。
- 将观察事实与原因推测分开；无法确定是否属于技能问题时标为
  “待确认”，保留环境或使用方式导致问题的可能。
- 任务状态仍以项目原有进度记录为准，反馈文件只记录技能问题，
  不维护第二份任务清单。
- 涉及数据安全或验收真实性时，先说明问题并暂停受影响的动作；
  其他情况记录有依据的临时处理方式后继续任务。
- 修改或升级已安装技能、向 GitHub 提交反馈，需另行获得授权。
  反馈记录不包含私人数据或凭据，对外分享前检查并脱敏相关材料。
- 未发现问题时无需生成反馈，也不为寻找技能问题额外启动实验。
```

检查本地记录后，选一个脱敏案例[提交 issue](https://github.com/Liar-zzy/plan-strata/issues/new)
即可，无需上传完整项目、聊天记录或未公开研究。确认的问题可以帮助我们修正规则、
补充回归检查，也删减不必要的流程。

## 仓库结构与贡献

`skills/plan-strata/` 是可分发技能包；`plans/` 管理技能自身的开发；`evals/` 和
`tests/` 用于复现检查。历史检查描述当时版本，不自动为后续变化背书。
私人设计会话与临时试用目录继续被 Git 忽略。

修改用户可见行为时，请同步中英文 README。

技能封装遵循 [Agent Skills](https://agentskills.io/specification)。设计讨论参考了
[Planning with Files](https://github.com/OthmanAdi/planning-with-files)、
[Superpowers](https://github.com/obra/superpowers)，以及
[COS 对探索与验证性研究的区分](https://www.cos.io/initiatives/prereg)。
规则与辅助代码为本项目实现，没有复制这些项目的工作流代码。授权见 [MIT License](LICENSE)。
