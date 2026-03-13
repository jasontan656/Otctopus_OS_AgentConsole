---
doc_id: functional_humenworkzone_manager.runtime.open_source_project_analysis_zone_policy
doc_type: topic_atom
topic: Dedicated open-source project analysis zone inside Human_Work_Zone
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends project analysis tasks here.
- target: ../governance/SKILL_EXECUTION_RULES.md
  relation: governed_by
  direction: upstream
  reason: The analysis zone must obey the skill execution boundary.
- target: ANSWER_OPEN_SOURCE_PROJECT_QUESTION_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Answering a project question is a separate operational flow.
- target: PROJECT_ANALYSIS_INDEX_MAINTENANCE_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Analysis index upkeep is split into its own maintenance flow.
- target: PROJECT_ANALYSIS_REPORT_STRUCTURE.md
  relation: routes_to
  direction: downstream
  reason: Report structure is a distinct rule set.
---

# Open Source Project Analysis Zone Policy

## 目标目录
- 开源项目分析集中区固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Open_Source_Project_Analysis`。
- 历史上的 `Extraction` 目录已被该目录接管，不再继续沿用旧命名。

## 目录职责
- 本目录负责承载针对开源项目问题的分析报告、项目级索引与证据目录。
- 分析产物必须先按项目归类，再按报告落地，避免不同项目的结论混写在一起。

## 目录形态
- 根层维护总 `README.md`，记录当前有哪些项目已经做过分析。
- 每个项目至少有一个项目级 `README.md`，用于登记该项目已有报告与当前状态。
- 报告建议落在 `<project>/reports/` 下，证据建议落在 `<project>/evidence/` 下。

## 本区原则
- 分析不只是写答案，还必须写清问题上下文、分析时间、项目对象与证据入口。
- 若同一项目被多次提问，应继续沉淀为多份报告，而不是覆盖旧结论。
