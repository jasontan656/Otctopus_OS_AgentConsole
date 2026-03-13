---
doc_id: functional_humenworkzone_manager.runtime.project_analysis_report_structure
doc_type: topic_atom
topic: Structure rule for open-source project analysis reports
anchors:
- target: OPEN_SOURCE_PROJECT_ANALYSIS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: Report structure is a governed part of the analysis zone.
- target: ANSWER_OPEN_SOURCE_PROJECT_QUESTION_FLOW.md
  relation: required_by
  direction: upstream
  reason: Question analysis needs a report structure before writeback.
- target: PROJECT_ANALYSIS_INDEX_MAINTENANCE_FLOW.md
  relation: referenced_by
  direction: upstream
  reason: Index entries should point to reports built with this structure.
---

# Project Analysis Report Structure

## 报告必备段落
- 问题背景：说明用户当时问了什么。
- 分析时间：说明本次分析沉淀发生在什么日期。
- 目标项目：说明针对哪个项目，以及必要时的本地路径。
- 结论：先给最核心答案。
- 证据：列出本次回答依赖的 README、源码、配置或其他本地文件。
- 详细分析：展开推理与判断过程。

## 目标形态
- 报告应做到“离开当时对话也能看懂”。
- 报告应做到“知道这个结论是怎么来的”。
- 报告可长，但不能没有上下文和证据。
