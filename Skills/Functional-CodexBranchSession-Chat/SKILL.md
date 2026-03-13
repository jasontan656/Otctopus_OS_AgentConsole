---
name: "Functional-CodexBranchSession-Chat"
description: 接收 resume/session id 与问题（可选关键词）定位会话证据，并基于证据直接回答用户问题。
---

# Functional-CodexBranchSession-Chat

## 1. 目标
- 接收用户输入的 `resume_id/session_id + question`（`keyword` 可选），定位指定 session 中的目标 assistant 回复与主题证据。
- 基于定位结果直接输出答疑内容，不引入“制作技能本身”的任务目标。
- 让用户在新窗口可以直接问答，不需要先手工整理历史上下文。

## 2. 可用工具
- 命名规则：工具统一命名为 `Cli_Toolbox.<tool_name>`。
- `Cli_Toolbox.locate_session`
  - 入口：`./.venv_backend_skills/bin/python Skills/Functional-CodexBranchSession-Chat/scripts/branch_chat_toolbox.py locate-session --session-id <session_id>`（或 `--resume-id <resume_id>`）
  - 作用：自动发现 Codex 安装目录（优先 `--codex-home`，其次 `<root>/.codex`，再到 `$CODEX_HOME`，最后回退 `~/.codex`），并在 `sessions/` 下定位对应 session 日志文件。
- `Cli_Toolbox.extract_assistant_final_reply`
  - 入口：`./.venv_backend_skills/bin/python Skills/Functional-CodexBranchSession-Chat/scripts/branch_chat_toolbox.py extract-final-reply --session-id <session_id> --keyword "<keyword>"`（或 `--resume-id <resume_id>`）
  - 作用：读取 session 日志中的 assistant 消息，按关键词匹配并返回最终命中的 assistant reply（默认取时间上最后一条命中）。
- `Cli_Toolbox.answer_question`
  - 入口：`./.venv_backend_skills/bin/python Skills/Functional-CodexBranchSession-Chat/scripts/branch_chat_toolbox.py answer-question --session-id <session_id> --question "<user_question>" [--keyword "<keyword>"] [--evidence-limit 8]`（或 `--resume-id <resume_id>`）
  - 作用：
    - 若提供 `keyword`：优先按关键词命中 assistant 回复，再补充主题证据。
    - 若不提供 `keyword`：按问题主题在 session 内自动收集高相关证据并定位主要 assistant 锚点回复。
    - 最终输出可直接答疑的 `answer_packet`（含 `answer_mode` 与 `evidence_bundle`）。
- 文档同步约束（强制）：
  - 使用文档：`references/tooling/Cli_Toolbox_USAGE.md`
  - 开发文档：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
  - 多模块开发索引：
    - `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
    - `references/tooling/development/10_MODULE_CATALOG.yaml`
    - `references/tooling/development/20_CATEGORY_INDEX.md`
    - `references/tooling/development/modules/MODULE_TEMPLATE.md`

## 3. 工作流约束
- 输入：
  - `session_id` 或 `resume_id`（二选一必填）
  - `keyword`（可选；用于精确命中 assistant 消息）
  - `question`（必填；用于直接回答问题）
  - `evidence_limit`（可选；默认 `8`）
- 标准流程：
  1. 执行 `Cli_Toolbox.locate_session`，确认 session 日志文件存在。
  2. 若用户提供关键词，可执行 `Cli_Toolbox.extract_assistant_final_reply` 获取精准命中回复。
  3. 执行 `Cli_Toolbox.answer_question`，在关键词模式或主题证据模式下输出直接答疑结果。
- 输出：
  - `session_files`、`assistant_message_count`、`selected_message`、`answer_mode`
  - `evidence_bundle`（主题证据列表，含来源/行号/匹配项/片段）
  - `answer_packet`（含 `direct_answer_draft`、`answer_prompt`、`uncertainty_note`）
- 完成判定：
  - 成功定位至少一个 session 文件；
  - 成功返回至少一条 assistant 消息；
  - 若提供 `keyword`，必须返回关键词命中证据或明确失败原因；
  - 若不提供 `keyword`，必须返回可解释的主题证据集合。

## 4. 规则约束
- 只读边界：
  - 默认只读取 `<root>/.codex/sessions/**`；若 `<root>/.codex` 不存在，则回退到 `$CODEX_HOME/sessions/**` 或 `~/.codex/sessions/**`，不修改会话原始文件。
- 关键词匹配策略：
  - 默认大小写不敏感；命中多条时选择时间上最后一条（closest to final reply）。
- 失败门禁：
  - `session_id` 未命中文件，必须返回 `status=error` + 修复建议。
  - 提供 `keyword` 但未命中 assistant 消息，必须返回 `status=error` + 可用候选提示。
  - 未提供 `keyword` 且 session 无 assistant 消息，必须返回 `status=error`。
- 目录边界：
  - 技能实现仅落地于 `Otctopus_OS_AgentConsole/Skills/Functional-CodexBranchSession-Chat`。
- 运行观测契约：
  - 必须保留双通道日志：`machine.jsonl`（机器可解析）与 `human.log`（人类可读）。
  - 日志根目录锚点：`<root>/Codex_Skill_Runtime/Functional-CodexBranchSession-Chat/`。

## 5. 方法论约束
- 何时使用：
  - 用户提供 `resume/session id`，并希望围绕历史会话内容直接提问时（可带关键词，也可只给问题）。
- 何时不使用：
  - 不需要引用历史 session 证据、当前上下文即可回答时。
- 回答建议：
  - 优先给直接答案，再引用主锚点回复与证据片段；若证据不足，明确指出不确定性。

## 6. 内联导航索引
- `Cli_Toolbox 工具入口` -> `scripts/branch_chat_toolbox.py`
- `技能元数据` -> `agents/openai.yaml`
- `Cli_Toolbox 使用文档` -> `references/tooling/Cli_Toolbox_USAGE.md`
- `Cli_Toolbox 开发文档` -> `references/tooling/Cli_Toolbox_DEVELOPMENT.md`
- `Cli_Toolbox 开发架构总览` -> `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
- `Cli_Toolbox 开发分类索引` -> `references/tooling/development/20_CATEGORY_INDEX.md`
- `Cli_Toolbox 模块目录` -> `references/tooling/development/10_MODULE_CATALOG.yaml`
- `Session 定位模块` -> `references/tooling/development/modules/session_locator.md`
- `Final Reply 提取模块` -> `references/tooling/development/modules/final_reply_extractor.md`
- `Answer Responder 模块` -> `references/tooling/development/modules/answer_responder.md`
- `可观测契约` -> `references/tooling/OBSERVABILITY_CONTRACT.md`

## 7. 架构契约
```text
Functional-CodexBranchSession-Chat/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── branch_chat_toolbox.py
├── references/
│   └── tooling/
│       ├── Cli_Toolbox_USAGE.md
│       ├── Cli_Toolbox_DEVELOPMENT.md
│       ├── OBSERVABILITY_CONTRACT.md
│       └── development/
│           ├── 00_ARCHITECTURE_OVERVIEW.md
│           ├── 10_MODULE_CATALOG.yaml
│           ├── 20_CATEGORY_INDEX.md
│           ├── 90_CHANGELOG.md
│           └── modules/
│               ├── MODULE_TEMPLATE.md
│               ├── session_locator.md
│               ├── final_reply_extractor.md
│               └── answer_responder.md
└── assets/
```
