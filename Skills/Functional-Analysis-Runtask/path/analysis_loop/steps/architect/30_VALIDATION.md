---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.architect.validation
doc_type: action_validation_doc
topic: Architect validation
---

# architect 阶段校验

- `architect/assessment.yaml` 必须存在，并包含 `should_change`、`should_not_change` 与 `architecture_judgement`。
- `architect/001_architecture_assessment_report.md` 必须存在。
- 若阶段标记完成，`research` 不能仍是 `pending`。
