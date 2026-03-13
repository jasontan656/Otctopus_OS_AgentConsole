---
doc_id: metadata.frontmatter_fields
doc_type: topic_atom
topic: Contract for frontmatter fields used by governed markdown docs
node_role: topic_atom
domain_type: metadata
anchors:
- target: 00_METADATA_INDEX.md
  relation: belongs_to
  direction: upstream
  reason: This contract is one branch under the metadata index.
- target: ../../assets/templates/ATOMIC_DOC_TEMPLATE.md
  relation: details
  direction: downstream
  reason: The atomic template shows how the frontmatter contract is instantiated in markdown form.
---

# Frontmatter Field Contract

## 必填字段
- `doc_id`
- `doc_type`
- `topic`
- `anchors`

## 可选字段
- `node_role`
- `domain_type`

## 使用规则
- `doc_type` 表达当前文档在当前 skill 中被消费的文档类型。
- `node_role` 可选，用来额外标记当前节点在 tree 中扮演的角色。
- `domain_type` 可选，用来补充该文档所属的领域语义。
