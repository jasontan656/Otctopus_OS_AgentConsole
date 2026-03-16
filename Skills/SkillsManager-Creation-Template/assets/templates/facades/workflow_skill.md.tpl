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
- 本技能当前采用 `workflow_path` 文档拓扑。
- workflow 正文下沉到 `path/`，治理规则与 contract 继续留在 `references/`。

## 2. 必读顺序
1. 先读取 `references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md`。
2. 再读取 `references/routing/TASK_ROUTING.md`。
3. 再进入 `path/development_loop/00_DEVELOPMENT_LOOP_ENTRY.md`。

## 3. 分类入口
- 路由：`references/routing/TASK_ROUTING.md`
- workflow：`path/development_loop/00_DEVELOPMENT_LOOP_ENTRY.md`
- tooling：`references/tooling/Cli_Toolbox_USAGE.md`
