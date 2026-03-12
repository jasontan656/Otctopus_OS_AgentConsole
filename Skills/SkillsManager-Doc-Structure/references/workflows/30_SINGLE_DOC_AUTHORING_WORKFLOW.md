---
doc_id: "workflows.single_doc_authoring"
doc_type: "topic_atom"
topic: "Workflow for authoring one governed markdown file after the tree is already known"
node_role: "topic_atom"
domain_type: "workflow"
anchors:
  - target: "00_WORKFLOW_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This workflow is one branch under the workflow index."
  - target: "../metadata/20_FRONTMATTER_FIELD_CONTRACT.md"
    relation: "details"
    direction: "downstream"
    reason: "Single-doc authoring depends on the frontmatter field contract."
---

# Single Doc Authoring Workflow

## 步骤
1. 先确认当前文件在 tree 里的位置和父子关系。
2. 再确认当前文件是 routing、index 还是 topic atom。
3. 写标题、`topic`、frontmatter 与 anchors。
4. 正文只写当前节点该承担的内容，不回填上层或旁支职责。
