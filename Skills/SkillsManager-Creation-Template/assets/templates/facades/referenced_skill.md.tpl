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
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the runtime contract.
---

# {{skill_name}}

## Runtime Entry
- Primary runtime entry: `./scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source; `SKILL.md` remains a facade.

## 1. 技能定位
- 本技能当前采用 `referenced` 文档拓扑。
- 门面只负责路由，正文下沉到 `references/`。

## 2. 必读顺序
1. 先读取 `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`。
2. 再读取 `references/routing/TASK_ROUTING.md`。
3. 再读取 `references/policies/SKILL_EXECUTION_RULES.md`。

## 3. 分类入口
- `references/routing/TASK_ROUTING.md`
- `references/policies/SKILL_EXECUTION_RULES.md`
- `references/tooling/Cli_Toolbox_USAGE.md`

## 4. 适用域
- 在这里补充该技能真正要治理的问题域。
