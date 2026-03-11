---
doc_id: "skill_creation_template.asset.stage_system_template"
doc_type: "template_doc"
topic: "Template for the staged skill stage system overview"
anchors:
  - target: "00_STAGE_INDEX_TEMPLATE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "The stage system overview and stage index are maintained together."
  - target: "../runtime/SKILL_RUNTIME_CONTRACT_TEMPLATE.md"
    relation: "implements"
    direction: "upstream"
    reason: "The stage system template depends on the staged runtime contract template."
---

# Stage System Template

适用技能：`${skill_name}`

## 目标
- 为复杂 staged skill 提供统一的阶段目录设计。
- 让阶段切换、读取边界和命令边界有固定出口，而不是散落在长文档里。
- markdown 用于人类审计与窄域导航；运行态边界由 CLI 输出的 machine-readable contracts 决定。

## 推荐结构
```text
references/stages/
├── 00_STAGE_INDEX.md
└── <stage_slug>/
    ├── INSTRUCTION.md
    ├── WORKFLOW.md
    ├── RULES.md
    ├── CHECKLIST.json
    ├── DOC_CONTRACT.json
    ├── COMMAND_CONTRACT.json
    └── GRAPH_CONTRACT.json
```

## 使用规则
- `00_STAGE_INDEX.md` 只做阶段入口索引。
- 每个阶段目录只承载该阶段自己的文档与 contracts。
- 阶段切换后，上一阶段文档不应继续保留在运行时 focus 中。
- 若某项合同依赖真实项目状态，应把动态部分放到 CLI 计算输出，而不是写死在模板里。
