---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.validation.validation
doc_type: action_validation_doc
topic: Validation validation
---

# validation 阶段校验

- 前置阶段状态必须与当前执行模式一致。
- 阶段沉淀文档与方案文档若已声明为写回目标，则路径必须存在。
- 若 `validation` 标记完成，不得残留“代码已改但无证据”“结论已写但无引用”“阶段虚假完成”等错误。
