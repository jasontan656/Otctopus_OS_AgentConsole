# Meta-Skill-Template Runtime Contract

> Audit copy for `references/runtime/SKILL_RUNTIME_CONTRACT.json`.

- `SKILL.md` role: entry only
- Runtime guidance source: `Cli_Toolbox.runtime-contract` plus referenced tooling docs
- Markdown role: human audit and reference
- Supported profiles: `basic`, `staged_cli_first`

## Tool Contracts
- `Cli_Toolbox.create_skill_from_template`: 统一入口创建或更新技能骨架。
- `Cli_Toolbox.skill_template`: 输出 `SKILL.md` 模板资产。
- `Cli_Toolbox.staged_skill_template`: 输出 staged CLI-first 复杂技能 `SKILL.md` 模板资产。
- `Cli_Toolbox.openai_template`: 输出 `openai.yaml` 模板资产。
- `Cli_Toolbox.contract_reference`: 输出模板契约参考。
- `Cli_Toolbox.staged_skill_reference`: 输出复杂技能 profile 提炼参考。
- `Cli_Toolbox.runtime_contract_template`: 输出运行合同模板资产。
- `Cli_Toolbox.architecture_playbook`: 输出模板架构手册。
- `Cli_Toolbox.runtime_contract`: 输出本技能运行合同。

## Governance Rules
- `SKILL.md` 必须保持轻量入口，不承载堆积式细节。
- 统一工具入口优先使用 `scripts/Cli_Toolbox.py`。
- 技能治理细节下沉到 `references/` 与模板资产。
- 未来生成技能默认采用“抽象层 + 业务需求层”分域写法。
- `3/4/5/6` 章节必须先写抽象层，再写各业务域；禁止混写。
- 允许统一 CLI 入口；抽象功能可共享，但业务域或阶段域命令必须独立，不得串用。
- 若目标技能属于 `staged_cli_first`，必须显式建模阶段目录、阶段合同与 resident docs。
- 若规则依赖真实项目状态，必须显式区分 static authoring contract 与 dynamic runtime contract。
- 若治理规则变化，同时更新 `SKILL.md` 入口、`references` 合同、tooling 文档与模板资产。
