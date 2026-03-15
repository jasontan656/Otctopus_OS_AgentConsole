---
doc_id: skill_creation_template.path.template_creation.executable.validation
doc_type: topic_atom
topic: Validation for executable_workflow_skill template creation
---

# Executable Workflow Validation

## 当前动作如何校验
- 输出存在 workflow index、步骤子闭环、`agents/` 与 `scripts/`。
- 门面不承载复合步骤正文。
- 不存在 `references/`、`assets/`、`tests/`。
- 目标 skill 的真实业务目标没有被“模板创建流程”污染。
