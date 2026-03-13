---
doc_id: templates.atomic_doc
doc_type: template_doc
topic: Template for a single-topic atom doc inside a governed skill folder
anchors:
- target: ../../references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_OVERVIEW.md
  relation: conforms_to
  direction: upstream
  reason: This template is defined by the runtime contract.
- target: ROUTING_DOC_TEMPLATE.md
  relation: pairs_with
  direction: cross
  reason: Routing and atomic templates are usually read together when organizing a tree.
---

# Atomic Doc Template

```yaml
doc_id: "<skill.area.topic>"
doc_type: "topic_atom"
topic: "<one stable topic statement>"
node_role: "topic_atom"
domain_type: "<optional domain marker>"
anchors:
  - target: "<relative/path/to/another/doc.md>"
    relation: "<governed_by|details|implements|belongs_to|expands>"
    direction: "<upstream|downstream|cross>"
    reason: "<why>"
```

## 适用场景
- 当前文档只承载一个稳定 topic。
- 当前文档已经不再继续做大的语义分叉。
- 当前文档需要承载局部规则、局部例外或局部执行面。

## Body Shape
- `Local Purpose`
- `Current Boundary`
- `Local Rule`
- `Exceptions`
- `Next Anchors`

## Split Check
- 如果正文同时包含多个独立分叉轴线，先回退到 `ROUTING_DOC_TEMPLATE.md`。
- 如果正文主要在列清单而不是给规则，改用 `INDEX_DOC_TEMPLATE.md`。
- 如果正文已经只剩一个稳定主题，再落到当前模板。
