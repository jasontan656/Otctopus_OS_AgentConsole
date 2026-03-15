---
doc_id: skillsmanager_mirror_to_codex.path.mirror_boundary.tools
doc_type: tools_doc
topic: Mirror boundary tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: Continue with how the boundary rules are applied at runtime.
---

# 镜像边界工具

## 可直接使用的命令
- 查看边界链路：
  - `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry mirror_boundary --json`
- 结合全量 push 验证边界：
  - `python3 ./scripts/Cli_Toolbox.py --scope all --mode push --dry-run`

## 工具约束
- `Cli_Toolbox.py` 负责根路径解析与同步根发现。
- 运行时 helper 负责链路编译，不重写同步语义。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
