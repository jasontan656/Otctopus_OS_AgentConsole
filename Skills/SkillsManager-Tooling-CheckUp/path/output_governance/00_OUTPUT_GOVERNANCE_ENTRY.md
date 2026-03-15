---
doc_id: skillsmanager_tooling_checkup.path.output_governance.entry
doc_type: path_doc
topic: Action-loop entry for output governance checking
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
  reason: output governance starts from the contract doc.
---

# 输出落点检查入口

## 这个入口是干什么的
- 本入口只服务目标技能的输出落点检查。
- 当前线路用于检查 runtime 日志、默认产物、定向产物与历史迁移责任是否闭合。

## 下一跳列表
- [contract]：`10_CONTRACT.md`
