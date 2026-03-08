# Collect Instruction

- 只处理 `collect` 阶段。
- 只读取本目录内的 `INSTRUCTION.md`、`WORKFLOW.md`、`RULES.md`。
- 禁止默认读取 `scan/` 或 `push/` 阶段文档，除非用户显式要求。
- 输入前提是 `assets/managed_targets/scan_report.json` 已存在。
