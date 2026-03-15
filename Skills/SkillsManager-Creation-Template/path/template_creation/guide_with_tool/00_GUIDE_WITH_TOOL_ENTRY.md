---
doc_id: skill_creation_template.path.template_creation.guide_with_tool.entry
doc_type: path_doc
topic: Action-loop entry for guide_with_tool template creation
anchors:
- target: ../00_TEMPLATE_CREATION_ENTRY.md
  relation: implements
  direction: upstream
  reason: Template creation entry routes guide_with_tool here.
- target: 10_CONTRACT.md
  relation: routes_to
  direction: downstream
  reason: guide_with_tool creation starts from the contract doc.
---

# Guide With Tool Entry

## 这个入口是干什么的
- 本入口只服务 `[guide_with_tool]` 模板创建。
- 当前线路采用动作闭环：合同 -> 模板 -> 工具 -> 实施 -> 校验。

## 下一跳列表
- [contract]：`10_CONTRACT.md`
