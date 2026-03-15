---
doc_id: skills_tooling_checkup.governance.remediation_gates
doc_type: topic_atom
topic: Gates and prohibitions that must hold before replacing self-built tooling code
  with mandatory baseline dependencies
---

# Remediation Gates

## 本地目的
- 收敛“什么时候可以替换、什么时候必须停止”的硬门禁。

## 当前门禁
- 不能因为“看起来像通用能力”就跳过行为证据直接替换。
- 不能为本技能新增并行 CLI 或 helper 体系。
- 不能把目标 skill 的 domain-specific policy 误删成第三方库默认行为。
- 不能只改新写入路径而忽略旧日志、旧产物或旧审计文件的迁移责任。
- 不能把“需要用户指定落点”的定向产物技能改成隐式散落输出；若没有显式落点，默认值也必须回到 `/home/jasontan656/AI_Projects/Codex_Skills_Result`。
- 不能在目标技能文档仍然缺失日志落点与产物落点声明时，宣称治理已经完成。
- 只有当依赖能力存在、语义可对齐、替换后更简单、且能验证行为不退化时，才允许进入实际修正。
