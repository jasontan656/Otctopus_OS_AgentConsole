# READ_AUDIT_DIRECTIVE

<part_A>
- 本指令用于只读检查。
- 人类阅读时，可把它理解为“先锁定目标，再判断是否真的命中重复造轮子或落盘治理缺口”。
- 模型运行时应通过 `python3 scripts/Cli_Toolbox.py directive --topic read-audit --json` 获取 Part B。
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
    "If runtime logs or outputs are in scope, also consume the output-governance directive before concluding."
  ],
  "workflow": [
    "Read the target skill facade or runtime contract only far enough to discover its local execution surface.",
    "Compare target behavior against the repo-local mandatory baseline and the common redundant wheel patterns.",
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
