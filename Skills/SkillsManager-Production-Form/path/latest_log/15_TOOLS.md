---
doc_id: skillsmanager_production_form.path.latest_log.tools
doc_type: tools_doc
topic: Latest log tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: Continue with active log policy and seed snapshot.
---

# 最近迭代工具

## 可直接使用的命令
- 读取最近一条日志：
  - `python3 ./scripts/Cli_Toolbox.py latest-log --json`
- 读取多条日志：
  - `python3 ./scripts/Cli_Toolbox.py latest-log --json --entry-count <n>`
- 快捷阅读当前入口：
  - `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry latest_log --json`

## 下一跳列表
- [execution]：`20_EXECUTION.md`
