---
doc_id: "templates.atomic_doc"
doc_type: "template_doc"
topic: "Template for a single-topic markdown doc inside a skill folder"
anchors:
  - target: "../../references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "conforms_to"
    direction: "upstream"
    reason: "This template is defined by the runtime contract."
  - target: "../../references/methodology/SEMANTIC_ROUTING_TREE.md"
    relation: "used_by"
    direction: "upstream"
    reason: "The semantic routing tree explains when this template should become a facade, routing, or atomic doc."
---

# Atomic Doc Template

```yaml
doc_id: "<skill.area.topic>"
doc_type: "<routing_doc|topic_atom|index_doc>"
topic: "<one stable topic statement>"
anchors:
  - target: "<relative/path/to/another/doc.md>"
    relation: "<governed_by|details|implements|routes_to|belongs_to>"
    direction: "<upstream|downstream|cross>"
    reason: "<why>"
```

## Role Choice
- 若当前文档负责把读者送入下一层分叉，用 `routing_doc`。
- 若当前文档只承载一个稳定主题，用 `topic_atom`。
- 若当前文档只做导航清单，不承载主规则，用 `index_doc`。

## Body Shape
- `Local Purpose`
- `Current Boundary`
- `Routing Decision` or `Local Rule`
- `Exceptions`
- `Next Anchors`

## Split Check
- 如果正文同时包含多个独立分叉轴线，先拆成多个 `routing_doc`。
- 如果正文已经只剩一个稳定主题，再落到 `topic_atom`。
- 如果正文主要在列清单而不是给规则，把它改成 `index_doc`。
