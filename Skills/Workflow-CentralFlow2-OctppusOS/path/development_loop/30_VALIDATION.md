---
doc_id: workflow_centralflow2_octppusos.path.development_loop.validation
doc_type: action_validation_doc
topic: Development loop validation
---

# 开发闭环校验

- 阶段顺序固定为 `mother_doc -> construction_plan -> implementation -> acceptance`。
- `mother_doc` 与 `construction_plan` 都必须完成各自 lint，才能进入下一阶段。
- `acceptance` 只在真实证据与 graph postflight 收口后结束闭环。
