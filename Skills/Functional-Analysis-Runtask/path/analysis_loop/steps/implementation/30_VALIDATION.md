---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.implementation.validation
doc_type: action_validation_doc
topic: Implementation validation
---

# implementation 阶段校验

- ledger 条目必须引用有效 `package_id`。
- 发生真实实现或验证时，`evidence_refs` 不得为空。
- 每条 ledger entry 都必须写透 consumed stage reports、preflight checks、derivation notes 与 writeback targets。
- 每条 ledger entry 都必须显式承接 research、architect、preview、design、impact、plan 的正式产物，而不是只记修改结果。
- package 若标记完成，必须能在 ledger 中找到对应验证记录与状态更新。
