---
doc_id: "templates.atomic_doc"
doc_type: "template_doc"
topic: "Template for a single-topic markdown doc inside a skill folder"
anchors:
  - target: "../../references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "conforms_to"
    direction: "upstream"
    reason: "This template is defined by the runtime contract."
  - target: "../../SKILL.md"
    relation: "used_by"
    direction: "upstream"
    reason: "The skill facade routes readers to this template."
---

# Atomic Doc Template

```yaml
doc_id: "<skill.area.topic>"
doc_type: "<template_doc>"
topic: "<one stable topic statement>"
anchors:
  - target: "<relative/path/to/another/doc.md>"
    relation: "<governed_by|details|implements>"
    direction: "<upstream|downstream|cross>"
    reason: "<why>"
```

## Body Shape
- `Topic Boundary`
- `Core Claim`
- `Local Rules`
- `Exceptions`
- `Anchor Notes`
