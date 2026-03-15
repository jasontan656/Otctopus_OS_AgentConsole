---
doc_id: skill_creation_template.path.maintenance.template_registry
doc_type: index_doc
topic: Single template registry for creation template maintenance
anchors:
- target: ../00_MAINTENANCE_ENTRY.md
  relation: implements
  direction: upstream
  reason: Maintenance entry routes template maintenance directly to this registry file.
- target: ../../template_creation/guide_only/12_TEMPLATE.md
  relation: routes_to
  direction: downstream
  reason: Registry exposes the guide_only template location.
- target: ../../template_creation/guide_with_tool/12_TEMPLATE.md
  relation: routes_to
  direction: downstream
  reason: Registry exposes the guide_with_tool template location.
- target: ../../template_creation/executable_workflow_skill/12_TEMPLATE.md
  relation: routes_to
  direction: downstream
  reason: Registry exposes the executable workflow template location.
---

# Template Registry

## 这个文件是干什么的
- `[模板维护]` 分支只保留这一个注册文件。
- 它不承载模板本体，只登记三条创建链路里实际模板文件的位置。

## 已注册模板位置
1. [guide_only]：`../../template_creation/guide_only/12_TEMPLATE.md`
2. [guide_with_tool]：`../../template_creation/guide_with_tool/12_TEMPLATE.md`
3. [executable_workflow_skill]：`../../template_creation/executable_workflow_skill/12_TEMPLATE.md`

## 维护要求
- 若任一创建链路的模板文件位置发生变化，必须先更新这里。
- 模板本体始终留在各自创建链路中；这里不复制模板内容。
- 生成器、CLI 与回归断言必须与这里的注册位置保持同步。
- 技能创建完成后的文档结构、锚点与门面规则，不在本技能维护范围内。
