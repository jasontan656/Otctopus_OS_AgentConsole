---
doc_id: skillsmanager_tooling_checkup.references.policies.remediation_gate
doc_type: topic_atom
topic: Remediation gate policy
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This policy defines what the remediation output may recommend.
---

# Remediation Gate

## 输出范围
- remediation gate 只能给出：
  - 缺失的 contract/doc/test 面
  - 推荐先进入的治理 topic
  - 是否需要继续触发 `SkillsManager-Doc-Structure`、`SkillsManager-RunStates-Manager` 或 `Dev-PythonCode-Constitution`

## 禁止事项
- 不要在 audit 命令里直接改 target skill。
- 不要默认补兼容壳来掩盖 contract 缺失。
