# Stage System Template

适用技能：`${skill_name}`

## 目标
- 为复杂 staged skill 提供统一的阶段目录设计。
- markdown 用于人类审计与窄域导航。
- 运行时边界由 CLI 输出的 machine-readable 合同决定。

## 推荐结构
```text
references/stages/
├── 00_STAGE_INDEX.md
└── <stage_slug>/
    ├── INSTRUCTION.md
    ├── WORKFLOW.md
    ├── RULES.md
    ├── DOC_CONTRACT.json
    ├── COMMAND_CONTRACT.json
    └── GRAPH_CONTRACT.json
```

## 使用规则
- `00_STAGE_INDEX.md` 只做阶段入口索引。
- 每个阶段目录只承载该阶段自己的文档。
- 若阶段切换，上一阶段文档不应继续保留在运行时 focus 中。
