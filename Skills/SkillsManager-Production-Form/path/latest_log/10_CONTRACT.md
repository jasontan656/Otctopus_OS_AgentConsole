---
doc_id: skillsmanager_production_form.path.latest_log.contract
doc_type: contract_doc
topic: Latest log contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: After the contract, read the log commands.
---

# 最近迭代合同

## 当前动作的目标
- 保证模型在延续现有设计线时，先读到最近的 console 产品化判断。

## 当前动作必须满足的约束
- active log 位于 runtime root，而不是 skill 目录。
- 如果 active log 不存在，允许从 seed snapshot 首次迁移。
- repo 内 seed snapshot 只读，不继续追加。

## 下一跳列表
- [tools]：`15_TOOLS.md`
