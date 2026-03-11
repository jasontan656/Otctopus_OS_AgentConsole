---
doc_id: "metadata.doc_header"
doc_type: "topic_atom"
topic: "Contract for document headers, titles, and topic statements in governed docs"
node_role: "topic_atom"
domain_type: "metadata"
anchors:
  - target: "00_METADATA_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This contract is one branch under the metadata index."
  - target: "20_FRONTMATTER_FIELD_CONTRACT.md"
    relation: "feeds"
    direction: "downstream"
    reason: "Header and topic choices should align with frontmatter fields."
---

# Doc Header Contract

## 规则
- 标题应表达当前文档的稳定主题，不应混入多个平级轴线。
- `topic` 应与标题同向，但更偏 machine-readable 的稳定主题句。
- 若标题和 `topic` 都无法保持单一主题，应先回到 tree 重新拆分。
