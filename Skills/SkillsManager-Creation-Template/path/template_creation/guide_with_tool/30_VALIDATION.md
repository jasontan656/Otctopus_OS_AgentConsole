---
doc_id: skill_creation_template.path.template_creation.guide_with_tool.validation
doc_type: topic_atom
topic: Validation for guide_with_tool template creation
---

# Guide With Tool Validation

## 当前动作如何校验
- 输出具备门面、`path/`、`agents/`、`scripts/`。
- 门面没有回填深规则正文。
- 默认主入口已经形成单线闭环；若存在新增入口，也没有在入口内部再次分叉。
- `scripts/` 内脚本存在，但命令说明没有逃离各入口自己的 `tools` 节点。
- 生成结果仍围绕目标 skill 的真实业务目标。
