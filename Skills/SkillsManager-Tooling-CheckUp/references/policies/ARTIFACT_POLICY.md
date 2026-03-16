---
doc_id: skillsmanager_tooling_checkup.references.policies.artifact_policy
doc_type: topic_atom
topic: Artifact policy governance
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This policy governs runtime/result path declarations.
---

# Artifact Policy

## 稳定要求
- runtime contract 若声明 `artifact_policy`，应优先表达：
  - `mode`
  - `resolver`
  - `notes`
- 不应在技能门面或 contract 中写死 repo-local 绝对路径。
- 若 target skill 的产物完全不落盘，可声明 `ephemeral_stdout_only`。

## 审计判断
- 发现绝对路径字符串时，默认视为错误。
- 缺失 `artifact_policy` 时，默认给出 warning，而不是自动判错。
