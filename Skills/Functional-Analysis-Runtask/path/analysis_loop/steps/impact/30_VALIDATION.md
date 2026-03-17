---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.impact.validation
doc_type: action_validation_doc
topic: Impact validation
---

# impact 阶段校验

- `impact/impact_map.yaml` 必须存在，并包含 consumed stage reports、问题框架、判断链、`direct_scope`、`indirect_scope`、`latent_related`、`validation_or_evidence`、`must_update`、`must_check_before_edit`、`regression_surface`、`confidence`、`evidence_gaps` 与 `evidence_refs`。
- `impact/impact_map.yaml` 必须显式引用 research、architect、preview、design 四份正式产物。
- `impact/001_impact_investigation.md` 必须存在，且不得残留占位文本，并必须具备阶段目标、消费的前序产物、关键影响面问题框架、`direct scope`、`indirect scope`、`latent related`、`regression surface`、影响面推导链与进入 plan 的门禁。
- 若阶段标记完成，`design` 不能仍是 `pending`。
