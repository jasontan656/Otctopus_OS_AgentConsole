---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.design.contract
doc_type: action_contract_doc
topic: Design contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 design 合同，再看工具。
---

# design 阶段合同

- 必须先消费 research 报告，再借助 `Functional-BrainStorm` 在 chat 呈现至少 3 种方案，不能跳过方案发散直接写单一结论。
- 用户未选型或未给出自定义方案前，不得把方案裁决伪装成已完成设计。
- 一旦用户做出选择，必须把“保留什么、推翻什么、升级什么”写成 `design/architecture_decisions.yaml`。
- 每个决策都必须引用旧资产或证据 id，不能只写主观偏好。
- 必须显式定义阶段门禁与目标形态，而不是把切换关系藏在叙述文字里。

## 下一跳列表
- [tools]：`15_TOOLS.md`
