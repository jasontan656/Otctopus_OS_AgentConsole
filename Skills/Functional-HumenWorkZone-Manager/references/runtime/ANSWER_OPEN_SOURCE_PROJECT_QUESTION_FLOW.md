---
doc_id: functional_humenworkzone_manager.runtime.answer_open_source_project_question_flow
doc_type: topic_atom
topic: Flow for answering a question about an open-source project and writing a report
anchors:
- target: OPEN_SOURCE_PROJECT_ANALYSIS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: Project-question analysis is one operational branch of the managed zone.
- target: PROJECT_ANALYSIS_REPORT_STRUCTURE.md
  relation: requires
  direction: downstream
  reason: Each analysis report must use the governed report structure.
- target: PROJECT_ANALYSIS_INDEX_MAINTENANCE_FLOW.md
  relation: triggers
  direction: downstream
  reason: Writing a report must be followed by index maintenance.
---

# Answer Open Source Project Question Flow

## 触发条件
- 当用户针对某个开源项目提问，并希望到项目中找答案时，使用本流程。

## 固定步骤
1. 先明确目标项目与问题本身，不要把多个项目混成一份报告。
2. 在项目源码、README、文档或本地证据中找答案。
3. 把结果写成项目内一份独立报告，而不是只在对话里给结论。
4. 报告必须套用 `PROJECT_ANALYSIS_REPORT_STRUCTURE.md`。
5. 写完报告后，同步更新项目级 `README.md` 与分析区总 `README.md`。

## 最小落地要求
- 不能只有结论没有问题背景。
- 不能只有答案没有证据来源。
- 不能把不同项目的问题写进同一个项目目录。
