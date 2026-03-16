---
doc_id: skillsmanager_doc_structure.references.profiles.doc_topology_profiles
doc_type: topic_atom
topic: Supported document topology profiles
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This profile registry defines the topology model used by the linter.
---

# Document Topology Profiles

## `inline`
- 正文只留在 `SKILL.md`。
- 不应强制要求 `references/` 或 `path/`。

## `referenced`
- `SKILL.md` 是门面。
- 正文与合同下沉到 `references/`。
- 只要存在 scripts，就应有 runtime contract 与 tooling 文档。

## `workflow_path`
- workflow 正文下沉到 `path/`。
- `references/` 继续承载 profile、policy 与 runtime contract。
- 结构检查应覆盖 entry、contract、workflow index、step chain 与 validation。
