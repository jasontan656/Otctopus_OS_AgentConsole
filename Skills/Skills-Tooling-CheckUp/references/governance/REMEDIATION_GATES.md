---
doc_id: "skills_tooling_checkup.governance.remediation_gates"
doc_type: "topic_atom"
topic: "Gates and prohibitions that must hold before replacing self-built tooling code with mandatory baseline dependencies"
anchors:
  - target: "TOOLING_REMEDIATION_PROTOCOL.md"
    relation: "implements"
    direction: "upstream"
    reason: "The remediation protocol depends on these explicit gates."
  - target: "SKILL_EXECUTION_RULES.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Execution rules and remediation gates must stay aligned."
---

# Remediation Gates

## 本地目的
- 收敛“什么时候可以替换、什么时候必须停止”的硬门禁。

## 当前门禁
- 不能因为“看起来像通用能力”就跳过行为证据直接替换。
- 不能为本技能新增并行 CLI 或 helper 体系。
- 不能把目标 skill 的 domain-specific policy 误删成第三方库默认行为。
- 只有当依赖能力存在、语义可对齐、替换后更简单、且能验证行为不退化时，才允许进入实际修正。
