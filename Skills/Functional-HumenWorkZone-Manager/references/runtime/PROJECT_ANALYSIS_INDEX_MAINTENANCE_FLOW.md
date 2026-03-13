---
doc_id: functional_humenworkzone_manager.runtime.project_analysis_index_maintenance_flow
doc_type: topic_atom
topic: Maintenance flow for project analysis indexes
anchors:
- target: OPEN_SOURCE_PROJECT_ANALYSIS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: The analysis indexes are required assets of the managed zone.
- target: ANSWER_OPEN_SOURCE_PROJECT_QUESTION_FLOW.md
  relation: triggered_by
  direction: upstream
  reason: New project reports must lead to index updates.
- target: PROJECT_ANALYSIS_REPORT_STRUCTURE.md
  relation: references
  direction: downstream
  reason: Index entries should point to reports built with the governed structure.
---

# Project Analysis Index Maintenance Flow

## 维护对象
- 总索引固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Open_Source_Project_Analysis/README.md`。
- 每个项目目录也应维护本项目自己的 `README.md`。

## 每次更新至少同步这些字段
- 项目名
- 最近分析主题或最新报告
- 报告路径
- 当前状态，例如：`active`、`archived`

## 更新原则
- 总索引负责让人快速知道“哪些项目已经做过分析”。
- 项目级 README 负责让人快速知道“这个项目问过哪些问题、最新报告在哪里”。
- 若报告新增、改名或归档，两个索引应同 turn 更新。
