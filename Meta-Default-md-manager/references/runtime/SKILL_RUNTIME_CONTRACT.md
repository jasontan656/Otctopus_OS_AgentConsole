# Skill Runtime Contract

> Audit copy generated from `references/runtime/SKILL_RUNTIME_CONTRACT.json`.
> Runtime models must call `python3 scripts/Cli_Toolbox.py contract --json` instead of reading this markdown for guidance.

- contract_name: `meta_default_md_manager_references_runtime_skill_runtime_contract`
- contract_version: `1.0.0`
- validation_mode: `strict`
- required_fields:
- `contract_name`
- `contract_version`
- `validation_mode`
- optional_fields:
- `notes`

- skill_name: `Meta-Default-md-manager`
- version: `1`
- description: 集中管理 workspace 内的常驻默认文档，运行态规则、约束与阶段指引必须通过 CLI 输出，不允许模型直接读取 markdown 获取指引。

## Runtime Access Policy
- guidance_source: `cli_only_machine_contracts`
- markdown_role: `human_audit_only`
- model_must_not_read_markdown_for_runtime_guidance: `True`
- model_must_call_contract_before_runtime_use: `True`
- model_must_call_directive_for_each_stage: `True`

## Command Map
- `contract`: 输出技能级运行合同，作为所有阶段的前置运行指引。
- `directive`: 按 stage 输出 machine-readable 阶段指引；运行态必须通过该命令读取阶段规则。
- `render-audit-docs`: 根据 machine-readable 合同重建 markdown 审计文档，保证双版本同步。
- `scan`: 扫描默认文档目标，只写 scan_report.json。
- `collect`: 消费 scan_report.json，回收托管副本并刷新 registry/index。
- `push`: 消费 registry.json，把托管副本回写到真实目标。
- `registry`: 读取当前托管映射，不提供阶段规则。

## Sync Policy
- machine_contract_paths: references/runtime/SKILL_RUNTIME_CONTRACT.json + references/stages/*/DIRECTIVE.json
- markdown_audit_paths: references/runtime/SKILL_RUNTIME_CONTRACT.md + references/stages/*/(INSTRUCTION.md|WORKFLOW.md|RULES.md)
- update_rule: 运行合同或阶段指引变更时，必须先更新 JSON，再执行 render-audit-docs 刷新 markdown 审计版。
- runtime_read_rule: 运行态禁止把 markdown 作为规则源；markdown 只供人类审计。
