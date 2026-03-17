---
doc_id: workflow_sitemap_creation.path.self_governance.intent_enhance
doc_type: action_contract_doc
topic: Intent enhance stage for self governance
reading_chain:
- key: subagent
  target: 40_BACKGROUND_SUBAGENT.md
  hop: next
  reason: 强化后的 INTENT 是 background subagent 的唯一正式输入。
---

# Intent Enhance

- `factory-intake` 完成后，不允许直接把 factory payload 回填成写盘动作。
- 主 AGENT 必须显式调用 `$Meta-Enhance-Prompt`，把 factory 输出压缩为单段 `INTENT:`。
- 该 `INTENT:` 必须回答三件事：
  - 当前这一轮到底要解决什么框架问题。
  - 当前轮次对技能本体、实验产物与验证边界各自要做什么。
  - 哪些动作必须交给 `Functional-Analysis-Runtask analysis_loop` 九阶段闭环处理。
- `INTENT:` 不是说明文字镜像，而是 background subagent 的可执行任务输入；禁止把 `codex/session/resume id`、wrapper 话术或方法论段落带入最终 `INTENT:`。
- 若无法产出可执行 `INTENT:`，`self-governance-run` 必须失败，而不是退化成默认常量意图。
