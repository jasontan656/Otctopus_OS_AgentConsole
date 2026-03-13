---
doc_id: functional_humenworkzone_manager.runtime.temp_project_naming_rule
doc_type: topic_atom
topic: Naming rule for temporary projects
anchors:
- target: TEMPORARY_PROJECTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: Naming is a governed part of the temporary-project zone.
- target: ORGANIZE_TEMPORARY_PROJECT_FLOW.md
  relation: required_by
  direction: upstream
  reason: Intake needs a naming decision before relocation.
- target: TEMP_PROJECT_README_MAINTENANCE_FLOW.md
  relation: referenced_by
  direction: upstream
  reason: Inventory entries should align with this naming rule.
---

# Temporary Project Naming Rule

## 默认格式
- 新建临时项目目录时，优先使用：`<project-core>__temp-project/`。

## 命名解释
- `<project-core>` 使用英文短语概括项目主题或主要用途。
- 目标是让人一眼看出“这是什么临时项目”，并且后续便于清理。

## 保留原名规则
- 若项目当前已经有一个明确、可识别且用户长期这么叫它的目录名，首次迁入 `Temporary_Projects` 时允许保留原名。
- `Rise_Bawang_Temp` 这类已经带有明显临时语义的目录名，可直接保留。

## 禁止项
- 不要把完全模糊的目录名直接迁入集中区。
- 不要为了形式统一而把用户已经稳定使用的识别名硬改得更难认。
