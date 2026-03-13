---
doc_id: functional_codexbranchsession_chat.references_tooling_development_modules_final_reply_extractor
doc_type: topic_atom
topic: final_reply_extractor 模块开发文档
anchors:
- target: ../../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# final_reply_extractor 模块开发文档

## 模块标识
- `module_id`: `final_reply_extractor`
- `tool_alias`: `Cli_Toolbox.extract_assistant_final_reply`
- `entrypoint`: `scripts/branch_chat_toolbox.py extract-final-reply`

## 职责
- 从 session JSONL 中提取 assistant 消息，并按关键词命中目标 final reply。

## 输入输出契约
- 输入：`session_id`, optional `keyword`, optional `case_sensitive`
- 输出：`assistant_message_count`, `selected_message`（含 timestamp/source_file/line_number/text）
- 失败模式：
  - session 未命中
  - 关键词未命中 assistant 消息

## 回归检查
```bash
./.venv_backend_skills/bin/python Skills/Functional-CodexBranchSession-Chat/scripts/branch_chat_toolbox.py extract-final-reply \
  --session-id 019c9775-52cb-7b83-a15c-5fafb7998f2f \
  --keyword "结构化 Prompt"
```
