# Cli_Toolbox 使用文档

适用技能：`5-Branch-Chat`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 工具清单
- `Cli_Toolbox.locate_session`
  - `python3 scripts/branch_chat_toolbox.py locate-session --session-id <session_id>`（或 `--resume-id <resume_id>`）
- `Cli_Toolbox.extract_assistant_final_reply`
  - `python3 scripts/branch_chat_toolbox.py extract-final-reply --session-id <session_id> --keyword "<keyword>"`（或 `--resume-id <resume_id>`）
- `Cli_Toolbox.answer_question`
  - `python3 scripts/branch_chat_toolbox.py answer-question --session-id <session_id> --question "<question>" [--keyword "<keyword>"] [--evidence-limit 8]`（或 `--resume-id <resume_id>`）

## 叙事式使用说明（固定格式）

### `Cli_Toolbox.locate_session`
- 人类叙事版输入：
  - 我给你一个 `resume_id/session_id`，请先确认这段历史会话日志到底在哪个文件。
- 电脑动作发生了什么：
  - 运行 `locate-session` 子命令；工具会按优先级解析 Codex 目录（`--codex-home` > `$CODEX_HOME` > `~/.codex`），在 `sessions/` 下递归查找 `*<session_id>*.jsonl`。
- 人类叙事版输出：
  - 返回命中的日志文件路径列表和数量，你可以直接看到后续读取来源。

### `Cli_Toolbox.extract_assistant_final_reply`
- 人类叙事版输入：
  - 我给你 `resume_id/session_id` 和一个关键词，请把该会话里最靠近“最终回复”的那条 assistant 消息找出来。
- 电脑动作发生了什么：
  - 工具读取命中的 session 文件，逐行解析 JSONL，仅保留 `response_item/message/assistant` 消息；按关键词匹配后取时间上最后一条命中。
- 人类叙事版输出：
  - 返回 `selected_message`（含时间戳、来源文件、行号和正文），并给出总 assistant 消息数，便于判断检索覆盖是否充分。

### `Cli_Toolbox.answer_question`
- 人类叙事版输入：
  - 我给你 `resume_id/session_id + 问题`（可选关键词），请直接回答并说明证据来自哪里。
- 电脑动作发生了什么：
  - 若提供 `keyword`，先按关键词命中 assistant 回复；若不提供，则按问题主题在 session 内自动收集证据并选出主锚点回复。
  - 工具会输出 `answer_mode`、`evidence_bundle`，并组装 `answer_packet`（direct answer draft + answer prompt + uncertainty note）。
- 人类叙事版输出：
  - 你会拿到“可直接回答问题”的结构化结果，并且能追溯回答依据，不需要先手工整理上下文。

### 快速示例
```bash
# 关键词精确模式
python3 scripts/branch_chat_toolbox.py answer-question \
  --resume-id 019c9775-52cb-7b83-a15c-5fafb7998f2f \
  --keyword "external-lint-all" \
  --question "这些 lint 脚本为什么在全扫时很慢？"

# 主题证据模式（不提供关键词）
python3 scripts/branch_chat_toolbox.py answer-question \
  --resume-id 019c9775-52cb-7b83-a15c-5fafb7998f2f \
  --question "这个会话里的 lint 全扫脚本工作原理是什么，为什么慢？" \
  --evidence-limit 10
```

## 参数与结果（供 AI/工程使用）
- 输入：
  - `session_id: string` or `resume_id: string`（one required）
  - `keyword: string`（`answer-question` optional; `extract-final-reply` optional）
  - `question: string`（`answer-question` required）
  - `evidence_limit: int`（`answer-question` optional, default=`8`）
  - `codex_home: string`（optional）
- 输出：
  - 统一 JSON：`status`, `session_id`, `session_files`, `assistant_message_count`, `selected_message`, `answer_mode`, `evidence_bundle`, `answer_packet`。
- 失败码约定：
  - `2`: session 文件未命中
  - `3`: 关键词未命中 assistant 消息，或无可用于主题定位的 assistant 消息

## 同步维护要求
- 修改工具行为后，必须同步更新本文件与 `Cli_Toolbox_DEVELOPMENT.md`。
- 若为多模块 Toolbox，还需同步更新：
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - 对应模块文档（`references/tooling/development/modules/*.md`）
- 可观测约束文档：
  - `references/tooling/OBSERVABILITY_CONTRACT.md`（包含 `machine.jsonl`、`human.log`、`Codex_Skill_Runtime` 锚点）。
