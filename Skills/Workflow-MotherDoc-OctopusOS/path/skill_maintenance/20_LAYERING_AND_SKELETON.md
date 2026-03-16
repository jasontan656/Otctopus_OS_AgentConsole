---
doc_id: workflow_motherdoc_octopusos.path.skill_maintenance.layering
doc_type: topic_atom
topic: Workflow-MotherDoc-OctopusOS layering principles and evolving skeleton
reading_chain:
- key: reorg_rules
  target: 25_ROUND_REORG_RULES.md
  hop: next
  reason: 读完分层与骨架后，继续读回合级结构调整和正文迁移规则。
---

# 分层原则与演进骨架

## 稳定分层原则
- 门面层：`SKILL.md`、`agents/openai.yaml` 与运行时合同镜像只负责稳定发现面、入口导航和高层约束，不承载会频繁迁移的细节正文。
- 业务执行层：`path/stage_flow/` 只服务真实 `mother_doc` 阶段执行链，保持单阶段职责，不掺入技能自维护说明。
- 自维护治理层：`path/skill_maintenance/` 负责承载本技能如何持续重构、何时重组结构、怎样迁移旧内容、何时需要新增稳定承载位。
- 资产与模板层：`assets/` 只保留模板、示例、审计注册表和业务资产，不把治理正文散落到模板目录。
- tooling 与验证层：`scripts/`、`tests/` 只承接 CLI 包装和最小回归验证；若只是文档结构治理，不额外发明新的独立 CLI。

## 当前推荐骨架
```text
Workflow-MotherDoc-OctopusOS/
├── SKILL.md
├── agents/
├── assets/
├── path/
│   ├── stage_flow/
│   └── skill_maintenance/
├── references/
├── scripts/
└── tests/
```

## 骨架演进原则
- 当前骨架是“可继续改”的稳定起点，不是假定终局。
- 当某一类主题形成稳定复用轴时，允许在当前技能内部新增更合适的子目录或主题文档。
- 当两个文档总是一起阅读、职责无法清晰切开时，应优先合并。
- 当一个文档同时承载不同读者、不同节奏或不同决策层级的内容时，应优先拆分。
- 当正文已经明显写在错误层级时，应直接迁移到更合适的位置，而不是继续在旧位置累积补丁。

## 文档职责判断准则
- 先判断该内容是在定义“阶段如何工作”，还是在定义“技能如何维护自身”；前者进 `stage_flow`，后者进 `skill_maintenance`。
- 先判断该内容需要稳定暴露给首次进入技能的模型，还是只服务演进治理；前者留在门面层，后者下沉到治理层。
- 先判断该内容是长期模板/资产，还是本轮治理判断；模板留在 `assets/`，治理判断写到 `path/`。

## 下一跳列表
- [reorg_rules]：`25_ROUND_REORG_RULES.md`
