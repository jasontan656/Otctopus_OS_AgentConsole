---
doc_id: functional_analysis_runtask.path.analysis_loop.validation
doc_type: action_validation_doc
topic: Analysis loop validation
---

# analysis_loop 全局校验

- 阶段顺序固定为 `research -> design -> plan -> implementation -> validation`。
- `single_stage` 允许直接进入任一阶段，但仍必须满足该阶段 checklist 指定的最小输入对象。
- `plan` 必须存在可施工切片后，才允许进入 `implementation`。
- `implementation` 只消费 active slice，且每回合必须回写 ledger。
- 新任务只有在 `task_runtime.yaml` 显示上一任务全部阶段已完成且 `task_status=closed` 时才允许启动。
- `validation` 只在对象层、阶段沉淀文档层与写回状态一致后结束闭环。
