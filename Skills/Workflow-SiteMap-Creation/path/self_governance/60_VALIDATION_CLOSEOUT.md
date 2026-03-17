---
doc_id: workflow_sitemap_creation.path.self_governance.validation_closeout
doc_type: action_contract_doc
topic: Validation closeout for self governance
---

# Validation Closeout

- `self-governance-run` 必须返回并落盘以下闭环对象：
  - factory payload
  - enhanced `INTENT:`
  - tmux / subagent 运行摘要
  - runtask workspace / task runtime / stage evidence 摘要
  - keyword-first 决策摘要
  - artifact refresh 摘要
  - lint audit 摘要
  - git traceability 摘要
- `validation` 阶段必须能证明：
  - 九阶段对象存在且未折叠。
  - implementation / validation 有真实证据。
  - 最新 skill 本体、规则、实验产物与 registry / round log 一致。
  - tmux subagent 已由主 AGENT 手工终止，不存在残留后台进程。
- 若任何一步缺失、被折叠、被默认常量替代或只剩叙事没有真实执行，入口必须失败。
