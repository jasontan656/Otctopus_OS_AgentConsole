---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.validation.validation
doc_type: action_validation_doc
topic: Validation validation
---

# validation 阶段校验

- 前置阶段状态必须与当前执行模式一致。
- 阶段沉淀文档与方案文档若已声明为写回目标，则路径必须存在。
- `task_runtime.yaml` 必须满足：九阶段齐备、当前推进位置可追踪、结束位置已记录，且仅在全部阶段完成后才允许 `task_status=closed`。
- `validation/001_acceptance_report.md` 必须说明如何验收、消费了哪些前序正式产物、观测到哪些成功反馈、哪些副作用可接受、为什么足以证明验收通过。
- validation report 不得残留占位文本，且必须具备阶段目标、消费的前序产物、验收问题框架、验收执行与成功反馈、残余风险与可接受副作用、验收推导链、阶段结论与进入 final_delivery 的门禁。
- 若 `validation` 标记完成，不得残留“代码已改但无证据”“结论已写但无引用”“阶段虚假完成”等错误。
