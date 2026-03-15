---
doc_id: skillsmanager_tooling_checkup.path.cli_surface.tools
doc_type: topic_atom
topic: Tools for CLI surface checking
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: CLI surface tools are applied in the execution step.
---

# CLI Surface 检查工具

## 当前动作会用到什么
- 本技能的 `scripts/Cli_Toolbox.py govern-target --target-skill-root <path> --json`
- 目标技能自己的 `scripts/Cli_Toolbox.py`
- 目标技能的 `read-contract-context`

## 当前动作必须满足什么
- 若目标技能声称自己能编译整条链路，就必须直接执行它，而不是只看文档声明。
- 若目标技能同时保留 `read-path-context`，应与 `read-contract-context` 指向同一编译结果。
- 不能把只打印文件路径或只打印提示语的命令视为合格的链路编译 CLI。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
