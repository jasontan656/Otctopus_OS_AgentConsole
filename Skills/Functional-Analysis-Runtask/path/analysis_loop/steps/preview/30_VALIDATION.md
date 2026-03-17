---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.preview.validation
doc_type: action_validation_doc
topic: Preview validation
---

# preview 阶段校验

- `preview/projection.yaml` 必须存在，并包含 consumed stage reports、问题框架、推演链、`future_shape`、`behavior_delta`、`failure_modes`、`rollback_triggers` 与 `evidence_refs`。
- `preview/projection.yaml` 必须显式引用 `research/001_research_report.md` 与 `architect/001_architecture_assessment_report.md`。
- `preview/001_future_shape_preview.md` 必须存在，且不得残留占位文本，并必须具备阶段目标、消费的前序产物、关键预演问题框架、`future shape`、`behavior delta`、`failure modes`、`rollback triggers`、预演推导链与进入 design 的门禁。
- 若阶段标记完成，`architect` 不能仍是 `pending`。
