# Cli_Toolbox 开发文档架构总览

适用技能：`4-Branch-Chat`

## 目标
- 用稳定的只读提取链路，支持“从历史 session 抽取目标 assistant 回复与主题证据，并直接回答问题”。

## 分层结构
1. 入口层：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
2. 索引层：`10_MODULE_CATALOG.yaml`、`20_CATEGORY_INDEX.md`
3. 模块层：`references/tooling/development/modules/`
4. 变更层：`90_CHANGELOG.md`

## 运行链路
1. `session_locator` 解析 Codex 根目录并定位 session 文件。
2. `final_reply_extractor` 解析 JSONL 并提取 assistant 消息（可按关键词精确定位目标回复）。
3. `answer_responder` 在 `keyword_match/topic_evidence` 两种模式下汇总证据并生成可直接答疑的 answer packet。

## 边界约束
- 默认只读 `~/.codex/sessions`。
- 不修改源日志，不做会话回写。
- 错误必须结构化输出，保证上游可自动处理。
