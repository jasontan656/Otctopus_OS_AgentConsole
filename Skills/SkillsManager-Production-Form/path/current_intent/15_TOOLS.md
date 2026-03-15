---
doc_id: skillsmanager_production_form.path.current_intent.tools
doc_type: tools_doc
topic: Current intent tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: Continue with the full current intent snapshot.
---

# 产品意图工具

## 可直接使用的命令
- 读取产品意图：
  - `python3 ./scripts/Cli_Toolbox.py intent-snapshot --json`
- 快捷阅读当前入口：
  - `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry current_intent --json`

## 下一跳列表
- [execution]：`20_EXECUTION.md`
