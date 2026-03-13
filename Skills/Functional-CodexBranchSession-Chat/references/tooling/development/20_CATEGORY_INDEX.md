---
doc_id: functional_codexbranchsession_chat.references_tooling_development_20_category_index
doc_type: index_doc
topic: Cli_Toolbox 开发文档分类索引
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Cli_Toolbox 开发文档分类索引

## 分类导航
- 架构与边界：`00_ARCHITECTURE_OVERVIEW.md`
- 模块清单与映射：`10_MODULE_CATALOG.yaml`
- 会话定位：`modules/session_locator.md`
- 回复提取：`modules/final_reply_extractor.md`
- 直接答疑：`modules/answer_responder.md`
- 模块模板：`modules/MODULE_TEMPLATE.md`
- 变更记录：`90_CHANGELOG.md`

## 分类维护规则
- 新增工具时，先更新模块目录，再补模块文档。
- 若分类结构变更，必须同步更新入口文档索引。
- 所有模块文档必须覆盖输入输出契约与失败模式。
