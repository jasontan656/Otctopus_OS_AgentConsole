---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.growth_architecture.horizontal_branch_family_registry
doc_type: topic_atom
topic: Mother doc horizontal branch family registry
reading_chain:
- key: doc_kind_registry
  target: 13_DOC_KIND_REGISTRY.md
  hop: next
  reason: 再确认分支文档的语义类型注册表。
---

# 横向分支家族注册表

当前允许的横向分支家族：
- `framework_branch`
- `domain_branch`
- `contract_branch`
- `scene_branch`
- `interaction_branch`
- `decision_branch`
- `execution_binding_branch`

使用规则：
- 横向分支家族不是“这个节点喜欢怎么长就怎么长”，而是当前节点长出的一棵可复用语义树。
- 同一个家族应能被别的同类节点复用。
- 若未来要新增新的横向分支家族，必须先更新本注册表，再落到真实 mother_doc。

## 下一跳列表
- [doc_kind_registry]：`13_DOC_KIND_REGISTRY.md`
