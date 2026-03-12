---
doc_id: "workflows.query"
doc_type: "topic_atom"
topic: "Workflow for querying the right knowledge track before reading deeper docs"
node_role: "topic_atom"
domain_type: "workflow"
anchors:
  - target: "00_WORKFLOW_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This workflow is one branch under the workflow index."
  - target: "../rules/00_RULE_SYSTEM_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Rule-track reading begins after the query workflow selects the correct track."
---

# Query Workflow

## 步骤
1. 先判断当前问题属于规则、fewshot 还是元信息。
2. 再判断自己是在查路径、组织树，还是写单文件。
3. 只进入当前需要的那条知识轨和 workflow。
4. 若当前节点不足，再继续下钻或补 cross-links。
