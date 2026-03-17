---
doc_id: workflow_sitemap_creation.path.artifact_lint_audit.rulebook
doc_type: topic_atom
topic: Artifact lint audit rulebook
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 规则书之后进入 pass/fail 校验。
---

# Artifact Lint Audit Rulebook

- 必备目录与必备文档必须存在。
- 必备文档必须具备可消费 frontmatter，而不是只有空壳三字段。
- root index、manifest 与实际受管文档集合必须一致。
- 文档关系、writeback 语义与下游消费边界必须显式存在。
- 禁用词不得出现。
- 若技能 runtime 宣称已执行九阶段闭环，则对应 evidence / summary 必须存在并可回读。
