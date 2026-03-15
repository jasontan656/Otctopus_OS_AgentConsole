---
doc_id: skillsmanager_doc_structure.path.primary_flow.path_chaining
doc_type: topic_atom
topic: Path chaining rules in the primary governance flow
reading_chain:
- key: next_hop
  target: 22A_NEXT_HOP_RULES.md
  hop: branch
  reason: Next-hop rules explain the universal downstream contract.
- key: linear_chain
  target: 22B_LINEAR_CHAIN_RULES.md
  hop: branch
  reason: Linear-chain rules explain single-line path requirements.
- key: compound_chain
  target: 22C_COMPOUND_CHAIN_RULES.md
  hop: branch
  reason: Compound-chain rules explain workflow-index and step branching requirements.
---

# 路径衔接检查

## 当前动作
- 检查 `SKILL.md` 是否只暴露功能入口层，而不是越级暴露深层正文。
- 检查被门面暴露的功能入口是否只把读者送到当前需要的下一跳。
- 检查每个入口目录是否物理下沉到自己的链路，而不是多个阶段文件平铺在同一层靠内联控制。
- 允许在入口选择层出现“分支索引节点”；真正要求单线的是分支索引下面的叶子闭环。

## 当前动作必须满足什么
- 单线路径型内部不能再出现子目录分叉。
- 但单线路径型允许先出现分支索引层，用于把读者送入各自独立的叶子闭环。
- 复合路径型必须把 workflow index 和 step 目录物理下沉。
- 任何入口内的下一跳都必须是当前步骤真正要看的内容。

## 下一跳列表
- [下一跳规则]：`22A_NEXT_HOP_RULES.md`
- [单线路径链路规则]：`22B_LINEAR_CHAIN_RULES.md`
- [复合路径链路规则]：`22C_COMPOUND_CHAIN_RULES.md`
