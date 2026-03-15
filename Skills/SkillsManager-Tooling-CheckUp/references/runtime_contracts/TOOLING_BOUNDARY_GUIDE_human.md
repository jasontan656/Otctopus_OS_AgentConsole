---
doc_id: skillsmanager_tooling_checkup.references_runtime_contracts_tooling_boundary_guide
doc_type: topic_atom
topic: TOOLING_BOUNDARY_GUIDE
---

# TOOLING_BOUNDARY_GUIDE

<part_A>
- 本 guide 只定义 tooling 模块的职责边界。
- 它不负责 Python/TypeScript 等语言本身的代码规范正文。
- 如果问题是胖文件、typing、异常风格、import side effect 之类语言专属规范，应交回对应语言 constitution。
</part_A>

<part_B>

```json
{
  "directive_name": "skills_tooling_checkup_tooling_boundary_guide",
  "directive_version": "1.0.0",
  "doc_kind": "guide",
  "topic": "tooling-boundary",
  "purpose": "Clarify which responsibilities belong to tooling modules and which must stay outside tooling governance.",
  "instruction": [
    "Parser code may parse and normalize external representations but must not silently become the target skill's domain policy engine.",
    "Schema or validation code may enforce declared shape contracts but must not absorb orchestration, migration strategy, or business meaning that belongs to domain workflows.",
    "Helper, lint, test, and glue modules should stay narrow: helpers support shared mechanics, lint modules diagnose or enforce, tests verify behavior, and glue code wires execution entrypoints."
  ],
  "workflow": [
    "Map each target tooling file to its actual role: CLI entry, parser, schema, helper, lint, test, or glue.",
    "Check whether the file is still performing only that role or has accumulated domain rules, workflow routing, or unrelated side effects.",
    "If a file crosses roles, shrink or split the minimal scope while preserving the target skill's external behavior."
  ],
  "rules": [
    "Do not use this guide to restate language-specific style rules such as Python fat-file policy; delegate those to the relevant language constitution.",
    "Do not treat cross-file reuse itself as a problem; only flag helpers or glue when they become hidden policy owners.",
    "Do not move target skill domain contracts into tooling modules under the pretext of consolidation."
  ]
}
```
</part_B>
