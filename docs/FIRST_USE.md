# 第一次使用 Plan Strata

从仓库根目录运行下面的流程，可以得到一个可交给新会话的隔离演示项目，核对
命令输出，并了解计划、进度和检查之间的关系。当前版本是 `0.1.0-alpha.1`
本地实验版。首次尝试无需安装 Python 包，也不需要 Git 元数据或联网。

## 准备

需要 Python 3.10+、bash 或 zsh，以及本仓库的完整副本。先在终端进入包含
`README.md`、`skills/`、`evals/` 和 `tests/` 的仓库根目录。
只有 `skills/plan-strata/` 是可安装技能包；下面的演示生成器与自动测试属于
仓库配套材料，单独安装技能后不会自动包含它们。

本仓库根目录的 `plans/` 管理技能本身的开发。下面生成的 `project/plans/`
管理求和工具的合成演示；两处都可能叫 P001，使用时要同时确认项目目录。

## 运行可复现的首次检查

把整个代码块复制到同一个终端执行。括号使变量与严格退出设置只影响本段命令。
临时目录创建在当前仓库内；每次运行使用新目录，不覆盖原文件。测试临时文件
也留在该目录范围内，由测试框架自行清理；演示项目会保留供接手。

```sh
(
  set -eu
  python3 --version
  strata_repo_dir="$PWD"
  strata_trial_dir=$(mktemp -d "$strata_repo_dir/.first-use.XXXXXX")
  printf '技能路径：%s\n试用项目：%s\n' "$strata_repo_dir/skills/plan-strata/SKILL.md" "$strata_trial_dir/project"
  PYTHONDONTWRITEBYTECODE=1 python3 evals/prepare.py \
    --scenario resume --destination "$strata_trial_dir/project"
  PYTHONDONTWRITEBYTECODE=1 python3 skills/plan-strata/scripts/strata.py \
    validate --project "$strata_trial_dir/project"
  PYTHONDONTWRITEBYTECODE=1 python3 skills/plan-strata/scripts/strata.py \
    fingerprint --project "$strata_trial_dir/project" \
    plans/ex-plans/P001/ex-plan-v0.1.0.md src/calc.py \
    tests/check_total.py observations/total.log
  (
    cd "$strata_trial_dir/project"
    PYTHONDONTWRITEBYTECODE=1 python3 tests/check_total.py
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -c \
      'from calc import total; print(total([1, 2, 3])); print(total([]))'
  )
  TMPDIR="$strata_trial_dir" PYTHONDONTWRITEBYTECODE=1 \
    python3 -m unittest discover -s tests -v
)
```

预期结果：

- Python 显示版本号；生成器打印新项目路径。请保存开头打印的技能和项目路径。
- `validate` 返回 JSON：`status` 为 `consistent`，`overall` 为 `open`，
  T01 为 `done`，T02 为 `planned`，当前计划为 `ex-plan-v0.1.0.md`。
  文件夹里的 `ex-plan-v0.2.0.md` 是未选中的草案，不能按版本号自动选它。
- `fingerprint` 打印四个文件的 SHA-256；这些值标识当前完整文件字节。
  日志中含实际 Python 路径，所以不同环境不必得到完全相同的日志哈希。
- 小项目检查打印 `empty input and numeric sum passed`；随后数字示例打印
  `6` 和 `0`，分别表示 `[1, 2, 3]` 求和与空输入的结果。
- 仓库自动检查以 `Ran 20 tests` 和 `OK` 结束。以上每条命令预期退出码为 0；
  任一失败会结束本段执行，应先查看该命令输出。

`consistent` 只说明记录、引用、已声明依赖与哈希一致；它不表示本轮完成，
也不代替实际测试。本演示的文档任务仍待完成，因此 `open` 是正常起点。
自动测试使用合成数据与小项目，不能据此推断生产环境或长期研究效果。

## 交给一个新会话

让支持读取本地技能的 Agent 打开上面打印的技能路径，以打印的试用项目目录
作为工作目录。将下文的两个方括号替换成真实绝对路径，再发送：

