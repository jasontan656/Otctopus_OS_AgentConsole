---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.architect.validation
doc_type: action_validation_doc
topic: Architect validation
---

# architect 阶段校验

- `architect/assessment.yaml` 必须存在，并包含 consumed stage reports、问题框架、判断链、`should_change`、`should_not_change`、`open_questions`、`architecture_judgement` 与 `evidence_refs`。
- `architect/assessment.yaml` 必须显式引用 `research/001_research_report.md`。
- `architect/001_architecture_assessment_report.md` 必须存在，且不得残留占位文本，并必须具备阶段目标、消费的前序产物、关键架构问题框架、`should change`、`should not change`、架构判断推导链、阶段结论与进入 preview 的门禁。
- 若阶段标记完成，`research` 不能仍是 `pending`。
