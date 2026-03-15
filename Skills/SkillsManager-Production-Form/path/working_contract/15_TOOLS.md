---
doc_id: skillsmanager_production_form.path.working_contract.tools
doc_type: tools_doc
topic: Working contract tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: Continue with the full working state.
---

# 工作合同工具

## 可直接使用的命令
- 读取工作合同：
  - `python3 ./scripts/Cli_Toolbox.py working-contract --json`
- 快捷阅读当前入口：
  - `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry working_contract --json`

## 工具约束
- `working-contract` 返回的是当前工作合同 JSON 视图。
- CLI 不是额外真源，文档链与合同 payload 应保持一致。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
