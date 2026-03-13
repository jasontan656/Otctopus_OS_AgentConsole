---
doc_id: skill_creation_template.asset.task_routing_template
doc_type: template_doc
topic: Template for the first routing doc in a generated skill
anchors:
- target: ../../SKILL_TEMPLATE.md
  relation: implements
  direction: upstream
  reason: The basic facade template routes into this task routing template.
- target: ../governance/SKILL_DOCSTRUCTURE_POLICY_TEMPLATE.md
  relation: routes_to
  direction: downstream
  reason: Generated skills must route into the doc-structure policy.
---

# Task Routing Template

## 当前分叉轴线
- [本文件只按一个语义轴线分流，例如任务意图、读写路径、角色或阶段入口。]

## 分支一
- [当前分支该读哪些下沉文档]

## 分支二
- [当前分支该读哪些下沉文档]

## 分支三（可选）
- [仅在确有第三个稳定分支时保留]
