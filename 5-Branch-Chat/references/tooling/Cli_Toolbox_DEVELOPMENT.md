# Cli_Toolbox 开发文档（入口）

适用技能：`5-Branch-Chat`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 内联索引（阅读顺序）
1. 架构总览：`references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
2. 模块目录：`references/tooling/development/10_MODULE_CATALOG.yaml`
3. 分类索引：`references/tooling/development/20_CATEGORY_INDEX.md`
4. 会话定位模块：`references/tooling/development/modules/session_locator.md`
5. Final Reply 提取模块：`references/tooling/development/modules/final_reply_extractor.md`
6. Answer Responder 模块：`references/tooling/development/modules/answer_responder.md`
7. 模块模板：`references/tooling/development/modules/MODULE_TEMPLATE.md`
8. 可观测契约：`references/tooling/OBSERVABILITY_CONTRACT.md`
9. 变更记录：`references/tooling/development/90_CHANGELOG.md`

## 文档分类规则
- 入口文档只负责导航、约束和模块边界。
- 结构和职责分拆见 `10_MODULE_CATALOG.yaml`。
- 每个工具能力都必须映射到一个模块文档，并保持命令参数、输出字段、失败码一致。

## 同步维护约束（强制）
- 工具变更必须同步更新：
  - `Cli_Toolbox_USAGE.md`
  - `10_MODULE_CATALOG.yaml`
  - 对应模块文档
- 新增子命令时，必须先登记模块目录再提交实现。

## 版本变更记录
- 2026-02-26：初始化 `5-Branch-Chat`，落地 session 定位、final reply 提取与 study packet 三个模块。
- 2026-02-26：语义收敛为“定位历史回复并直接答疑”，新增 `answer-question` 命令与 `resume_id` 入参别名。
- 2026-02-26：`answer-question` 增强为双模式：`keyword_match` 与 `topic_evidence`；支持仅 `resume_id + question` 自动收集证据并答疑，新增 `--evidence-limit`。
