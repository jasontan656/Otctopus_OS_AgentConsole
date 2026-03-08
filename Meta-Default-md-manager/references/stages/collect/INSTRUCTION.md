# Collect Instruction

> Audit copy generated from `references/stages/collect/DIRECTIVE.json`.
> Runtime models must call `python3 scripts/Cli_Toolbox.py directive --stage collect --json` instead of reading this markdown for guidance.

- 只处理 collect 阶段。
- 运行态只允许通过 Cli_Toolbox.directive 读取本阶段 machine-readable 指引。
- 禁止把 references/stages/collect/*.md 当作运行规则源，除非用户显式要求审计 markdown。
- 输入前提是 assets/managed_targets/scan_report.json 已存在。
