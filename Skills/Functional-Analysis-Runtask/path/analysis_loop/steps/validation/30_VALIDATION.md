---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.validation.validation
doc_type: action_validation_doc
topic: Validation validation
---

# validation 阶段校验

- 前置阶段状态必须与当前执行模式一致。
- 阶段沉淀文档与方案文档若已声明为写回目标，则路径必须存在。
- `task_runtime.yaml` 必须满足：五阶段齐备、当前推进位置可追踪、结束位置已记录，且仅在全部阶段完成后才允许 `task_status=closed`。
- 若 `validation` 标记完成，不得残留“代码已改但无证据”“结论已写但无引用”“阶段虚假完成”等错误。
