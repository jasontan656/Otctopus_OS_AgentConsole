---
doc_id: skillsmanager_naming_manager.references_tooling_development_00_architecture_overview
doc_type: index_doc
topic: Cli_Toolbox 开发文档架构总览
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Cli_Toolbox 开发文档架构总览

适用技能：`SkillsManager-Naming-Manager`

## 目标
- 显式声明本技能当前没有本地 Toolbox，避免模板生成后的占位文案误导后续维护。
- 为未来若新增 CLI 时的治理位置预留稳定骨架。

## 分层结构
1. 入口层：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
2. 索引层：`10_MODULE_CATALOG.yaml`、`20_CATEGORY_INDEX.md`
3. 模块层：`references/tooling/development/modules/`
4. 变更层：`90_CHANGELOG.md`

## 当前实现状态
- `modules: []` 是正确状态，不代表漏写。
- 运行入口由命名、注册、调用语义与重组协议文档组成，不依赖脚本。
- 若未来补充 CLI，应新增模块文档并更新模块目录，而不是继续在本文件追加临时说明。
