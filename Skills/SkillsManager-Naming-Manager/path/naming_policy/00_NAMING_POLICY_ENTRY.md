---
doc_id: skillsmanager_naming_manager.path.naming_policy.entry
doc_type: path_doc
topic: Naming policy entry
actor_id: skill_runtime_operator
role: naming_governance_reader
scope: naming_policy_entry
action: read_contract_context
policy_version: naming_manager_permission_v1
authz_result: allow
deny_code: none
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
  reason: Naming governance starts from its contract.
---

# 命名规范入口

## 这个入口是干什么的
- 本入口只服务技能命名规范治理。
- 当前线路用于统一 `canonical_id`、`display_name`、`prefix`、`family` 与 `role_tag` 的命名边界。

## 下一跳列表
- [contract]：`10_CONTRACT.md`
