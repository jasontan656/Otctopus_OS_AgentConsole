---
doc_id: skillsmanager_doc_structure.references.policies.reference_graph_policy
doc_type: topic_atom
topic: Reference graph policy for referenced skills
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This policy governs referenced document topology.
---

# Reference Graph Policy

## `referenced` 技能最小要求
- `references/routing/TASK_ROUTING.md`
- 至少一个 policy 文档：
  - `references/policies/`
  - 或 repo 既有命名 `references/governance/`
- 若存在 scripts：
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`
  - `references/tooling/`
  - `tests/`

## 允许事项
- 不要求固定 policy 文件名。
- 不要求 `references/` 只包含一种子目录。
