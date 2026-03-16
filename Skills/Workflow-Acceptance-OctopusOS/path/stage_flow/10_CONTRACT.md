---
doc_id: workflow_acceptance_octopusos.path.stage_flow.contract
doc_type: topic_atom
topic: Acceptance stage contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 读完合同后看共享工具面。
---

# acceptance 阶段合同

## 当前动作要完成什么
- 把当前实现带到可交付判断所需的本地运行态。
- 收集真实 witness、matrix/report 与 closeout 证据。

## 当前动作必须满足什么
- 本地可控环境必须先完成 bring-up、health check 与至少一条模拟使用路径。
- 只有真实证据足够时才允许进入交付结论。
- `acceptance-lint` 与 `graph-postflight` 是固定收口动作。

## 下一跳列表
- [tools]：`15_TOOLS.md`
