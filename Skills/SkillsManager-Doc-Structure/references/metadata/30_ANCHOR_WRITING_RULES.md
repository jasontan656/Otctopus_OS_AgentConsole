---
doc_id: metadata.anchor_writing
doc_type: topic_atom
topic: Contract for writing anchors that preserve tree-first readability
node_role: topic_atom
domain_type: metadata
anchors:
- target: 00_METADATA_INDEX.md
  relation: belongs_to
  direction: upstream
  reason: This contract is one branch under the metadata index.
- target: ../rules/30_TREE_GRAPH_BINDING_RULES.md
  relation: implements
  direction: upstream
  reason: Anchor-writing is the concrete layer of the tree-graph binding rule.
---

# Anchor Writing Contract

## 规则
- 每个 markdown 文档至少一个 anchor。
- 主路径优先使用 `upstream` 与 `downstream`。
- 横向补充或跨层复用再使用 `cross` 或 `lateral`。
- anchor 的 `reason` 应解释“为什么需要这条关系”，而不是重复 relation 名称。
