---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.growth_architecture.doc_kind_registry
doc_type: topic_atom
topic: Mother doc doc kind registry
reading_chain:
- key: content_structure_family_registry
  target: 14_CONTENT_STRUCTURE_FAMILY_REGISTRY.md
  hop: next
  reason: 注册完语义类型后，再确认内容结构家族。
---

# 文档语义类型注册表

当前允许的 `doc_kind`：
- `trunk_node`
- `branch_root`
- `taxonomy_doc`
- `contract_doc`
- `scene_spec`
- `interaction_spec`
- `decision_doc`
- `execution_binding_doc`

使用规则：
- `display_layer` 负责显示层级；`doc_kind` 负责语义角色。
- 同一文档若同时承担多个 `doc_kind`，通常意味着它应继续拆分。
- `branch_root` 若出现，应同时声明自己属于哪个 `branch_family`。
- overview 节点、主链节点和 layer 节点都可以是 `branch_root`；只要它开始承担一个完整可复用的细分语义树，就应该显式升格为分支根。

## 下一跳列表
- [content_structure_family_registry]：`14_CONTENT_STRUCTURE_FAMILY_REGISTRY.md`
