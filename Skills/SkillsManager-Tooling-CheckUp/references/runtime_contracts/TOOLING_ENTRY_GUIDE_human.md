---
doc_id: skillsmanager_tooling_checkup.references_runtime_contracts_tooling_entry_guide
doc_type: topic_atom
topic: TOOLING_ENTRY_GUIDE
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# TOOLING_ENTRY_GUIDE

<part_A>
- 本 guide 说明本技能自己的 CLI-first 入口。
- 人类可以直接看本文件；模型则必须通过 `contract` 与 `directive` 读 Part B payload。
- 未来若新增任何运行时可消费的 contract/workflow/instruction/guide，也必须继续遵守 `*_human.md + same-name .json` 的双文件形态。
</part_A>

<part_B>

```json
{
  "directive_name": "skills_tooling_checkup_tooling_entry_guide",
  "directive_version": "1.0.0",
  "doc_kind": "guide",
  "topic": "tooling-entry",
  "purpose": "Explain the local toolbox surface and the human-versus-model reading boundary for this skill.",
  "instruction": [
    "The local toolbox entrypoint is scripts/Cli_Toolbox.py and it is now the primary runtime instruction source for this skill.",
    "Models must call contract first, then directive by topic, instead of walking markdown files for runtime guidance.",
    "When auditing a target skill, only judge its tooling surface and do not require the target to adopt this skill's own runtime asset layout."
  ],
  "workflow": [
    "Call contract to discover runtime constraints and directive topics.",
    "Call directive with the active topic to obtain direct instruction, workflow, and rules.",
    "Use cli-surface for command/parameter/output contracts, tooling-boundary for parser/helper/schema/lint/test/glue responsibilities, techstack-baseline for dependency replacement, and output-governance for write-path governance.",
    "Only use legacy governance or tooling markdown as secondary evidence when the JSON payload still leaves a real gap."
  ],
  "rules": [
    "Do not reinterpret target skill shape issues as tooling violations.",
    "Do not require a target skill to adopt references/runtime_contracts or CLI-first facade wording just because it ships scripts/.",
    "Judge only the target's actual tooling surface, execution entry, dependency-baseline drift, and output governance evidence."
  ]
}
```
</part_B>
