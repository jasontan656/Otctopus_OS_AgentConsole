---
doc_id: skillsmanager_doc_structure.path.primary_flow.reading_chain_lint
doc_type: topic_atom
topic: Reading-chain lint in the primary governance flow
reading_chain:
- key: 24a_chain_scope_rules
  target: 24A_CHAIN_SCOPE_RULES.md
  hop: next
  reason: Reading-chain scope rules are read before final validation.
---

# Reading-Chain 检查

## 当前动作
- 抽取目标技能中所有 markdown frontmatter 的 `reading_chain`。
- 检查每个 `target` 是否存在且仍指向 markdown 节点。
- 检查 `hop` 是否只表达入口、下一跳或分支。
- 检查 CLI 是否能沿这条链正确编译整条上下文。

## 当前动作必须满足什么
- reading-chain 目标必须存在。
- reading-chain 不能把读者直接拉回已经被废弃的旧主组织轴。
- reading-chain 的作用是定义模型下一步该读什么，以及 CLI 下一步该编译什么。
- reading-chain 不能代替物理目录结构补洞；缺节点时应先补节点，再写链路。

## 下一跳列表
- [reading-chain 作用域规则]：`24A_CHAIN_SCOPE_RULES.md`
- [reading-chain 下一跳规则]：`24B_CHAIN_HOP_RULES.md`
