---
doc_id: functional_humenworkzone_manager.runtime.external_research_report_naming_rule
doc_type: topic_atom
topic: Naming rule for external research report folders and key files
anchors:
- target: EXTERNAL_RESEARCH_REPORTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: The zone policy delegates naming decisions here.
- target: ORGANIZE_EXTERNAL_RESEARCH_REPORTS_FLOW.md
  relation: referenced_by
  direction: upstream
  reason: Intake must use this naming rule before relocation.
- target: EXTERNAL_RESEARCH_REPORTS_README_MAINTENANCE_FLOW.md
  relation: referenced_by
  direction: upstream
  reason: Inventory entries depend on the governed names.
---

# External Research Report Naming Rule

## 目录命名目标
- 目录名必须优先表达“调研主题”，而不是原始导出名、下载名或泛化占位名。
- 当前统一格式固定为 `<topic>__external-research-pack`。

## 主报告文件命名
- 若目录内存在主 markdown、pdf、docx 或等价主报告文件，默认命名为 `<date>_<topic>__research-report.<ext>`。
- `date` 优先取报告内可识别日期；若缺失，再退回文件时间或迁移当日。

## 资料包文件命名
- 若目录内存在承载附件、视频、原始资料或整包导出的压缩文件，默认命名为 `<date>_<topic>__source-bundle.<ext>`。

## 命名判断原则
- `topic` 使用 2 到 6 个英文词的 kebab-case，重点表达对象与用途，例如 `hospital-ai-leadership`。
- 若原目录名已经清晰表达主题，也可吸收其核心词，但仍要改成统一格式。
- 不为了追求短而牺牲可识别性；用户应一眼能知道这是哪类调研。
