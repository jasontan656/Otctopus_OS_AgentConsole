---
doc_id: skillsmanager_tooling_checkup.references_runtime_contracts_cli_surface_contract
doc_type: topic_atom
topic: CLI_SURFACE_CONTRACT
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# CLI_SURFACE_CONTRACT

<part_A>
- 本合同只治理目标技能的 tooling CLI surface。
- 它不要求目标技能采用本技能自己的门面、根目录或 runtime asset 组织方式。
- 它只要求：若目标技能对外暴露受管 tooling CLI，则命令、参数、JSON 输出和错误返回必须可稳定消费。
</part_A>

<part_B>

```json
{
  "directive_name": "skills_tooling_checkup_cli_surface_contract",
  "directive_version": "1.0.0",
  "doc_kind": "contract",
  "topic": "cli-surface",
  "purpose": "Define the governed contract for target skill CLI surfaces without imposing facade or root-shape requirements.",
  "instruction": [
    "A governed tooling surface must expose one explicit CLI entry when scripts/ exists and the skill intends runtime invocation through local tools.",
    "CLI commands should use stable verb-style or noun-action names, keep option names descriptive, and avoid ambiguous short aliases unless the target skill already standardizes them.",
    "Machine-readable mode must return structured JSON payloads for normal success and structured JSON errors for known failures instead of relying on prose-only stdout."
  ],
  "workflow": [
    "Confirm whether the target scripts surface is intended for direct runtime use or only internal helper execution.",
    "If the surface is user- or model-facing, inspect command names, required options, JSON mode, and known error returns.",
    "Record gaps in command clarity, output shape, exit semantics, or argument contract before proposing remediation."
  ],
  "rules": [
    "Do not require the target skill to adopt this skill's contract/directive command names.",
    "Do not treat internal helper scripts with no governed public entry as malformed just because they are not exposed as standalone CLIs.",
    "Require explicit and stable JSON success/error shapes only for surfaces that claim governed runtime use."
  ]
}
```
</part_B>
