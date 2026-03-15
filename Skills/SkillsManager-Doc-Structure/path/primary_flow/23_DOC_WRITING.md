---
doc_id: skillsmanager_doc_structure.path.primary_flow.doc_writing
doc_type: topic_atom
topic: Doc writing responsibilities in the primary governance flow
reading_chain:
- key: skill_facade
  target: 23A_SKILL_FACADE_RULES.md
  hop: branch
  reason: Read the facade rule branch when reviewing SKILL.md responsibilities.
- key: entry_node
  target: 23B_ENTRY_NODE_RULES.md
  hop: branch
  reason: Read the entry-node rule branch when reviewing 00_*.md entry docs.
- key: contract_node
  target: 23C_CONTRACT_NODE_RULES.md
  hop: branch
  reason: Read the contract-node rule branch when reviewing contract docs.
- key: tools_node
  target: 23D_TOOLS_NODE_RULES.md
  hop: branch
  reason: Read the tools-node rule branch when reviewing tool or lint docs.
- key: execution_node
  target: 23E_EXECUTION_NODE_RULES.md
  hop: branch
  reason: Read the execution-node rule branch when reviewing execution docs.
- key: validation_node
  target: 23F_VALIDATION_NODE_RULES.md
  hop: branch
  reason: Read the validation-node rule branch when reviewing validation docs.
- key: workflow_index
  target: 23G_WORKFLOW_INDEX_RULES.md
  hop: branch
  reason: Read the workflow-index branch when reviewing compound workflow indexes.
- key: step_node
  target: 23H_STEP_NODE_RULES.md
  hop: branch
  reason: Read the step-node branch when reviewing step-local docs.
- key: branch_index
  target: 23I_BRANCH_INDEX_RULES.md
  hop: branch
  reason: Read the branch-index branch when reviewing function grouping nodes.
- key: terminal_index
  target: 23J_TERMINAL_INDEX_RULES.md
  hop: branch
  reason: Read the terminal-index branch when reviewing registry-only end nodes.
---

# 文档职责检查

## 当前动作
- 先确认正文没有重新破坏结构边界。
- 再沿目标技能自己的文档链路做语义审查，判断该层内容是否承担了正确职责。
- 这一步不要求所有技能写成完全相同的正文模板。

## 当前动作必须满足什么
- 单个文档只承担当前层的职责。
- 若某段规则只属于某个步骤，就必须下沉到该步骤文档里。
- 不允许把“整个技能所有规则”重新集中回一个总索引。
- CLI 不检查正文措辞是否一致；模型只检查语义是否越层、错层或重新总则化。

## 下一跳列表
- [门面规则]：`23A_SKILL_FACADE_RULES.md`
- [入口节点规则]：`23B_ENTRY_NODE_RULES.md`
- [合同节点规则]：`23C_CONTRACT_NODE_RULES.md`
- [tool/lint 节点规则]：`23D_TOOLS_NODE_RULES.md`
- [执行节点规则]：`23E_EXECUTION_NODE_RULES.md`
- [校验节点规则]：`23F_VALIDATION_NODE_RULES.md`
- [workflow index 规则]：`23G_WORKFLOW_INDEX_RULES.md`
- [step 节点规则]：`23H_STEP_NODE_RULES.md`
- [分支索引节点规则]：`23I_BRANCH_INDEX_RULES.md`
- [终止索引节点规则]：`23J_TERMINAL_INDEX_RULES.md`
