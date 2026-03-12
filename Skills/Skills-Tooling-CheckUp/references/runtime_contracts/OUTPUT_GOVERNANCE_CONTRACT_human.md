# OUTPUT_GOVERNANCE_CONTRACT

<part_A>
- 本合同专门治理目标 skill 的 runtime 日志与结果落点。
- 人类阅读时，应关注五件事是否闭合：代码路径、默认回退、显式落点参数、文档声明、历史迁移责任。
- 模型运行时应通过 `python3 scripts/Cli_Toolbox.py directive --topic output-governance --json` 获取 Part B。
</part_A>

<part_B>

```json
{
  "directive_name": "skills_tooling_checkup_output_governance_contract",
  "directive_version": "1.0.0",
  "doc_kind": "contract",
  "topic": "output-governance",
  "purpose": "Govern runtime logs, audit traces, default outputs, directed outputs, and migration duties in target skill tooling.",
  "instruction": [
    "Runtime logs, audit traces, and debug artifacts must govern to /home/jasontan656/AI_Projects/Codex_Skill_Runtime.",
    "Default outputs and generic result artifacts must govern to /home/jasontan656/AI_Projects/Codex_Skills_Result.",
    "Directed-output skills must support or require an explicit output path; if omitted, the default must still fall back to /home/jasontan656/AI_Projects/Codex_Skills_Result."
  ],
  "workflow": [
    "Inspect code semantics for write paths, fallback paths, and user-controlled output arguments.",
    "Inspect skill-facing docs or runtime contracts to confirm the same paths are declared, not merely implied in code.",
    "If legacy artifacts exist outside governed roots, include migration or explicit disposition rules in the remediation scope."
  ],
  "rules": [
    "Do not treat string grep alone as output governance proof.",
    "Do not declare governance complete when code, docs, defaults, and migration duties are not all closed.",
    "Do not silently preserve scattered historical paths without a declared migration or retention policy."
  ]
}
```
</part_B>
