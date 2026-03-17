---
name: Meta-Enhance-Prompt
description: '将用户原始 prompt / instruction / workflow 请求澄清为可直接复用的 `INTENT:` 输出。核心职责是压缩噪音、补齐逻辑闭环，并发布最终意图结果而不是六段合同。Manual invoke: $Meta-Enhance-Prompt.'
metadata:
  doc_structure:
    doc_id: meta_enhance_prompt.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Meta-Enhance-Prompt skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# Meta Enhance Prompt

## 1. 定位
- 本技能用于把用户原始表达澄清成单段可复用的 `INTENT:` 输出。
- 本技能只治理 prompt / instruction / workflow 的意图强化，不承担 repo 调研的替代执行，也不输出方法论报告。
- 当用户提供 `codex id / session id / resume id` 并要求先读取隔壁会话最后一轮 assistant 回复时，该 id 属于前置上下文参数，不属于被强化 prompt 正文。
- 当用户提供 `codex id / session id / resume id` 并要求先阅读聊天记录时，助理必须优先调用 `Cli_Toolbox.py read-session-context` 快速提取所需聊天内容，再继续强化、分析或回答。
- 本技能的模型运行时入口已经切换为 CLI-first；`SKILL.md` 只保留人类门面与路由叙事。

## 2. 工具入口
- 统一 runtime 入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py contract --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py directive --topic <topic> --json`
- 会话上下文快速读取入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py read-session-context --lookup-key <rollout_key> --lookup-id <id> --json`
  - 可直接用别名：`--codex-id <id>` / `--session-id <id>` / `--resume-id <id>`
  - 默认输出聚焦 `focused_chat.user_prompt + focused_chat.assistant_reply`；需要同会话其他上下文时，再补 `--message-key/--message-query/--context-mode`
- 意图澄清过滤入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py intent-clarify --input-file <path_to_raw_intent_text_file> --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py active-invoke --input-file <path_to_raw_intent_text_file> --json`（兼容别名）
  - `./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py skill-directive --input-file <path_to_user_intent_text_file> --json`
  - 若未提供 `--input-file`，上述三个子命令默认从 `stdin` 读取原始文本，避免 shell quoting 风险
- 模型读取合同、workflow、instruction、guide 时必须优先消费 CLI JSON；human markdown 只作为叙事镜像。

## 3. 必读顺序
1. 先执行 `scripts/Cli_Toolbox.py contract --json`。
2. 若请求里出现 `codex/session/resume id` 且用户要求先阅读聊天记录，先执行 `scripts/Cli_Toolbox.py directive --topic session-context-read --json`，再调用 `scripts/Cli_Toolbox.py read-session-context ... --json` 获取所需聊天内容。
3. 再按任务意图读取 directive：
   - 澄清用户意图：`--topic intent-clarify`（`active-invoke` 为兼容别名）
   - 读取历史聊天：`--topic session-context-read`
   - 运行时入口提示：`--topic skill-directive`
   - 日志与结果治理：`--topic output-governance`
4. 真正执行 `filter_active_invoke_output.py` 前，必须先把用户原话澄清成一段可发布的意图草稿；草稿可以是单段文字，也可以显式带 `INTENT:` 头。
   - 若原话形如 `先阅读 codex id : xxxx 的最后一轮助理回复，理解上下文后，帮我强化如下prompt:("xxx")`，只把 `xxx` 作为被强化目标；`codex id` 与“先阅读”属于前置上下文读取要求。
5. 只有当 CLI JSON 仍留有真实语义缺口时，才打开 human mirror 或模板文件。

## 4. 运行时约束
- 最终发布结果固定为单段：
  - `INTENT:`
- `intent-clarify` 是 canonical topic；`active-invoke` 仅作为兼容入口保留。
- `intent_clarify` / `active_invoke` 不允许用默认占位文案伪造空意图；无有效意图时必须失败。
- 输入里若出现 `codex id / session id / resume id` 与“先阅读最后一轮 assistant 回复”的描述，运行时必须先当作上下文读取参数处理，而不是把这段话直接写进最终 `INTENT:`。
- 输入里若出现 `codex id / session id / resume id` 与“先阅读聊天记录”的描述，运行时必须优先使用 `read-session-context`；禁止退化成手工搜索原始 session jsonl。
- `skill_directive` 不再把模型路由回 `SKILL.md`，而是返回 CLI-first 入口指引。
- 原始长文本输入的 canonical 入口固定走 `Cli_Toolbox.py intent-clarify / active-invoke / skill-directive` 的 `--input-file` 或 `stdin`；不要把整段 prompt 继续塞进 shell 参数里的 `--input-text`。
- 运行时日志默认治理到受管 runtime root；结果文件默认治理到受管 result root，并支持显式 `--output-path`。

## 5. 参考入口
- Runtime 合同：`references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`
- Directive 索引：`references/runtime_contracts/DIRECTIVE_INDEX.json`
- Human mirrors：`references/runtime_contracts/*_human.md`
- 模板：`references/templates/intent_clarify_template_v1.txt`

## 6. 结构索引
```text
Meta-Enhance-Prompt/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── runtime_contracts/
│   └── templates/
├── scripts/
│   ├── Cli_Toolbox.py
│   ├── filter_active_invoke_output.py
│   ├── filter_prompt_shape_helper.py
│   ├── filter_runtime_governance.py
│   ├── filter_skill_directive_support.py
│   └── session_context_support.py
└── tests/
```
