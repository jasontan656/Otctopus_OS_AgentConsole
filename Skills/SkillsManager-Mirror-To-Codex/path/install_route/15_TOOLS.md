---
doc_id: skillsmanager_mirror_to_codex.path.install_route.tools
doc_type: tools_doc
topic: Install route tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: After reading the route command surface, continue with execution order.
---

# Install 路由工具

## 可直接使用的命令
- 单技能 install 路由：
  - `python3 ./scripts/Cli_Toolbox.py --scope skill --skill-name <skill_name> --mode install`
- 自动路由到 install：
  - `python3 ./scripts/Cli_Toolbox.py --scope skill --skill-name <skill_name>`

## 工具约束
- 当前工具只给出下一步技能，不直接执行业务安装。
- `next_skills` 与 `next_steps` 应能帮助后续技能继续处理。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
