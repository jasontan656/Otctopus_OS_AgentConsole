# answer_responder 模块开发文档

## 模块标识
- `module_id`: `answer_responder`
- `tool_alias`: `Cli_Toolbox.answer_question`
- `entrypoint`: `scripts/branch_chat_toolbox.py answer-question`

## 职责
- 基于历史会话证据构建直接答疑结果（answer packet）。
- 支持两种模式：
  - `keyword_match`：用户提供关键词时，优先精准命中 assistant 回复。
  - `topic_evidence`：用户仅提供问题时，自动收集主题证据并选取主锚点回复。

## 输入输出契约
- 输入：`session_id|resume_id`, `question`, `keyword?`, `evidence_limit?`
- 输出：`answer_mode`, `selected_message`, `evidence_bundle`, `answer_packet.assistant_final_reply`, `answer_packet.direct_answer_draft`, `answer_packet.answer_prompt`
- 失败模式：
  - session/resume id 未命中
  - keyword 提供但未命中
  - 无 assistant 消息可用于主题定位

## 回归检查
```bash
python3 scripts/branch_chat_toolbox.py answer-question \
  --session-id 019c9775-52cb-7b83-a15c-5fafb7998f2f \
  --question "这个会话里的 lint 全扫脚本为什么慢？"

python3 scripts/branch_chat_toolbox.py answer-question \
  --session-id 019c9775-52cb-7b83-a15c-5fafb7998f2f \
  --keyword "external-lint-all" \
  --question "这些脚本的工作原理是什么？" \
  --evidence-limit 10
```
