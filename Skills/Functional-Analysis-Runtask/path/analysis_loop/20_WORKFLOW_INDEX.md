---
doc_id: functional_analysis_runtask.path.analysis_loop.workflow_index
doc_type: workflow_index_doc
topic: Analysis loop workflow index
reading_chain:
- key: research
  target: steps/research/00_RESEARCH_ENTRY.md
  hop: branch
  reason: research 负责锁定目标意图或目标项目、问题链、证据入口与未收口问题。
- key: architect
  target: steps/architect/00_ARCHITECT_ENTRY.md
  hop: branch
  reason: architect 负责承接 research 报告，对当前结构与目标结构做 should/should_not 架构裁决。
- key: preview
  target: steps/preview/00_PREVIEW_ENTRY.md
  hop: branch
  reason: preview 负责承接 research+architect，推演未来形态、行为变化、失败模式与回滚阈值。
- key: design
  target: steps/design/00_DESIGN_ENTRY.md
  hop: branch
  reason: design 负责承接前三阶段，比较候选路径并裁决 selected strategy。
- key: impact
  target: steps/impact/00_IMPACT_ENTRY.md
  hop: branch
  reason: impact 负责承接前四阶段，补齐 direct/indirect/latent/regression 影响面与验证面。
- key: plan
  target: steps/plan/00_PLAN_ENTRY.md
  hop: branch
  reason: plan 负责承接前五阶段，把结论拆成可逐步实现、逐步验证、逐步写回的 milestone package。
- key: implementation
  target: steps/implementation/00_IMPLEMENTATION_ENTRY.md
  hop: branch
  reason: implementation 只消费 active milestone package 与前序正式产物，并逐回合写回事实证据。
- key: validation
  target: steps/validation/00_VALIDATION_ENTRY.md
  hop: branch
  reason: validation 负责承接所有前序产物做 backend terminal 验收、成功反馈判定与副作用观测。
- key: final_delivery
  target: steps/final_delivery/00_FINAL_DELIVERY_ENTRY.md
  hop: branch
  reason: final_delivery 负责承接 validation 与全链路正式产物，对人类输出可追溯的最终摘要。
---

# analysis_loop 阶段索引

## 当前入口的复合阶段
1. [research]：`steps/research/00_RESEARCH_ENTRY.md`
2. [architect]：`steps/architect/00_ARCHITECT_ENTRY.md`
3. [preview]：`steps/preview/00_PREVIEW_ENTRY.md`
4. [design]：`steps/design/00_DESIGN_ENTRY.md`
5. [impact]：`steps/impact/00_IMPACT_ENTRY.md`
6. [plan]：`steps/plan/00_PLAN_ENTRY.md`
7. [implementation]：`steps/implementation/00_IMPLEMENTATION_ENTRY.md`
8. [validation]：`steps/validation/00_VALIDATION_ENTRY.md`
9. [final_delivery]：`steps/final_delivery/00_FINAL_DELIVERY_ENTRY.md`

## 常驻约束
- 每个阶段都必须先消费前序正式产物，再写本阶段问题框架、显式推导链与正式结论。
- 任一阶段未完成前，后阶段不得预写、不得偷跑、不得在聊天里先行裁决。

## 下一跳列表
- [research]：`steps/research/00_RESEARCH_ENTRY.md`
- [architect]：`steps/architect/00_ARCHITECT_ENTRY.md`
- [preview]：`steps/preview/00_PREVIEW_ENTRY.md`
- [design]：`steps/design/00_DESIGN_ENTRY.md`
- [impact]：`steps/impact/00_IMPACT_ENTRY.md`
- [plan]：`steps/plan/00_PLAN_ENTRY.md`
- [implementation]：`steps/implementation/00_IMPLEMENTATION_ENTRY.md`
- [validation]：`steps/validation/00_VALIDATION_ENTRY.md`
- [final_delivery]：`steps/final_delivery/00_FINAL_DELIVERY_ENTRY.md`
