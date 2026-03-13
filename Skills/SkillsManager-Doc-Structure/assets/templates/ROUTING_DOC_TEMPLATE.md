---
doc_id: templates.routing_doc
doc_type: template_doc
topic: Template for a single-axis routing doc inside a governed skill folder
anchors:
- target: ../../references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_OVERVIEW.md
  relation: conforms_to
  direction: upstream
  reason: This routing template is defined by the runtime contract.
- target: INDEX_DOC_TEMPLATE.md
  relation: pairs_with
  direction: cross
  reason: Routing and index templates are often used together when shaping a tree.
---

# Routing Doc Template

```yaml
doc_id: "<skill.branch.axis>"
doc_type: "routing_doc"
topic: "<one branching axis statement>"
node_role: "routing_doc"
domain_type: "<optional domain marker>"
anchors:
  - target: "<relative/path/to/upstream/doc.md>"
    relation: "belongs_to"
    direction: "upstream"
    reason: "<why this routing doc belongs there>"
  - target: "<relative/path/to/next/doc.md>"
    relation: "routes_to"
    direction: "downstream"
    reason: "<why readers should continue there>"
```

## 适用场景
- 当前文档负责把读者送入下一层语义分支。
- 当前文档只承载一个分叉轴线。
- 当前文档可以有最小必要的边界说明，但不承载深层规则正文。

## Body Shape
- `Axis Purpose`
- `Current Boundary`
- `Child Entries`
- `Selection Rule`
- `Next Anchors`
