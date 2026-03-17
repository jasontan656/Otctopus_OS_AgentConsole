---
doc_id: workflow_sitemap_creation.path.self_governance.artifact_refresh
doc_type: action_contract_doc
topic: Artifact refresh stage for self governance
reading_chain:
- key: validation_closeout
  target: 60_VALIDATION_CLOSEOUT.md
  hop: next
  reason: 产物刷新后，必须进入 lint、对账与闭环校验。
---

# Artifact Refresh

- background subagent 完成 skill 本体改造后，主 AGENT 必须重新读取：
  - 最新技能门面
  - 最新 runtime contracts
  - 最新治理规则
  - 最新 runstate 要求
  - 最新 runtask 证据对象
- 主 AGENT 依据最新规则刷新：
  - `Octopus_OS/Development_Docs/mother_doc`
  - `Octopus_OS/Client_Applications/mother_doc`
  - 技能内部演化注册表与轮次日志
- 刷新动作必须展示规则变动后的框架形态，而不是固定模板重刷。
- 允许刷新样例内容、frontmatter、字段语义、文档关系、消费边界与 manifest，但必须基于本轮显式决策对象。
- 刷新前必须先判断是删掉重写、keyword-first 替换还是最小必要新增；禁止无差别清空整个 truth root。
