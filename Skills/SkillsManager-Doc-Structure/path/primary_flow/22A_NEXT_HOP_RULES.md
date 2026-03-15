---
doc_id: skillsmanager_doc_structure.path.primary_flow.next_hop_rules
doc_type: topic_atom
topic: Immediate next-hop rules in doc-structure governance
reading_chain:
- key: 22b_linear_chain_rules
  target: 22B_LINEAR_CHAIN_RULES.md
  hop: next
  reason: After generic next-hop rules, read the relevant chain shape rule.
---

# 下一跳规则

## 语义审查规则
- 下一跳必须是“当前步骤真正要看的内容”，不能越过中间层。
- 当前节点只暴露最小必要集合，不应一口气列出深层兄弟节点。
- 下一跳可以有条件分支，但分支必须属于当前层真实可选路径。

## 不合格信号
- 从 `SKILL.md` 直接跳到深层 step 文档。
- 在入口层并列暴露大量深层文档。
- 用一个节点承担“当前层 + 后续层”的混合路由。

## 下一跳列表
- [单线路径链路规则]：`22B_LINEAR_CHAIN_RULES.md`
- [复合路径链路规则]：`22C_COMPOUND_CHAIN_RULES.md`
