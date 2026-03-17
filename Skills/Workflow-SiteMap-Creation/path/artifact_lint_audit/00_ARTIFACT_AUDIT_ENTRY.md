---
doc_id: workflow_sitemap_creation.path.artifact_lint_audit.entry
doc_type: workflow_entry
topic: Artifact lint audit entry for Workflow-SiteMap-Creation
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
  reason: 先锁定审计边界。
- key: runstates
  target: ../../references/runstates/RUNSTATE_METHOD_CONTRACT.md
  hop: side
  reason: 审计 workflow 也必须遵守中间态消费。
---

# Artifact Lint Audit Entry

- 本入口只依赖当前技能自带规则。
- 本入口审计对象是 `mother_doc` 统一架构及其 client mirror 一致性。
