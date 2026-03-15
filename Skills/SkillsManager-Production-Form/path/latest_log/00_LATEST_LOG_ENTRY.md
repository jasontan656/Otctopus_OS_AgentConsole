---
doc_id: skillsmanager_production_form.path.latest_log.entry
doc_type: path_doc
topic: Latest log entry
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
  reason: Latest log flow starts from its contract.
---

# 最近迭代入口

## 这个入口是干什么的
- 本入口用于读取 active runtime log 的最近记录，并管理 seed snapshot 的迁移规则。

## 下一跳列表
- [contract]：`10_CONTRACT.md`
