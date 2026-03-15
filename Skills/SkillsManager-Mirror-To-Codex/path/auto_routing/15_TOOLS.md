---
doc_id: skillsmanager_mirror_to_codex.path.auto_routing.tools
doc_type: tools_doc
topic: Auto routing tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: After command shapes are clear, continue with execution order.
---

# 自动导航工具

## 可直接使用的命令
- 自动路由单技能：
  - `python3 ./scripts/Cli_Toolbox.py --scope skill --skill-name <skill_name>`
- 自动路由全量镜像：
  - `python3 ./scripts/Cli_Toolbox.py --scope all`
- 快捷阅读当前入口：
  - `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry auto_routing --json`

## 当前动作的工具约束
- `Cli_Toolbox.py` 是唯一受管本地工具入口。
- 工具输出保持 JSON；自动导航不另起独立合同源。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
