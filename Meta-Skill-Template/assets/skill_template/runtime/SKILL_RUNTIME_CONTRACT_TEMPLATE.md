# Runtime Contract Template

## Contract Header
- `contract_name`: `meta_skill_template_assets_skill_template_runtime_skill_runtime_contract_template`
- `contract_version`: `2.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

> Audit copy for `SKILL_RUNTIME_CONTRACT_TEMPLATE.json`.

## Required Shape
- `skill_name`: `${skill_name}`
- `skill_profile`: `staged_cli_first`
- `SKILL.md` role: `entry_only`
- required façade sections:
  - `定位`
  - `必读顺序`
  - `分类入口`
  - `适用域`
  - `执行入口`
  - `读取原则`
  - `结构索引`

## Required Stage Surface
- `stage-checklist`
- `stage-doc-contract`
- `stage-command-contract`
- `stage-graph-contract`

## Governance Rules
- `SKILL.md` 必须保持门面化。
- 运行态规则必须从 machine-readable contracts 消费，不得把 markdown 当真实规则源。
- staged skill 必须显式定义 resident docs、stage order 和 stage-switch discard policy。
- 阶段模板的人类叙事文件与 machine-readable contracts 必须分开维护。
