---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.plan.validation
doc_type: action_validation_doc
topic: Plan validation
---

# plan 阶段校验

- 每个 slice 必须包含 `slice_id`、借鉴来源、基线差异、验证方法、证据要求、写回目标与退出信号。
- `active` slice 不得多于 1 个。
- 若 `plan` 标记完成，必须至少存在 1 个可施工切片。
