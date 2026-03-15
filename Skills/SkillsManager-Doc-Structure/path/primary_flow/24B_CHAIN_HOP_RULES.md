---
doc_id: skillsmanager_doc_structure.path.primary_flow.chain_hop_rules
doc_type: topic_atom
topic: Reading-chain hop rules in doc-structure governance
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Final validation closes the governance flow.
---

# Reading-Chain 下一跳规则

## 语义审查规则
- `hop: entry` 只用于 `SKILL.md` 暴露顶层功能入口。
- `hop: next` 只用于当前节点进入唯一的下一跳。
- `hop: branch` 只用于当前节点暴露若干可选分支或步骤入口。
- 任何 `reading_chain` 都必须能解释“模型下一步为什么要读这里”。

## 不合格信号
- 用 `hop` 名字掩盖越级跳转。
- 一个节点同时挂载大量与当前动作无关的下一跳。
- 本应使用物理下沉的关系，被硬塞成一条跨层 reading-chain。

## 下一跳列表
- [最终校验]：`30_VALIDATION.md`
