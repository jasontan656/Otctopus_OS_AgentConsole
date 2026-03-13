---
doc_id: tooling.architecture.overview
doc_type: tooling_architecture
topic: Architecture overview of the TS CLI and markdown graph core
anchors:
- target: modules/mod_docstructure_core.md
  relation: indexes
  direction: downstream
  reason: The core module doc explains the doc graph engine.
- target: ../Cli_Toolbox_DEVELOPMENT.md
  relation: belongs_to
  direction: upstream
  reason: This overview belongs to the CLI development entry.
---

# Architecture Overview

## 核心组成
- `scripts/Cli_Toolbox.ts`
- `src/lib/docstructure.ts`
- `src/lib/types.ts`
- `assets/runtime/anchor_query_matrix.json`
- `references/rules/`
- `references/fewshot/`
- `references/metadata/`
- `references/workflows/`

## 设计目标
- 让 markdown 文档结构可被 lint、建图、重建 self graph。
- 让规则轨、fewshot 轨、元信息轨与 workflow 轨共用同一套 graph core。
- 保持技能只聚焦文档结构组织，不承担展示层职责。
