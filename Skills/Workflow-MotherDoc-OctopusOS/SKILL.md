---
name: Workflow-MotherDoc-OctopusOS
description: Octopus_OS 的 mother_doc 阶段技能；负责把需求按既有文档体系逐层写回，并同步整体架构。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: workflow_motherdoc_octopusos.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Workflow-MotherDoc-OctopusOS skill
---

# Workflow-MotherDoc-OctopusOS

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能只负责 `mother_doc` 阶段。
- 正确目标不是造一棵巨型混写知识树，而是把用户需求按既有 mother doc 体系逐层写回。
- 顶层文档先承担常驻规范、知识索引与产品级基线；越向下越从人类叙事过渡到机械叙事。
- 当主题需要进入更深锚点文档时，必须由用户显式指定下一个文档主题；本技能负责同步 overview/index/entry-map 等整体架构文档。

### 2. 技能约束
- 只处理 `mother_doc`，不在本技能里切 pack、不落 implementation、不做 acceptance 收口。
- 工作目录统一由本技能自己的 `target-runtime-contract` 解析；默认落在 `Octopus_OS/Development_Docs/mother_doc`。
- `mother-doc-audit` 只作为可选治理动作，不能替代 live requirement source。
- 真实写回后必须经过 `mother-doc-lint`、`mother-doc-refresh-root-index` 与 `mother-doc-sync-client-copy`。

### 3. 顶层常驻合同
- 先锁定当前主题与归属层级，再决定当前轮最小写回切片。
- 若用户尚未指定更深锚点主题，不得自动创建新的下层 anchor doc。
- 后续若要继续推进到下游阶段，必须由用户显式切换到对应的新技能，而不是经由兼容壳跳转。

## 2. 功能入口
- [stage_flow]：`path/stage_flow/00_STAGE_FLOW_ENTRY.md`
  - 作用：进入 `mother_doc` 阶段的最小执行链。

## 3. 目录结构图
```text
Workflow-MotherDoc-OctopusOS/
├── SKILL.md
├── agents/
└── path/
    └── stage_flow/
```
