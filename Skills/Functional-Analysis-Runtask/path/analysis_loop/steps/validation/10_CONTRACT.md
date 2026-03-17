---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.validation.contract
doc_type: action_contract_doc
topic: Validation contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 validation 合同，再看工具。
---

# validation 阶段合同

- validation 负责检查对象完整性、引用有效性、阶段状态一致性、Human_Work_Zone 写回状态与九阶段显式承接链是否真实闭合。
- validation 只消费前序阶段已落盘产物，不得代替 research/architect/preview/design/impact/plan/implementation 补内容。
- validation 必须先问透本阶段专属问题：到底验证了什么、没验证什么、哪些成功反馈足以支持通过、哪些副作用可接受、哪些残余风险仍需保留。
- validation 同时负责检查 `task_runtime.yaml` 是否已完整闭环，且不会错误阻塞下一任务。
- `validation/001_acceptance_report.md` 必须至少写透：阶段目标、消费的前序产物、验收问题框架、验收执行与成功反馈、残余风险与可接受副作用、验收推导链、阶段结论与进入 final_delivery 的门禁。
- validation 报告必须显式引用 research 到 implementation 的正式产物，不能只写一份孤立 pass/fail 结论。
- 不得把“暂时没写回”“代码已改但无证据”“结论已写但无引用”伪装成阶段完成。

## 下一跳列表
- [tools]：`15_TOOLS.md`
