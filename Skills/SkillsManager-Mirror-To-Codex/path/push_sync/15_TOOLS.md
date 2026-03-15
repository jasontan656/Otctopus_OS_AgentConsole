---
doc_id: skillsmanager_mirror_to_codex.path.push_sync.tools
doc_type: tools_doc
topic: Push sync tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: After the command surface, continue with execution order.
---

# Push 同步工具

## 可直接使用的命令
- 单技能 push：
  - `python3 ./scripts/Cli_Toolbox.py --scope skill --skill-name <skill_name> --mode push`
- 全量 push：
  - `python3 ./scripts/Cli_Toolbox.py --scope all --mode push`
- 只读演练：
  - `python3 ./scripts/Cli_Toolbox.py --scope skill --skill-name <skill_name> --mode push --dry-run`

## 工具约束
- `.system/*` 技能会自动映射到 codex 目录中的小写规范名。
- CLI 输出 `command` 或 `commands`，用于确认实际同步命令。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
