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

- plan 必须从已收敛的 design decisions 正式生成。
- 每个 slice 都要声明借鉴来源、当前基线差异、验证方法、证据要求、写回目标与退出信号。
- `active` slice 在任一时刻只能有 1 个。

## 下一跳列表
- [tools]：`15_TOOLS.md`
