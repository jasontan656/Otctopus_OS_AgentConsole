---
doc_id: workflow_sitemap_creation.path.artifact_lint_audit.contract
doc_type: topic_atom
topic: Artifact lint audit contract
contract_name: workflow_sitemap_creation_artifact_audit_contract
contract_version: 1.0.0
validation_mode: rulebook_audit
required_fields:
- reading_chain
- audit_scope
- governance_decision
optional_fields:
- evidence_writeback
- mirror_consistency
reading_chain:
- key: rulebook
  target: 20_RULEBOOK.md
  hop: next
  reason: 先锁定审计范围，再执行规则书。
---

# Artifact Lint Audit Contract

- 本入口只使用当前技能自身承载的规则，不借外部模糊判断。
- 审计对象至少覆盖：
  - 文件夹组织
  - frontmatter 完整度与字段语义
  - 文档关系与下游消费边界
  - manifest / root index 一致性
  - tmux subagent / runtask 闭环证据是否已回写
- 审计失败时必须返回可执行治理判断，而不是仅给模糊建议。
