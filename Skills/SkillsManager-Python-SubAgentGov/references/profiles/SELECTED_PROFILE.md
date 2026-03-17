---
doc_id: skillsmanager_python_subagentgov.references.profiles.selected_profile
doc_type: topic_atom
topic: Selected skill profile for SkillsManager-Python-SubAgentGov
---

# Selected Skill Profile

- `doc_topology`: `referenced`
- `tooling_surface`: `automation_cli`
- `workflow_control`: `guardrailed`
- 选择理由：
  - 运行时主合同、执行边界与 closeout 顺序需要稳定文档真源
  - 技能本身要暴露正式 CLI，而不是只靠 workflow 文案调度
  - Python subagent 治理属于高约束自动化流程，必须 guardrailed，不能退回 advisory
