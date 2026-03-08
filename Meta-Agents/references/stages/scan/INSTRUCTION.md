# Scan Instruction

- 只处理 `scan` 阶段。
- 只读取当前目录下的 `INSTRUCTION.md`、`WORKFLOW.md`、`RULES.md`。
- 禁止默认读取 `collect/` 或 `push/` 阶段文档，除非用户显式要求。
- 输出目标是 `assets/managed_agents/scan_report.json`。
