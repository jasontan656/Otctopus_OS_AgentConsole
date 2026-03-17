---
doc_id: skillsmanager_python_subagentgov.references.runtime_contracts.closeout_sequence_directive
doc_type: topic_atom
topic: Closeout sequence for SkillsManager-Python-SubAgentGov
---

# Closeout Sequence Directive

- 任一技能完成治理与验证后，主控必须立刻收口，而不是继续放任并发跑完再统一处理。
- 串行收口顺序固定为：
  - `verify`
  - `commit-and-push`
  - `mirror sync`
  - `session closeout`
- 这样可以确保每个技能都有独立 traceability，并避免并发 remote write。
