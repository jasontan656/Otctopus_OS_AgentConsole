---
doc_id: skillsmanager_creation_template.references.profiles.skill_profile_schema
doc_type: topic_atom
topic: Stable scaffold profile schema
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The profile schema is the stable contract source for this skill.
---

# Skill Profile Schema

```yaml
metadata:
  skill_profile:
    doc_topology: inline | referenced | workflow_path
    tooling_surface: none | contract_cli | automation_cli
    workflow_control: advisory | guardrailed | compiled
```

## 语义定义
- `doc_topology`
  - `inline`：正文只在 `SKILL.md`。
  - `referenced`：正文下沉到 `references/`。
  - `workflow_path`：高约束流程正文下沉到 `path/`，治理规则仍下沉到 `references/`。
- `tooling_surface`
  - `none`：没有机器入口。
  - `contract_cli`：只提供 contract/directive 一类稳定入口。
  - `automation_cli`：提供 contract 之外的受治理动作入口。
- `workflow_control`
  - `advisory`：只提供轻量指导。
  - `guardrailed`：带固定治理门禁。
  - `compiled`：需要 workflow compiler 或步骤型执行闭环。

## 稳定规则
- 三个字段必须正交理解，不得再用一个字段包办全部职责。
- contract schema 稳定优先于命令名稳定。
- `workflow_path` 只是一种正式 profile，不是默认模板。
