---
name: ${skill_name}
description: ${description}
skill_mode: executable_workflow_skill
doc_id: skill_creation_template.asset.staged_skill_template
doc_type: template_doc
topic: Executable workflow skill facade template asset
anchors:
- target: references/routing/TASK_ROUTING_TEMPLATE.md
  relation: implements
  direction: downstream
  reason: This asset routes to the task routing template in the current template pack.
- target: runtime/SKILL_RUNTIME_CONTRACT_TEMPLATE.md
  relation: governed_by
  direction: downstream
  reason: The staged facade template depends on the staged runtime contract template.
metadata:
  doc_structure:
    doc_id: ${skill_name}.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the staged skill ${skill_name}
    anchors:
    - target: references/routing/TASK_ROUTING.md
      relation: routes_to
      direction: downstream
      reason: The staged facade should still route readers through task routing.
    - target: references/runtime/SKILL_RUNTIME_OVERVIEW.md
      relation: governed_by
      direction: downstream
      reason: Staged skills must declare runtime governance explicitly.
---

# ${skill_name}

## 1. Immediate Contract
- 本文件只做门面入口，且只保留 `Immediate Contract` 与 `Structured Entry` 两段。
- 本技能采用 `executable_workflow_skill` 形态。
- 本技能的唯一主轴是：`[stage_1] -> [stage_2] -> [stage_3] -> [stage_4]`。
- 各阶段的读取边界、命令边界与 graph 角色以 runtime contract 与 stage contracts 为准。
- `SkillsManager-Doc-Structure` 仍是必用规则：即使是 staged skill，也要先有 façade、routing 与原子文档树。
- 阶段切换后，显式丢弃上一阶段 checklist、阶段文档与临时 focus，只保留顶层常驻文档。
- 不适用于：[明确排除域；若依赖 companion skill，只写边界，不回填其规则正文]
- 若某段内容不是立刻生效的约束，就必须下沉到 runtime、stages、topic atoms 或 tooling docs。

## 2. Structured Entry
1. 先读取 `references/runtime/SKILL_RUNTIME_OVERVIEW.json`。
2. 再读取 `references/routing/TASK_ROUTING.md`。
3. 再读取 `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`。
4. 进入 `references/stages/00_STAGE_INDEX.md`，再按阶段进入当前所需合同。
5. 再按需要进入 `SKILL_EXECUTION_RULES.md`、tooling docs 或其他原子文档。
- 入口：
  - `references/runtime/SKILL_RUNTIME_OVERVIEW.json`
  - `references/runtime/SKILL_RUNTIME_OVERVIEW.md`
  - `references/routing/TASK_ROUTING.md`
  - `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`
  - `references/governance/SKILL_EXECUTION_RULES.md`
  - `references/stages/00_STAGE_INDEX.md`
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `runtime-contract --json`
  - `stage-checklist --stage <stage>`
  - `stage-doc-contract --stage <stage>`
  - `stage-command-contract --stage <stage>`
  - `stage-graph-contract --stage <stage>`
