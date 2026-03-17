---
doc_id: skillsmanager_python_subagentgov.references.runtime_contracts.execution_boundary_directive
doc_type: topic_atom
topic: Execution boundary for SkillsManager-Python-SubAgentGov
---

# Execution Boundary Directive

- 主控负责编排和收口，subagent 只负责单技能 Python 代码治理。
- subagent 的编辑边界严格限制在 `Skills/<target_skill>/`。
- subagent 的运行边界严格限制在对应 runtime 目录。
- Git、push、mirror sync 都不是 subagent 的职责。
