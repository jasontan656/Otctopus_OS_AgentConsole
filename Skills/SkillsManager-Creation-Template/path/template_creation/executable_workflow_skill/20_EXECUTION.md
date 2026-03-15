---
doc_id: skill_creation_template.path.template_creation.executable.execution
doc_type: topic_atom
topic: Execution for executable_workflow_skill template creation
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validation closes the action loop.
---

# Executable Workflow Execution

## 当前动作怎么做
1. 明确目标 skill 是否真的需要入口内复合 workflow 形态。
2. 先对照 `12_TEMPLATE.md` 确认目标技能模板结构。
3. 渲染门面、`path/primary_flow/`、`20_WORKFLOW_INDEX.md` 与 `steps/` 子路径。
4. 让主入口先进入 workflow index，再进入各个复合步骤。
5. 把 CLI 脚本留在 `scripts/`，把命令说明写在主入口或步骤自己的 `tools` 节点。
6. 让步骤正文留在各自步骤路径，而不是回填门面。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
