---
doc_id: skillsmanager_tooling_checkup.path.tooling_boundary.entry
doc_type: path_doc
topic: Action-loop entry for tooling boundary checking
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
  reason: tooling boundary checking starts from the contract doc.
---

# Tooling 职责边界检查入口

## 这个入口是干什么的
- 本入口只服务目标技能的 tooling 职责边界检查。
- 当前线路用于判断 parser / schema / helper / lint / test / glue 是否越权吸收了域内规则或工作流语义。

## 下一跳列表
- [contract]：`10_CONTRACT.md`
