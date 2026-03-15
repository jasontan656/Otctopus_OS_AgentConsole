---
doc_id: skill_creation_template.path.maintenance.entry
doc_type: path_doc
topic: Maintenance entry for template registry only
anchors:
- target: ../00_SKILL_ENTRY.md
  relation: implements
  direction: upstream
  reason: The main skill entry routes readers here for maintenance.
- target: template_registry/00_TEMPLATE_REGISTRY.md
  relation: routes_to
  direction: downstream
  reason: Template maintenance is represented by the single registry file.
---

# Maintenance Entry

## 这个入口是干什么的
- 本入口只处理模板注册维护，不处理新模板创建。
- 本技能不再承载“如何维护文档结构规则”或“如何维护技能自身 workflow”的说明。
- 这些内容后续统一由 `SkillsManager-Doc-Structure` 承载。

## 下一跳列表
- [模板维护]：`template_registry/00_TEMPLATE_REGISTRY.md`
