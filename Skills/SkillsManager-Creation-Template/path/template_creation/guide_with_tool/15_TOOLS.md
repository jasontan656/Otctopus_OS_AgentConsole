---
doc_id: skill_creation_template.path.template_creation.guide_with_tool.tools
doc_type: topic_atom
topic: Tool or lint surface for guide_with_tool template creation
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: Execution follows the tool context.
---

# Guide With Tool/Lint Surface

## 当前动作使用什么
- 生成入口：`scripts/create_skill_from_template.py`
- 模式参数：`--skill-mode guide_with_tool`
- 当前动作要生成的脚本：
  - `scripts/Cli_Toolbox.py`
  - `scripts/test_skill_layout.py`
- 当前节点承载该入口自己的 tool/lint 说明；若目标技能只有 lint，也直接在这里声明。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
