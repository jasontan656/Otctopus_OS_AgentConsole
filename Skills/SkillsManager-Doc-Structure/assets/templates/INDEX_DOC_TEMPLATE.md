---
doc_id: templates.index_doc
doc_type: template_doc
topic: Template for a pure index doc inside a governed skill folder
anchors:
- target: ../../references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_OVERVIEW.md
  relation: conforms_to
  direction: upstream
  reason: This index template is defined by the runtime contract.
- target: ATOMIC_DOC_TEMPLATE.md
  relation: pairs_with
  direction: cross
  reason: Indexes often route toward downstream atomic docs.
---

# Index Doc Template

```yaml
doc_id: "<skill.index.topic>"
doc_type: "index_doc"
topic: "<one index scope statement>"
node_role: "index_doc"
domain_type: "<optional domain marker>"
anchors:
  - target: "<relative/path/to/upstream/doc.md>"
    relation: "belongs_to"
    direction: "upstream"
    reason: "<why this index belongs there>"
  - target: "<relative/path/to/first/listed/doc.md>"
    relation: "indexes"
    direction: "downstream"
    reason: "<why this listed doc is part of the index>"
```

## 适用场景
- 当前文档的主要价值是列清单、做索引、做导航。
- 当前文档不承担核心规则正文。
- 当前文档为规则轨、fewshot 轨、元信息轨或 workflow 轨提供入口清单。
