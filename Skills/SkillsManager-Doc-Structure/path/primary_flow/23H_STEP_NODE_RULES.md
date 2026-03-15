---
doc_id: skillsmanager_doc_structure.path.primary_flow.step_node_rules
doc_type: topic_atom
topic: Step-node semantic rules in doc-structure governance
anchors:
- target: 23B_ENTRY_NODE_RULES.md
  relation: implements
  direction: upstream
  reason: Step-node review is a branch of entry-node review.
- target: 24_ANCHOR_LINT.md
  relation: routes_to
  direction: downstream
  reason: Anchor lint follows after step-node review.
---

# Step 节点规则

## 语义审查规则
- step entry 只把读者送到该 step 自己的局部闭环。
- 一个 step 内只承载这个 step 自己的规则，不跨写其他 step。
- step 层级内如果还需规则拆分，也必须继续物理下沉到本 step 内部。

## 不合格信号
- step entry 直接承担 step 全文。
- step 文档跨写兄弟 step 的规则。
- 用 step 文档重新集中整个 workflow 的总规则。

## 下一跳列表
- [anchor lint]：`24_ANCHOR_LINT.md`
