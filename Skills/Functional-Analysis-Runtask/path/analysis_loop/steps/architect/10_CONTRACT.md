---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.architect.contract
doc_type: action_contract_doc
topic: Architect contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 architect 合同，再看工具。
---

# architect 阶段合同

- architect 必须强制使用 `Meta-Architect-MindModel`。
- architect 只消费 research 阶段已落盘的调研报告与 evidence registry，并且必须在对象层和报告层显式引用 `research/001_research_report.md`。
- architect 必须先回答本阶段专属问题：哪些结构必须改、哪些不能改、哪些仍未被 research 充分覆盖、哪些误判会污染后续 preview/design/impact。
- `architect/assessment.yaml` 必须写透：consumed stage reports、问题框架、判断链、should change、should not change、未收口问题、architecture judgement 与 evidence refs。
- `architect/001_architecture_assessment_report.md` 必须至少写透：阶段目标、消费的前序产物、关键架构问题框架、should change、should not change、架构判断推导链、阶段结论与进入 preview 的门禁。
- architect 只允许给结构性裁决，不得提前展开代码级实现步骤、计划切片或验收结论。
- architect 若仍有关键未收口问题，必须显式写出并阻止 preview 伪装成可继续推进。

## 下一跳列表
- [tools]：`15_TOOLS.md`
