---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.preview.validation
doc_type: action_validation_doc
topic: Preview validation
---

# preview 阶段校验

- `preview/projection.yaml` 必须存在，并包含 `future_shape`、`behavior_delta`、`failure_modes` 与 `rollback_triggers`。
- `preview/001_future_shape_preview.md` 必须存在。
- 若阶段标记完成，`architect` 不能仍是 `pending`。
