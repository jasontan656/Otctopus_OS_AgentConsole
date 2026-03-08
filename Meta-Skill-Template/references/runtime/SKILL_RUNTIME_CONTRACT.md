# Meta-Skill-Template Runtime Contract

> Audit copy for `references/runtime/SKILL_RUNTIME_CONTRACT.json`.

- `SKILL.md` role: entry only
- Runtime guidance source: `Cli_Toolbox.runtime-contract` plus referenced tooling docs
- Markdown role: human audit and reference

## Tool Contracts
- `Cli_Toolbox.create_skill_from_template`: 统一入口创建或更新技能骨架。
- `Cli_Toolbox.skill_template`: 输出 `SKILL.md` 模板资产。
- `Cli_Toolbox.openai_template`: 输出 `openai.yaml` 模板资产。
- `Cli_Toolbox.contract_reference`: 输出模板契约参考。
- `Cli_Toolbox.architecture_playbook`: 输出模板架构手册。
- `Cli_Toolbox.runtime_contract`: 输出本技能运行合同。

## Governance Rules
- `SKILL.md` 必须保持轻量入口，不承载堆积式细节。
- 统一工具入口优先使用 `scripts/Cli_Toolbox.py`。
- 技能治理细节下沉到 `references/` 与模板资产。
- 若治理规则变化，同时更新 `SKILL.md` 入口、`references` 合同、tooling 文档与模板资产。
