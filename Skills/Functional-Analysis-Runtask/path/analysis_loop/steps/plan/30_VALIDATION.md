---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.plan.validation
doc_type: action_validation_doc
topic: Plan validation
---

# plan 阶段校验

- `planning_basis` 必须存在，并写明 consumed stage reports、问题框架与 package derivation chain。
- 每个 milestone package 必须包含 `package_id`、前置输入、交付目标、验证方法、`derives_from_stage_reports`、`stage_gates`、`evidence_expectations`、`writeback_targets`、`exit_signals` 与 `blocked_by`。
- package 拆分必须能回指 research、architect、preview、design、impact 的正式产物，不能是脱离前序结论的空壳 TODO。
- `active` package 不得多于 1 个。
- 若 `plan` 标记完成，必须至少存在 1 个可施工 milestone package。
