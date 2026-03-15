---
doc_id: skillsmanager_tooling_checkup.references_runtime_contracts_read_audit_directive
doc_type: topic_atom
topic: READ_AUDIT_DIRECTIVE
---

# READ_AUDIT_DIRECTIVE

<part_A>
- 本指令用于只读检查。
- 人类阅读时，可把它理解为“先锁定目标，再判断是否真的命中重复造轮子或落盘治理缺口”。
- 模型运行时应通过 `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py directive --topic read-audit --json` 获取 Part B。
</part_A>

<part_B>

```json
{
  "directive_name": "skills_tooling_checkup_read_audit_directive",
  "directive_version": "1.0.0",
  "doc_kind": "instruction",
  "topic": "read-audit",
  "purpose": "Run read-only semantic diagnosis for a target skill without inventing write scope.",
  "instruction": [
    "Lock the target skill path and the concrete tooling file scope before reading details.",
    "Use this skill to judge semantic redundancy against the repo-local mandatory tech stack baseline, not by filename or function-name resemblance alone.",
    "If the task touches CLI contract, command surface, or output shape, also consume the cli-surface directive before concluding.",
    "If runtime logs or outputs are in scope, also consume the output-governance directive before concluding.",
    "If the target issue is really about Python or TypeScript language style rather than tooling boundary, hand it off to the relevant language constitution instead of restating those rules here."
  ],
  "workflow": [
    "Read the target skill facade or runtime contract only far enough to discover its local execution surface.",
    "Compare target behavior against the repo-local mandatory baseline, CLI-surface contract, tooling-boundary guide, and common redundant wheel patterns as needed.",
    "State which conclusions are proven, which are still unknown, and whether remediation is justified."
  ],
  "rules": [
    "Do not escalate a pattern match into a rewrite without behavior evidence.",
    "Do not claim governance is complete if logs, outputs, or migration duties remain undocumented.",
    "Keep the result focused on evidence, risk, and next action rather than ad-hoc solution design."
  ]
}
```
</part_B>
