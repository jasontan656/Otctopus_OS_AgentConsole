---
doc_id: skillsmanager_doc_structure.path.primary_flow.workflow_index_rules
doc_type: topic_atom
topic: Workflow-index semantic rules in doc-structure governance
reading_chain:
- key: reading_chain_lint
  target: 24_READING_CHAIN_LINT.md
  hop: next
  reason: Reading-chain lint follows after workflow-index review.
---

# Workflow Index 规则

## 语义审查规则
- `20_WORKFLOW_INDEX.md` 只负责列步骤、顺序和每个步骤的入口。
- 它的作用是告诉模型“下一步去哪”，不是承载 step-local 正文。
- 只有复合路径型技能才应出现该类节点。

## 不合格信号
- workflow index 直接展开各步骤完整内容。
- 在线性技能中额外长出 workflow index。
- workflow index 跳过 step entry 直接指向深层局部文档。

## 下一跳列表
- [reading-chain 检查]：`24_READING_CHAIN_LINT.md`
