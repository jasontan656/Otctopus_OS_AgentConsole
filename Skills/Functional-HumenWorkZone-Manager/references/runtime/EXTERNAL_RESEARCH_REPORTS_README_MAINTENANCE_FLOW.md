---
doc_id: functional_humenworkzone_manager.runtime.external_research_reports_readme_maintenance_flow
doc_type: topic_atom
topic: Maintenance flow for the external research report inventory README
anchors:
- target: EXTERNAL_RESEARCH_REPORTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: The inventory README is a required asset of the external-research-report zone.
- target: ORGANIZE_EXTERNAL_RESEARCH_REPORTS_FLOW.md
  relation: triggered_by
  direction: upstream
  reason: Intake must lead to an inventory update.
- target: EXTERNAL_RESEARCH_REPORT_NAMING_RULE.md
  relation: references
  direction: downstream
  reason: Inventory entries should align with the governed naming rule.
---

# External Research Reports README Maintenance Flow

## 维护对象
- 维护文件固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/External_Research_Reports/README.md`。

## 每次更新至少同步这些字段
- 调研目录名
- 当前本地路径或受管目录名
- 主题或对象的一句话说明
- 指向主报告的本地链接
- 当前状态，例如：`active`、`paused`、`archive_candidate`

## 更新原则
- 说明文字保持简短，重点帮助用户快速回忆“这份调研主要在讲什么”。
- 目录名、主报告名或状态调整后，清单必须同 turn 更新。
- 若某份调研后续确认不再需要继续保留，应先把状态改成 `archive_candidate` 或直接移除，不要留下失真条目。
