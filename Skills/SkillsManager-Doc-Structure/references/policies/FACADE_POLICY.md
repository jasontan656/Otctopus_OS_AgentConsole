---
doc_id: skillsmanager_doc_structure.references.policies.facade_policy
doc_type: topic_atom
topic: Facade policy for skills
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This policy defines what the facade must contain.
---

# Facade Policy

## `inline`
- 必须包含 `## 1. 技能定位`。
- 应直接包含正文，不强制外跳到 `references/` 或 `path/`。

## `referenced` / `workflow_path`
- 必须包含：
  - `## Runtime Entry`
  - `## 1. 技能定位`
  - `## 2. 必读顺序`
  - `## 3. 分类入口`
- 门面只做路由，不把深规则重新长回门面。
- `metadata.skill_profile` 应与实际目录结构一致。
