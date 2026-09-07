# main 基础验收 hotfix

日期：2026-09-07。基于 d3b28e3，只修复基础验收，不合入 dev 的并行交接功能。
保留 alpha.1 标记；本次不是新 Release/tag，以 Git 提交及保留的源码指纹区分修复。
用户已授权验证后推送 main，再同步公共修复到 dev；不修改分支保护或全局技能安装。

## 修复范围

- 普通计划任务禁止使用保留 ID integration，避免绕过科研解释字段或复用终验。
- 在项目根和记录路径的解析边界转换旧版 pathlib 的循环链接 RuntimeError。
  validate/fingerprint 返回 JSON 错误和非零退出码；保留合法项目内符号链接、
  项目外路径隔离、只读校验及有效科研负结果的原行为。不捕获整个工作流的所有异常。
- 协议说明本地输入清单成员需显式列入 subjects；没有实现清单自动展开或依赖推断。

## 实际验证

先将原审查反例写入回归。在 Python 3.10.9 上运行 26 项，出现 6 次失败，退出 1，
见[红色回归](../evals/results/main-hotfix-red-001.json)。之后做局部修复，并补充
合法项目内符号链接的兼容检查；最终两版 Python 各 27 项通过，退出 0：

- [Python 3.10.9](../evals/results/main-hotfix-py310-001.json)
- [Python 3.14.7](../evals/results/main-hotfix-py314-001.json)

命令：python3 evals/run_checks.py --output <new-file.json>。输出文件保留实际
unittest 日志和源码指纹；红色运行的历史指纹不要求匹配修复后的文件。
新增测试覆盖两种任务类型的保留 ID、循环计划引用、循环检查对象、fingerprint、
循环项目根及合法内部链接。原有 20 项测试保留，未引入并行样例来替代基础验证。

另外用修复后的校验器复跑上一轮审查脚本，见[原反例复跑](../evals/results/main-hotfix-replay-001.json)：
保留 ID 返回 invalid/open；循环链接返回 JSON 而非异常堆栈。只列清单时成员变化
仍不自动撤销接受，明确列入成员时会变为 open；这是声明范围限制，不伪称已解决。

技能格式检查使用已有离线临时 PyYAML 环境，输出 Skill is valid!。用户侧
Python 运行依赖仍仅标准库，安装接口和技能自动发现策略不变。双语入口指向此记录。
当前本地接受见 [P005 检查](../plans/ex-plans/P005/check/T01-check-001.md)。

## 交付边界

未做新 Agent 行为试用、真实科研实验或客户端发现测试。历史 P001/P002 验收文件
不改写；当前修复使用新检查。推送后的 CI 必须核对对应提交，不能以本地结果代替。
dev 的修复同步与完整并行回归另行验证，不沿用 main 的 27 项结果证明 dev 的行为。
