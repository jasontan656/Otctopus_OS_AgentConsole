---
doc_id: workflow_implementation_octopusos.path.stage_flow.validation
doc_type: topic_atom
topic: Implementation stage validation
---

# implementation 阶段校验

- 当前阶段只消费 active pack，没有偷带 construction_plan 的拆包焦点。
- 代码、测试和 pack 证据已经一起落盘。
- 只有在本地验证完成后，才推动相关 state sync。
