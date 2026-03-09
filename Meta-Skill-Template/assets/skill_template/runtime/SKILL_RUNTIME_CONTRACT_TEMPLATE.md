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
- 未来生成技能默认采用“抽象层 + 业务需求层”写法。
- `3/4/5/6` 章节必须先写抽象层，再写各业务域；禁止混写。
- 允许统一 CLI 入口；抽象功能可共享，但域命令必须独立，不得串用。
- 阶段切换时只保留 resident docs，并显式丢弃上一阶段 focus。
- 若规则依赖真实项目状态，必须显式标记为 dynamic runtime contract。
