---
doc_id: skillsmanager_mirror_to_codex.path.rename_sync.tools
doc_type: tools_doc
topic: Rename sync tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: After the command surface, continue with rename order.
---

# Rename 同步工具

## 可直接使用的命令
- `python3 ./scripts/Cli_Toolbox.py --scope skill --skill-name <new_name> --mode rename --rename-from <old_name>`
- 只读演练：
  - `python3 ./scripts/Cli_Toolbox.py --scope skill --skill-name <new_name> --mode rename --rename-from <old_name> --dry-run`

## 工具约束
- rename 之前先盘清影响面。
- 覆盖同步与目录改名保持同一闭环，不拆成长期双目录策略。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
