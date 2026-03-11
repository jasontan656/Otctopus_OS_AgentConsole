# Cli_Toolbox 开发变更记录

- 2026-02-26
  - 初始化 `Functional-CodexBranchSession-Chat` 技能骨架与 1-7 章节文档。
  - 新增 `scripts/branch_chat_toolbox.py`。
  - 新增三个模块文档：`session_locator`、`final_reply_extractor`、`study_packet_builder`。
  - 补齐 usage/development/index/catalog 的文档联动。
- 2026-02-26
  - 将语义从“study packet”收敛为“直接答疑”。
  - 新增命令 `answer-question`，并支持 `--resume-id` 作为 `--session-id` 别名。
  - 模块 `study_packet_builder` 重命名为 `answer_responder`。
- 2026-02-26
  - `answer-question` 支持“仅 `resume_id + question`”的主题证据模式（`topic_evidence`）。
  - `--keyword` 从必填改为可选；新增 `--evidence-limit` 控制证据返回条数。
  - 回答结果新增 `answer_mode` 与 `evidence_bundle`，并补充性能慢问题的证据化回答草稿策略。