> 请读取并使用 [技能路径]。目标项目是 [试用项目路径]。接着把当前这一轮剩下的
> 工作做完，留下检查和交接记录。请从项目文件恢复范围，记录实际执行的命令、
> 输出与退出码，并核对证据后再决定是否完成。

作为首次体验，只提供技能、生成项目与请求即可。正式开展无历史上下文评测时，
不要提前向接手者提供生成器、自动测试或评分标准；完整评测方法见
[评测说明](../evals/README.md)。本说明的命令核对与真实仓库文档交接，不能
替代该项独立前向试用。

接手者应先读 `plans/CURRENT.md`，恢复选中的 core、执行计划和 progress，
再读下一项所需的实际产物及已有证据。对于已经开始的任务，使用 progress 中
的 `plan` 和 `plan_sha256`，即使 CURRENT 后来选择了别的版本也要先处理原绑定。
演示项目的剩余 T02 是写 `docs/usage.md`；本仓库的 T02 则是本说明，二者不同。

## 在自己的项目中开始或恢复

已有计划时保留项目原有位置与术语，并让 Agent 读取项目指令和任务交接。
新建迭代时，从技能的 `assets/` 取 core、ex-plan、progress、CURRENT 模板，
填写本轮目标、资源边界、任务输入输出、依赖和实际验收方法。新计划默认
`ready: false`；完成定义后才能显式选择为新工作入口。

文件职责及执行顺序是：

1. core 固定项目目的与关键边界；执行计划固定任务与验收。首次使用前计算
   core 哈希填入计划；选定 ready 计划后计算其哈希，一次更新 CURRENT 的
   `plan`、`plan_sha256` 和 `progress`。
2. progress 是任务实时状态的唯一位置。开始时填写负责人、下一步、计划路径
   与哈希。多人工作时指定一个进度维护者，各自提交独立报告及隔离产物。
3. 执行实际验收方法，保存日志或具体审阅观察；用 `fingerprint` 记录产物与证据。
   check 需写明检查者、日期、方法、实际结果、限制和下一步，不能引用自身作证据。
4. 在检查通过且依赖完成后，progress 引用该检查并标为 `done`。需要集成时还要
   单独检查集成；科研检查还要区分活动有效性、研究发现与后续决定。
5. 再运行 `validate --project <目标项目目录>` 核对记录。当前所有任务完成，且
   所需集成检查通过，才可能得到 `overall: verified`。

上述 metadata 使用两个 `---` 之间的 JSON 对象，模板中的 `REPLACE_WITH_HASH`
必须替换为真实哈希。工具不会把普通 YAML 当作这个受限格式解析。所有记录路径
以目标项目为基准，使用无 `..` 的相对 POSIX 路径。命令和完整协议见
[协议](../skills/plan-strata/references/protocol.md)；开发与科研分别遵循
[开发说明](../skills/plan-strata/references/development.md)和
[科研说明](../skills/plan-strata/references/research.md)。

已开始使用的 core 和计划保持原字节；变更范围、依赖或验收时新建修订，明确
切换入口并重新判断旧结果的适用性。产物或证据变化后不能继续沿用旧通过声明。
交接时记录路径、已检查内容、限制、下一步，以及仍在运行的作业编号和输出位置。

## 常见起步问题

- 找不到 `evals/prepare.py`：检查当前目录与是否只有安装后的技能包。最小技能包
  可以管理目标项目；本说明的演示需要完整仓库。
- 生成器提示目标已存在：它明确拒绝覆盖。重新运行完整代码块产生新目录即可。
- 校验退出码 1：存在记录不一致，按 JSON 的 `errors` 检查。退出码 2：调用或
  路径失败。退出码 0 也应单独读取 `overall` 与 `warnings`。
- `PLAN_CHANGED`、`CORE_CHANGED` 或 `STALE_SUBJECTS`：先检查实际变化，保留
  原快照与历史检查，再按修订或重新验收流程处理，不能只改哈希掩盖变更。
- 提示 `INTEGRATION_OPEN`：整轮仍缺少适用的通过集成检查，不可仅据任务测试收尾。

本次 T02 的实际环境、命令输出、问题和检查范围见
[首次使用验证证据](evidence/T02-first-use-commands.md)与
[T02 验收记录](../plans/ex-plans/P001/check/T02-check-001.md)。
