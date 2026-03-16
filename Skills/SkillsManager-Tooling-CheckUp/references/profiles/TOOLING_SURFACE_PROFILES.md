---
doc_id: skillsmanager_tooling_checkup.references.profiles.tooling_surface_profiles
doc_type: topic_atom
topic: Supported tooling surface profiles
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This profile registry defines the tooling surfaces audited by this skill.
---

# Tooling Surface Profiles

## `none`
- 没有 scripts，也不要求 runtime contract。
- 审计重点是确认 target skill 没有假装存在机器入口。

## `contract_cli`
- 有稳定 `contract`/`directive` 一类机器入口。
- 应同时有 runtime contract、tooling 文档与 tests。

## `automation_cli`
- 除 contract 之外还有实际动作命令。
- 仍然必须先满足 contract_cli 的全部基线。
