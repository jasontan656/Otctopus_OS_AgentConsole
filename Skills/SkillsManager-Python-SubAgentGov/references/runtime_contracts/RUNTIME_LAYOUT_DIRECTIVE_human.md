---
doc_id: skillsmanager_python_subagentgov.references.runtime_contracts.runtime_layout_directive
doc_type: topic_atom
topic: Runtime layout for SkillsManager-Python-SubAgentGov
---

# Runtime Layout Directive

- `controller_status.json` 用来描述整轮主控当前的 pending / active / completed 视图。
- 每个技能独享一个 runtime 子目录，用于保存 prompt、日志、结果和 closeout 证据。
- `closure.json` 存在才表示这个技能已经完成 verify、Git 留痕、mirror sync 与 session closeout，不只是 subagent 结束。
