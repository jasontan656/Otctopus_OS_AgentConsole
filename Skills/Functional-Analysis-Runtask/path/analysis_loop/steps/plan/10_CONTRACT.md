---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.plan.contract
doc_type: action_contract_doc
topic: Plan contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 plan 合同，再看工具。
---

# plan 阶段合同

- plan 必须从 research、architect、preview、design、impact 的正式产物生成，不得补写或重裁决前序阶段结论。
- plan 必须先写 `planning_basis`，把 consumed stage reports、问题框架和 package derivation chain 固定下来，再生成 package。
- plan 必须先问透本阶段专属问题：为什么这样拆 package、每个 package 消费什么、交付什么、验证什么、写回什么、遇到什么条件必须停住。
- 每个 milestone package 都要声明前置输入、交付目标、验证方法、阶段边界、stage gates、evidence expectations、writeback targets、exit signals 与 blocked_by。
- package 的拆分理由必须能回指 design/impact 正式结论；不能退化成泛泛 TODO 列表。
- `active` milestone package 在任一时刻只能有 1 个。
- 未形成至少 1 个可施工 package，或 package derivation chain 仍不清楚时，plan 不得标记完成。

## 下一跳列表
- [tools]：`15_TOOLS.md`
