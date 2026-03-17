---
doc_id: workflow_sitemap_creation.path.self_governance.contract
doc_type: topic_atom
topic: Self governance contract
contract_name: workflow_sitemap_creation_self_governance_contract
contract_version: 1.0.0
validation_mode: reading_chain_contract
required_fields:
- reading_chain
- workflow_runtime_checklist
- stage_runtime_checklist
optional_fields:
- managed_writebacks
- evidence_summary
reading_chain:
- key: factory
  target: 20_FACTORY_CONVERSION.md
  hop: next
  reason: 先锁定 factory 规则，再进入 intent 强化与 subagent 主链。
---

# Self Governance Contract

- 当前入口固定服务 `Workflow-MotherDoc-OctopusOS` 的上游协作。
- 用户输入必须被拆成：
  - 产物侧目标
  - 技能侧固化目标
- factory 完成后，必须显式调用 `$Meta-Enhance-Prompt` 产出单段 `INTENT:`，不得直接回填写盘。
- `INTENT:` 后必须进入 background tmux subagent；subagent 不是可选优化，而是正式受管执行路径。
- 该 subagent 必须以 `Functional-Analysis-Runtask analysis_loop` 九阶段闭环消费 `INTENT:`，不得折叠中间阶段。
- `design` 阶段必须显式应用 `$Meta-keyword-first-edit` 的结构动作裁决。
- 本入口消费：
  - `workflow_runtime_checklist`
  - `stage_runtime_checklist`
- 本入口写回：
  - 受管 mother_doc 架构
  - 技能内部演化信号注册表
  - 轮次演化日志
  - background subagent 与 runtask 证据摘要
