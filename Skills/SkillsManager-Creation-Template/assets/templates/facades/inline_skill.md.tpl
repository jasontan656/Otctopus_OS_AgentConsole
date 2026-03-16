---
name: {{skill_name}}
description: {{description}}
metadata:
  skill_profile:
    doc_topology: {{doc_topology}}
    tooling_surface: {{tooling_surface}}
    workflow_control: {{workflow_control}}
  doc_structure:
    doc_id: {{slug}}.entry.facade
    doc_type: skill_facade
    topic: Entry facade for {{skill_name}}
---

# {{skill_name}}

## 1. 技能定位
- 本技能当前采用 `inline` 文档拓扑。
- 全部正文保留在本门面，不再外跳到 `references/` 或 `path/`。

## 2. 技能正文
- 在这里补充该技能的单一主题规则与使用方式。
- 若后续正文开始膨胀，应先升级到 `referenced`，而不是继续堆在门面里。
