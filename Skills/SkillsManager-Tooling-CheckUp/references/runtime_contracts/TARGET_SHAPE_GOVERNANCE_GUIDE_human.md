---
doc_id: skillsmanager_tooling_checkup.references_runtime_contracts_target_shape_governance_guide
doc_type: topic_atom
topic: TARGET_SHAPE_GOVERNANCE_GUIDE
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# TARGET_SHAPE_GOVERNANCE_GUIDE

<part_A>
- 本 guide 说明如何用本技能治理“目标 skill 的运行时形态”。
- `govern-target` 在审计前必须先看目标 `SKILL.md` 的 `skill_mode`。
- `guide_only` 直接豁免，`guide_with_tool` 放松 runtime-contract 形态检查，`executable_workflow_skill` 保持完整 CLI-first shape enforcement。
</part_A>

<part_B>

```json
{
  "directive_name": "skills_tooling_checkup_target_shape_governance_guide",
  "directive_version": "1.1.0",
  "doc_kind": "guide",
  "topic": "target-shape-governance",
  "purpose": "Govern a target skill so shape enforcement matches its declared skill_mode instead of forcing one global CLI-first shape.",
  "instruction": [
    "Use govern-target with --target-skill-root to audit the target skill against the governed shape.",
    "Read target SKILL.md skill_mode first and branch the audit policy before flagging violations.",
    "Only executable_workflow_skill requires full CLI-first dual-file runtime_contracts enforcement."
  ],
  "workflow": [
    "If skill_mode=guide_only, return exempt/skip guidance and stop the CLI/runtime-contract shape audit.",
    "If skill_mode=guide_with_tool, skip CLI-first dual-file runtime_contract checks and route the user to tooling/remediation directives for actual tooling code governance.",
    "If skill_mode=executable_workflow_skill, audit runtime_contracts, dual-file pairs, facade CLI-first wording, and agent prompt CLI-first wording, then validate with the target skill's own tests and repo-local lint."
  ],
  "rules": [
    "Payload JSON must contain the contract content itself, not a pointer telling the model to read another file.",
    "Human markdown mirrors may keep narrative Part A, but Part B must mirror the same JSON payload emitted by the tool.",
    "govern-target is an audit and governance-entry surface; it does not by itself rewrite the target skill.",
    "guide_only must not be marked non-compliant merely because it lacks runtime_contracts or CLI-first prompts."
  ]
}
```
</part_B>
