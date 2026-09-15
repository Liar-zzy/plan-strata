# Plan Strata

[English](README.md) · 简体中文

面向 AI 辅助开发与科研的版本化计划、可恢复进度与基于证据的交接。

Plan Strata 是一个用于跨会话工作的开源 Agent skill。它帮助 Agent 从文件恢复：
之前约定了什么、任务开始时依据哪个计划、实际检查过什么，以及下一步该做什么。
开发与科研任务可以共用一份计划，同时保留各自的验收含义。

**状态：`0.2.0-alpha.1` · MIT · 可选校验器需要 Python 3.10+。**
适合早期试用，尚不承诺生产级工作流可靠性。

> **Schema 2：默认流程不再使用哈希。** 此版本移除必填哈希与 `fingerprint` 命令；
> 校验器只检查结构，不证明文件未变或测试充分。旧 schema 1 项目需明确迁移，见
> [迁移与版本说明](docs/v0.2.0-alpha.1.md)。下面的默认安装使用 `main`，
> 包含这套无哈希流程。

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

### 选择安装来源

上面的仓库简写使用 `main`，包含 schema 2 流程与精简指令。`dev` 是独立开发
分支，不是安装前提，也不保证与 `main` 指向同一快照。

已有同名安装请先检查并备份。需要审查源码或使用未发布修改时，检查选定 checkout，
再按上面的手动方式复制整个 `skills/plan-strata/` 目录。远端 checkout 只包含
已推送修改；仓库更新不会自行升级已安装副本。

来源可确定时，记录分支、commit 和本地修改。同一个 alpha 版本号可能对应不同
快照；安装包来源不明时，记录不确定性、安装位置与可见版本，无需计算文件
哈希，也不要求为记账额外 commit。不能用另一个
仓库的 HEAD 冒充安装版本。本项目是独立 skill，不是已经上架的插件市场包。

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

Agent 使用你的语言撰写项目记录。明确要求建立 Plan Strata 计划，或执行、恢复、修订、
验收已纳入其管理的工作时使用本技能。未绑定的普通问答、诊断和小改不自动触发。
当前请求或可追溯到用户批准批次的派工，在原范围内提供授权；CURRENT、`ready`
和工具可用性本身不构成授权。

实施与范围内返修可以保留在同一个任务内：

> 完成已约定的完整能力并自检，修复不符合原验收标准的问题。在当前范围和资源
> 限制内继续，向我汇报结果或需要我决策的阻塞。新增需求单独列出，不 push、不发布。

普通本地返修不必自设轮次、测试额度或预算账本；明确限额和实质资源消耗仍有边界。
同一 Worker 可以沿原派工继续，用新交付版本返回，不必重新派工。保留旧交付与检查，
被检输入改变后重新验证。详见[返修与交付](skills/plan-strata/references/repair-loop.md)。

## 文件如何分工

优先复用项目已有任务卡、PR/CI 证据和进度记录。下表是可选的 bundled 格式，
不要求在现有流程旁再建一套台账。项目替代格式手工核对，不由 bundled 解析器校验。

| 文件 | 负责的信息 |
|---|---|
| `core` | 项目目的、范围、关键约束和停止边界 |
| `ex-plan` | 一轮工作的任务定义、依赖、方法和验收要求 |
| `progress` | 当前状态、负责人、确切执行绑定、下一步和检查引用 |
| `check/` | 实际检查对象、证据、适用范围内的结论及限制 |
| `CURRENT.md` | 为新的 Plan Strata 管理工作显式选定的入口 |

任务开始时保留明确绑定：bundled schema 2 使用版本化计划路径，项目替代格式使用
其明示绑定，schema 2 不要求哈希。切换 `CURRENT.md` 不会静默重分配运行中的任务。
相关输入变化后，由指定 writer 重开受影响的验收，获准审阅者复测；校验器不会
自动发现这些变化。单项任务通过，集成仍可能未完成。
有效的科研活动可以以负结果或不确定发现结束。

恢复时补齐缺失或过时的上下文，不必每轮重读全部记录。实现、调试和测试方式可在
已约定的范围、验收、接口依赖和资源边界内自主调整；只有这些承诺或固定科研方法
改变时才修订计划，项目目的与关键约束未变则沿用 core。

