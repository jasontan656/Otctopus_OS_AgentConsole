---
doc_id: workflows.architecture_organization
doc_type: topic_atom
topic: Workflow for organizing a target skill's document architecture from the entry downward
node_role: topic_atom
domain_type: workflow
anchors:
- target: 00_FLOW_INDEX.md
  relation: belongs_to
  direction: upstream
  reason: This workflow is one branch under the workflow index.
- target: ../fewshot/00_FEWSHOT_INDEX.md
  relation: routes_to
  direction: downstream
  reason: The fewshot track provides reusable deep-tree examples for architecture work.
---

# Architecture Organization Workflow

## 步骤
1. 识别目标 skill 的入口节点。
2. 先确定需要几条主分支，再决定每条分支是否继续下钻。
3. 优先组织 tree，不先堆 cross-links。
4. fewshot 只用于理解组织手法，不允许直接照抄。
5. tree 稳定后，再补 metadata 与 anchors。
