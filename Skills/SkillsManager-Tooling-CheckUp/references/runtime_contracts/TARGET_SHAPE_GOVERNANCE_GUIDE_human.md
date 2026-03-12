# TARGET_SHAPE_GOVERNANCE_GUIDE

<part_A>
- 本 guide 说明如何用本技能治理“目标 skill 的运行时形态”。
- 模型运行时应先调用 `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py govern-target --target-skill-root <path> --json` 获取目标感知审计结果。
- 人类可以看本 mirror；模型仍应以 Part B payload 为主。
</part_A>

<part_B>

```json
{
  "directive_name": "skills_tooling_checkup_target_shape_governance_guide",
  "directive_version": "1.0.0",
  "doc_kind": "guide",
  "topic": "target-shape-governance",
  "purpose": "Govern a target skill so runtime-facing contract, workflow, instruction, and guide assets become CLI-first dual-file outputs.",
  "instruction": [
    "Use govern-target with --target-skill-root to audit the target skill against the governed shape.",
    "Treat every runtime-facing contract/workflow/instruction/guide asset as dual-file: *_human.md plus same-name .json.",
    "Keep SKILL.md as a facade, but make the model enter the target skill through CLI JSON rather than markdown path chains."
  ],
  "workflow": [
    "Audit the target skill root for runtime_contracts, dual-file pairs, facade CLI-first wording, and agent prompt CLI-first wording.",
    "List markdown-only legacy runtime assets and json-only orphan runtime assets that still violate the governed shape.",
    "Rewrite the target skill so runtime instructions are emitted by tool output, then validate with the target skill's own tests and repo-local lint."
  ],
  "rules": [
    "Payload JSON must contain the contract content itself, not a pointer telling the model to read another file.",
    "Human markdown mirrors may keep narrative Part A, but Part B must mirror the same JSON payload emitted by the tool.",
    "govern-target is an audit and governance-entry surface; it does not by itself rewrite the target skill."
  ]
}
```
</part_B>
