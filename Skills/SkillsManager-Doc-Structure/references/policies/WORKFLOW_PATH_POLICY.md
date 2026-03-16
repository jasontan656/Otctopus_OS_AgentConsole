---
doc_id: skillsmanager_doc_structure.references.policies.workflow_path_policy
doc_type: topic_atom
topic: Workflow path policy for compiled skills
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This policy governs workflow_path topology.
---

# Workflow Path Policy

## 最小要求
- `path/` 下至少存在一个 `00_*.md` 入口。
- workflow 节点的 `reading_chain` 必须只指向存在的 markdown 文件。
- 至少应存在：
  - contract 节点
  - validation 节点
- 若存在 branch hop，则 `compile-context` 在未给选择时必须返回 `branch_selection_required`。

## 不再要求
- 不再要求固定 root shape 只能是旧 family layout。
- 不再要求每个 workflow 都必须叫 `primary_flow`。
