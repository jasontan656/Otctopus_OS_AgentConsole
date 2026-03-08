# Runtime Contract Template

> Audit copy for `SKILL_RUNTIME_CONTRACT_TEMPLATE.json`.

- `skill_name`: `${skill_name}`
- `profile`: `staged_cli_first`
- `SKILL.md` role: entry only
- Runtime guidance source: `Cli_Toolbox` commands
- Markdown role: human audit and reference

## Governance Rules
- `SKILL.md` 必须保持轻量入口，不承载堆积式细节。
- 模型禁止直接阅读 markdown 获取运行指引；必须通过 CLI 获取 machine-readable 合同。
- 阶段切换时只保留 resident docs，并显式丢弃上一阶段 focus。
- 若规则依赖真实项目状态，必须显式标记为 dynamic runtime contract。
