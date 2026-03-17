---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.impact.contract
doc_type: action_contract_doc
topic: Impact contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 impact 合同，再看工具。
---

# impact 阶段合同

- impact 必须强制使用 `Meta-Impact-Investigation`。
- impact 只消费 research、architect、preview 与 design 已落盘产物，并且必须在对象层和报告层显式引用这些正式报告。
- impact 必须先问透本阶段专属问题：这次设计会直接影响什么、间接拖动什么、潜在无锚点关联在哪里、回归面与证据面如何约束后续 plan/implementation。
- `impact/impact_map.yaml` 必须写透：consumed stage reports、问题框架、判断链、direct_scope、indirect_scope、latent_related、validation_or_evidence、must_update、must_check_before_edit、regression_surface、confidence、evidence_gaps 与 evidence refs。
- `impact/001_impact_investigation.md` 必须至少写透：阶段目标、消费的前序产物、关键影响面问题框架、direct scope、indirect scope、latent related、regression surface、影响面推导链与进入 plan 的门禁。
- impact 不得偷渡 implementation 结果、validation 结论或 final delivery 摘要。
- latent_related、regression_surface、must_check_before_edit 任一没写透时，impact 不得标记完成。

## 下一跳列表
- [tools]：`15_TOOLS.md`