完整记录定义见[协议](skills/plan-strata/references/protocol.md)；审阅遵循
[验收约定](skills/plan-strata/references/protocol.md#acceptance)与
[科研说明](skills/plan-strata/references/research.md)。

## 可选的并行交接

并行执行默认关闭，需明确授权当前迭代/批次。已批准派工沿用该授权；只请求方案
不授权实际派发。不需要额外技能开关，例如：

> 使用 $plan-strata，为当前这一轮启用并行交接。把已就绪且独立的任务交给最多
> 两个本地 Worker。你作为 Manager 检查交付，验证最终组合状态。所有工作保持
> 本地，不创建 Issue、不 push、不合入主分支。

沿用宿主工具和已有分配适配。宿主派工消息与绑定任务卡可共同构成完整交接，
不必另建 packet。已有适配保证独占分配时，由指定 writer 在宿主返回 Agent ID 后
补记回执；否则先登记分配再执行。共享接口、冲突写入和实际资源限制仍需协调。
宿主不能派发子 Agent 时，可在授权内使用手工交接或串行执行。

Worker 完成产物、自检和报告即交付待审；Reviewer 完成范围内检查。只有获准
Manager 决定接受，只有指定 writer 修改进度（默认 Manager）。同一 Agent 可兼任
已获准角色。现有 CI 或合适环境可以验证最终组合状态，不强制另设 Integrator
Agent 或工作目录；实际冲突写入仍需隔离。

本模式覆盖一份 ex-plan，不要求 Git/GitHub。Issue 可以承载完整任务说明，引用
固定且可访问的上下文；说明完整、依赖就绪和已被分配是不同条件。任务单或 Issue
不会启动 Agent，对外发布、付费任务及合并仍需相应授权。

输入缺失、范围冲突或需要新授权时，只暂停受影响动作，继续独立的授权工作。
只有验收关键路径无法继续时才阻塞整个任务；明确停止指令与共享资源限制仍有效。

详见[交接说明](skills/plan-strata/references/parallel-handoff.md)及可选的
[Worker](skills/plan-strata/assets/task-handoff.md) /
[集成交接](skills/plan-strata/assets/integration-handoff.md)模板。
贡献者可[重建本地双 Worker 试用](evals/README.md#parallel-handoff-trial)。
这些 Markdown 契约是指导，不是机器校验记录或内置调度器。

## 可选的只读校验器

完成 Codex 项目级安装后，从**目标项目根目录**运行：

```sh
python3 .agents/skills/plan-strata/scripts/strata.py validate --project .
```

需要先让 Agent 创建或适配项目计划；安装技能本身不会自动生成计划文件。
其他安装位置请相应调整脚本路径。此流程不再要求计算哈希。

工具只依赖 Python 3.10+ 标准库。项目 metadata 使用两个 `---` 之间的 **JSON**，
之后是 Markdown 正文，而非任意 YAML。已有不同格式的工作流可手工检查，无需迁移。

输出明确包含 `validation_scope: structure_only`。
`status: consistent` 表示声明的记录一致；`overall: accepted` 表示当前记录满足
本轮验收结构。两者都不能证明输入未变、测试实际运行且充分、证据真实或科学结论成立。
相关修改后需显式复核，保留旧检查，并在受影响的验证完成后新增检查。
工具不会执行 Markdown 中的命令、修改记录、启动实验或上传内容。先报告不一致，
仅在当前角色和写入范围授权时修复；其他角色将发现交给负责的 writer。

自动化调用请按[退出码契约](skills/plan-strata/references/protocol.md#reading-validation-output)
处理：记录校验问题（包括非法 `--current` 路径）使用 `1`，参数解析或项目根目录
初始化失败使用 `2`。退出 `0` 本身不代表任务完成。

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

[0.2.0-alpha.1 版本说明](docs/v0.2.0-alpha.1.md)记录无哈希迁移、本轮验证和剩余
限制。下方旧验证记录属于历史证据，不为当前版本自动背书。

首轮 alpha 在 Python 3.10 与 3.14 上通过 20 个合约检查，完成五类场景试用，以及
一次无原会话上下文 Agent 接手的真实文档任务。科研场景数据为合成数据。
[验证记录](docs/validation.md)链接了保留的证据；[发布准备说明](docs/PUBLISHING.md)
区分本地安装检查和 push 后仍需进行的 GitHub 检查。

[主分支 hotfix 记录](docs/validation-main-hotfix.md)说明保留任务标识、循环链接诊断
及输入清单范围的修复与验证。

alpha.2 的[首次并行交接试用](docs/validation-parallel.md)保留为历史证据；随后针对
接收端基线与保留标识的修复，见[对应回归记录](docs/validation-handoff-fixes.md)。
[Issue 冷启动记录](docs/validation-issue-handoff.md)另行保留“本地 Issue 正文 →
新 worktree”的独立接手过程及实际失败。这些检查不代表真实 GitHub 派发、
运行时编排或生产并发已验证。
[有限修复回归记录](docs/validation-repair-loop.md)覆盖证据保留和 CLI 分类，
不代表自主 Agent 的闭环行为或人工交接成本下降已得到验证。

- 工具检查显式列出的本地文件与依赖，不推断隐含依赖或内容真实性；外部对象需另行核验。
- 使用单一进度维护者。并行执行依赖实际环境的隔离和集成方式，技能不提供调度器或锁。
- 不要求哈希。工具不读取产物内容、不自动发现变化，也不判断测试覆盖；由审阅者
  复核相关修改，利用已有版本控制或交付记录保留必要版本，Git 本身仍可选。
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
  来源可确定时补充 commit 和本地修改；否则标为未知并标识实际安装文件，
  不默认认为某个 checkout 与安装副本相同。
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
