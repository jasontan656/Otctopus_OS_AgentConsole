# Push Instruction

- 只处理 `push` 阶段。
- 只读取当前目录下的 `INSTRUCTION.md`、`WORKFLOW.md`、`RULES.md`。
- 禁止默认读取 `scan/` 或 `collect/` 阶段文档，除非用户显式要求。
- 输入前提是 `registry.json` 和托管副本已存在。
