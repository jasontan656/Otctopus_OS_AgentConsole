---
name: ${skill_name}
description: ${description}
doc_id: skill_creation_template.asset.staged_skill_template
doc_type: template_doc
topic: Staged skill facade template asset
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

## 1. 技能定位
- 本文件只做门面入口，不承载阶段正文。
- 本技能的唯一主轴是：`[stage_1] -> [stage_2] -> [stage_3] -> [stage_4]`。
- 各阶段的读取边界、命令边界与 graph 角色以 runtime contract 与 stage contracts 为准。

## 2. 必读顺序
1. 先读取 `references/runtime/SKILL_RUNTIME_OVERVIEW.json`。
2. 再读取 `references/routing/TASK_ROUTING.md`。
3. 再读取 `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`。
4. 进入 `references/stages/00_STAGE_INDEX.md`，再按阶段进入当前所需合同。

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- 治理层：
  - `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`
  - `references/governance/SKILL_EXECUTION_RULES.md`
- 运行合同层：
  - `references/runtime/SKILL_RUNTIME_OVERVIEW.json`
  - `references/runtime/SKILL_RUNTIME_OVERVIEW.md`
- 阶段层：
  - `references/stages/00_STAGE_INDEX.md`

## 4. 适用域
- 适用于：[明确该 staged skill 负责的 staged workflow]
- 不适用于：[明确排除域]
- [若依赖 companion skill，只写边界，不回填其规则正文]

## 5. 执行入口
- `runtime-contract --json`
- `stage-checklist --stage <stage>`
- `stage-doc-contract --stage <stage>`
- `stage-command-contract --stage <stage>`
- `stage-graph-contract --stage <stage>`

## 6. 读取原则
- 门面只负责阶段入口与顶层边界，不回填阶段正文。
- `SkillsManager-Doc-Structure` 仍是必用规则：即使是 staged skill，也要先有 facade、routing 与原子文档树。
- 阶段切换后，显式丢弃上一阶段 checklist、阶段文档与临时 focus，只保留顶层常驻文档。
- 若此 skill 也是模板或治理类 skill，可在下沉文档中使用 `技能本体 / 规则说明` 双段式，但不应让 facade 膨胀。

## 7. 结构索引
```text
<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── Cli_Toolbox.py
├── references/
│   ├── governance/
│   ├── routing/
│   ├── runtime/
│   ├── stages/
│   └── tooling/
├── assets/
│   └── templates/
│       └── stages/
└── tests/
```
