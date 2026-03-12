# REMEDIATION_WORKFLOW

<part_A>
- 本工作流用于真正进入目标 skill 做改写。
- 人类应把它理解为“先证明可替换，再做最小改写，再跑目标 skill 自己的验证链”。
- 模型运行时应通过 `python3 scripts/Cli_Toolbox.py directive --topic remediation --json` 获取 Part B。
</part_A>

<part_B>

```json
{
  "directive_name": "skills_tooling_checkup_remediation_workflow",
  "directive_version": "1.0.0",
  "doc_kind": "workflow",
  "topic": "remediation",
  "purpose": "Drive behavior-preserving tooling remediation after evidence proves the target skill is rebuilding mandatory baseline capability or violating output governance.",
  "instruction": [
    "Enter remediation only after read-only evidence shows the target implementation is replaceable without semantic loss.",
    "Prefer delete or shrink over stacking adapters on top of redundant custom code.",
    "When outputs are in scope, remediation must include code path changes, default path changes, document declaration changes, and historical migration responsibility."
  ],
  "workflow": [
    "Read the target skill local contract and execution surface before editing.",
    "Use the techstack-baseline and output-governance directives to confirm replacement gates are satisfied.",
    "Rewrite the minimal correct scope, then validate with the target skill's existing tests and lint commands.",
    "If Python files changed, finish by running Dev-PythonCode-Constitution-Backend lint on the concrete target scope."
  ],
  "rules": [
    "Do not add a parallel helper system when the repo-local baseline dependency already covers the need.",
    "Do not remove target-skill domain policy, compatibility semantics, or audit meaning under the pretext of simplification.",
    "Do not close the turn before downstream mirror-to-codex sync has completed for an installed skill."
  ]
}
```
</part_B>
