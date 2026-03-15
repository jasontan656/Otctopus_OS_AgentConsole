---
doc_id: skill_creation_template.path.template_creation.executable.entry
doc_type: path_doc
topic: Action-loop entry for executable_workflow_skill template creation
anchors:
- target: ../00_TEMPLATE_CREATION_ENTRY.md
  relation: implements
  direction: upstream
  reason: Template creation entry routes executable_workflow_skill here.
- target: 10_CONTRACT.md
  relation: routes_to
  direction: downstream
  reason: executable workflow creation starts from the contract doc.
---

# Executable Workflow Entry

## 这个入口是干什么的
- 本入口只服务 `[executable_workflow_skill]` 模板创建。
- 当前线路采用动作闭环：合同 -> 模板 -> 工具 -> 实施 -> 校验。

## 下一跳列表
- [contract]：`10_CONTRACT.md`
